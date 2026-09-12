from django.shortcuts import render
from django.http import HttpResponse

from main.models import Experience
from main.models import Education


def show_main(request):
    context = {
        "name": "Fahira Ryhanabila",
        "npm": "2506623660",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "I'm an Information Systems student at Universitas Indonesia who enjoys exploring the intersection of technology, business, and user experience."
            "I'm always excited to learn, collaborate, and create solutions that make a real impact — whether through product, research, or meaningful conversations."
        ),
        "education_list": Education.objects.all()
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Fahira",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Fahira",
        "education_list": Education.objects.all()
    }
    return render(request, "education.html", context)

def seeder_data(request):
    Experience.objects.get_or_create(
        title="Staff Ambassador Open House Fasilkom UI",
        defaults={
            "description": "Managed the Open House Fasilkom UI Ambassador program, including candidate selection, organizing supporting events and the farewell party, and monitoring ambassador performance in producing promotional content.",
            "category": "part-time",
            "ended_at" : "2025-11-04"
        }
    )
    
    Experience.objects.get_or_create(
        title="Staff Hubungan Masyarakat BETIS Fasilkom UI",
        defaults={
            "description": "Served as the main communication bridge between BETIS Fasilkom UI and high school students, managed BETIS's content and social media accounts, drafted broadcast announcements, and disseminated registration information.",
            "category": "part-time",
            "ended_at": "2025-09-01",
        }
    )
    
    Experience.objects.get_or_create(
        title="Product Management Academy Staff at COMPFEST 18",
        defaults={
            "description": "Managed class operations and mentor coordination for a product management training program, monitored participant progress, and compiled program outcome reports covering completion rate, satisfaction, and career outcomes.",
            "category": "part-time",
            "ended_at": None,   
        }
    )
    
    Experience.objects.get_or_create(
        title="IT Force Staff at FUKI Fasilkom UI",
        defaults={
            "description": "Designed wireframes, mockups, and prototypes for organizational digital platforms, maintained design system consistency, and collaborated with developers to ensure accurate implementation.",
            "category": "part-time",
            "ended_at": None,
        }
    )
    return HttpResponse("Seeding data berhasil!")