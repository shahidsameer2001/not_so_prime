# from .forms import Recomendation
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from matplotlib.pyplot import title
from .models import *
from .forms import OrderForm, CreateUserForm
# from .filters import OrderFilter
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Room, Message
from django.shortcuts import render, HttpResponse
from .models import Movie, Series, SeriesVideo


# Create your views here.
# def home(request):
#     movies = Movie.objects.all().order_by('-uploaded')
#     return render(request,'movies/home.html',{'movies':movies})

# def moviePage(request,slug):
#     movie = Movie.objects.get(id=slug)
#     return render(request,'movies/viewpage.html',{'movie':movie})


# def home(request):
#     series = Series.objects.all().order_by('-uploaded')
#     return render(request, 'series/series.html', {'series': series})


# register
def registerPage(request):
    form = CreateUserForm()

    if(request.method == "POST"):
        form = CreateUserForm(request.POST)
        if(form.is_valid()):
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created successfully for '+user)
            return redirect('login')

    context = {'form': form}
    return render(request, '../templates/register/register.html', context)



# login page
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('seriesHome')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('seriesHome')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, '../templates/login/login.html', context)


# logout page
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def seriesHome(request):
    series = Series.objects.all().order_by('-uploaded')
    return render(request, 'series/series.html', {'series': series})


@login_required(login_url='login')
def seriesPage(request, slug):
    serie = Series.objects.get(id=slug)
    videos = SeriesVideo.objects.filter(series=serie)
    return render(request, 'series/seriesPage.html', {'videos': videos, 'serie': serie})


@login_required(login_url='login')
def search(request):

    if(request.method == "GET"):
        query = request.GET.get("search")
        movies = Movie.objects.filter(name__contains=query)
        seriesList = Series.objects.filter(name__contains=query)
        if(not movies):
            items = query.split()
            for item in items:
                films = Movie.objects.filter(name__contains=item)
                movies = movies.union(films)

        if(not seriesList):
            items = query.split()
            for item in items:
                ser = Series.objects.filter(name__contains=item)
                seriesList = seriesList.union(ser)

    return render(request, 'search/search.html', {'movies': movies, 'series': seriesList})


@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')


@login_required(login_url='login')
def room(request, room):
    username = request.GET.get('username')  # henry
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {

        'username': username,
        'room': room,
        'room_details': room_details,
    })


@login_required(login_url='login')
def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)


@login_required(login_url='login')
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(
        value=message, user=username, room=room_id)
    new_message.save()
    # return HttpResponse("Hi, Message Sent Successfully!!")


@login_required(login_url='login')
def getMessages(request,  room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})


# def loginpage(request):
#     return render(request, 'login/login.html')
@login_required(login_url='login')
def game(request):
    return render(request, 'games/game.html')


@login_required(login_url='login')
def labs(request):
    return render(request, 'labs/svit_labs.html')


@login_required(login_url='login')
def question(request):
    question=Questions.objects.all()
    return render(request, 'labs/questions.html', {'question':question})


@login_required(login_url='login')
def profile(request):
    return render(request, 'profile/main.html')


@login_required(login_url='login')
def wordbeater(request):
    return render(request, 'games/wordbeater.html')

def notices(request):
    title = NoticeBoard.objects.all().order_by('-uploaded')
    return render(request, 'base.html', {'title': title})



