#밝기변화
import os
import cv2
import numpy as np
import pandas as pd
import random
import os
import xml.etree.ElementTree as ET
class Augmentation_bri:
    def __init__(self, input_val, img_path, xml_path, output_folder):
        self.input_val= input_val
        self.img_path = img_path
        self.xml_path = xml_path
        self.output_folder = output_folder+"/images"
        self.output_label_path = output_folder+"/labels"
        os.makedirs(self.output_label_path, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)
        self.brightness_var()
    # %% pcb 기판 밝기 조절
    def brightness_var(self):
    
        pcb_image = cv2.imread(self.img_path)
        
        avg_intensity = np.mean(pcb_image)

        target_intensity = avg_intensity + self.input_val  # 평균조도 input_val 값에 따라 변화
        pcb_var = np.clip(pcb_image * (target_intensity / avg_intensity), 0, 255).astype(np.uint8)
    
        
        filename = os.path.basename(self.img_path)
        output_file = os.path.join(self.output_folder, f"var_{filename}")
        cv2.imwrite(output_file, pcb_var)
        
        output_file2 = os.path.join(self.output_label_path, f"var_{filename[:-4]}.txt")
        
        text=""
        with open(self.xml_path, "r") as input_file:
            lines = input_file.readlines()
            for line in lines:
                a=line.split("\n")[0].split(" ")
                cl=a[0]
                xmin=a[1]
                ymin=a[2]
                xmax=a[3]
                ymax=[4]
                x_center=(xmax+xmin)/2
                y_center=(ymax+ymin)/2
                w_=xmax-xmin
                h_=ymax-ymin
                text+=f"{cl} {x_center} {y_center} {w_} {h_}\n"
        # 읽어온 텍스트를 다른 파일에 저장하기
        with open(output_file2, "w") as output_file:
            output_file.write(text)
  