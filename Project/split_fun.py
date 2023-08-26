import os
import shutil
import random
class file_split:
    def __init__(self,source_directory,train_target_dir,test_target_dir,ratio = 0.8 ):
        self.source_directory = source_directory#"C:/Users/USER/Desktop/archive/PCB_DATASET/qw"
        self.train_target_dir =train_target_dir #"C:/Users/USER/Desktop/archive/PCB_DATASET/train_1"
        self.test_target_dir =test_target_dir #"C:/Users/USER/Desktop/archive/PCB_DATASET/test_1"
        self.ratio = ratio  # 필요한 비율로 설정
    
        # 함수 호출하여 클래스별 txt 파일 분할 수행 및 검증 출력
        self.split_and_verify_by_class(self.source_directory, self.train_target_dir, self.test_target_dir, self.ratio)  
    def extract_class_from_txt(self,txt_path):
        with open(txt_path, 'r') as txt_file:
            line = txt_file.readline()
            class_name = int(line.strip().split()[0])  # txt 내용의 첫 단어를 클래스로 해석
            return class_name
    
    def split_and_verify_by_class(self,source_directory, train_target_dir, test_target_dir, ratio=0.8):
        # 클래스별로 파일 분류
        class_files = {}
        txt_files = [filename for filename in os.listdir(source_directory) if filename.endswith(".txt")]
        for filename in txt_files:
            txt_path = os.path.join(source_directory, filename)
            class_name = self.extract_class_from_txt(txt_path)
            if class_name not in class_files:
                class_files[class_name] = []
            class_files[class_name].append(filename)
        
        total_train_files = 0
        total_test_files = 0
        
        # 비율에 따라 train과 test 파일 분할
        num_train_files = int(len(txt_files) * ratio)
        train_files = txt_files[:num_train_files]
        test_files = txt_files[num_train_files:]
        
        total_train_files += num_train_files
        total_test_files += len(txt_files) - num_train_files
        
        # train과 test 디렉토리 생성
        os.makedirs(train_target_dir, exist_ok=True)
        os.makedirs(test_target_dir, exist_ok=True)
        
        # 파일을 train과 test 디렉토리로 이동
        for filename in train_files:
            source_path = os.path.join(source_directory, filename)
            target_path = os.path.join(train_target_dir, filename)
            shutil.copy(source_path, target_path)
        
        for filename in test_files:
            source_path = os.path.join(source_directory, filename)
            target_path = os.path.join(test_target_dir, filename)
            shutil.copy(source_path, target_path)
        
        # 클래스별 파일 검증 비율 출력
        for class_name, class_filenames in class_files.items():
            total_class_files = len(class_filenames)
            train_class_files = len([filename for filename in class_filenames if filename in train_files])
            test_class_files = total_class_files - train_class_files
            class_ratio = train_class_files / total_class_files
            
            print(f"클래스 {class_name}의 총 파일 수: {total_class_files}")
            print(f"Train 파일 수: {train_class_files}, Test 파일 수: {test_class_files}")
            print(f"클래스 검증 비율: Train({class_ratio:.4f}) : Test({1 - class_ratio:.4f})")
        
        # 전체 train과 test 파일의 총 합 및 비율 출력
        total_ratio = total_train_files / (total_train_files + total_test_files)
        print("\n전체 클래스 검증 비율")
        print(f"전체 Train 파일의 총 합: {total_train_files}")
        print(f"전체 Test 파일의 총 합: {total_test_files}")
        print(f"전체 파일 검증 비율: Train({total_ratio:.4f}) : Test({1 - total_ratio:.4f})")
    
        # 중복 파일 검증
        duplicated_files = set(train_files) & set(test_files)
        if duplicated_files:
            print("\n같은 이름을 가진 파일이 두 폴더에 중복으로 존재합니다:")
            for filename in duplicated_files:
                print(filename)
        else:
            print("\n같은 이름을 가진 파일이 두 폴더에 중복으로 존재하지 않습니다.")

# 경로 및 비율 설정
