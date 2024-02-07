from django.shortcuts import render
from .models import *
from django.template import loader
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from datetime import datetime
import random
import jieba
import json
import pandas as pd
import csv
from django.core.cache import cache
import ast
import ujson
from time import time
from django.core.paginator import Paginator
def show_blog(request, id):
    blog = Blog.objects.get(id=id)
    template = loader.get_template('blog_page.html')
    context = {
        'blog_id': id,
        'title': blog.title,
        'comments': blog.comment_set.all().order_by('-time'), # 通过外键反向查询
        'paras': blog.para_set.all(),
        'author': blog.author,
        'pub_date': blog.pub_date,
        'comment_count': blog.comment_count,
        'hot': blog.hot,
        'link': blog.link,        
    }
    return HttpResponse(template.render(context, request))

def comment(request, id):  # 这里 request 是 HttpRequest 类型的对象
    data = request.POST
    # 验证请求数据是否满足接口要求，若通过所有的验证，则将新的消息添加到数据库中
    # 这里的字段均有最大长度限制
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = data['user']
    comment_content = data['content']
    blog = Blog.objects.get(id=id) # 在数据库中根据标题找到对应的博客
    obj = Comment(blog=blog, user=user, time=time, comment_content=comment_content)
    blog.comment_count+=1
    blog.hot += (75+15*random.random())
    blog.save()
    obj.full_clean() #对数据进行验证
    obj.save() #存储在表中
    return HttpResponseRedirect(f'/index/blog/{id}')

def delcomment(request,id):
    comment = Comment.objects.get(id=id)
    blog = comment.blog
    blog.comment_count-=1
    blog.hot -= 75
    if blog.hot<0: blog.hot=0
    blog.save()
    comment.delete()
    
    return HttpResponseRedirect(f'/index/blog/{blog.id}')

def show_home(request):
    template = loader.get_template('home.html')
    N = 5000 # 新闻总数，需要修改
    randomid = random.sample(range(1,N+1),20)
    randomblogs = [Blog.objects.get(id=i) for i in randomid]
    context = {
        'random_blogs':randomblogs
    }
    return HttpResponse(template.render(context,request))

def show_list(request):
    template = loader.get_template('list.html')
    
    page = int(request.GET.get('page'))
    cache_key = f'list'
    bloglist = cache.get(cache_key)
    if bloglist is None:
        bloglist = Blog.objects.all()
        cache.set(cache_key, bloglist, 60 * 60)
    paginator = Paginator(bloglist, 20)
    try:
        current_page = paginator.get_page(page)
    except EmptyPage:
        current_page = paginator.get_page(1)
    


    context = {
        'current_page':current_page,
    }


    return HttpResponse(template.render(context,request))

def show_classes(request):
    template = loader.get_template('classes.html')
    context = {}
    return HttpResponse(template.render(context,request))

def show_classes_1(request):
    page = int(request.GET.get('page'))
    template = loader.get_template('listclass.html')
    cache_key = f'class1'
    bloglist = cache.get(cache_key)
    if bloglist is None:
        bloglist = [Blog.objects.get(id=i) for i in range(1,114)]
        cache.set(cache_key, bloglist, 60 * 60)
    paginator = Paginator(bloglist, 20)
    try:
        current_page = paginator.get_page(page)
    except EmptyPage:
        current_page = paginator.get_page(1)
    context = {
        'current_page':current_page,
    }
    return HttpResponse(template.render(context,request))

def show_classes_2(request):
    page = int(request.GET.get('page'))
    template = loader.get_template('listclass.html')
    cache_key = f'class2'
    bloglist = cache.get(cache_key)
    if bloglist is None:
        bloglist = [Blog.objects.get(id=i) for i in range(114,792)]
        cache.set(cache_key, bloglist, 60 * 60)
    paginator = Paginator(bloglist, 20)
    try:
        current_page = paginator.get_page(page)
    except EmptyPage:
        current_page = paginator.get_page(1)
    context = {
        'current_page':current_page,
    }
    return HttpResponse(template.render(context,request))

def show_classes_3(request):
    page = int(request.GET.get('page'))
    template = loader.get_template('listclass.html')
    cache_key = f'class3'
    bloglist = cache.get(cache_key)
    if bloglist is None:
        bloglist = [Blog.objects.get(id=i) for i in range(792,5001)]
        cache.set(cache_key, bloglist, 60 * 60)
    paginator = Paginator(bloglist, 20)
    try:
        current_page = paginator.get_page(page)
    except EmptyPage:
        current_page = paginator.get_page(1)
    context = {
        'current_page':current_page,
    }
    return HttpResponse(template.render(context,request))

def show_search(request):
    template = loader.get_template('search.html')
    context = {}
    return HttpResponse(template.render(context,request))

def search(request):
    if request.GET.get('page') is not None:
        page = int(request.GET.get('page'))
    else: page=1
    time1 = time()
    template=loader.get_template('listresult.html')
    data = request.POST
    keys = request.GET.get('keys')
    order = request.GET.get('order')

    state1 = request.GET.get('class1')
    state2 = request.GET.get('class2')
    state3 = request.GET.get('class3')

    
    cache_key = f'search_results_{keys}_{order}_{state1}_{state2}_{state3}'
    sorted_bloglist = cache.get(cache_key)
    if sorted_bloglist is not None:
        result_num = len(sorted_bloglist)
        ftime = 0
    if sorted_bloglist is None:
        idallowed = set()
        if state1=="selected":
            idallowed.update(range(1, 114))
        if state2=="selected":
            idallowed.update(range(114,792))
        if state3=="selected":
            idallowed.update(range(792,5001))
        if len(idallowed)==0:
            idallowed.update(range(1,5001))
        word_dict = {}
        bloglist = []
        time3=time()
        with open('../tf_idf_correct.json', encoding="utf-8") as f:
            word_dict = ujson.load(f)
            print("loaded")
        time4=time()
        ftime = time4-time3
        if request.GET.get('order')=='by_match':
            result_num = 0
            seg_list = jieba.cut_for_search(keys)
            tfidf = {id:0 for id in range(1,5001)}
            word_lengths = {word: len(word) for word in seg_list}
            for word in word_lengths:
                if word in word_dict:
                    for id in word_dict[word]:
                        if int(id) in idallowed:
                            tfidf[int(id)] += word_lengths[word]*word_dict[word][id]

            sorted_tfidf = dict(sorted(tfidf.items(), key=lambda item: -item[1]))
            tfidf_keys = list(sorted_tfidf.keys())[:200]
            sorted_bloglist = [Blog.objects.get(id=key) for key in tfidf_keys]
            result_num = len(sorted_bloglist)


        else:
            chosen = {id:False for id in range(1,5001)}
            
            if keys in word_dict:
                for id in word_dict[keys]:
                    id=int(id)
                    if chosen[id]==False and id in idallowed:
                        bloglist.append(id)
                        chosen[int(id)]=True

            result_num = len(bloglist)

            if request.GET.get('order')=='by_time': sorted_bloglist = Blog.objects.filter(id__in=bloglist).order_by('-pub_date')        
            elif request.GET.get('order')=='by_hot': sorted_bloglist = Blog.objects.filter(id__in=bloglist).order_by('-hot')
        cache.set(cache_key, sorted_bloglist, 60 * 60)

    paginator = Paginator(sorted_bloglist, 20)
    try:
        current_page = paginator.get_page(page)
    except EmptyPage:
        current_page = paginator.get_page(1)
    time2=time()
    

    context = {
        'current_page':current_page,
        'addition':f'&order={order}&keys={keys}',
        'order':order,
        'keys':keys,
        'resultnum':result_num,
        'state1':state1,
        'state2':state1,
        'state3':state1,
        'alltime':time2-time1,
        'ftime':ftime,
        'stime':time2-time1-ftime,
    }
    return HttpResponse(template.render(context,request))
