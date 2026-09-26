import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from main.models import Experience
from main.models import Education
from main.forms import EducationForm
from main.forms import ExperienceForm

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Fahira Ryhanabila",
        "npm": "2506623660",
        "study_program": "S1 Sistem Informasi",
        "last_login": last_login,
        "bio": (
            "I'm an Information Systems student at Universitas Indonesia who enjoys exploring the intersection of technology, business, and user experience."
            " I'm always excited to learn, collaborate, and create solutions that make a real impact — whether through product, research, or meaningful conversations."
        ),
        "education_list": Education.objects.all()
    }
    return render(request, "index.html", context)


def show_experience(request):
    json_response = get_experience_json(request)

    experience = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experience = [item.object for item in experience]
    title_query = request.GET.get("title", "").strip()
    context = {
        "name": "Fahira",
        "experience_list": experience,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)


def show_education(request):
    json_response = get_education_json(request)

    education = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    education = [item.object for item in education]
    title_query = request.GET.get("title", "").strip()
    context = {
        "name": "Fahira",
        "education_list": education,
        "title_query": title_query,
    }
    return render(request, "education.html", context)


@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pendidikan baru berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Fahira Ryhanabila",
        "form": form,
    }
    return render(request, "education_form.html", context)


def get_education_json(request):
    title_query = request.GET.get("title", "").strip()
    education = Education.objects.all()

    if title_query:
        education = education.filter(title__icontains=title_query)

    education_json = serializers.serialize(
        "json", education, use_natural_foreign_keys=True
    )
    return HttpResponse(education_json, content_type="application/json")


@login_required(login_url="/login/")
def delete_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Riwayat pendidikan berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")


@login_required(login_url="/login/")
def edit_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, instance=education)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pendidikan berhasil diperbarui!")
        return redirect("main:show_education")

    context = {
        "name": "Fahira",
        "form": form,
    }
    return render(request, "education_form.html", context)


@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")
    context = {
        "name": "Fahira Ryhanabila",
        "form": form,
        "is_edit": False,
    }
    return render(request, "experience_form.html", context)


def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experience = Experience.objects.all()

    if title_query:
        experience = experience.filter(title__icontains=title_query)

    experience_json = serializers.serialize(
        "json", experience, use_natural_foreign_keys=True
    )
    return HttpResponse(experience_json, content_type="application/json")


@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Riwayat experience berhasil ditambahkan!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


@login_required(login_url="/login/")
def edit_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Fahira",
        "form": form,
        "is_edit": True,
        "experience_id": experience_id,
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")


@login_required(login_url="/login/")
def star_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        if request.user in education.starred_by.all():
            education.starred_by.remove(request.user)
        else:
            education.starred_by.add(request.user)

    return redirect("main:show_education")


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Fahira",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Fahira",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response


def seeder_data(request):
    Experience.objects.update_or_create(
        title="Staff Ambassador Open House Fasilkom UI",
        defaults={
            "description": "Managed the Open House Fasilkom UI Ambassador program, including candidate selection, organizing supporting events and the farewell party, and monitoring ambassador performance in producing promotional content.",
            "category": "part-time",
            "ended_at": "2025",
            "thumbnail": "/static/img/ambass-photo.jpeg",
        }
    )

    Experience.objects.update_or_create(
        title="Staff Hubungan Masyarakat BETIS Fasilkom UI",
        defaults={
            "description": "Served as the main communication bridge between BETIS Fasilkom UI and high school students, managed BETIS's content and social media accounts, drafted broadcast announcements, and disseminated registration information.",
            "category": "part-time",
            "ended_at": "2025",
            "thumbnail": "/static/img/betis-photo.jpeg",
        }
    )

    Experience.objects.update_or_create(
        title="Product Management Academy Staff at COMPFEST 18",
        defaults={
            "description": "Managed class operations and mentor coordination for a product management training program, monitored participant progress, and compiled program outcome reports covering completion rate, satisfaction, and career outcomes.",
            "category": "part-time",
            "ended_at": None,
            "thumbnail": "/static/img/compest-photo.jpeg",
        }
    )

    Experience.objects.update_or_create(
        title="IT Force Staff at FUKI Fasilkom UI",
        defaults={
            "description": "Designed wireframes, mockups, and prototypes for organizational digital platforms, maintained design system consistency, and collaborated with developers to ensure accurate implementation.",
            "category": "part-time",
            "ended_at": None,
            "thumbnail": "/static/img/itf-photo.jpeg",
        }
    )

    Experience.objects.update_or_create(
        title="Facilitator Baitul Arqam Madya 2026 PD IPM Yogyakarta",
        defaults={
            "description": "Volunteered as a facilitator, guiding participants throughout the Baitul Arqam Madya program and supporting their learning and engagement.",
            "category": "volunteer",
            "ended_at": "2026",
            "thumbnail": "/static/img/ba-photo.jpeg",
        }
    )

    Experience.objects.update_or_create(
        title="Staff at SBF Adkesma 2025",
        defaults={
            "description": "Supported student advocacy and welfare initiatives by assisting in identifying student concerns, developing solutions, and organizing related programs.",
            "category": "internship",
            "ended_at": "2026",
            "thumbnail": "/static/img/adkesma-photo.jpeg",
        }
    )

    return HttpResponse("Seeding data berhasil!")