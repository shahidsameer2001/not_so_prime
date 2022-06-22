# from .forms import Recomendation
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from matplotlib.pyplot import title
from .models import *
from .forms import *

# from .filters import OrderFilter
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Room, Message
from django.shortcuts import render, HttpResponse
from .models import Movie, Series, SeriesVideo
from django.urls import reverse


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
        if(form.is_valid() ):
            form.save()
            user = form.cleaned_data.get('username')

            
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
    note = NoticeBoard.objects.all()
    return render(request, 'series/series.html', {'series': series, 'note': note})


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
    que = Questions.objects.all()
    return render(request, 'labs/svit_labs.html', {'que': que})


@login_required(login_url='login')
def question(request):
    id = request.GET.get('id')
    que = Questions.objects.get(id=id)
    return render(request, 'labs/questions.html', {'que': que})


@login_required(login_url='login')
def profile(request):
    series = Series.objects.all().order_by('-uploaded')
    return render(request, 'profile/main.html', {'series': series})


@login_required(login_url='login')
def wordbeater(request):
    return render(request, 'games/wordbeater.html')


# @login_required(login_url='login')
# def notice(request):
#     id=request.GET.get('id')
#     note = NoticeBoard.objects.get(id=id)
#     return render(request, 'series/series.html', {'note': note})


@login_required(login_url='login')
def sudoku(request):
    return render(request, 'games/sudoku.html')


@login_required(login_url='login')
def tic_tac_toe(request):
    return render(request, 'games/tic_tac_toe.html')


# edit profile
@login_required(login_url='login')
def edit_profile(request):

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
        context = {'form': form}
        # print(context)
        form.fields['last_login'].widget = forms.HiddenInput()
        form.fields['password'].widget = forms.HiddenInput()
        form.fields['is_superuser'].widget = forms.HiddenInput()
        form.fields['groups'].widget = forms.MultipleHiddenInput()
        form.fields['user_permissions'].widget = forms.MultipleHiddenInput()
        form.fields['is_staff'].widget = forms.HiddenInput()
        form.fields['is_active'].widget = forms.HiddenInput()
        form.fields['date_joined'].widget = forms.HiddenInput()
        form.fields['first_name'].label = 'Full_Name'
        form.fields['last_name'].label = 'Image_Url'


        return render(request, 'profile/edit_profile.html', context)


@login_required(login_url='login')
def about(request):
    return render(request,'about.html')