from blog.models import *
from django.core.files import File
csv_path = "../with_local_img/"
import pandas as pd
import ast
import random
N = 5000 #要添加的blog范围
img_count = 0
for k in range(N):
    print(k)
    df = pd.read_csv(f"{csv_path}{k+1}.csv",encoding='utf-8')
    title = df.values[0][1]
    pub_date = df.values[1][1]
    author = df.values[2][1]
    paras = ast.literal_eval(df.values[3][1]) #list
    origin_comment_count = int(df.values[4][1])
    origin_comment_users = int(df.values[5][1])
    hot = origin_comment_count*(50+10*random.random())+origin_comment_users*(1+0.1*random.random())+10*random.random()
    link = df.values[6][1]
    

    blog = Blog(title=title, pub_date=pub_date, author=author, comment_count=0, hot=hot, link=link)
    blog.save()

    intro = ""
    for i in paras:
        para = Para(blog=blog)
        para.save()
        if isinstance(i,list):
            img_path = i[0]
            img_desc = i[1]
            
            img_para = Img_para(para=para,img_desc=img_desc)
            img_count+=1
            with open('../'+img_path, 'rb') as f:
                img_para.image.save(f'{img_count}.jpg', File(f))
            img_para.save()
        else:
            text_para = Text_para(text=i)
            text_para.para = para
            intro = intro + i
            text_para.save()

    intro = intro[:50]
    blog.intro = intro
    blog.save()


df = pd.read_csv("../tf_idf.csv",encoding='utf-8')
tfidflist = df.values
N = len(df.values)
for k in range(N):
    print(k)
    realword = tfidflist[k][0]
    vals = ast.literal_eval(tfidflist[k][1])
    word = Word(realword=realword)
    word.save()
    for val in vals:
        blogid = val
        tfidf = vals[val]
        blog = Blog.objects.get(id=blogid)
        doc = Doc(word=word,blog=blog,tfidf=tfidf)
        doc.save()
