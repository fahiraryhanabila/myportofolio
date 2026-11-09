import uuid

from django.contrib.auth.models import Group, Permission, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Education, Experience


def make_editor(codename, username="editor"):
    """Editor = user yang punya izin change_<model>, tanpa add/delete."""
    editor = User.objects.create_user(username=username, password="test-password")
    editor.user_permissions.add(Permission.objects.get(codename=codename))
    return editor


# ---------------------------------------------------------------- Experience
class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.experience = Experience.objects.create(
            title="Backend Intern", description="Membangun REST API", category="internship",
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star", args=[self.experience.id])
        self.payload = {
            "title": "Asisten Riset",
            "description": "Membantu pengumpulan data",
            "category": "research",
            "thumbnail": "https://example.com/foto.png",
        }

    def assert_unchanged(self):
        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Backend Intern")
        self.assertEqual(self.experience.description, "Membangun REST API")

    # --- baca / cari
    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.experience.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        for forbidden in ("email", "password", "starred_by"):
            self.assertNotIn(forbidden, response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"query": "BACKEND"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"query": "not-found"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_search_blank_query_returns_all(self):
        response = self.client.get(self.list_url, {"query": "   "})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_legacy_title_param_still_works(self):
        response = self.client.get(self.list_url, {"title": "BACKEND"})
        self.assertEqual(len(response.data), 1)

    def test_missing_experience(self):
        url = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    # --- peran
    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assert_unchanged()

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Experience.objects.filter(pk=response.data["id"]).exists())
        self.assertEqual(Experience.objects.count(), 2)
        self.assertTrue(response.data["is_ongoing"])

    def test_owner_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Changed")
        self.assertEqual(self.experience.description, "Membangun REST API")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=self.experience.id).exists())

    def test_editor_can_patch_but_not_create_or_delete(self):
        self.client.force_authenticate(user=make_editor("change_experience"))
        response = self.client.patch(self.detail_url, {"title": "Diedit"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Riset")

        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertTrue(Experience.objects.filter(pk=self.experience.id).exists())

    def test_editor_can_star(self):
        self.client.force_authenticate(user=make_editor("change_experience"))
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_200_OK)

    def test_user_without_change_permission_cannot_patch(self):
        # staff atau anggota grup bernama "Editor" tanpa izin change tetap ditolak
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_unchanged()

    # --- validasi
    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),  # kosong setelah strip_tags
            ({"category": "magang"}, "category"),
            ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=changes)
            self.assertIn(field, response.data, msg=changes)
        self.assertEqual(Experience.objects.count(), 1)

    def test_html_in_title_is_stripped(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.list_url, {**self.payload, "title": "<b>Halo</b>"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Halo")

    def test_post_rejects_list_body(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, [self.payload], format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Experience.objects.count(), 1)

    # --- star
    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.experience.starred_by.count(), 0)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertIn(self.visitor, self.experience.starred_by.all())
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_star_get_is_405_when_logged_in_and_403_when_guest(self):
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "is_ongoing": False,
            "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")
        self.assertTrue(response.data["is_ongoing"])

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # --- CSRF
    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # --- view lama harus sama ketatnya
    def test_old_views_enforce_same_roles(self):
        delete_url = reverse("main:delete_experience", args=[self.experience.id])
        # guest: diarahkan ke login
        self.assertEqual(self.client.post(delete_url).status_code, 302)
        # user biasa dan Editor: ditolak
        for user in (self.visitor, make_editor("change_experience")):
            self.client.force_login(user)
            self.assertEqual(self.client.post(delete_url).status_code, 403)
            self.assertEqual(
                self.client.post(reverse("main:create_experience_ajax"), {"title": "X"}).status_code, 403,
            )
        self.client.force_login(self.visitor)
        edit_url = reverse("main:edit_experience", args=[self.experience.id])
        self.assertEqual(self.client.get(edit_url).status_code, 403)
        self.assert_unchanged()


# ----------------------------------------------------------------- Education
class EducationAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser("owner", "o@example.com", "test-password")
        self.visitor = User.objects.create_user("visitor", password="test-password")
        self.education = Education.objects.create(
            title="Universitas Indonesia", description="Sistem Informasi",
            category_edu="Bachelor's Degree", start_year=2023, is_ongoing=True,
            skills="Python, Django",
        )
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.education.id])
        self.star_url = reverse("api:education-star", args=[self.education.id])
        self.payload = {
            "title": "SMA Negeri 1", "description": "IPA",
            "category_edu": "Senior High School",
            "start_year": 2020, "end_year": 2023, "is_ongoing": False,
            "skills": "Biologi", "thumbnail": "https://example.com/a.png",
        }

    def assert_unchanged(self):
        self.assertEqual(Education.objects.count(), 1)
        self.education.refresh_from_db()
        self.assertEqual(self.education.title, "Universitas Indonesia")
        self.assertEqual(self.education.description, "Sistem Informasi")

    # --- baca / cari
    def test_public_list_detail_and_search(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], self.education.id)
        self.assertEqual(response.data[0]["skill_list"], ["Python", "Django"])
        for forbidden in ("email", "password", "starred_by"):
            self.assertNotIn(forbidden, response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.client.get(self.list_url, {"query": "INDO"}).data), 1)
        empty = self.client.get(self.list_url, {"query": "tidak-ada"})
        self.assertEqual(empty.status_code, status.HTTP_200_OK)
        self.assertEqual(empty.data, [])

    def test_search_blank_query_returns_all(self):
        response = self.client.get(self.list_url, {"query": "   "})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_legacy_title_param_still_works(self):
        self.assertEqual(len(self.client.get(self.list_url, {"title": "INDO"}).data), 1)

    def test_missing_education(self):
        url = reverse("api:education-detail", args=[999999])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    # --- peran
    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "X"}, format="json").status_code, 403)
            self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assert_unchanged()

    def test_owner_create_patch_put_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Education.objects.count(), 2)
        response = self.client.patch(self.detail_url, {"title": "UI"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.title, "UI")
        self.assertEqual(self.education.description, "Sistem Informasi")
        self.assertEqual(
            self.client.put(self.detail_url, {"title": "Incomplete"}, format="json").status_code, 400,
        )
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Education.objects.filter(pk=self.education.pk).exists())

    def test_editor_can_patch_but_not_create_or_delete(self):
        self.client.force_authenticate(user=make_editor("change_education"))
        response = self.client.patch(self.detail_url, {"title": "Diedit"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.title, "SMA Negeri 1")

        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Education.objects.count(), 1)
        self.assertTrue(Education.objects.filter(pk=self.education.pk).exists())

    def test_editor_can_star(self):
        self.client.force_authenticate(user=make_editor("change_education"))
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_200_OK)

    def test_editor_put_respects_validation(self):
        self.client.force_authenticate(user=make_editor("change_education"))
        bad = {**self.payload, "end_year": 1999}
        self.assertEqual(self.client.put(self.detail_url, bad, format="json").status_code, 400)
        self.assert_unchanged()

    def test_user_without_change_permission_cannot_patch(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "X"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_unchanged()

    # --- validasi
    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": "<img src=x onerror=alert(1)>"}, "title"),  # kosong setelah strip_tags
            ({"category_edu": "Kindergarten"}, "category_edu"),
            ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
            ({"start_year": 2023, "end_year": 2020}, "end_year"),
            ({"is_ongoing": True, "end_year": 2023}, "end_year"),
            ({"is_ongoing": False, "end_year": None}, "end_year"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=changes)
            self.assertIn(field, response.data, msg=changes)
        self.assertEqual(Education.objects.count(), 1)

    def test_html_in_title_is_stripped(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.list_url, {**self.payload, "title": "<b>Halo</b>"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Halo")

    def test_patch_cannot_break_year_rules(self):
        self.client.force_authenticate(user=self.owner)
        self.education.is_ongoing = False
        self.education.end_year = 2026
        self.education.save()
        response = self.client.patch(self.detail_url, {"end_year": 1999}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.education.refresh_from_db()
        self.assertEqual(self.education.end_year, 2026)

    def test_post_rejects_list_body(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, [self.payload], format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Education.objects.count(), 1)

    # --- star
    def test_star_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.education.starred_by.count(), 0)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertIn(self.visitor, self.education.starred_by.all())
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(self.education.starred_by.count(), 0)

    def test_star_get_is_405_when_logged_in_and_403_when_guest(self):
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "skill_list": ["x"],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertEqual(response.data["skill_list"], ["Biologi"])

    # --- CSRF
    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)

    # --- view lama harus sama ketatnya
    def test_old_views_enforce_same_roles(self):
        delete_url = reverse("main:delete_education", args=[self.education.id])
        self.assertEqual(self.client.post(delete_url).status_code, 302)  # guest -> login
        for user in (self.visitor, make_editor("change_education")):
            self.client.force_login(user)
            self.assertEqual(self.client.post(delete_url).status_code, 403)
            self.assertEqual(
                self.client.post(reverse("main:create_education_ajax"), {"title": "X"}).status_code, 403,
            )
        self.client.force_login(self.visitor)
        edit_url = reverse("main:edit_education", args=[self.education.id])
        self.assertEqual(self.client.get(edit_url).status_code, 403)
        self.assert_unchanged()