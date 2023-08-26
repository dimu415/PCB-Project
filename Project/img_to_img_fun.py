import xml.etree.ElementTree as ET
import os
import shutil
class img_to_img_fun:
    def __init__(self,directory,output):
        self.directory=directory
        self.output=output
        self.img_to_img()
    def list_files_in_directory(self):
        file_list = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".jpg"):
                    file_path = os.path.join(root, file)
                    file_list.append(file_path)
        return file_list
    
    def img_to_img(self): 
        xml_paths=[]
        if os.path.exists(self.directory):
            source_paths = self.list_files_in_directory()
        for source_path in source_paths:
            name=source_path.split("\\")[-1]
            destination_path=f"{self.output}/{name}"
            if not os.path.exists(self.output):
                os.makedirs(self.output)
            try:
                shutil.copy(source_path, destination_path)
                
            except Exception as e:
                print("이미지 복사 중 오류가 발생했습니다:", e)
        