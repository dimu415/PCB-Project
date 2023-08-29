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
        self.truths,self.truths_cl = self.return_score()
        self.preds,self.preds_cl=self.pred_xyxy()
        
    def return_score(self):
        names=self.files_load(self.label_path,".txt")
        truth_boxes={}
        cl={}
        for name in names: 
            line_count = self.lines_in_file(self.label_path+"/"+name+".txt")
            truth_boxes[name]=[]
            cl[name]=[]
            for i in line_count:
                q=i.split(" ")[1:]
                r=i.split(" ")[0]
                a=[float(j) for j in q]
                w,h=self.get_image_size(self.image_path+"/"+name+".jpg")
                xmin = (a[0]-a[2]/2)*w
                xmax=(a[0]+a[2]/2)*w
                ymin=(a[1]-a[3]/2)*h
                ymax=(a[1]+a[3]/2)*h
                truth_boxes[name].append((xmin,ymin,xmax,ymax))
                cl[name].append(r)
        return dict(sorted(truth_boxes.items())),dict(sorted(cl.items()))
        
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
        clss={}
        for img in imgs:
            for result in self.model([img]):
                name=result.path.split("/")[-1][:-4]
                boxes[name]=result.boxes.xyxy
                clss[name]=result.boxes.cls
        return dict(sorted(boxes.items())),dict(sorted(clss.items()))
    
#%% 정밀도,재현도,f1-socre 계산
class return_score:
    def __init__(self,truths,preds,tr_cl,pred_cl,iou_threshold=0.5):
        self.truths=truths
        self.truths_cls=tr_cl
        self.pred_cl=pred_cl
        self.preds=preds
        self.iou_threshold=iou_threshold
        self.score=self.calculate_recall_precision()
    def calculate_recall_precision(self):
        true_positives = {}
        false_positives = {}
        false_negatives = {}
        len_truth={}
        for ground_truth_cl in self.truths_cls:
            for n in self.truths_cls[ground_truth_cl]:
                try:
                    len_truth[n]+=1
                except:
                    true_positives[n]=0
                    false_positives[n]=0
                    len_truth[n]=1
        for truth,pred in zip(self.truths,self.preds):
            ground_truth=self.truths[truth]
            predictions=self.preds[pred]
            
            ground_truth_cl=self.truths_cls[truth]
            predictions_cl=self.pred_cl[pred]
           
            
            
            for pred_box,pred_cl in zip(predictions,predictions_cl):
                pred_box_detected = False
        
                for gt_box,gt_cl in zip(ground_truth,ground_truth_cl):
                    iou = self.calculate_iou(pred_box, gt_box)
                    gt=int(gt_cl)
                    if iou >= self.iou_threshold and pred_cl==gt:
                        pred_box_detected = True
                        break
                if pred_box_detected:
                    true_positives[str(int(pred_cl))] += 1
                else:
                    false_positives[str(int(pred_cl))] += 1
        a={}
        for i in len_truth:
            t=len_truth[i]
            tp=true_positives[i]
            fp=false_positives[i]
            fn = t - tp
            recall = tp / (tp + fn)
            precision = tp/ (tp + fp)
            # print(t,tp,fp,fn)
            F1_score = (2*precision*recall)/(precision+recall)
            # print("============",i,"============")
            # print(f"Recall: {recall:.2f}")
            # print(f"Precision: {precision:.2f}")
            # print(f"F1_score: {F1_score:.2f}")
            a[str(i)]=[recall,precision,F1_score]
        truth=sum(len_truth.values())
        true_positive=sum(true_positives.values())
        false_positive=sum(false_positives.values())
        false_negative=truth-true_positive
        total_recall= true_positive/(true_positive+false_negative)
        total_precision=true_positive/(true_positive+false_positive)
        total_F1score=(2*total_precision*total_recall)/(total_precision+total_recall)
        # print("===total====")
        # print(f"Recall: {total_recall:.2f}")
        # print(f"Precision: {total_precision:.2f}")
        # print(f"F1_score: {total_F1score:.2f}")
        a['total']=[total_recall,total_precision,total_F1score]
        
        return a 
            
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

# labels_path="C:/Users/USER/Desktop/test_train/test/labels" #test label 경로
# images_path="C:/Users/USER/Desktop/test_train/test/images" #test image 경로
# model=YOLO('C:/work/python/project/runs/detect/train3/weights/best.pt') #모델 가져오기
# info=get_info(labels_path,images_path,model)
# truths=info.truths
# preds =info.preds

# truths_cl=info.truths_cl
# preds_cl =info.preds_cl
# score = return_score(truths,preds,truths_cl,preds_cl,0.5) # (실제,예측,iou설정값)
