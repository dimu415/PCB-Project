###상하반전
import os
from PIL import Image

class Augmentation_ver_rev:
    def __init__(self, original_label_path, original_image_path, flipped_image_folder, flipped_label_folder, transform=True):
        self.original_label_path = original_label_path
        self.original_image_path = original_image_path
        self.flipped_image_folder = flipped_image_folder
        self.flipped_label_folder = flipped_label_folder
        self.transform = transform
        self.process_data()
        
    def process_data(self):
        img_basename = os.path.splitext(os.path.basename(self.original_image_path))[0]
        
        with open(self.original_label_path, 'r') as label_file:
            lines = label_file.readlines()

        bndboxes = []
        for line in lines:
            parts = line.strip().split()
            obj_index = int(parts[0])
            xmin = int(parts[1])
            ymin = int(parts[2])
            xmax = int(parts[3])
            ymax = int(parts[4])
            bndboxes.append({'name': obj_index, 'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax})

        # 이미지 불러오기
        image = Image.open(self.original_image_path)
        size = image.size
        
        if self.transform:
            # 상하반전 수행
            flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
        
       
        
            # 새 이미지 저장
            flipped_filename = f"r{os.path.basename(self.original_image_path)}"
            flipped_image_path = os.path.join(self.flipped_image_folder, flipped_filename)
            os.makedirs(os.path.dirname(flipped_image_path), exist_ok=True)
            flipped_image.save(flipped_image_path)
            w,h=flipped_image.size
                  # 새 라벨 생성 또는 업데이트
            flipped_label_filename = f"r{os.path.basename(self.original_label_path)}"
            flipped_label_path = os.path.join(self.flipped_label_folder, flipped_label_filename)
            os.makedirs(os.path.dirname(flipped_label_path), exist_ok=True)
        
            with open(flipped_label_path, 'w') as label_file:
                for obj in bndboxes:
                    flipped_xmin = obj['xmin']/w
                    flipped_xmax = obj['xmax']/w
                    flipped_ymin = (size[1] - obj['ymax'])/h  # Vertical flip
                    flipped_ymax = (size[1] - obj['ymin'])/h  # Vertical flip
                    
                    x_center=(flipped_xmax+flipped_xmin)/2
                    y_center=(flipped_ymax+flipped_ymin)/2
                    w_=flipped_xmax-flipped_xmin
                    h_=flipped_ymax-flipped_ymin
                    
                    
                    label_file.write(f"{obj['name']} {x_center} {y_center} {w_} {h_}\n")

class Augmentation_hor_rev:
    def __init__(self, original_label_path,original_image_path,  flipped_image_folder, flipped_label_folder, transform=True):
        self.original_image_path = original_image_path
        self.original_label_path = original_label_path
        self.flipped_image_folder = flipped_image_folder
        self.flipped_label_folder = flipped_label_folder
        self.transform = transform
        self.process_data()

    def process_data(self):
        img_basename = os.path.splitext(os.path.basename(self.original_image_path))[0]

        # Load original label data from txt file
        with open(self.original_label_path, 'r') as label_file:
            original_labels = label_file.readlines()

        if self.transform:
            # Load and flip the image
            image = Image.open(self.original_image_path)
            size = image.size
            flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)

            # Save flipped image
            flipped_filename = f"rlr{os.path.basename(self.original_image_path)}"
            flipped_image_path = os.path.join(self.flipped_image_folder, flipped_filename)
            os.makedirs(os.path.dirname(flipped_image_path), exist_ok=True)
            flipped_image.save(flipped_image_path)
            w,h=flipped_image.size
            # Process and save flipped labels
            flipped_label_filename = f"rlr{os.path.basename(self.original_label_path)}"
            flipped_label_path = os.path.join(self.flipped_label_folder, flipped_label_filename)
            os.makedirs(os.path.dirname(flipped_label_path), exist_ok=True)

            with open(flipped_label_path, 'w') as flipped_label_file:
                for label in original_labels:
                    parts = label.strip().split()
                    obj_class = parts[0]  # 클래스
                    xmin = int(parts[1])
                    ymin = int(parts[2])
                    xmax = int(parts[3])
                    ymax = int(parts[4])
                    # 좌우 반전에 따른 좌표 변경
                    flipped_xmin = (size[0] - xmax)/w
                    flipped_xmax = (size[0] - xmin)/w
                    flipped_ymin = ymin/h 
                    flipped_ymax = ymax/h 

                    x_center=(flipped_xmax+flipped_xmin)/2
                    y_center=(flipped_ymax+flipped_ymin)/2
                    w_=flipped_xmax-flipped_xmin
                    h_=flipped_ymax-flipped_ymin




                    # 새 라벨 파일에 저장
                    flipped_label_file.write(f"{obj_class} {x_center} {y_center} {w_} { h_}\n")
