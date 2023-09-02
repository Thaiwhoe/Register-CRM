from django.shortcuts import render
# Create your views here.


def index(request):
    return render(request, 'core/index.html')


def about(request):
    return render(request, 'core/about.html')


def userInfo(request):
    name = request.user.username[:2]

    return render(request, {
        'name': name
    })
