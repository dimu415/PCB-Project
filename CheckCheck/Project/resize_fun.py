##resize
import os
from PIL import Image

def convert_and_save(x, image_path, txt_label_path, output_path):
    output_image_path = os.path.join(output_path, "images")
    output_label_path = os.path.join(output_path, "labels")
    
    # 이미지 열기
    image = Image.open(image_path)

    # 이미지 크기 얻기
    image_width, image_height = image.size

    # x로 나눈 결과 계산
    result_width = int(image_width / x)
    result_height = int(image_height / x)

    # 이미지 크기 조정
    rescaled_image = image.resize((result_width, result_height))

    # 폴더 생성
    os.makedirs(output_image_path, exist_ok=True)
    os.makedirs(output_label_path, exist_ok=True)

    # 저장할 이미지 경로 설정
    image_output_filename = f"rescaled_{x:.2f}_x_{os.path.basename(image_path)}"
    image_output_file_path = os.path.join(output_image_path, image_output_filename)
    rescaled_image.save(image_output_file_path)
    w,h=rescaled_image.size
    # 라벨 파일 불러오기
    with open(txt_label_path, 'r') as label_file:
        lines = label_file.readlines()

    # 변환된 라벨 정보 저장
    label_output_filename = f"rescaled_{x:.2f}_x_{os.path.basename(txt_label_path).replace('.txt', '.txt')}"
    label_output_file_path = os.path.join(output_label_path, label_output_filename)

    with open(label_output_file_path, 'w') as label_file:
        for line in lines:
            parts = line.strip().split()
            obj_index = int(parts[0])
            xmin = int(int(parts[1]) / x)/w
            ymin = int(int(parts[2]) / x)/h
            xmax = int(int(parts[3]) / x)/w
            ymax = int(int(parts[4]) / x)/h
            
            x_center=(xmax+xmin)/2
            y_center=(ymax+ymin)/2
            w_=xmax-xmin
            h_=ymax-ymin
            
            label_file.write(f"{obj_index} {x_center} {y_center} {w_} {h_}\n")
