from django.db import models
import bcrypt

class UserManager(models.Manager):
    def registrationValidator(self, postData):
        errors={}
        if (len(postData['name']))<1:
            errors['name']="You have to enter your name!"
        elif (len(postData['name']))<2:
            errors['name']="The name you entered is too short! Try again."
        if (len(postData['uname']))<1:
            errors['username']='You have to create a username!'
        elif (len(postData['uname']))<3:
            errors['username']='This username is too short! You must create a username that is 3 or more characters.'
        if (len(postData['password']))<8:
            errors['password']="Your password must be at least 8 characters!"
        elif postData['password'] != postData['password2']:
            errors['password']="Passwords do not match!"
        return errors 
    def loginValidator(self, postData):
        loginerrors={}
        user = User.objects.filter(username=postData['uname']) #list
        if len(user)==0:
            loginerrors['usernotfound']="This user does not exist. Please register."
        else:
            loggeduser = user[0] 
            if bcrypt.checkpw(postData['password'].encode(), loggeduser.password.encode()):
                print('Passwords match!')
            else:
                print('Passwords do not match')
                loginerrors['pwnotfound']="This password for the user was not found. Please try again."

        return loginerrors

class User(models.Model):
    name=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=60)
    birthdate=models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()
class Song(models.Model):
    title=models.CharField(max_length=255)
    artist=models.CharField(max_length=255)
    genre=models.CharField(max_length=255, null=True)
    users=models.ForeignKey(User, related_name='songs', on_delete=models.CASCADE)
    likes=models.ManyToManyField(User, related_name='likedsongs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Playlist(models.Model):
    name=models.CharField(max_length=255)
    songs=models.ManyToManyField(Song, related_name='playlistsongs')
    creator=models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE, null=True)
    users=models.ManyToManyField(User, related_name='playlistcreators')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
