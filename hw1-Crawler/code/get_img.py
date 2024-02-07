import os,stat
import urllib.request
import ast
import pandas as pd
N=5000
img_id=0
for k in range(N):
    print(k)
    df = pd.read_csv(f"./new/{k+1}.csv",encoding='utf-8')

    paras = ast.literal_eval(df.values[3][1]) #list

    for para in paras:
        if isinstance(para,list): 
            img_link = para[0]
            img_id+=1
            try:
                suffix = os.path.splitext(img_link)[1]
                filename = f"imgs/{img_id}{suffix}"
                urllib.request.urlretrieve(img_link,filename=filename)
                para[0] = filename
            except IOError as e:
                print("IOError")
            except Exception as e:
                print("Exception")
    df.values[3][1] = paras    
    df.to_csv(f"./with_local_img/{k+1}.csv",index=False,encoding='utf-8')    