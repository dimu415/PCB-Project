#!pip install tensorflow
#!pip install ultralytics
#!pip install PyYAML

import yaml
from ultralytics import YOLO
import ultralytics
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.patches as patches
from sklearn.model_selection import train_test_split
import shutil

def model_train():
    model=YOLO('yolov8n.pt') # 모델 불러오기
    model.train
    model.train(data='C:/Users/USER/Desktop/img/data.yaml',#yaml 경로
            epochs=10000, 
            patience=10,
            batch=32,
            imgsz=416,
            pretrained=True)
#%% file -> DataFrame    
    
def file_open(path_an):
        dataset = {
                "xmin":[],
                "ymin":[],
                "xmax":[],
                "ymax":[],
                "class":[],
                "file":[],
                "width":[],
                "height":[],
               }
        all_files = []
        for path, subdirs, files in os.walk(path_an):
        #     print([path, subdirs, files])
            for name in files:
                all_files.append(os.path.join(path, name))
        for anno in all_files:
        # print(anno)
            tree = ET.parse(anno)
        
            for elem in tree.iter():
                # print(elem)
        
                if 'size' in elem.tag:
                    # print('[size] in elem.tag ==> list(elem)\n'), print(list(elem))
                    for attr in list(elem):
                        if 'width' in attr.tag:
                            width = int(round(float(attr.text)))
                        if 'height' in attr.tag:
                            height = int(round(float(attr.text)))
        
                if 'object' in elem.tag:
                    # print('[object] in elem.tag ==> list(elem)\n'), print(list(elem))
                    for attr in list(elem):
        
                        # print('attr = %s\n' % attr)
                        if 'name' in attr.tag:
                            name = attr.text
                            dataset['class']+=[name]
                            dataset['width']+=[width]
                            dataset['height']+=[height]
                            dataset['file']+=[anno.split('/')[-1].split('\\')[-1][0:-4]]
        
                        if 'bndbox' in attr.tag:
                            for dim in list(attr):
                                if 'xmin' in dim.tag:
                                    xmin = int(round(float(dim.text)))
                                    dataset['xmin']+=[xmin]
                                if 'ymin' in dim.tag:
                                    ymin = int(round(float(dim.text)))
                                    dataset['ymin']+=[ymin]
                                if 'xmax' in dim.tag:
                                    xmax = int(round(float(dim.text)))
                                    dataset['xmax']+=[xmax]
                                if 'ymax' in dim.tag:
                                    ymax = int(round(float(dim.text)))
                                    dataset['ymax']+=[ymax]
                                    
        df=pd.DataFrame(dataset)
        class_pcb={"missing_hole": 0, "mouse_bite": 1, "open_circuit":2, "short": 3, 'spur': 4,'spurious_copper':5}
        df2=df.copy()
        df2['class']=df2['class'].apply(lambda x : class_pcb[x])
        
        return df2

#%% 0~1 (X_center,Y_center,width,hight)

def create_txt(df):
    df['xmin']=df['xmin']/df['width']
    df['xmax']=df['xmax']/df['width']
    df['ymin']=df['ymin']/df['height']
    df['ymax']=df['ymax']/df['height']
    
    df['x_center']=(df['xmin']+df['xmax'])/2
    df['y_center']=(df['ymin']+df['ymax'])/2
    df['wid']=df['xmax']-df['xmin']
    df['hig']=df['ymax']-df['ymin']
    
    result_df = df.groupby('file').apply(
        lambda x: ', '.join(
            [f"x_center: {','.join(map(str, x['x_center']))}" if 'x_center' in x.columns else '',
             f"y_center: {','.join(map(str, x['y_center']))}" if 'y_center' in x.columns else '',
            f"wid: {','.join(map(str, x['wid']))}" if 'wid' in x.columns else '',
            f"hig: {','.join(map(str, x['hig']))}" if 'hig' in x.columns else '']
        )
    ).reset_index(name='merged_data')
    
    re_df=pd.DataFrame(result_df)
    cl=[]

    for name in re_df['file']:
        if "missing" in name.split('_'):
            cl.append(0)
        if "mouse" in name.split('_'):
            cl.append(1)
        if "open" in name.split('_'):
            cl.append(2)
        if "short" in name.split('_'):
            cl.append(3)
        if "spur" in name.split('_'):
            cl.append(4)
        if "spurious" in name.split('_'):
            cl.append(5)
    re_df['class']=cl
    return re_df
    
#%% image copy
def copy_image(path,name,nm):
    
    path=path+"/"
    
    if "missing" in name.split('_'):
        path += 'Missing_hole/'
    if "mouse" in name.split('_'):
        path += 'Mouse_bite/'
    if "open" in name.split('_'):
        path += 'Open_circuit/'
    if "short" in name.split('_'):
        path += 'Short/'
    if "spur" in name.split('_'):
        path += 'Spur/'
    if "spurious" in name.split('_'):
        path += 'Spurious_copper/'
    path += name+'.jpg'
    
    try:
        shutil.copy(path,nm)
        print(f"Image copied from '{path}' to '{nm}' successfully.")
    except FileNotFoundError:
        print(f"Error: The source file '{path}' could not be found.")
    except IOError as e:
        print(f"Error: An error occurred while copying the file: {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        
def copy_image2(path,path2,re_df):
    train,test = train_test_split(re_df,test_size=0.2)
    datas=[re_df,train,test]
    paths=["val","train","test"]
    for d,n in zip(datas,paths):    
        for name in d['file']:
            nm=f"{path}/{n}/images/"+name+".jpg"
            copy_image(path2,name,nm)
    return train,test
#%% class insert
def cl_num(test_train):
    
    dfs=[]
    for df in test_train:
        cl=[]
        for name in df['file']:
            if "missing" in name.split('_'):
                cl.append(0)
            if "mouse" in name.split('_'):
                cl.append(1)
            if "open" in name.split('_'):
                cl.append(2)
            if "short" in name.split('_'):
                cl.append(3)
            if "spur" in name.split('_'):
                cl.append(4)
            if "spurious" in name.split('_'):
                cl.append(5)
        df['class']=cl
        dfs.append(df)
    return dfs[0],dfs[1]

#%% txt create
def txt_crt(datas): #(re_df,train,test)
    paths=["val","train","test"]
    for d,n in zip(datas,paths): 
        for data,cl,name in zip(d["merged_data"],d['class'],d['file']):
    
            split_data = data.replace(':', '').split()
            a=[]
            for i in range(len(split_data[1].replace(',',' ').split())):
                a.append(split_data[1] .replace(',',' ').split()[i]+" "+split_data[3] .replace(',',' ').split()[i]+" "+split_data[5] .replace(',',' ').split()[i]+" "+split_data[7] .replace(',',' ').split()[i])
    
    
            # 추출한 데이터를 파일로 저장
    
            output_file_path = f"C:/Users/USER/Desktop/img/{n}/labels/"+name+".txt"
            with open(output_file_path, "w") as file:
                for data,cl,name in zip(d["merged_data"],d['class'],d['file']):
            
                    split_data = data.replace(':', '').split()
                    a=[]
                    for i in range(len(split_data[1].replace(',',' ').split())):
                        a.append(split_data[1] .replace(',',' ').split()[i]+" "+split_data[3] .replace(',',' ').split()[i]+" "+split_data[5] .replace(',',' ').split()[i]+" "+split_data[7] .replace(',',' ').split()[i])
            
        
                # 추출한 데이터를 파일로 저장
        
                output_file_path = f"C:/Users/USER/Desktop/img/{n}/labels/"+name+".txt"
                with open(output_file_path, "w") as file:
                    for x in a:
                        file.write(f"{cl} {x}\n")
        
                print(f"데이터가 '{output_file_path}'에 저장되었습니다.")
            
#%% yaml create
def yaml_crt(train,val,test,path):
    data={
    'train':train,
    'val':val,
    'test':test,
    'names':['missing_hole','mouse_bite','open_circuit','short','spur','spurious_copper'],
    'nc':6
    }
    yaml_data = yaml.dump(data)
    print(yaml_data)
    
    # YAML 데이터를 파일에 저장
    file_path = path+"/data.yaml"
    with open(file_path, "w") as file:
        file.write(yaml_data)
        
    with open(file_path,'w') as f:
        yaml.dump(data,f)
        
    with open(file_path,'r') as f:
        pcb_yaml=yaml.safe_load(f)
        
#!cat C:/Users/USER/Desktop/img/data.yaml

#%% 실행 과정

path_an="C:/Users/USER/Desktop/archive/PCB_DATASET/Annotations"
df=file_open(path_an) #Annotations 경로
re_df=create_txt(df)
path1="C:/Users/USER/Desktop/archive/PCB_DATASET/images"
path2="C:/Users/USER/Desktop/img2"
test,train=copy_image2(path1,path2,re_df) #복사할 이미지경로,복사될 곳 경로
datas=[re_df,train,test]
txt_crt(datas) # 텍스트파일저장
train_path="C:/Users/USER/Desktop/img2/train/images"
val_path="C:/Users/USER/Desktop/img2/val/images"
test_path="C:/Users/USER/Desktop/img/test/images"
save_path="C:/Users/USER/Desktop/img2/data.yaml"
yaml_crt(train_path,val_path,test_path,save_path) #yaml 생성