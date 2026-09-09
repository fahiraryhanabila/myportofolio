from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Fahira Ryhanabila",
        "npm": "2506623660",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "I'm an Information Systems student at Universitas Indonesia who enjoys exploring the intersection of technology, business, and user experience."
            "I'm always excited to learn, collaborate, and create solutions that make a real impact — whether through product, research, or meaningful conversations."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Fahira",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)