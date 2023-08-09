from ultralytics import YOLO
import ultralytics
import os
import glob
from PIL import Image
import pandas as pd


#%% 실제 값, 예측 값 가져오기
class get_info:
    def __init__(self,label_path,image_path,md):
        self.label_path=label_path
        self.image_path=image_path
        self.model=md
        self.truths = self.return_score()
        self.preds=self.pred_xyxy()
        
    def return_score(self):
        names=self.files_load(self.label_path,".txt")
        truth_boxes={}
        for name in names: 
            line_count = self.lines_in_file(self.label_path+"/"+name+".txt")
            truth_boxes[name]=[]
            
            for i in line_count:
                q=i.split(" ")[1:]
                a=[float(j) for j in q]
                w,h=self.get_image_size(self.image_path+"/"+name+".jpg")
                xmin = (a[0]-a[2]/2)*w
                xmax=(a[0]+a[2]/2)*w
                ymin=(a[1]-a[3]/2)*h
                ymax=(a[1]+a[3]/2)*h
                truth_boxes[name].append((xmin,ymin,xmax,ymax))
        return dict(sorted(truth_boxes.items()))
        
    def files_load(self,path, ext='.jpg'): #파일 안오 모든 파일 불러오기
        files = []
        
        search_pattern = os.path.join(path, '*' + ext)
        files.extend(glob.glob(search_pattern))
        filenames = [os.path.basename(file)[:-4] for file in files]
        return filenames
        
    def lines_in_file(self,file_path): # file 정보 불러오기
        try:
            with open(file_path, 'r') as file:
                text = file.read()
                lines = text.splitlines()
                return lines
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
            return -1
            
    def get_image_size(self,path): #이미지 사이즈 구하기
        try:
            with Image.open(path) as img:
                width, height = img.size
                return width, height
        except Exception as e:
            print(f"이미지 크기를 가져오는 동안 오류 발생: {e}")
            return None

    

    def pred_xyxy(self):
        
        files=self.files_load(self.image_path, ext='.jpg')
        imgs=[self.image_path+"/"+img+".jpg" for img in files]
        boxes={}
        results=self.model(imgs)
        for result in results:
            name=result.path.split("/")[-1][:-4]
            boxes[name]=result.boxes.xyxy
        return dict(sorted(boxes.items()))
    
#%% 정밀도,재현도,f1-socre 계산
class return_score:
    def __init__(self,truths,preds,iou_threshold=0.5):
        self.truths=truths
        self.preds=preds
        self.iou_threshold=iou_threshold
        self.score=self.calculate_recall_precision()
    def calculate_recall_precision(self):
        true_positives = 0
        false_positives = 0
        false_negatives = 0
        len_truth=0
    
        for truth,pred in zip(self.truths,self.preds):
            ground_truth=self.truths[truth]
            predictions=self.preds[pred]
            len_truth+=len(truth)
            for pred_box in predictions:
                pred_box_detected = False
        
                for gt_box in ground_truth:
                    iou = self.calculate_iou(pred_box, gt_box)
                    if iou >= self.iou_threshold:
                        pred_box_detected = True
                        break
        
                if pred_box_detected:
                    true_positives += 1
                else:
                    false_positives += 1
    
        false_negatives = len_truth - true_positives
    
        recall = true_positives / (true_positives + false_negatives)
        precision = true_positives / (true_positives + false_positives)
        F1_score = (2*precision*recall)/(precision+recall)
        
        print(f"Recall: {recall:.2f}")
        print(f"Precision: {precision:.2f}")
        print(f"F1_score: {F1_score:.2f}")
        
        return recall, precision,F1_score

    def calculate_iou(self,box1, box2):
        # box: (x_min, y_min, x_max, y_max)
        x1, y1, x2, y2 = box1
        x3, y3, x4, y4 = box2
    
        x_intersection = max(0, min(x2, x4) - max(x1, x3))
        y_intersection = max(0, min(y2, y4) - max(y1, y3))
    
        intersection_area = x_intersection * y_intersection
    
        box1_area = (x2 - x1) * (y2 - y1)
        box2_area = (x4 - x3) * (y4 - y3)
    
        union_area = box1_area + box2_area - intersection_area
    
        iou = intersection_area / union_area
        return iou
    
#%% 실행 부분
labels_path="C:/Users/USER/Desktop/img/test/labels" #test label 경로
images_path="C:/Users/USER/Desktop/img/test/images" #test image 경로
model=YOLO('C:/work/python/project/runs/detect/train3/weights/best.pt') #모델 가져오기
info=get_info(labels_path,images_path,model)
truths=info.truths
preds =info.preds

score = return_score(truths,preds,0.5) # (실제,예측,iou설정값)
