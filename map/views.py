from calendar import c
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm
from .models import *

from LnF.models import LnF_Post
from brand.models import Brand
from user.models import User

from django.templatetags.static import static
from django.db.models import Q
from pytz import timezone
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def mymap(request):
    booths = Booth.objects.all() 
    ctx = {'booths': booths} # 너무 많으면 여기서 booths[:10] 로 몇개만 뽑아도 됨!
    return render(request, 'map/mymap.html', context=ctx)

def avg(pk): # 평균 별점 계산 함수
    booth = Booth.objects.get(id=pk)
    reviews = Review.objects.filter(booth = booth.pk)

    n=0
    sum =0
    for review in reviews:
        n += 1
        sum += review.rate
    booth.rating = sum/n
    booth.review_number = n
    booth.save()

def booth_detail(request,pk):
    booth = Booth.objects.get(id=pk)  # id가 pk인 게시물 하나를 가져온다.
    reviews = Review.objects.filter(booth = booth.pk)
    lnfs = LnF_Post.objects.filter(booth= booth.pk)
    avg(pk) # 왜 새로고침해야 뜨는거지
    ctx = {'booth': booth, 'lnfs' : lnfs, 'reviews': reviews}
    return render(request, template_name='map/booth_detail.html', context=ctx)

def review_list(request):
    reviews = Review.objects.all()
    ctx = {'reviews': reviews}
    return render(request, template_name='map/review_list.html', context=ctx)  # context를 딕셔너리 형태로 만들어서 보낸다.

def review_detail(request, pk):  # request도 받고 몇번 인덱스인지 = pk를 받는다. 게시물 상세조
    review = Review.objects.get(id=pk)  # id가 pk인 게시물 하나를 가져온다
    ctx = {'review': review}  # template로 보내기 위해선 context를 만들어야한다.
    return render(request, template_name='map/review_detail.html', context=ctx)

def review_create(request):
    user = request.user
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.save()
            return redirect('map:review_list')
    else:
        form = ReviewForm()
    ctx = {'form': form}
    return render(request, template_name='map/review_create.html', context=ctx)

def review_update(request, pk):
    review = get_object_or_404(Review, id=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            return redirect('reviews:review_detail', pk)
    else:
        form = ReviewForm(instance=review)
        ctx = {'form': form}

        return render(request, template_name='map/review_create.html', context=ctx)

def review_delete(request, pk):
    review = get_object_or_404(Review, id=pk)
    review.delete()
    return redirect('reviews:review_list')


'''
@csrf_exempt
def like_ajax(request):
    req = json.loads(request.body)
    booth_id = req['id']
    booth = Booth.objects.get(id =booth_id)

    if booth.dolike == True:
        post.dolike = False
        status = post.dolike
        k=1
    else:
        post.dolike = True
        status = post.dolike
        k=0
    post.save()

    return JsonResponse({'id': post_id, 'k': k, 'status':status})
    
'''

def search(request):
    search = request.GET.get('search','')
    boothlist = Booth.objects.filter(name__contains=search)
    ctx = {'booths':boothlist}
    return render(request, 'map/mymap.html', context=ctx)
