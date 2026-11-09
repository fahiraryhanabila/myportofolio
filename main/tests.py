from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import Permission

from main.models import Education, Experience


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            thumbnail="https://test.com/experience.jpg",
        )
        self.education = Education.objects.create(
            title="Tes",
            category_edu="Bachelor's Degree",
            start_year=2025,
            is_ongoing=True,
            description="Studying Information Systems at Universitas Indonesia.",
            skills="Programming, UX Research",
            thumbnail="https://test.com/education.jpg",
        )

    # ------------------------------------------------------------ umum
    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    # ------------------------------------------------------ model Experience
    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)
        self.assertEqual(self.experience.thumbnail, "https://test.com/experience.jpg")

    # ------------------------------------------------- halaman Experience
    def test_experience_page_skeleton(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        # Kerangka yang diisi JavaScript
        for element_id in ("loading", "error", "empty", "grid", "search-input"):
            self.assertContains(response, f'id="{element_id}"')
        # Halaman memakai API DRF, bukan endpoint lama
        self.assertContains(response, reverse("api:experience-list"))
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        # Data tidak lagi dirender server
        self.assertNotContains(response, self.experience.title)

    def test_experience_page_empty_state_message(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(
            response, "Belum ada pengalaman yang ditambahkan atau ditemukan."
        )
        api = self.client.get(reverse("api:experience-list"))
        self.assertEqual(api.status_code, 200)
        self.assertEqual(api.data, [])

    def test_experience_page_hides_add_button_from_guest(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertNotContains(response, 'popovertarget="add-experience-modal"')
        self.assertNotContains(response, 'id="add-experience-modal"')

    def test_experience_page_shows_add_button_to_owner(self):
        owner = User.objects.create_superuser("owner", "o@example.com", "test-password")
        self.client.force_login(owner)
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, 'popovertarget="add-experience-modal"')
        self.assertContains(response, 'id="add-experience-modal"')

    # ---------------------------------------------------- data Experience
    def test_experience_data_via_api(self):
        response = self.client.get(reverse("api:experience-list"))

        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item["title"], self.experience.title)
        self.assertEqual(item["description"], self.experience.description)
        self.assertEqual(item["category"], "part-time")
        self.assertEqual(item["category_display"], "Part-Time")
        self.assertEqual(item["thumbnail"], "https://test.com/experience.jpg")
        self.assertTrue(item["is_ongoing"])

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now() - timedelta(days=1)
        self.experience.save()
        response = self.client.get(reverse("api:experience-list"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertFalse(response.data[0]["is_ongoing"])
        self.assertIsNotNone(response.data[0]["ended_at"])

    def test_legacy_experience_json_still_works(self):
        response = self.client.get(reverse("main:get_experience_json"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["title"], self.experience.title)

    # -------------------------------------------------- halaman Education
    def test_education_url_is_accessible(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_page_skeleton(self):
        response = self.client.get(reverse("main:show_education"))

        for element_id in ("loading", "error", "empty", "grid", "search-input"):
            self.assertContains(response, f'id="{element_id}"')
        self.assertContains(response, reverse("api:education-list"))
        self.assertNotContains(response, self.education.title)
        self.assertNotContains(response, self.education.description)

    def test_education_page_empty_state_message(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(
            response, "Belum ada riwayat pendidikan yang ditambahkan atau ditemukan."
        )
        api = self.client.get(reverse("api:education-list"))
        self.assertEqual(api.status_code, 200)
        self.assertEqual(api.data, [])

    def test_education_page_hides_add_button_from_guest(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertNotContains(response, 'popovertarget="add-education-modal"')
        self.assertNotContains(response, 'id="add-education-modal"')

    def test_education_page_shows_add_button_to_owner(self):
        owner = User.objects.create_superuser("owner", "o@example.com", "test-password")
        self.client.force_login(owner)
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, 'popovertarget="add-education-modal"')
        self.assertContains(response, 'id="add-education-modal"')
        self.assertContains(response, "education-add-button")

    # ----------------------------------------------------- data Education
    def test_education_data_via_api(self):
        response = self.client.get(reverse("api:education-list"))

        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item["title"], self.education.title)
        self.assertEqual(item["description"], self.education.description)
        self.assertEqual(item["category_edu"], "Bachelor's Degree")
        self.assertEqual(item["category_edu_display"], "Bachelor's Degree")
        self.assertEqual(item["skill_list"], ["Programming", "UX Research"])
        self.assertEqual(item["thumbnail"], "https://test.com/education.jpg")
        self.assertTrue(item["is_ongoing"])
        self.assertEqual(item["start_year"], 2025)
        self.assertIsNone(item["end_year"])

    def test_completed_education_shows_year_range(self):
        self.education.is_ongoing = False
        self.education.end_year = 2029
        self.education.save()

        response = self.client.get(reverse("api:education-list"))

        item = response.data[0]
        self.assertFalse(item["is_ongoing"])
        self.assertEqual(item["start_year"], 2025)
        self.assertEqual(item["end_year"], 2029)

    def test_legacy_education_json_still_works(self):
        response = self.client.get(reverse("main:get_education_json"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["title"], self.education.title)
        self.assertEqual(data[0]["fields"]["start_year"], 2025)
    
    def test_education_page_renders_modal_for_editor_without_add_button(self):
        editor = User.objects.create_user("editor", password="test-password")
        editor.user_permissions.add(Permission.objects.get(codename="change_education"))
        self.client.force_login(editor)
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, 'id="add-education-modal"')
        self.assertNotContains(response, "education-add-button")