import xml.etree.ElementTree as ET
from PIL import Image
import os

class Augmentation_ver_rev:
    def __init__(self, data_files, xml_file_path, original_image_path, flipped_image_folder, flipped_label_folder, transform=True):
        self.xml_file_path = xml_file_path
        self.original_image_path = original_image_path
        self.flipped_image_folder = flipped_image_folder
        self.flipped_label_folder = flipped_label_folder
        self.data_files = data_files
        self.transform = transform
        self.process_data()
        
    #%% PCB 이미지와 xml 파일 리스트 수집        
    def create_list(self):
        defect_list = []
        defect_xlist = []
        
        for data_file in self.data_files:
            img_folder = os.path.join(self.original_image_path, data_file)
            xml_folder = os.path.join(self.xml_file_path, data_file)
    
            img_files = [file for file in os.listdir(img_folder) if file.lower().endswith('.jpg')]
            xml_files = [file for file in os.listdir(xml_folder) if file.lower().endswith('.xml')]
    
            defect_list.extend([os.path.join(img_folder, img_file) for img_file in img_files])
            defect_xlist.extend([os.path.join(xml_folder, xml_file) for xml_file in xml_files])
        
        return defect_list, defect_xlist

    def process_data(self):
        defect_list, defect_xlist = self.create_list()
        
        class_mapping = {
            "missing_hole": 0,
            "mouse_bite": 1,
            "open_circuit": 2,
            "short": 3,
            "spur": 4,
            "spurious_copper": 5
        }
        
        #xml와 jpg 파일명 매칭하여 실행 
        for img_filename in defect_list:
            img_basename = os.path.splitext(os.path.basename(img_filename))[0]
            matching_xml_filename = None

            for xml_filename in defect_xlist:
                xml_basename = os.path.splitext(os.path.basename(xml_filename))[0]
                if img_basename == xml_basename:
                    matching_xml_filename = xml_filename
                    break

            if matching_xml_filename is None:
                continue
                
            img_path = img_filename
            xml_path = matching_xml_filename

            # XML 파일을 파싱하여 Element 객체 생성
            tree = ET.parse(xml_path)
            root = tree.getroot()
      
            # 필요한 정보 추출
            filename = root.find('filename').text
            bndboxes = []

            for obj in root.findall('.//object'):
                obj_name = obj.find('name').text
                obj_index = class_mapping.get(obj_name, -1)
                if obj_index != -1:
                    bndbox = obj.find('bndbox')
                    xmin = int(bndbox.find('xmin').text)
                    ymin = int(bndbox.find('ymin').text)
                    xmax = int(bndbox.find('xmax').text)
                    ymax = int(bndbox.find('ymax').text)
                    bndboxes.append({'name': obj_index, 'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax})

            if self.transform:
                # 이미지 불러오기
                image = Image.open(img_path)
                size = image.size
                
                #좌우반전 수행
                flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
                
                #새 이미지 저장
                os.makedirs(flipped_image_folder, exist_ok=True)
                flipped_image_path = os.path.join(self.flipped_image_folder, filename)
                flipped_image.save(flipped_image_path)

                # 새 라벨 생성 또는 업데이트
                os.makedirs(flipped_label_folder, exist_ok=True)
                flipped_label_path = os.path.join(self.flipped_label_folder, filename.replace('.jpg', '.txt'))
                with open(flipped_label_path, 'w') as label_file:
                    for obj in bndboxes:
                        flipped_xmin = obj['xmin']
                        flipped_xmax = obj['xmax']
                        flipped_ymin = size[1] - obj['ymax']  # Vertical flip
                        flipped_ymax = size[1] - obj['ymin']  # Vertical flip

                        label_file.write(f"{obj['name']} {flipped_xmin} {flipped_ymin} {flipped_xmax} {flipped_ymax}\n")

                #print("이미지와 라벨 정보가 저장되었습니다.")
                #print("이미지 저장 경로:", flipped_image_path)
                #print("라벨 저장 경로:", flipped_label_path)
            #else:
                #print("변환 작업을 수행하지 않습니다.")

# 경로 설정
xml_file_path = 'C:/work/python/PCB/PCB_DATASET/Annotations'
original_image_path = 'C:/work/python/PCB/PCB_DATASET/images' 
flipped_image_folder = 'C:/work/python/PCB/PCB_DATASET/images/Rescaled_images3/i/'
flipped_label_folder = 'C:/work/python/PCB/PCB_DATASET/images/Rescaled_images3/l/'

data_files = ['Missing_hole']

# 클래스 인스턴스 생성 및 process_data 함수 호출 (True로 호출하면 변환이 수행됨)
Augmentation_ver_rev(data_files, xml_file_path, original_image_path, flipped_image_folder, flipped_label_folder, transform=True)



# In[ ]:




