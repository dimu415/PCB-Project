import xml.etree.ElementTree as ET
import os
import shutil
class xml_to_txt_fun:
    def __init__(self,directory,output):
        self.directory=directory
        self.output=output
        self.xml_to_txt()
    def list_files_in_directory(self):
        file_list = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".xml"):
                    file_path = os.path.join(root, file)
                    file_list.append(file_path)
        return file_list
    
    def xml_to_txt(self): 
        xml_paths=[]
        if os.path.exists(self.directory):
            xml_paths = self.list_files_in_directory()
        cl={}
        cl_num=0
        for xml_path in xml_paths:
            txt=""
            tree = ET.parse(xml_path)
            root = tree.getroot()
                
            for obj in root.iter('object'):
                bbox = obj.find('bndbox')
                name = obj.find('name').text
                    
                xmin = int(bbox.find('xmin').text)
                ymin = int(bbox.find('ymin').text)
                xmax = int(bbox.find('xmax').text)
                ymax = int(bbox.find('ymax').text)
                try:
                    txt+=f"{cl[name]} {xmin} {ymin} {xmax} {ymax}\n"
                except:
                    cl[name]=cl_num
                    cl_num+=1
                    txt+=f"{cl[name]} {xmin} {ymin} {xmax} {ymax}\n"
            file_name=xml_path.split("\\")[-1][:-4]
            file_path =f"{self.output}/{file_name}.txt"
            if not os.path.exists(self.output):
                os.makedirs(self.output)
            # 파일 열기 (새 파일을 생성하거나 이미 존재하는 파일 열기)
            with open(file_path, "w") as file:
                file.write(txt)
        