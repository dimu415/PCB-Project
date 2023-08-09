import os
import re
import cv2
import pandas as pd
from skimage.metrics import structural_similarity as compare_ssim

class PCBDefectMatcher:
    def __init__(self, defect_folders, good_folder, output_path):
        self.defect_folders = defect_folders
        self.good_folder = good_folder
        self.output_path = output_path
        self.defect_list = {}
        self.matching_pairs = []
    
    # 파일 이름의 앞자리 추출
    def extract_prename(self, filename):
        match = re.match(r'^\d+', os.path.basename(filename))
        if match:
            return match.group()
        return None

    def load_defect_images(self, defect_folder): #1
        
        defect_path = os.path.join('C:/work/python/PCB/PCB_DATASET/images', defect_folder) # 경로 수정
        defect_list = [os.path.join(defect_path, file) for file in os.listdir(defect_path) if file.lower().endswith('.jpg')]
        for defect_img in defect_list:
            prename = self.extract_prename(defect_img)
            if prename:
                self.defect_list.setdefault(prename, []).append(defect_img)
        
        self.match_goods_with_defects(defect_folder)
    # defect_list 결과
    # {'01': ['C:/work/python/PCB/PCB_DATASET/images\\Open_circuit\\01_open_circuit_01.jpg',
    #       'C:/work/python/PCB/PCB_DATASET/images\\Open_circuit\\01_open_circuit_02.jpg',
    #    ....], '02': [...], ...}  형태
    
    
    def match_goods_with_defects(self, defect_folder): #2
        good_images = [os.path.join(self.good_folder, file) for file in os.listdir(self.good_folder) if file.lower().endswith('.jpg')]
        for good_image in good_images:
            prename_g = self.extract_prename(good_image)
            if prename_g and prename_g in self.defect_list:
                self.matching_pairs.append((good_image, self.defect_list[prename_g]))
                
        self.compare_and_save_diff(defect_folder)                
    # matching_pairs 결과
    # [('C:/work/python/PCB/PCB_DATASET/PCB_USED\\01.JPG',
    #       ['C:/work/python/PCB/PCB_DATASET/images\\Open_circuit\\01_open_circuit_01.jpg',
    #       'C:/work/python/PCB/PCB_DATASET/images\\Open_circuit\\01_open_circuit_02.jpg',
    #    ....]), ...] 형태    

    def generate_diff_boxes(self, good_image, defect_image):
        imageA = cv2.imread(good_image)
        imageB = cv2.imread(defect_image)

        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        (score, diff) = compare_ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")

        thresh = cv2.threshold(
            diff, 0, 200,
            cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        )[1]
        cnts, _ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # 결함 박스 생성
        diff_boxes = []

        for i, c in enumerate(cnts, start=1):
            area = cv2.contourArea(c)
            if area > 40:
                x, y, w, h = cv2.boundingRect(c)
                xmax = x + w
                ymax = y + h
                cv2.rectangle(imageA, (x, y), (xmax, ymax), (0, 0, 255), 10)
                cv2.drawContours(imageB, [c], -1, (0, 0, 255), 10)
                diff_boxes.append((x, y, xmax, ymax))

        return diff_boxes, imageA, imageB
    
    # diff_boxes 정보 저장
    def compare_and_save_diff(self, defect_folder): #3
        data = []
        for pair in self.matching_pairs:
            good_image = pair[0]
            g_name = good_image.split('\\')[-1][0:2]
            defect_images = pair[1]
            for defect_image in defect_images:
                diff_boxes, _, _ = self.generate_diff_boxes(good_image, defect_image)
                for xmin, ymin, xmax, ymax in diff_boxes:
                    dnames = [defect_image]
                    d_name = []
                    for dname in dnames:
                        parts = dname.split("\\")
                        shortened_name = parts[-1].split(".")[0]
                        d_name.append(shortened_name)
                    output_filename = f"diff_{defect_folder}.txt"
                    output_path = os.path.join(self.output_path, output_filename)
                    data.append({'Good Image': g_name, 'Defect Image': d_name[0],
                                 'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax})
        df = pd.DataFrame(data)
        df.to_csv(output_path, sep='\t', index=False)
        print(f"Annotations saved to {output_path}")    
        


def main():
    selected_defect_folders = ['Mouse_bite', 'Open_circuit']  # 원하는 결함 입력
    good_folder = 'C:/work/python/PCB/PCB_DATASET/PCB_USED' # 경로 수정
    output_folder = 'C:/work/python/PCB/PCB_DATASET' # 경로 수정
    
    for defect_folder in selected_defect_folders:
        output_path = os.path.join(output_folder, f"diff_{defect_folder}.txt")
        pcb_matcher = PCBDefectMatcher([defect_folder], good_folder, output_folder)
        pcb_matcher.load_defect_images(defect_folder)

if __name__ == "__main__":
    main()

