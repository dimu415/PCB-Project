import streamlit as st
import os
from PIL import Image

class MyApp:
    def __init__(self):
        categories=['a','b','c']
        selected_category = st.sidebar.radio("", ["Upload", "Label", "Split", "Train", "Analyze"])
        selected_categories = st.sidebar.multiselect("카테고리 선택", categories)
            # 각 카테고리에 따라 내용 출력

        for category in selected_categories:
            st.write(f"- {category}")
        if selected_category == "Upload":
                self.Upload()
        elif selected_category == "Label":
                self.Label_work()
        elif selected_category == "Split":
                self.split()
        elif selected_category == "Train":
                self.train()
        elif selected_category == "Analyze":
                st.write("Analyze 카테고리 내용을 여기에 표시")
#%% Upload        
    def Upload(self):
        
        if st.button("파일 선택"):
            
            file_path = self.file_dialog()
            if file_path:
                st.write(f"선택한 파일 경로: {file_path}")
            else:
                st.write("파일을 선택하지 않았습니다.")
                
        
        
        box_style = (
     "border: 2px dotted gray; padding: 300px; background-color: transparent;"
 )

        box_container = st.container()
        
        box_container.markdown(f'<div style="{box_style}">', unsafe_allow_html=True)
        
        
           # 경계선 닫기
        box_container.markdown("</div>", unsafe_allow_html=True)


    
        # 나중에 이미지 추가 # 이미지 파일의 경로
       
    def file_dialog(self):
        file_path = st.file_uploader("파일 선택", type=["jpg", "jpeg", "png"], key="file_uploader")
        return file_path
        
    

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

#%%
    def split(self):
        col1, empty,col2= st.columns([2,3,2])
        box_style = (
     "border: 2px dotted gray; padding: 10px; background-color: transparent;"
 )
        
        with col1:
            st.write("file name")
            self.slider_value = st.slider("슬라이더", min_value=0, max_value=100, value=50,
                                          format="%s", key="custom_slider")
            st.write(self.slider_value)
        with col2:
            

            st.container()
            
            st.markdown(f'<div style="{box_style}">'
                                f'<h3>train_val</h3>'
                                f'<p style="margin-top: 0;">train:81% </p>'
                                f'<p style="margin-top: 0;">val:19%</p>'
                                f'</div>', unsafe_allow_html=True)
                    
            
            
        with col2:
            st.write("clss:80% , 20%")
            st.write("clss:79% , 21%")
            st.write("clss:82% , 18%")
       
            
#%%
    def train(self):
        
        a="asd"
        
            # 첫 번째 박스 생성
        with st.expander("첫 번째 박스"):
            model=st.button("yolo")
            if model:
                a="yolo"
            st.write(a)
    
            # 두 번째 박스 생성
        with st.expander("두 번째 박스"):
            st.write("두 번째 박스 내용")
            
        st.button("학습 시작")
        
    
#%%
if __name__ == "__main__":
    MyApp()