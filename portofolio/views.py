from django.shortcuts import render

#nampilin halaman teretentu 
def landing_page(request):
    return render(request, "index.html")