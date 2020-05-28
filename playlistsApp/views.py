from django.shortcuts import render, redirect, HttpResponse
from . models import User, Song, Playlist
from django.contrib import messages
import bcrypt
from django.db.models import Q





def index(request):
    return render(request, 'index.html')
def processnewuser(request):
    print(request.POST)
    
    errors=User.objects.registrationValidator(request.POST)
    if len(errors)>0:
        for k,v in errors.items():
            messages.error(request, v)
        return redirect('/')
    else:

        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
        print(pw_hash)
        createnew=User.objects.create(name=request.POST['name'], username=request.POST['uname'], birthdate=request.POST['birthdate'], password=pw_hash)
        request.session['userid']=createnew.id

    return redirect('/welcome')
def login(request):
    loginerrors=User.objects.loginValidator(request.POST)
    if len(loginerrors)>0:
        for k,v in loginerrors.items():
            messages.error(request, v)
        return redirect('/')
    else:
        user = User.objects.get(username=request.POST['uname'])
        request.session['userid']=user.id
        
    return redirect('/welcome')

def logout(request):
    request.session.clear()
    return redirect('/')

def welcome(request):
    if 'userid' not in request.session:
        return redirect('/')
    loggedinuser=User.objects.get(id=request.session['userid'])
    context={
        'loggedinuser':loggedinuser,
        'allmusic': Song.objects.all()
    }
    
    return render(request, 'welcome.html', context)

def addsong(request):
    
    
    return render(request, 'addsong.html')
def processsong(request):

    thisuser=User.objects.get(id=request.session['userid'])
    createsong=Song.objects.create(title=request.POST['title'], artist=request.POST['artist'], genre=request.POST['genre'], users=thisuser)
    return redirect('/addsong')

def createplaylist(request):
    allsongs=Song.objects.all()
    allusers=User.objects.all()
    thisuser=User.objects.get(id=request.session['userid'])
    thisuserplaylists=Playlist.objects.filter(Q(creator=thisuser) | Q(users=thisuser))

    context={
        'allsongs': allsongs,
        'allusers': allusers,
        'allplaylists': thisuserplaylists

    }

    return render (request, 'addplaylist.html', context)

def processplaylist(request):
    print(request.POST)
    thisuser=User.objects.get(id=request.session['userid'])

    if int(request.POST['otheruser']) != 0:
        createplaylist=Playlist.objects.create(name=request.POST['title'], creator=thisuser)
        otheruser=User.objects.get(id=request.POST['otheruser'])
        createplaylist.users.add(otheruser)
    elif int(request.POST['otheruser']) == 0:
        createplaylist=Playlist.objects.create(name=request.POST['title'], creator=thisuser)
        
    return redirect('/createplaylist')
def addsongstoplaylist(request):
    print(request.POST)
    selectedplaylist=Playlist.objects.get(id=request.POST['playlists'])

    print(selectedplaylist.id)

    if int(request.POST['song1']) != 0:
        addsong=Song.objects.get(id=request.POST['song1'])
        selectedplaylist.songs.add(addsong)
    if int(request.POST['song2']) != 0:
        addsong=Song.objects.get(id=request.POST['song2'])
        selectedplaylist.songs.add(addsong)
    if int(request.POST['song3']) != 0:
        addsong=Song.objects.get(id=request.POST['song3'])
        selectedplaylist.songs.add(addsong)
    if int(request.POST['song4']) != 0:
        addsong=Song.objects.get(id=request.POST['song4'])
        selectedplaylist.songs.add(addsong)
    if int(request.POST['song5']) != 0:
        addsong=Song.objects.get(id=request.POST['song5'])
        selectedplaylist.songs.add(addsong)
    if request.POST['whichform']=='fromdisplay':
        return redirect(f'displayplaylist/{selectedplaylist.id}')
    if request.POST['whichform']=='fromadd':
        return redirect('/createplaylist')

def seeplaylists(request):
    thisuser=User.objects.get(id=request.session['userid'])
    userplaylists=Playlist.objects.filter(creator=thisuser)
    collabplaylists=Playlist.objects.filter(users=thisuser)
    otherplaylists=Playlist.objects.exclude(Q(creator=thisuser) | Q(users=thisuser))
    
    context={
        'allplaylists': userplaylists,
        'collabplaylists':collabplaylists,
        'otherplaylists': otherplaylists

    }

    return render(request, 'viewplaylists.html', context)

def displayplaylist(request, playlistId):
    thisplaylist=Playlist.objects.get(id=playlistId)
    allsongs=Song.objects.all()
    allusers=User.objects.all()
    thisuser=User.objects.get(id=request.session['userid'])
    context={
        'allsongs': allsongs,
        'allusers': allusers,
        'thisplaylist':thisplaylist

    }
    return render(request, 'displayplaylist.html', context)


def delete(request):
    print(request.POST)
    print(request.POST['song'])
    thissong=Song.objects.get(id=request.POST['song'])
    thissong.delete()
    

    return redirect('/welcome')

def deleteplaylist(request):
    
    print(request.POST)
    print(request.POST['playlist'])
    thisplaylist=Playlist.objects.get(id=request.POST['playlist'])
    thisplaylist.delete()

    return redirect('/seeplaylists')