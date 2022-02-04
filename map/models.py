from hashlib import blake2b
from tkinter import CASCADE
from django.db import models
from brand.models import Brand
from django.contrib.auth.models import User

# Create your models here.

# 부스 이름, 부스 종류, 부스 주소, 부스 운영시간, 부스 브랜드
class Booth(models.Model):
    name = models.CharField(max_length=100)
    type = models.IntegerField()
    location = models.TextField()
    operationHour = models.TimeField()
    brand = models.OneToOneField(Brand, on_delete=models.CASCADE)
    
    user = models.ManyToManyField(User, through='Liked', through_fields=('booth', 'user'))
    
    def __str__(self):
        return self.name

# user - liked - booth 다 대 다 연결
class Liked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    date = models.DateField()


# 리뷰 작성할 부스, 리뷰 작성하는 user, title, 리뷰 작성한 시간, 사진, 별점
# tag 추가해야 됨
class Review(models.Model):
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    date = models.DateField()
    img = models.ImageField(blank=True, null=True, upload_to = "")
    rate = models.IntegerField()

