#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET

#%% Annotation  결함 좌표와 학습 결과 좌표 시각화
class Check:
    def __init__(self, fname, pred, cls):
        self.fname = fname
        self.pred = pred
        self.cls = cls
        self.ymodel_box()

    #%% Annotation 시각화
    def check_result(self):
        xml_path = os.path.join('C:/work/python/PCB/PCB_DATASET/Annotations/Missing_hole', self.fname + '.xml')
        image_path = os.path.join('C:/work/python/PCB/PCB_DATASET/images/Missing_hole', self.fname + '.jpg')
        sample_image = Image.open(image_path)
        sample_image_annotated = sample_image.copy()
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # 폰트 설정
        font_size = 18 
        font = ImageFont.truetype("arial.ttf", 30)
        
        img_bbox = ImageDraw.Draw(sample_image_annotated)
        
        index = 0
        name_list = []        
        for obj in root.iter('object'):
            name_xml = obj.find('name').text
            name_list.append(name_xml)
            bbox = obj.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)
            img_bbox.rectangle([(xmin, ymin), (xmax, ymax)], outline="red", width=5)
            name = name_list[index]  
            name_text = img_bbox.textbbox((xmin - 175, ymin - 20), name, anchor='lt', font=font)
            img_bbox.rectangle([(name_text[0], name_text[1]), (name_text[2], name_text[3])], fill='red')
            img_bbox.text((name_text[0], name_text[1]), name, fill='white', font=font)  # cls가 아닌 name을 사용해야 합니다.

        return font, img_bbox, sample_image_annotated
        
    #%% 학습 결과 class 구분    
    def extract_defect_class(self):
        cls_list = []
        clsf = []
        for i in range(len(self.cls[self.fname])):
            at = int(self.cls[self.fname][i])
            cls_list.append(at)
        for j in cls_list:
            d_class = {0: 'missing_hole',
                       1: 'mouse_bite',
                       2: 'open_circuit',
                       3: 'short',
                       4: 'spur',
                       5: 'spurious_copper'}
            dc = d_class[j]
            clsf.append(dc)
        return clsf
        
    #%% 학습 결과 시각화
    def ymodel_box(self):
        font, img_bbox, sample_image_annotated = self.check_result()

        # pred 결과
        in_value = self.fname
        if in_value in self.pred:
            show_value = self.pred[in_value]
            show = pd.DataFrame(show_value)
            show.columns = ['xmin', 'ymin', 'xmax', 'ymax']
            print(f' {show} 입니다.')

            # show(dataframe) 각 행을 순회하며 박스와 클래스 레이블 표시
            for index, row in show.iterrows():
                xmin = row['xmin']
                ymin = row['ymin']
                xmax = row['xmax']
                ymax = row['ymax']

                # text box 생성
                clsf = self.extract_defect_class()  # clsf 반환
                cls = clsf[index]  # clsf : 좌표 박스별 결함 레이블
                cls_text = img_bbox.textbbox((xmax + 10, ymin - 3), cls, anchor='lt', font=font)

                # 결함별 박스 색깔 선정
                if cls == 'missing_hole':
                    box_color = 'yellow'
                    text_color = 'black'
                elif cls == 'mouse_bite':
                    box_color = 'green'
                    text_color = 'white'
                elif cls == 'open_circuit':
                    box_color = 'cyan'
                    text_color = 'black'
                elif cls == 'short':
                    box_color = 'blue'
                    text_color = 'white'
                elif cls == 'spur':
                    box_color = 'orange'
                    text_color = 'white'
                else:
                    box_color = 'purple'
                    text_color = 'white'
                    
                img_bbox.rectangle([(xmin, ymin), (xmax, ymax)], outline=box_color, width=5)
                img_bbox.rectangle([(cls_text[0], cls_text[1]), (cls_text[2], cls_text[3])], fill=box_color)
                img_bbox.text((cls_text[0], cls_text[1]), cls, fill=text_color, font=font)
        
        else:
            print("해당 값이 없습니다.")
    
        # 최종 이미지 출력
        return sample_image_annotated.show()

Check('01_missing_hole_01', pred, cls)


# In[ ]:




