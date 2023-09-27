from django.contrib.auth.models import User
from django.db import models


class RecordLabel(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Record(models.Model):
    artist = models.CharField(max_length=30)
    album = models.CharField(max_length=40)
    year = models.IntegerField()
    condition = models.CharField(max_length=3)
    genre = models.ManyToManyField("records.RecordGenre")
    record_label = models.ForeignKey(RecordLabel, on_delete=models.PROTECT)
    price = models.FloatField(max_length=6)
    quantity = models.IntegerField()

    def cover_path(self):
        name = str(self.album)
        cover = f'/records/{name}.jpg'
        return cover

    def __str__(self):
        return self.album


class RecordGenre(models.Model):
    genre = models.CharField(max_length=20)

    def __str__(self):
        return self.genre


class Order(models.Model):
    record = models.ManyToManyField(Record)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.TextField(default='created')
    date = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.pk}'

