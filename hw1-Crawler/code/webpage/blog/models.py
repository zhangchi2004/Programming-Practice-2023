from django.db import models
import uuid

# Create your models here.
class Blog(models.Model):
    app_label = 'blog'
    title = models.CharField(max_length=300)
    pub_date = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    comment_count = models.IntegerField(default=0)
    hot = models.IntegerField()
    link = models.CharField(max_length=200)
    intro = models.CharField(max_length=400,null=True,blank=True)

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    user = models.CharField(max_length=50)
    comment_content = models.CharField(max_length=1000)
    time = models.CharField(max_length=50)
    
class Para(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)

class Text_para(models.Model):
    para = models.OneToOneField(Para, on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=2000)

class Img_para(models.Model):
    para = models.OneToOneField(Para, on_delete=models.CASCADE, null=True, blank=True)
    #img_link = models.CharField(max_length=200)
    img_desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images/',null=True)

class Word(models.Model):
    realword = models.CharField(max_length=50)

class Doc(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, null=True, blank=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    tfidf = models.IntegerField()