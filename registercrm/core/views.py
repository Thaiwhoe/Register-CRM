from django.shortcuts import render
# Create your views here.


def index(request):
    short_name = request.user.username[:2]
    print(short_name)
    return render(request, 'core/index.html', {
        'short_name': short_name
    })


def about(request):
    return render(request, 'core/about.html')


def userInfo(request):
    short_name = request.user.username[:2]
    print(short_name)
    return {'short_name': short_name}
