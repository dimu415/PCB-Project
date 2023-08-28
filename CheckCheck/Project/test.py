import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import pandas as pd
import shutil
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET
from PIL.ImageQt import ImageQt
from pyqt_switch import PyQtSwitch
import yaml
from split_fun import file_split
from qtrangeslider import QLabeledRangeSlider
from resize_fun import convert_and_save 
from reversal_fun import Augmentation_ver_rev,Augmentation_hor_rev
from rotation_fun import Rotation
from brightness_fun import Augmentation_bri
from performance_calculation import get_info,return_score
from xml_to_txt_fun import xml_to_txt_fun
from img_to_img_fun import img_to_img_fun
import ultralytics
from ultralytics import YOLO
import pyqtgraph as pg
import random
import time



class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("진문이짱")
        self.resize(1600, 800)
        self.setStyleSheet("QMainWindow {border: 13px solid #1A2D3A;}") 
        self.df = pd.DataFrame()
        self.My_path=os.getcwd()
        self.image_paths=""
        self.ano_paths=""
        self.df=pd.DataFrame()
        self.colors= ["Red", "Green", "Blue", "Yellow", "Orange", "Purple", "Brown"]
        os.environ['KMP_DUPLICATE_LIB_OK']='True'
        self.Main_UI()
        
    def Main_UI(self):
        self.sidebar_widget = QWidget()
        self.setCentralWidget(self.sidebar_widget)
        self.sidebar_widget.setStyleSheet("border-right: 3px solid #1A2329;")

        self.project_label = QLabel('project name')
        self.project_label.setAlignment(Qt.AlignCenter)  # 중앙 정렬
        self.project_label.setStyleSheet("font-size: 16px; xcolor: white; font-weight: bold;"
                                    "background-color:#673AB7; border-radius: 10px")       
        self.project_label.setFixedSize(200,30)
        
        button_stylesheet = """
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 18px;
                font-family: Arial, sans-serif;
                font-weight: bold;
                border: none;
                padding: 5px;
            }
            
            QPushButton:hover {
                background-color:#673AB7; 
                border-radius: 10px;
            }
        """
        self.widget_upload = QWidget()
        self.widget_label = QWidget()
        self.widget_agu = QWidget()
        self.widget_split = QWidget()
        self.widget_train = QWidget()
        self.widget_ana= QWidget()
        
        Upload_btn = QPushButton('파일 ')
        label_btn = QPushButton('라벨')
        agu_btn = QPushButton('여의봉')
        split_btn = QPushButton('분리')
        train_btn = QPushButton('학습')
        ana_btn = QPushButton('분석')
        save_btn = QPushButton('save')
        load_btn = QPushButton('load')
        
        buttons = [Upload_btn, label_btn, split_btn,agu_btn, 
                   train_btn, ana_btn, load_btn, save_btn]

        for button in buttons:
            button.setStyleSheet(button_stylesheet)
            button.setCursor(Qt.PointingHandCursor)  # 마우스 커서에 반응
            if button in [load_btn, save_btn]:
                button.setFixedSize(80, 50)
            else:
                button.setFixedSize(200, 50)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(load_btn)

        self.vlayout = QVBoxLayout()
        self.vlayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.vlayout.setContentsMargins(20, 20, 0, 0)
        self.vlayout.setSpacing(50)
        
        self.vlayout.addWidget(self.project_label)
        for button in buttons[:-2]:
            self.vlayout.addWidget(button)
        self.vlayout.addSpacing(30)
        self.vlayout.addLayout(btn_layout) 
        
        Upload_btn.clicked.connect(self.show_upload_layout)
        label_btn.clicked.connect(self.show_label_layout)
        split_btn.clicked.connect(self.show_split_layout)
        agu_btn.clicked.connect(self.show_agu_layout)
        train_btn.clicked.connect(self.show_train_layout)
        ana_btn.clicked.connect(self.show_analyze_layout)

# mainwindow
        #%%Upload
        self.Upload_layout=QVBoxLayout()

        
        load_file=QPushButton("불러오기")
        load_file.clicked.connect(self.Load_file)
        load_file.setStyleSheet("background-color:#673AB7;"
                            "color:white;"
                            "font-size: 18px;"
                            "font-family: Arial, sans-serif;"
                            "font-weight: bold;"
                            "border-radius: 20px;")
        load_file.setFixedSize(200,50)
        
        upload_hlayout = QHBoxLayout()
        self.Upload_lb = QListWidget()
        self.Upload_lb.setStyleSheet("background-color: rgba(128, 128, 128, 150); ")
        font = QFont("Broadway", 10, QFont.StyleNormal)
        self.Upload_lb.setFont(font)
        self.Upload_lb.setFixedSize(600, 400)
        self.Upload_lb.itemClicked.connect(self.show_img)
        
        self.load_df_widget = QLabel()
        self.load_df_widget.setFixedSize(600, 400)
        self.load_df_widget.setStyleSheet("background-color: rgba(128, 128, 128, 150); ")
        upload_hlayout.addWidget(self.Upload_lb)
        upload_hlayout.addWidget(self.load_df_widget)
        upload_hlayout.setSpacing(20)


        upload_hlayout2 = QHBoxLayout()      
        self.file_name_line= QLineEdit("file name")
        self.file_name_line.setStyleSheet("background-color:#EDE7F6;")
        self.file_name_line.setFixedSize(300, 30)
        self.file_name=""
        
        

        upload_hlayout2.setAlignment(Qt.AlignTop)
        upload_hlayout2.addWidget(self.file_name_line)
        upload_hlayout2.setSpacing(50)
        self.Upload_layout.addWidget(load_file)
        self.Upload_layout.addLayout(upload_hlayout)
        self.Upload_layout.addLayout(upload_hlayout2)
        self.Upload_layout.setAlignment(Qt.AlignTop)
        self.Upload_layout.setSpacing(20)
        
        #%% label
        self.label_layout=QHBoxLayout()
        
        label_vlayout1 = QVBoxLayout()
        
        load_ano=QPushButton("불러오기")
        load_ano.clicked.connect(self.Load_ano)
        load_ano.setStyleSheet("background-color:#512DA8;"
                            "color:white;"
                            "font-size: 18px;"
                            "font-family: Arial, sans-serif;"
                            "font-weight: bold;"
                            "border-radius: 20px;")
        load_ano.setFixedSize(200,40) 
        file_list=QLabel("이미지 이름")
        file_list.setFixedSize(200,30)
        file_list.setAlignment(Qt.AlignCenter)
        file_list.setStyleSheet("background-color: #673AB7; color: white; border: none; padding: 5px; border-radius: 10px;")

        
        self.label_ls=QListWidget()
        self.label_ls.itemClicked.connect(self.set_annotated_image) 
        self.label_ls.setFixedSize(200, 660)
        self.label_ls.setStyleSheet("background-color: rgba(255, 255, 255, 100); color: black; border: 1px solid gray; padding: 5px; border-radius: 10px;")
        ls_h=QHBoxLayout()
        sort_btn=QPushButton("↓")
        sort_btn.setFixedSize(30,20)
        
        self.cnt_list=QLabel("0")
        self.cnt_list.setFixedSize(30,20)
        ls_h.addWidget(sort_btn)
        ls_h.addWidget(self.cnt_list)
        ls_h.setSpacing(100)
        
        label_vlayout1.addWidget(load_ano)
        label_vlayout1.addWidget(file_list)
        label_vlayout1.setSpacing(1)
        label_vlayout1.addWidget(self.label_ls)
        label_vlayout1.addLayout(ls_h)
        label_vlayout1.setAlignment(Qt.AlignTop)
        label_vlayout2 = QVBoxLayout()
        
        self.img_name=QLabel("file_name")
        self.img_name.setFixedSize(1000,30)
        self.img_name.setAlignment(Qt.AlignCenter)
        self.img_name.setStyleSheet("background-color: #673AB7; color: white; border: none; padding: 5px; border-radius: 10px;")
        self.label_lb=QLabel()
        self.label_lb.setStyleSheet("background-color: rgba(255, 255, 255, 100);"
                            "border: 1px solid gray;"
                            "border-radius: 10px;")
        self.label_lb.setFixedSize(1000, 700)
        self.label_lb.setAlignment(Qt.AlignTop)
        label_vlayout2.addWidget(self.img_name)
        label_vlayout2.addWidget(self.label_lb)
        label_vlayout2.setSpacing(1)
        label_vlayout2.setAlignment(Qt.AlignTop)
        
        label_vlayout3 = QVBoxLayout()
        
        label_cl=QLabel("Class")
        label_cl.setFixedSize(300, 30)
        label_cl.setAlignment(Qt.AlignCenter)
        label_cl.setStyleSheet("background-color: #673AB7; color: white; border: none; padding: 5px; border-radius: 10px;")
        self.label_info= QListWidget()
        self.label_info.setStyleSheet("background-color: rgba(255, 255, 255, 100);"
                            "border: 1px solid gray; border-radius: 10px;")
        self.label_info.setFixedSize(300, 500)
        self.label_info.clicked.connect(self.item_clicked)
        

        label_vlayout3.addWidget(label_cl)
        label_vlayout3.addWidget(self.label_info)

        label_vlayout3.setAlignment(Qt.AlignTop)
        label_vlayout3.setSpacing(1)
        self.label_layout.addLayout(label_vlayout1)
        self.label_layout.addLayout(label_vlayout2)
        self.label_layout.addLayout(label_vlayout3)
        
        self.label_layout.addLayout(label_vlayout1)
        self.label_layout.addSpacing(20)  # 간격 추가
        self.label_layout.addLayout(label_vlayout2)
        self.label_layout.addSpacing(20)  # 간격 추가
        self.label_layout.addLayout(label_vlayout3)
        
        #%%agu
        self.agu_layout=QHBoxLayout()
        
        agu_vlayout = QVBoxLayout()

        resize=QHBoxLayout()
        resize_lb=QLabel("크기 조절")
        resize_lb.setFixedSize(200,30)
        resize_lb.setAlignment(Qt.AlignCenter)
        resize_lb.setStyleSheet("background-color: #673AB7; color: white; border: none; padding: 5px; border-radius: 10px;")
        self.resize_slider = QLabeledRangeSlider(Qt.Horizontal)
        self.resize_slider.setMinimum(1)
        self.resize_slider.setMaximum(10)
        self.resize_slider.setFixedWidth(300)
        self.resize_checkbox = QCheckBox()
        self.resize_checkbox.setStyleSheet("margin-top: 27px;") 
        resize.addWidget(self.resize_slider)
        resize.addWidget(self.resize_checkbox)
        resize.setSpacing(30)

            
        brightness=QHBoxLayout()
        brightness_lb=QLabel("명도")
        brightness_lb.setFixedSize(200,30)
        brightness_lb.setAlignment(Qt.AlignCenter)
        brightness_lb.setStyleSheet("background-color: #673AB7; color: white; border: none; padding: 5px; border-radius: 10px;")
        self.brightness_slider = QLabeledRangeSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(70)       
        #self.brightness_slider = QSlider(1)
        #self.brightness_slider.setOrientation(1)  # 수직 방향 슬라이더
        #self.brightness_slider.setTickPosition(QSlider.TicksBothSides)
        self.brightness_slider.setFixedWidth(300) 
        self.brightness_checkbox = QCheckBox()
        self.brightness_checkbox.setStyleSheet("margin-top: 27px;") 
        brightness.addWidget(self.brightness_slider)
        brightness.addWidget(self.brightness_checkbox)
        brightness.setSpacing(30)
        
        rotation=QHBoxLayout()
        rotation_lb=QLabel("회전")
        rotation_lb.setFixedSize(200,30)
        rotation_lb.setAlignment(Qt.AlignCenter)
        rotation_lb.setStyleSheet("background-color: #673AB7; color: white; border: none; padding: 5px; border-radius: 10px;")
        self.rotation_slider = QLabeledRangeSlider(Qt.Horizontal)
        self.rotation_slider.setMinimum(0)
        self.rotation_slider.setMaximum(30) 
        self.rotation_slider.setFixedWidth(300) 
        self.rotation_checkbox = QCheckBox()
        self.rotation_checkbox.setStyleSheet("margin-top: 27px;") 
        rotation.addWidget(self.rotation_slider)
        rotation.addWidget(self.rotation_checkbox)
        rotation.setSpacing(30)

        
        reversal_lb=QLabel("반전")
        reversal_lb.setFixedSize(200,30)
        reversal_lb.setAlignment(Qt.AlignCenter)
        reversal_lb.setStyleSheet("background-color: #673AB7; color: white; border: none; padding: 5px; border-radius: 10px;")
        
        reversal_layout = QHBoxLayout()
        reversal_H = QHBoxLayout()
        reversal_H.setAlignment(Qt.AlignLeft)  
        self.reversal_H_switch = PyQtSwitch()
        self.reversal_H_switch.toggled.connect(self.toggle_H_reversal)
        self.reversal_H_switch.setAnimation(True)
        self.reversal_H_label = QLabel('수평 Off')
        reversal_H.addWidget(self.reversal_H_label)
        reversal_H.addWidget(self.reversal_H_switch)
        reversal_H.setSpacing(10)
        
        
        reversal_V = QHBoxLayout()
        reversal_V.setAlignment(Qt.AlignLeft)
        self.reversal_V_switch = PyQtSwitch()
        self.reversal_V_switch.toggled.connect(self.toggle_V_reversal)
        self.reversal_V_switch.setAnimation(True)
        self.reversal_V_label = QLabel('수직 Off')
        self.V_jug=False
        self.H_jug=False
        reversal_V.addWidget(self.reversal_V_label)
        reversal_V.addWidget(self.reversal_V_switch)
        reversal_V.setSpacing(10)
        reversal_layout.addLayout(reversal_H)
        reversal_layout.addLayout(reversal_V)
        reversal_layout.setSpacing(10)
        
        self.agu_btn=QPushButton("go")
        self.agu_btn.clicked.connect(self.Augmetation)
       
        agu_vlayout.addWidget(resize_lb)
        agu_vlayout.addLayout(resize)
        agu_vlayout.addWidget(brightness_lb)
        agu_vlayout.addLayout(brightness)
        agu_vlayout.addWidget(rotation_lb)
        agu_vlayout.addLayout(rotation)
        agu_vlayout.addWidget(reversal_lb)
        agu_vlayout.addLayout(reversal_layout)
        agu_vlayout.addWidget( self.agu_btn)

        
        agu_vlayout.setSpacing(10)
        agu_vlayout.setAlignment(Qt.AlignTop)
        agu_vlayout.setSpacing(50)
        agu_img=QLabel()
        agu_img.setFixedSize(1000, 700)
        agu_img.setStyleSheet("background-color: rgba(255, 255, 255, 100);"
                            "border: 1px solid gray;")
        
        
        
        self.agu_layout.addLayout(agu_vlayout)
        self.agu_layout.addWidget(agu_img)
    #%% split
        self.split_layout=QHBoxLayout()
        split_vlayout = QVBoxLayout()
       
        #logo
        pixmap = QPixmap('C:/Users/USER/Desktop/logo.png')
        # 이미지 크기 조절
        lbl_img = QLabel()
        lbl_img.setFixedSize(400,100)
        w = lbl_img.width()
        h = lbl_img.height()
        pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatioByExpanding)
        lbl_img.setPixmap(pixmap)



        #hello world
        a=QLabel("base:기본적인 분리 방법으로 클래스 종류 상관없이 원하는 비율에 맞게 학습용과 실험용으로 분리를 합니다"+"\n\n"+
                 "custom:데이트의 모든 클래스별로 사용자가 지정한 비율로 나누어집니다.\n 따라서, 클래스별로 훈련데이터와 테스트 데이터의 비율이 일정합니다. ")
        font = QFont()
        font.setPointSize(10)  # 원하는 크기로 설정
        a.setFont(font)
        
        #split_gb
        split_gb=QGroupBox()
        split_gb.setStyleSheet("QGroupBox { border: 1px solid gray; border-radius: 10px; }")
        split_header_label = QLabel("분리", split_gb)
        split_header_label.setFixedSize(800,30)
        split_header_label.setAlignment(Qt.AlignCenter)
        split_header_label.setStyleSheet("background-color: #673AB7; color: white; padding: 5px;" 
                                         "border-top-left-radius: 10px; border-top-right-radius: 10px;")
        split_gb_layout = QVBoxLayout()
        split_gb.setLayout(split_gb_layout)
        split_gb_layout.addSpacing(30)
     
        split_combo =QComboBox()
        split_combo.setFixedSize(500,40)
        split_combo.addItem("base")
        split_combo.addItem("custom")
        split_combo.setStyleSheet("background-color: white; border: 1px solid #D1C4E9;"
                                  "color: black; padding: 5px; border-radius: 10px; ")        
        font = QFont()
        font.setPointSize(16)  # 원하는 크기로 설정
        split_combo.setFont(font)
        
        self.split_slider = QSlider(Qt.Horizontal)
        self.split_slider.setFocusPolicy(Qt.StrongFocus)
        self.split_slider.setTickPosition(QSlider.TicksBothSides)
        self.split_slider.setMinimum(0)
        self.split_slider.setMaximum(100)
        self.split_slider.setTickInterval(10)
        self.split_slider.setSingleStep(1)
        self.split_slider.setValue(80)  
        self.split_slider.setFixedSize(700,70)
        self.split_slider.valueChanged.connect(self.update)
        self.split_result_label = QLabel('■ Train: 80, Val: 20',self)
        
        split_btn=QPushButton("Split")
        split_btn.setStyleSheet('background-color: #D1C4E9;'
                                'border-radius: 10px;')
        split_btn.setFixedSize(700,30)
        split_btn.clicked.connect(self.split_file)
        split_gb_layout.addWidget(split_combo)
        split_gb_layout.addSpacing(40)
        split_gb_layout.addWidget(self.split_slider)
        split_gb_layout.addWidget(self.split_result_label)
        split_gb_layout.addSpacing(40)
        split_gb_layout.addWidget(split_btn)
        split_gb_layout.addWidget(split_gb)
        split_gb_layout.setAlignment(Qt.AlignTop)
        split_gb.setFixedSize(800,400)
  
        #label
        split_info=QLabel()
        split_info.setStyleSheet("background-color: rgba(255, 255, 255, 100);"
                            "border: 1px solid gray; border-radius: 10px")
        split_info.setFixedSize(400,700)
        split_info_label = QLabel("분리 결과", split_info)
        split_info_label.setFixedSize(400,30)
        split_info_label.setAlignment(Qt.AlignCenter)
        split_info_label.setStyleSheet("background-color: #673AB7; color: white; padding: 5px;"
                                       "border-top-left-radius: 10px; border-top-right-radius: 10px;"
                                       "border-bottom-left-radius: 0px; border-bottom-right-radius: 0px;")
        

        split_vlayout.addWidget(lbl_img)
        split_vlayout.addSpacing(43)
        split_vlayout.addWidget(a)
        split_vlayout.addSpacing(48)
        split_vlayout.addWidget(split_gb)
        split_vlayout.setAlignment(Qt.AlignCenter)
        split_vlayout.setSpacing(10)
        self.split_layout.addLayout(split_vlayout)
        self.split_layout.addWidget(split_info)
        self.split_layout.setSpacing(50)
    #%% train
        self.train_layout=QVBoxLayout()
        
        train_vlayout1 = QHBoxLayout()
       
        
        train_Box1 = QGroupBox()
        train_Box1.setFixedSize(200,130)
        train_Box1.setStyleSheet('QGroupBox {border: 1px solid gray; border-radius : 10px;}')
        train_header_label = QLabel('실행', train_Box1)
        train_header_label.setFixedSize(200,30)
        train_header_label.setAlignment(Qt.AlignCenter)
        train_header_label.setStyleSheet("background-color: #673AB7; color: white; padding: 5px;"
                                        "border-top-left-radius: 10px; border-top-right-radius: 10px;")
        train_prebox1 = QVBoxLayout()
        spacer1 = QSpacerItem(20, 25, QSizePolicy.Minimum, QSizePolicy.Fixed)
        train_prebox1.addItem(spacer1) 
        start_btn = QPushButton('Start')
        start_btn.clicked.connect(self.Model_train)
        start_btn.setFixedSize(100,30)
        start_btn.setStyleSheet('background-color: #D1C4E9;'
                                'border-radius: 10px;')
        stop_btn = QPushButton('Stop')
        stop_btn.setFixedSize(100,30)
        stop_btn.setStyleSheet('background-color: #D1C4E9;'
                                'border-radius: 10px;')

        train_prebox1.addWidget(start_btn)
        train_prebox1.addWidget(stop_btn)
        train_prebox1.setSpacing(10)  # 버튼 사이의 간격 조절
        train_prebox1.setAlignment(Qt.AlignCenter)  # 버튼을 위쪽에 정렬
        train_Box1.setLayout(train_prebox1)
        

        train_Box2 = QGroupBox()
        train_Box2.setFixedSize(600,130)
        train_Box2.setStyleSheet('QGroupBox {border: 1px solid gray; border-radius : 10px;}')
        train_header_label2 = QLabel('모드', train_Box2)
        train_header_label2.setFixedSize(600,30)
        train_header_label2.setAlignment(Qt.AlignCenter)
        train_header_label2.setStyleSheet("background-color: #673AB7; color: white; padding: 5px;"
                                        "border-top-left-radius: 10px; border-top-right-radius: 10px;")
        gLayout = QGridLayout()   
        epoch_label = QLabel('Epoch')
        batch_label = QLabel('Batch_size')
        learnrate_label = QLabel('Learning_Rate')
        epoch_edit = QSpinBox()
        batch_edit = QSpinBox()
        learnrate_edit = QSpinBox()
        apply_btn = QPushButton('Apply')  
        apply_btn.setFixedSize(400, 30)
        apply_btn.setStyleSheet('background-color: #D1C4E9; border-radius: 10px;')  
        gLayout.addWidget(epoch_label, 0, 0)       
        gLayout.addWidget(batch_label, 0, 3)
        gLayout.addWidget(learnrate_label, 0, 6)
        gLayout.addWidget(epoch_edit, 0, 1)
        gLayout.addWidget(batch_edit, 0, 4) 
        gLayout.addWidget(learnrate_edit, 0, 7)     
        gLayout.addWidget(apply_btn, 1, 0, 1, 7)      
        gLayout.setAlignment(Qt.AlignCenter) 
        spacer_layout = QVBoxLayout()
        spacer_layout.addSpacing(40)
        gLayout.addLayout(spacer_layout, 0, 0) 
        train_Box2.setLayout(gLayout)
        
        
        train_Box3 = QGroupBox()
        train_Box3.setFixedSize(300,130)
        train_Box3.setStyleSheet('QGroupBox {border: 1px solid gray; border-radius : 10px;}') 
        train_header_label3 = QLabel('진행률', train_Box3)
        train_header_label3.setFixedSize(300,30)
        train_header_label3.setAlignment(Qt.AlignCenter)
        train_header_label3.setStyleSheet("background-color: #673AB7; color: white; padding: 5px;"
                                        "border-top-left-radius: 10px; border-top-right-radius: 10px;")
        train_box3 = QVBoxLayout()
        self.train_pgbar = QProgressBar()
        self.train_pgbar.setAlignment(Qt.AlignCenter)
        train_box3.addWidget(self.train_pgbar)
        train_Box3.setLayout(train_box3)
        
        train_vlayout1.addWidget(train_Box2)
        train_vlayout1.addWidget(train_Box1)
        train_vlayout1.addWidget(train_Box3)
        
        train_vlayout2 = QVBoxLayout()
        train_result_Box = QGroupBox()
        train_result_Box.setFixedSize(1115,620)
        train_result_Box.setStyleSheet('QGroupBox {border: 1px solid gray; border-radius : 10px;}')
        train_result_label = QLabel('실행', train_result_Box)
        train_result_label.setFixedSize(1115,30)
        train_result_label.setAlignment(Qt.AlignCenter)
        train_result_label.setStyleSheet("background-color: #673AB7; color: white; padding: 5px;"
                                        "border-top-left-radius: 10px; border-top-right-radius: 10px;")
        graph_box =QHBoxLayout()   
        self.pw1 = pg.PlotWidget(title = 'Chart 1') 
        self.pw1.setFixedSize(400,400)
        self.pw2 = pg.PlotWidget(title = 'Chart 2')
        self.pw2.setFixedSize(400,400)
        graph_box.addWidget(self.pw1)
        graph_box.addWidget(self.pw2)
        train_vlayout2.addWidget(train_result_Box)
        train_result_Box.setLayout(graph_box)





        self.train_layout.addLayout(train_vlayout1)
        self.train_layout.addLayout(train_vlayout2)
 
    #%% Analyze
        self.analyze_layout=QHBoxLayout()
        
        analyze_vlayout1 = QVBoxLayout()
        
        anfile_list=QLabel("이미지 이름")
        anfile_list.setFixedSize(200,30)
        anfile_list.setAlignment(Qt.AlignCenter)
        anfile_list.setStyleSheet("background-color: #673AB7; color: white; border: none; padding: 5px; border-radius: 10px;")

        
        self.anlabel_ls=QListWidget()
        self.anlabel_ls.itemClicked.connect(self.set_annotated_image) 
        self.anlabel_ls.setFixedSize(200, 700)
        self.anlabel_ls.setStyleSheet("background-color: rgba(255, 255, 255, 100); color: black; border: 1px solid gray; padding: 5px; border-radius: 10px;")
        anls_h=QHBoxLayout()
        ansort_btn=QPushButton("↓")
        ansort_btn.setFixedSize(30,20)
        
        self.ancnt_list=QLabel("0")
        self.ancnt_list.setFixedSize(30,20)
        anls_h.addWidget(ansort_btn)
        anls_h.addWidget(self.ancnt_list)
        anls_h.setSpacing(100)
        
        analyze_vlayout1.addWidget(anfile_list)
        analyze_vlayout1.setSpacing(1)
        analyze_vlayout1.addWidget(self.anlabel_ls)
        analyze_vlayout1.addLayout(anls_h)
        analyze_vlayout1.setAlignment(Qt.AlignTop)
        analyze_vlayout2 = QVBoxLayout()
    
        self.animg_name=QLabel("file_name")
        self.animg_name.setFixedSize(1000,30)
        self.animg_name.setAlignment(Qt.AlignCenter)
        self.animg_name.setStyleSheet("background-color: #673AB7; color: white; border: none; padding: 5px; border-radius: 10px;")
        self.anlabel_lb=QLabel()
        self.anlabel_lb.setStyleSheet("background-color: rgba(255, 255, 255, 100);"
                            "border: 1px solid gray;"
                            "border-radius: 10px;")
        self.anlabel_lb.setFixedSize(1000, 700)
        self.anlabel_lb.setAlignment(Qt.AlignTop)
        
        analyze_vlayout2.addWidget(self.animg_name)
        analyze_vlayout2.addWidget(self.anlabel_lb)
        analyze_vlayout2.setSpacing(1)
        analyze_vlayout2.setAlignment(Qt.AlignTop)
        
        analyze_vlayout3 = QVBoxLayout()
        
        anlabel_cl=QLabel("Class")
        anlabel_cl.setFixedSize(300, 30)
        anlabel_cl.setAlignment(Qt.AlignCenter)
        anlabel_cl.setStyleSheet("background-color: #673AB7; color: white; border: none; padding: 5px; border-radius: 10px;")
        self.anlabel_info=QListView()
        self.anlabel_info.setStyleSheet("background-color: rgba(255, 255, 255, 100);"
                            "border: 1px solid gray; border-radius: 10px;")
        self.anlabel_info.setFixedSize(300, 500)
        
        analyze_vlayout3.addWidget(anlabel_cl)
        analyze_vlayout3.addWidget(self.anlabel_info)
        analyze_vlayout3.setAlignment(Qt.AlignTop)
        analyze_vlayout3.setSpacing(1)
        self.analyze_layout.addLayout(analyze_vlayout1)
        self.analyze_layout.addLayout(analyze_vlayout2)
        self.analyze_layout.addLayout(analyze_vlayout3)
        
        self.analyze_layout.addLayout(analyze_vlayout1)
        self.analyze_layout.addSpacing(20)  
        self.analyze_layout.addLayout(analyze_vlayout2)
        self.analyze_layout.addSpacing(20)
        self.analyze_layout.addLayout(analyze_vlayout3)
        
                
        #%%layout
        self.sidebar_widget = QWidget()
        self.setCentralWidget(self.sidebar_widget)
        self.sidebar_widget.setStyleSheet("border-left: 10px solid #121D27; border-right: 10px solid #121D27; background-color: #121D27;")
        w_hlayout = QHBoxLayout()
        w_hlayout.addLayout(self.vlayout)
        self.sidebar_widget.setLayout(w_hlayout)
        
        
        u_hlayout= QHBoxLayout()
        u_hlayout.addLayout(self.Upload_layout)
        self.widget_upload.setLayout(u_hlayout)
        
        l_hlayout= QHBoxLayout()
        l_hlayout.addLayout(self.label_layout)
        self.widget_label.setLayout(l_hlayout)
        
        a_hlayout= QHBoxLayout()
        a_hlayout.addLayout(self.agu_layout)
        self.widget_agu.setLayout(a_hlayout)
        
        s_hlayout= QHBoxLayout()
        s_hlayout.addLayout(self.split_layout)
        self.widget_split.setLayout(s_hlayout)
        
        t_hlayout= QHBoxLayout()
        t_hlayout.addLayout(self.train_layout)
        self.widget_train.setLayout(t_hlayout)

        r_hlayout= QHBoxLayout()
        r_hlayout.addLayout(self.analyze_layout)
        self.widget_ana.setLayout(r_hlayout)        
        
        
        self.setGeometry(100, 100, 1600, 800)
        
        
        self.combined_layout = QHBoxLayout()
        self.combined_layout.addWidget(self.sidebar_widget)
        self.combined_layout.addWidget(self.widget_upload)
        
        self.window_widget=QWidget()
        self.window_widget.setLayout(self.combined_layout)
        # 초기 중앙 위젯 설정
        self.setCentralWidget( self.window_widget)
        self.currentWidget=self.widget_upload

#%%widget change
    def show_upload_layout(self):
        self.switch_layout(self.widget_upload)
    def show_label_layout(self):
        self.switch_layout(self.widget_label)
        
    def show_agu_layout(self):
        self.switch_layout(self.widget_agu)
    ##
    def toggle_H_reversal(self, checked):
        if checked:
            self.H_jug=True
            self.reversal_H_label.setText('수평 On')
        else:
            self.H_jug=False
            self.reversal_H_label.setText('수평 Off')
            
    def toggle_V_reversal(self, checked):
        if checked:
            self.V_jug=True
            self.reversal_V_label.setText('수직 On')
        else:
            self.V_jug=False
            self.reversal_V_label.setText('수직 Off')
    ##
    def show_split_layout(self):
        self.switch_layout(self.widget_split)
        
    def show_train_layout(self):
        self.switch_layout(self.widget_train)
    
    def show_analyze_layout(self):
        self.switch_layout(self.widget_ana)    
    
    def switch_layout(self, widget):
        if self.currentWidget:
            self.currentWidget.hide()
        self.combined_layout.removeWidget(self.currentWidget)
        self.combined_layout.addWidget(widget)
        widget.show()
        self.currentWidget = widget
        
        
#%% part -Upload
    def Load_file(self):
        options = QFileDialog.Options()
        directory_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
        if directory_path:
            print("Selected folder:", directory_path)
            if os.path.exists(directory_path):
                self.image_paths=directory_path
                files = self.list_files_in_directory(directory_path)
                dataframe = self.create_dataframe(files)
                self.df["img_path"]=dataframe['File Path']
                self.df["name"]=[ name.split("\\")[-1][:-4] for name in dataframe['File Path']]
                for name in self.df['name']:
                    self.Upload_lb.addItem(name)
    def show_img(self,item):
        selected_text = item.text()
        d = self.df[self.df['name'] == selected_text].reset_index(drop=True)
        image_path=d['img_path'][0]
        pixmap = QPixmap(image_path)
        self.load_df_widget.setPixmap(pixmap.scaled(self.load_df_widget.size(), aspectRatioMode=True))
   
    def Load_ano(self):
        options = QFileDialog.Options()
        directory_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
        if directory_path:
            print("Selected folder:", directory_path)
            if os.path.exists(directory_path):
                self.ano_paths=directory_path
                files = self.list_files_in_directory(directory_path)
                dataframe = self.create_dataframe(files)
                self.df["ano_path"]=dataframe['File Path']
                self.df["name"]=[ name.split("\\")[-1][:-4] for name in dataframe['File Path']]
                
        self.xml_to_txt()
    def xml_to_txt(self):
        self.file_name=self.file_name_line.text()
        self.project_label.setText(self.file_name_line.text())
        output1=f"{self.My_path}/{self.file_name}/base_labels"
        self.class_name=xml_to_txt_fun(self.ano_paths, output1).cl
        
        output2=f"{self.My_path}/{self.file_name}/base_images"
        img_to_img_fun(self.image_paths,output2)
        
        self.List_view()
    def list_files_in_directory(self,directory):
        file_list = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                file_list.append((file_path, file_size))
        return file_list
    def create_dataframe(self,file_list):
        df = pd.DataFrame(file_list, columns=['File Path', 'File Size'])
        return df
    
    
            
    
#%% part-label
    def List_view(self):
        if len(self.df) !=0:
            self.img_name.setText(self.file_name)
            self.class_lb={}
            labels_path=[]
            images_path=[]
            names=[]
            for root, dirs, files in os.walk(f"{self.My_path}/{self.file_name}/base_labels"):
                for file in files:
                    if file.endswith(".txt"):
                        file_path = os.path.join(root, file)
                        with open(file_path, "r") as file:
                            for line in file:
                                try:
                                    self.class_lb[str(line.split(" ")[0])]+=1
                                except:
                                    self.class_lb[str(line.split(" ")[0])]=0
                        name=file_path.split("\\")[-1][:-4]
                        self.label_ls.addItem( name)
                        names.append(name)
                        labels_path.append(file_path)
                        img_path=f"{self.My_path}/{self.file_name}/base_images/{name}.jpg"
                        
                        images_path.append(img_path)
            data={"name":names,
                  "img_path":images_path,
                  "ano_path":labels_path}
            self.df=pd.DataFrame(data)
            clo_num=0
            cu=len(self.colors)
            self.cl_color={}
            for n,f in enumerate(self.class_lb):
                item=f"{f}:{self.class_name[f]}:"+str(self.class_lb[f])
                self.label_info.addItems([item])
                self.label_info.item(n).setForeground(QColor(self.colors[clo_num]))
                font = self.label_info.item(n).font()
                font.setPointSizeF(font.pointSizeF() + 2)  # 폰트 크기를 2 포인트 증가시킴
                font.setBold(True)  # 볼드체 설정
                self.label_info.item(n).setFont(font)
                self.cl_color[f]=self.colors[clo_num]
                if clo_num<(cu-1):
                    clo_num+=1
                
            
            self.cnt_list.setText(str(len(self.df['name'])))
    def item_clicked(self, index):
        orig=self.label_info.itemFromIndex(index).text().split(":")[0]
        class_name, ok = QInputDialog.getText(self, orig, "class name:")
            
        
        if ok :
            self.class_name[orig]=class_name
            item=self.label_info.itemFromIndex(index)
            item.setText(f"{orig}:{class_name}: {self.class_lb[orig]}")
        
        
    def image_label(self, image_path, xml_path):
        sample_image_annotated = Image.open(image_path)
        

        # 폰트 설정
        font = ImageFont.truetype("arial.ttf", 55)

        img_draw = ImageDraw.Draw(sample_image_annotated)
        with open(xml_path, "r") as file:
            for line in file:
                
                a=line.split("\n")[0].split(" ")
                    
                xmin = int(a[1])
                ymin = int(a[2])
                xmax = int(a[3])
                ymax = int(a[4])

                img_draw.rectangle([(xmin, ymin), (xmax, ymax)], outline=self.cl_color[a[0]], width=5)
        
                   
                name_text = img_draw.textbbox((xmax - 175, ymax + 20),self.class_name[a[0]], anchor='lt', font=font)
                img_draw.rectangle([(name_text[0], name_text[1]), (name_text[2], name_text[3])], fill=self.cl_color[a[0]])
                img_draw.text((name_text[0], name_text[1]), self.class_name[a[0]], fill='white', font=font)
        
        return sample_image_annotated
                
    def set_annotated_image(self, item):
        selected_text = item.text()
        d = self.df[self.df['name'] == selected_text].reset_index(drop=True)

        img = d['img_path'][0]
        ano = d['ano_path'][0]
        print(img,ano)
        annotated_image = self.image_label(img, ano)
        
        
        qt_image = self.pil_to_qt(annotated_image)
     #   self.label_lb.setPixmap(qt_image.scaled(self.label_lb.size(), aspectRatioMode=True))
        self.label_lb.setPixmap(QPixmap(qt_image).scaled(1000, 700, Qt.KeepAspectRatio))
        #self.label_lb.setPixmap(QPixmap.fromImage(qt_image))
    def pil_to_qt(self, pil_image):
        image = pil_image.convert("RGBA")
        width, height = image.size
        q_image = QImage(image.tobytes(), width ,height, QImage.Format_RGBA8888)
        return q_image
        
    #%%part-split
    def split_file(self):
        
        ratio=self.split_slider.value()/100
        source_path=f"{self.My_path}/{self.file_name}/base_labels"
        train_target_dir =f"{self.My_path}/{self.file_name}/split/train_label"
        test_target_dir =f"{self.My_path}/{self.file_name}/split/test_label"
        file_split(source_path,train_target_dir,test_target_dir,ratio)
        
        train_img=f"{self.My_path}/{self.file_name}/split/train_images"
        test_img=f"{self.My_path}/{self.file_name}/split/test_images"
        if not os.path.exists(train_img):
            os.makedirs(train_img)
        if not os.path.exists(test_img):
            os.makedirs(test_img)
        for root, dirs, files in os.walk(train_target_dir):
            for file in files:
                if file.endswith(".txt"):
                    file_path =f"{self.My_path}/{self.file_name}/base_images/"+ os.path.join(root, file).split("\\")[-1][:-4]+".jpg"
                    destination_path=train_img+"/"+os.path.join(root, file).split("\\")[-1][:-4]+".jpg"
                    shutil.copy(file_path, destination_path)
                    
        for root, dirs, files in os.walk(test_target_dir):
            for file in files:
                if file.endswith(".txt"):
                    file_path2 =f"{self.My_path}/{self.file_name}/base_images/"+ os.path.join(root, file).split("\\")[-1][:-4]+".jpg"
                    destination_path= test_img+"/"+os.path.join(root, file).split("\\")[-1][:-4]+".jpg"
                    shutil.copy(file_path2, destination_path)
        
 
    def update(self, value):
        maximum_value = self.split_slider.maximum()   
        remaining_value = maximum_value - value
        self.split_result_label.setText(f'■ Train: {value}, Val: {remaining_value}')            
    #%% part-aug
    def Augmetation(self):
        if self.resize_checkbox.isChecked():
            self.img_resize()
        if self.V_jug:
            self.img_reversal_V()
        if self.H_jug:
            self.img_reversal_H()
        if self.rotation_checkbox.isChecked():
            self.img_rotation()
        if  self.brightness_checkbox.isChecked():
            self.img_brightness()
        self.Create_yaml()
    def img_resize(self):
        train_output=f"{self.My_path}/{self.file_name}/data/train"
        train_path_images=f"{self.My_path}/{self.file_name}/split/train_images"
        train_path_txt=f"{self.My_path}/{self.file_name}/split/train_label"
        train_img_file_list=[]
        train_txt_file_list=[]
        for root, dirs, files in os.walk(train_path_images):
            for file in files:
                if file.endswith(".jpg"):
                    file_path = os.path.join(root, file)
                    train_img_file_list.append(file_path)
        for root, dirs, files in os.walk(  train_path_txt):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    train_txt_file_list.append(file_path)
        for img,txt in zip(train_img_file_list,train_txt_file_list):
            x=random.randint(self.resize_slider.value()[0], self.resize_slider.value()[1])
            convert_and_save(2,img,txt,train_output)
        
        test_output=f"{self.My_path}/{self.file_name}/data/test"
        test_path_images=f"{self.My_path}/{self.file_name}/split/test_images"
        test_path_txt=f"{self.My_path}/{self.file_name}/split/test_label"
        test_img_file_list=[]
        test_txt_file_list=[]
        for root, dirs, files in os.walk(test_path_images):
            for file in files:
                if file.endswith(".jpg"):
                    file_path = os.path.join(root, file)
                    test_img_file_list.append(file_path)
        for root, dirs, files in os.walk(  test_path_txt):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    test_txt_file_list.append(file_path)
        for img,txt in zip(test_img_file_list,test_txt_file_list):
            x=random.randint(self.resize_slider.value()[0], self.resize_slider.value()[1])
            convert_and_save(2,img,txt,test_output)
      
        
        
    def img_reversal_V(self):
        train_output=f"{self.My_path}/{self.file_name}/data/train"
        train_path_images=f"{self.My_path}/{self.file_name}/split/train_images"
        train_path_txt=f"{self.My_path}/{self.file_name}/split/train_label"
        train_img_file_list=[]
        train_txt_file_list=[]
        for root, dirs, files in os.walk(train_path_images):
            for file in files:
                if file.endswith(".jpg"):
                    file_path = os.path.join(root, file)
                    train_img_file_list.append(file_path)
        for root, dirs, files in os.walk(  train_path_txt):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    train_txt_file_list.append(file_path)
        for img,txt in zip(train_img_file_list,train_txt_file_list):
            out_img=train_output+"/images"
            out_txt=train_output+"/labels"
            Augmentation_ver_rev(txt,img,out_img,out_txt)
        
        test_output=f"{self.My_path}/{self.file_name}/data/test"
        test_path_images=f"{self.My_path}/{self.file_name}/split/test_images"
        test_path_txt=f"{self.My_path}/{self.file_name}/split/test_label"
        test_img_file_list=[]
        test_txt_file_list=[]
        for root, dirs, files in os.walk(test_path_images):
            for file in files:
                if file.endswith(".jpg"):
                    file_path = os.path.join(root, file)
                    test_img_file_list.append(file_path)
        for root, dirs, files in os.walk(  test_path_txt):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    test_txt_file_list.append(file_path)
        for img,txt in zip(test_img_file_list,test_txt_file_list):
            out_img=test_output+"/images"
            out_txt=test_output+"/labels"
            Augmentation_ver_rev(txt,img,out_img,out_txt)
            
    def img_reversal_H(self):
        train_output=f"{self.My_path}/{self.file_name}/data/train"
        train_path_images=f"{self.My_path}/{self.file_name}/split/train_images"
        train_path_txt=f"{self.My_path}/{self.file_name}/split/train_label"
        train_img_file_list=[]
        train_txt_file_list=[]
        for root, dirs, files in os.walk(train_path_images):
            for file in files:
                if file.endswith(".jpg"):
                    file_path = os.path.join(root, file)
                    train_img_file_list.append(file_path)
        for root, dirs, files in os.walk(  train_path_txt):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    train_txt_file_list.append(file_path)
        for img,txt in zip(train_img_file_list,train_txt_file_list):
            out_img=train_output+"/images"
            out_txt=train_output+"/labels"
            Augmentation_hor_rev(txt,img,out_img,out_txt)
        
        test_output=f"{self.My_path}/{self.file_name}/data/test"
        test_path_images=f"{self.My_path}/{self.file_name}/split/test_images"
        test_path_txt=f"{self.My_path}/{self.file_name}/split/test_label"
        test_img_file_list=[]
        test_txt_file_list=[]
        for root, dirs, files in os.walk(test_path_images):
            for file in files:
                if file.endswith(".jpg"):
                    file_path = os.path.join(root, file)
                    test_img_file_list.append(file_path)
        for root, dirs, files in os.walk(  test_path_txt):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    test_txt_file_list.append(file_path)
        for img,txt in zip(test_img_file_list,test_txt_file_list):
            out_img=test_output+"/images"
            out_txt=test_output+"/labels"
            Augmentation_hor_rev(txt,img,out_img,out_txt)
    def img_rotation(self):
        train_output=f"{self.My_path}/{self.file_name}/data/train"
        train_path_images=f"{self.My_path}/{self.file_name}/split/train_images"
        train_path_txt=f"{self.My_path}/{self.file_name}/split/train_label"
        train_img_file_list=[]
        train_txt_file_list=[]
        for root, dirs, files in os.walk(train_path_images):
            for file in files:
                if file.endswith(".jpg"):
                    file_path = os.path.join(root, file)
                    train_img_file_list.append(file_path)
        for root, dirs, files in os.walk(  train_path_txt):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    train_txt_file_list.append(file_path)
        for img,txt in zip(train_img_file_list,train_txt_file_list):
            x=random.randint(self.rotation_slider.value()[0], self.rotation_slider.value()[1])
            Rotation(img,txt,train_output,x)
        
        test_output=f"{self.My_path}/{self.file_name}/data/test"
        test_path_images=f"{self.My_path}/{self.file_name}/split/test_images"
        test_path_txt=f"{self.My_path}/{self.file_name}/split/test_label"
        test_img_file_list=[]
        test_txt_file_list=[]
        for root, dirs, files in os.walk(test_path_images):
            for file in files:
                if file.endswith(".jpg"):
                    file_path = os.path.join(root, file)
                    test_img_file_list.append(file_path)
        for root, dirs, files in os.walk(  test_path_txt):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    test_txt_file_list.append(file_path)
        for img,txt in zip(test_img_file_list,test_txt_file_list):
            x=random.randint(self.rotation_slider.value()[0], self.rotation_slider.value()[1])
            Rotation(img,txt,test_output,x)
            
    def img_brightness(self):
        train_output=f"{self.My_path}/{self.file_name}/data/train"
        train_path_images=f"{self.My_path}/{self.file_name}/split/train_images"
        train_path_txt=f"{self.My_path}/{self.file_name}/split/train_label"
        train_img_file_list=[]
        train_txt_file_list=[]
        for root, dirs, files in os.walk(train_path_images):
            for file in files:
                if file.endswith(".jpg"):
                    file_path = os.path.join(root, file)
                    train_img_file_list.append(file_path)
        for root, dirs, files in os.walk(  train_path_txt):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    train_txt_file_list.append(file_path)
        for img,txt in zip(train_img_file_list,train_txt_file_list):
            x=random.randint(self.brightness_slider.value()[0]-50, self.brightness_slider.value()[1]-50)
            Augmentation_bri(x,img,txt,train_output)
        
        test_output=f"{self.My_path}/{self.file_name}/data/test"
        test_path_images=f"{self.My_path}/{self.file_name}/split/test_images"
        test_path_txt=f"{self.My_path}/{self.file_name}/split/test_label"
        test_img_file_list=[]
        test_txt_file_list=[]
        for root, dirs, files in os.walk(test_path_images):
            for file in files:
                if file.endswith(".jpg"):
                    file_path = os.path.join(root, file)
                    test_img_file_list.append(file_path)
        for root, dirs, files in os.walk(  test_path_txt):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    test_txt_file_list.append(file_path)
        for img,txt in zip(test_img_file_list,test_txt_file_list):
            x=random.randint(self.brightness_slider.value()[0]-50, self.brightness_slider.value()[1]-50)
            Augmentation_bri(x,img,txt,test_output)
            
    def txt_to_txt(self):
        train=f"{self.My_path}"
    #%% train
    def Create_yaml(self):
        
        names=[self.class_name[i] for i in self.class_name]
        print(names)
        
        data={
        'train':f"{self.My_path}/{self.file_name}/data/train/images/",
        'val':f"{self.My_path}/{self.file_name}/data/test/images/",
        'names':names,
        'nc':len(names),
        'cls':0.2
        }
        yaml_data = yaml.dump(data)
        print(yaml_data)
        
        # YAML 데이터를 파일에 저장
        file_path = f"{self.My_path}/{self.file_name}/data/data.yaml"
        with open(file_path, "w") as file:
            file.write(yaml_data)
            
        with open(file_path,'w') as f:
            yaml.dump(data,f)
            
        with open(file_path,'r') as f:
            pcb_yaml=yaml.safe_load(f)
    def Model_train(self):
        model=YOLO('yolov8n.pt') # 모델 불러오기
        model.train(data=f"{self.My_path}/{self.file_name}/data/data.yaml",#yaml 경로
                epochs=100, 
                patience=10,
                batch=32,
                imgsz=416,
                pretrained=True)
    def calculation(self):
        labels_path=f"{self.My_path}/{self.file_name}/test/labels" #test label 경로
        images_path=f"{self.My_path}/{self.file_name}/test/images" #test image 경로
        model=YOLO(f'C:/work/python/project/runs/detect/train3/weights/best.pt') #모델 가져오기
        info=get_info(labels_path,images_path,model)
        truths=info.truths
        preds =info.preds

        truths_cl=info.truths_cl
        preds_cl =info.preds_cl
        score = return_score(truths,preds,truths_cl,preds_cl,0.5) # (실제,예측,iou설정값)
   
    def do_training(self):
            max_epochs = int(self.epoch_edit.value())  # 예시로 epoch_edit를 가져와서 사용하였습니다.
            for epoch in range(max_epochs):
                # 여기서 실제 학습 작업을 수행하고 epoch 진행 상황에 따라 train_pgbar 업데이트
                # 예시로 진행률을 증가시키는 코드를 작성합니다.
                progress_percent = (epoch + 1) / max_epochs * 100
                self.train_pgbar.setValue(progress_percent)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())