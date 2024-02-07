csv_path = "with_local_img/"
import pandas as pd
import ast
import random
import os
N = 5000 
for k in range(39,N):
    print(k)
    df = pd.read_csv(f"{csv_path}{k+1}.csv",encoding='utf-8')
    pub_date = df.values[1][1].replace(':','')
    while os.path.exists(csv_path+pub_date):
        pub_date = pub_date[:-1]+f"{int(pub_date[-1])+1}"
    os.rename(f"{csv_path}{k+1}.csv", csv_path+pub_date)

file_list = os.listdir(csv_path)
file_list.sort(reverse=True)

for index, old_filename in enumerate(file_list, start=1):
    new_filename = f"{index}.csv"  
    old_filepath = os.path.join(csv_path, old_filename)
    new_filepath = os.path.join(csv_path, new_filename)
    os.rename(old_filepath, new_filepath)
    print(f"Renamed {old_filename} to {new_filename}")
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)
    
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        first_row = next(reader)
        if first_row: 
            first_value = first_row[0]
        else:
            first_value = ''
   
    new_file_name = f"{first_value}.csv"
    new_file_path = os.path.join(folder_path, new_file_name)
    os.rename(file_path, new_file_path)
    print(f"Renamed {csv_file} to {new_file_name}")