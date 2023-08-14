import streamlit as st
import os
from PIL import Image
import pandas as pd
class MyApp:
    def __init__(self):
        
        
        
            # 각 카테고리에 따라 내용 출력
        self.logged=False
        st.write(self.logged)
        if self.logged==False:
            self.login()
            
        else:
            selected_category = st.sidebar.radio("", ["login","Upload", "Label", "Split", "Train", "Analyze"])
            #selected_categories = st.sidebar.multiselect("카테고리 선택", categories)
            #for category in selected_categories:
                #st.write(f"- {category}")
                
            if selected_category == "login":
                    self.login()    
            elif selected_category == "Upload":
                    self.Upload()
            elif selected_category == "Label":
                    self.Label_work()
            elif selected_category == "Split":
                    self.split()
            elif selected_category == "Train":
                    self.train()
            elif selected_category == "Analyze":
                    st.write("Analyze 카테고리 내용을 여기에 표시")
        
        self.path=""
        
#%% login
    def login(self):
        user_id = st.text_input("아이디", type='password')
        user_pass = st.text_input("비밀번호", type='password')
        if user_id == "user" and user_pass == "4321":
            self.logged = True
            st.write("aa")
        else:
            self.logged=False
       
        
# %% Upload        
    def Upload(self):
        
        file = st.file_uploader("파일을 선택하세요")
    
    # 파일이 선택되었을 경우에만 파일 경로를 표시합니다.
        if file is not None:
            file_name = file.name
            st.write("선택된 파일 경로:", file_name[:-4])
            
            self.path=os.path.abspath(file_name)
            st.write(self.path)
    
        
    

#%% label
    def Label_work(self):
        
        
        
        image_folder = "C:/Users/lg/Desktop/work/images"
        image_files = self.get_image_files(image_folder)
        if not image_files:
            st.write("이미지 파일이 없습니다.")
        else:
            selected_index = st.session_state.get("selected_indx", 0)
    
            # 이미지 표시
            col1, col2, col3, col4 = st.columns([1, 10, 1,5])
            with col2:
                st.write("")
                st.write("")
                st.image(image_files[selected_index], use_column_width=True, caption=image_files[selected_index])
    
            # 화살표 표시 및 이동 처리
            with col1:
                if st.button("←", key="prev_button"):
                    if selected_index > 0:
                        selected_index -= 1
    
            with col3:
                if st.button("→", key="next_button"):
                    if selected_index < len(image_files) - 1:
                        selected_index += 1
                        
            with col4:
                st.title("")
            with col4:
                st.title("class")
                st.markdown(f'<div style="color: red;">Missing_hole</div>', unsafe_allow_html=True)
                st.markdown('<div style="color: green;">Mouse_bite</div>', unsafe_allow_html=True)
                
        
            # 세 번째 열: 박스 2
            with col2:
                name="이름:"+image_files[selected_index].split("/")[-1][:-4]
                
                width="너비:"+"2000"
    
                hight="높이:"+"3048"
                st.markdown(
                f"""
                <div style="border: 2px solid gray; padding: 10px;">
                    <h3>info</h3>
                    <p>{name}</p>
                    <p>{width}</p>
                    <p>{hight}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
                
    
            st.session_state.selected_index = selected_index

    

    def get_image_files(self,folder_path):
        image_extensions = [".jpg", ".jpeg", ".png", ".gif"]
        image_files = [folder_path+"/"+ file for file in os.listdir(folder_path) if any(file.lower().endswith(ext) for ext in image_extensions)]
        return image_files

#%% split
    def split(self):
        col1, col2,col3,col4 =st.columns([1,1,2,1])
        box_style = (
     "border: 2px dotted gray; padding: 10px; background-color: transparent;"
 )
        self.slider_value=0
        with col1:
            st.write("")
            st.write("")
            st.write("file name")
        with col3:
            self.slider_value = st.slider("", min_value=0, max_value=100, value=50,
                                          format="%s", key="custom_slider")
            
            
        with col2:
            st.write("")
            st.write("")
            st.write(f"train:{self.slider_value}% val:{100-self.slider_value}")
            
            
            
        with col4:
            st.write("")
            st.write("")
            split_button= st.button("yolo")
            
        if split_button:
            st.success("휘리릭 뽕")
            st.write("train:81%     val:81%")
            
            indexs=["test", "missing", "bite", "hole"]
            val=[100, 80, 79, 88]
            test= [0, 20, 31, 12]
            
            data = {
                "val": val,
                "test": test
            }
            
            
            df = pd.DataFrame(data,index=indexs)
            st.dataframe(df,height=600,width=800)
           
    def train(self):
        
        a="asd"
        
            # 첫 번째 박스 생성
        with st.expander("모델 선택"):
            model_selected = st.checkbox("yolo")
            if model_selected:
                st.success("Yolo 모델이 선택되었습니다.")
    
            # 두 번째 박스 생성
        with st.expander("학습할 파일 선택"):
            model_selected = st.checkbox("PCB")
            if model_selected:
                st.success("PCB  선택되었습니다.")
            
        with st.expander("옵션 입력"):
            
            col1,col2,col3=st.columns([1,1,1])
            with col1:
                input_ecpho = st.text_input("ecpho")
            with col2:
                input_cls = st.text_input("cls")
            with col3:
                input_size = st.text_input("size")
            
        if st.button("학습 시작"):
            st.write("학습을 시작했습니다.")
            
            st.success("~~에서 확인 해주세요.")
        
    
#%%
if __name__ == "__main__":
    MyApp()
    
