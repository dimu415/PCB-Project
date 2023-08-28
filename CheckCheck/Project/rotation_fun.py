##rotation
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

class Rotation:
    def __init__(self, image_path, txt_label_path, output_folder, angle):
        self.image_path = image_path
        self.txt_label_path = txt_label_path
        self.output_folder = output_folder
        self.angle = angle

        self.process_rotation()

    def process_rotation(self):
        # 라벨 파일 불러오기
        with open(self.txt_label_path, 'r') as label_file:
            lines = label_file.readlines()

        # 변환된 라벨 정보 저장할 파일 경로 설정
        filename = os.path.splitext(os.path.basename(self.image_path))[0]
        save_path = os.path.join(self.output_folder, "labels", f"rotated_{filename}.txt")

        # 이미지 로드
        image = cv2.imread(self.image_path)
        image_height, image_width = image.shape[:2]

        # 이미지 중심점 기반 회전 행렬 계산
        rotation_matrix = cv2.getRotationMatrix2D((image_width / 2, image_height / 2), self.angle, 1)

        # 새로운 이미지 크기 계산
        cos_theta = np.abs(rotation_matrix[0, 0])
        sin_theta = np.abs(rotation_matrix[0, 1])
        new_width = int(image_height * sin_theta + image_width * cos_theta)
        new_height = int(image_height * cos_theta + image_width * sin_theta)

        # 이미지 중심을 기준으로 회전한 이미지 생성
        rotation_matrix[0, 2] += (new_width - image_width) / 2
        rotation_matrix[1, 2] += (new_height - image_height) / 2

        rotated_image = cv2.warpAffine(image, rotation_matrix, (new_width, new_height), borderValue=(255, 255, 255))

        rotated_image_folder = os.path.join(self.output_folder, "images")
        rotated_image_path = os.path.join(rotated_image_folder, f'rotated_{filename}.jpg')
        os.makedirs(rotated_image_folder, exist_ok=True)
        cv2.imwrite(rotated_image_path, rotated_image)

        # 라벨 정보 회전 및 업데이트
        updated_labels = []

        for line in lines:
            label_info = line.strip().split(' ')
            class_label = label_info[0]
            xmin, ymin, xmax, ymax = map(int, label_info[1:])

            # 좌표 회전
            rotated_xmin = int(xmin * rotation_matrix[0, 0] + ymin * rotation_matrix[0, 1] + rotation_matrix[0, 2])/new_width
            rotated_ymin = int(xmin * rotation_matrix[1, 0] + ymin * rotation_matrix[1, 1] + rotation_matrix[1, 2])/new_height
            rotated_xmax = int(xmax * rotation_matrix[0, 0] + ymax * rotation_matrix[0, 1] + rotation_matrix[0, 2])/new_width
            rotated_ymax = int(xmax * rotation_matrix[1, 0] + ymax * rotation_matrix[1, 1] + rotation_matrix[1, 2])/new_height
            
            x_center=(rotated_xmax+rotated_xmin)/2
            y_center=(rotated_ymax+rotated_ymin)/2
            w=rotated_xmax-rotated_xmin
            h=rotated_ymax-rotated_ymin
            updated_labels.append(f"{class_label} { x_center} {y_center} {w} {h}\n")

        # 변경된 라벨 정보 저장
        rotated_label_folder = os.path.join(self.output_folder, "labels")
        os.makedirs(rotated_label_folder, exist_ok=True)

        with open(save_path, 'w') as updated_label_file:
            updated_label_file.writelines(updated_labels)
