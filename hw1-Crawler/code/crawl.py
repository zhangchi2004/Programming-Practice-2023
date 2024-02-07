import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import json
from time import sleep
from fake_useragent import UserAgent


def extract_text(p_elem):
    if p_elem.find() is not None:
        return extract_text(p_elem.find())
    else:
        return p_elem.text

df = pd.read_csv("links_processed.csv",encoding='utf-8')
links = df["link"].values #python list
titles = df["title"].values
N = df.shape[0]

for i in range(4952,N):# 此处从249开始
    try:
        if i%11==5: sleep(1)
        if i%37==6: sleep(2)
        if i%97==7: sleep(5)

        print(i)
        link = links[i]
        ua=UserAgent()
        headers={"User-Agent":ua.random} 
        response = requests.get(link,headers=headers)
        sleep(0.1)
        response.encoding = 'UTF-8'
        soup = BeautifulSoup(response.text,'lxml')

        author = ""

        a = soup.find(class_='source')
        if a is not None:
            author = extract_text(a)
        else:
            b = soup.find(class_='author')
            if b is not None:
                author = extract_text(b)
            else:
                c = soup.find(id='media_name')
                if c is not None:
                    author = extract_text(c)

        article = []
        artibody = soup.find(id='artibody')
        if artibody is not None:
            paras = artibody.find_all()
            for para in paras:
                if para.name=='p':
                    article.append(para.text)
                elif 'class' in para.attrs:
                    if para.attrs['class']==['img_wrapper']:
                        img = para.find('img')
                        
                        if img is not None:
                            img_link = ""
                            img_text = ""
                            if 'src' in img.attrs:
                                img_link = "https:"+img.attrs["src"]
                            if 'alt' in img.attrs:
                                img_text = img.attrs["alt"]
                            article.append([img_link,img_text])

        match = re.search(r"doc-i(.+?)\.shtml",link)
        newsid = match.group(1)
        comment_url_kj = f"https://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=kj&newsid=comos-{newsid}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1"
        comment_url_cj = f"https://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=cj&newsid=comos-{newsid}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1"

        comment_count_cj = 0
        comment_count_kj = 0
        comment_users_cj = 0
        comment_users_kj = 0

        response_cj = requests.get(comment_url_cj)
        response_kj = requests.get(comment_url_kj)
        sleep(0.1)

        response_cj.encoding = 'UTF-8'
        cmtpg_cj = response_cj.text
        jd_cj = json.loads(cmtpg_cj)
        if 'count' in jd_cj['result']:
            cntcj = jd_cj['result']['count']
            comment_count_cj = cntcj['show']
            comment_users_cj = cntcj['total']

        response_kj.encoding = 'UTF-8'
        cmtpg_kj = response_kj.text
        jd_kj = json.loads(cmtpg_kj)
        if 'count' in jd_kj['result']:
            cntkj = jd_kj['result']['count']
            comment_count_kj = cntkj['show']
            comment_users_kj = cntkj['total'] 

        comment_count = max(comment_count_cj,comment_count_kj)
        comment_users = max(comment_users_cj,comment_users_kj)

        pub_date = ""
        if 'news' in jd_cj['result']:
            pub_date = jd_cj['result']['news']['time']
        if pub_date=='' and 'news' in jd_kj['result']:
            pub_date = jd_kj['result']['news']['time']

        title = titles[i]
        link = links[i]
        data = {"title":title,"pub_date":pub_date,"author":author,"article":article,"comment_count":comment_count,"comment_users":comment_users,"link":link}
        df = pd.DataFrame(data.items())
        df.to_csv(f"./results/{i+1}.csv",index=False,encoding='utf-8')
    except:pass 