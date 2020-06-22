from django.db import models
from django.urls import reverse

# Create your models here.
class Album(models.Model):
    artist= models.CharField(max_length=20)
    album_title=models.CharField(max_length=40)
    genre =models.CharField(max_length=10)
    album_logo= models.FileField()

    def get_absolute_url(self):
        return reverse('music:detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.album_title+ "-" + self.artist + "-"+ self.genre

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type=models.CharField(max_length=10)
    song_title= models.CharField(max_length=250)
    is_favourite=models.BooleanField(default=False)

    def __str__(self):
        return self.song_title