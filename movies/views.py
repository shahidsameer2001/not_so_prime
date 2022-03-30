from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Room, Message
from django.shortcuts import render,HttpResponse
from .models import Movie,Series,SeriesVideo
# Create your views here.
def home(request):
    movies = Movie.objects.all().order_by('-uploaded')
    return render(request,'movies/home.html',{'movies':movies})

def moviePage(request,slug):
    movie = Movie.objects.get(id=slug)
    return render(request,'movies/viewpage.html',{'movie':movie})

def seriesHome(request):
    series = Series.objects.all().order_by('-uploaded')
    return render(request,'series/series.html',{'series':series})
    
def seriesPage(request,slug):
    serie = Series.objects.get(id = slug)
    videos = SeriesVideo.objects.filter(series = serie)
    return render(request,'series/seriesPage.html',{'videos':videos,'serie':serie})


def search(request):
    
    if(request.method == "GET"):
        query = request.GET.get("search")
        movies = Movie.objects.filter(name__contains=query)
        seriesList = Series.objects.filter(name__contains=query)
        if(not movies):
            items = query.split()
            for item in items:
                films = Movie.objects.filter(name__contains = item)
                movies = movies.union(films)

        if(not seriesList):
            items = query.split()
            for item in items:
                ser = Series.objects.filter(name__contains = item)
                seriesList = seriesList.union(ser)

    return render(request, 'search/search.html', {'movies': movies, 'series': seriesList})


def index(request):
    return render(request, 'index.html')


def room(request, room):
    username = request.GET.get('username')  # henry
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {

        'username': username,
        'room': room,
        'room_details': room_details,
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(
        value=message, user=username, room=room_id)
    new_message.save()
    # return HttpResponse("Hi, Message Sent Successfully!!")


def getMessages(request,  room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})
