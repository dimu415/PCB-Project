![스크린샷 2023-09-02 161633](https://github.com/GoodJinMo/PCB-Project/assets/97722297/f932c8b7-6e2a-44a0-a87b-202e0b7a6559)# PCB-Project
<h2>화이팅</h2>
제조 결함 탐지 프로그램으로 다양한 제조품의 결함에 대해서 분석과 탐지를 할 수 Pyqt로 만든 프로그램입니다.

<h2>환경</h2>
언어 : python 3.11
spyder 에서 Pyqt를 이용하여 프로그램을 구현했습니다.

 <h2>테스트한 이미지</h2>
<img src="https://github.com/GoodJinMo/PCB-Project/assets/97722297/bb6b44c4-ddad-42fa-b200-48557ba732d3" width=500 hight=500>
<a href="https://www.kaggle.com/datasets/akhatova/pcb-defects">pcb-Dataset</a>




<h2>테스트한 라벨링(xml)</h2>

<img src="https://github.com/GoodJinMo/PCB-Project/assets/97722297/f5ba4382-19ed-469a-aaf0-2e4350fec7f8" width=500 hight=500>

<h2>yolov8</h2>
다른 모델에 비해 정확하고 추론성능이 좋았다.

<img src="https://github.com/GoodJinMo/PCB-Project/assets/97722297/e875f856-1cc5-472f-9f73-46158adc2229" width=500 hight=500>

<h2>성능</h2>
<b>base</b>
  <table>
    <tr>
      <th scope="col">Recall</td>
      <th scope="col">Precision</td>
      <th scope="col">F1-score</td>
    </tr>
    <tr>
      <td>0.49</td>
      <td>0.84</td>
      <td>0.61</td>
    </tr>
  </table>

  <b>image Agumentation</b>
   <table>
    <tr>
      <th scope="col">Recall</td>
      <th scope="col">Precision</td>
      <th scope="col">F1-score</td>
    </tr>
    <tr>
      <td>0.73</td>
      <td>0.89</td>
      <td>0.81</td>
    </tr>
  </table>

  <b>last score</b>

  <table>
    <tr>
      <th scope="col">Recall</td>
      <th scope="col">Precision</td>
      <th scope="col">F1-score</td>
    </tr>
    <tr>
      <td>0.9</td>
      <td>0.94</td>
      <td>0.92</td>
    </tr>
  </table>



<h2>앱 구현</h2>

<img src="https://github.com/GoodJinMo/PCB-Project/assets/97722297/14861cc2-5edd-4f8c-a500-aed06770efb1" width=200 hight=200>

<img src="https://github.com/GoodJinMo/PCB-Project/assets/97722297/64c86225-6267-4393-bb8a-26d62dbeab85" width=200 hight=200>

<img src="https://github.com/GoodJinMo/PCB-Project/assets/97722297/cc0b5d24-3f03-45be-ab86-b8e9c348bae6" width=200 hight=200>

<img src="https://github.com/GoodJinMo/PCB-Project/assets/97722297/c3070156-578e-4712-a349-f95374aad554" width=200 hight=200>

<img src="https://github.com/GoodJinMo/PCB-Project/assets/97722297/cb6e7220-1c3f-4c82-9479-e6b814295aad" width=200 hight=200>

<img src="https://github.com/GoodJinMo/PCB-Project/assets/97722297/dc42c759-151d-42fe-ab5b-da8ec062723f" width=200 hight=200>

1.upload 

   -  이미지 파일을 불러와 제대로 불러왔는지 확인합니다.

2. labeling
   
    - xml 형태에 라벨링 정보값을 불러와 txt로 변환과정을 거칩니다.
      
    - 이미지 사진에 불러온 라벨링정보를 토대로 박스 바운딩을 합니다
      
    - 무슨 클래스가 있는지와 제대로 정보가 기입되어있는지 육안으로 확인할 수 있습니다.
3. spllit
   
    - 원하는 비율에 맞게 클래스와 총 파일 수가 나눠집니다

4. augmention
   
    - 부족한 데이터를 늘리기 위해 이미지 증강하는 부분입니다.
      
    - 밝기,이미지크기,회전,상하 반전, 좌우 반전 을 원하는 비율에 맞게 설정할 수 있습니다.
  
5. tra5in
   
    - 우리는 yolov8을 이용하여 학습을 시도합니다.
      
    - 원하는 값을 주워 학습을 진행합니다.
      
    - 실시간으로 손실값을 확인하실 수 있습니다.(예정)
      
6.analysis

   - 학습한 모델을 가지고 분석을 시도합니다.
     
   - 이미지에 결합을 잘 찾아내는지 육안으로 확인이 가능하며
     
   - recall,precision,F1-score 표시됩니다.
   
  
