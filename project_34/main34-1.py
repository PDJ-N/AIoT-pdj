import cv2  # OpenCV 영상 처리를 위한 라이브러리 불러오기
from gpiozero import Buzzer  # 라즈베리파이 GPIO 핀에 연결된 부저를 제어하기 위한 클래스 불러오기
import time  # 시간 관련 기능을 사용하기 위한 라이브러리 불러오기

buzzerPin = Buzzer(16)  # GPIO 16번 핀에 연결된 능동부저 객체 생성

def main():
    camera = cv2.VideoCapture(-1)  # 연결된 웹캠을 자동으로 탐지하여 열기
    camera.set(3,640)  # 카메라 가로 해상도를 640픽셀로 설정
    camera.set(4,480)  # 카메라 세로 해상도를 480픽셀로 설정
    
    face_xml = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'  # 정면 얼굴 탐지 모델 경로 지정
    eye_xml = cv2.data.haarcascades + 'haarcascade_eye.xml'  # 눈 탐지 모델 경로 지정
    face_cascade = cv2.CascadeClassifier(face_xml)  # 얼굴 탐지 분류기 객체 생성
    eye_cascade = cv2.CascadeClassifier(eye_xml)  # 눈 탐지 분류기 객체 생성
    
    while( camera.isOpened() ):  # 카메라가 정상적으로 열려 있는 동안 반복
        _, image = camera.read()  # 카메라에서 현재 프레임 한 장을 읽어오기
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 얼굴과 눈 탐지를 위해 컬러 영상을 흑백 영상으로 변환

        faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(100,100),flags=cv2.CASCADE_SCALE_IMAGE)  # 흑백 영상에서 얼굴 영역 탐지
        print("faces detected Number: " + str(len(faces)))  # 현재 프레임에서 탐지된 얼굴 수 출력

        if len(faces):  # 얼굴이 1개 이상 탐지되었을 때
            for (x,y,w,h) in faces:  # 탐지된 얼굴 영역의 좌표를 하나씩 가져오기
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)  # 얼굴 위치에 파란색 사각형 표시
                
                face_gray = gray[y:y+h, x:x+w]  # 눈 탐지를 위해 얼굴 영역의 흑백 영상만 추출
                face_color = image[y:y+h, x:x+w]  # 눈 위치를 표시하기 위해 얼굴 영역의 컬러 영상만 추출
                
                eyes = eye_cascade.detectMultiScale(face_gray,scaleFactor=1.1,minNeighbors=5)  # 얼굴 영역 안에서 눈 탐지
                
                if len(eyes) <= 1:  # 눈이 1개 이하로 감지되면 졸음 상태로 판단
                    buzzerPin.on()  # 능동부저를 켜서 경보음 출력
                else:  # 눈이 2개 이상 감지되면 정상 상태로 판단
                    buzzerPin.off()  # 능동부저 끄기
                
                for (ex,ey,ew,eh) in eyes:  # 탐지된 눈 영역의 좌표를 하나씩 가져오기
                    cv2.rectangle(face_color, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)  # 눈 위치에 초록색 사각형 표시
        
        cv2.imshow('result', image)  # 얼굴과 눈 탐지 결과를 GUI 창에 출력
        
        if cv2.waitKey(1) == ord('q'):  # q 키를 누르면 반복문 종료
            break
    
    cv2.destroyAllWindows()  # 열려 있는 OpenCV 창 모두 닫기
    buzzerPin.off()  # 프로그램 종료 시 부저가 계속 울리지 않도록 강제로 끄기

if __name__ == '__main__':
    main()  # 이 파일을 직접 실행할 때 main 함수 호출

# 이 코드는 OpenCV로 웹캠 영상에서 얼굴과 눈을 탐지한 뒤,
# 눈이 1개 이하로 감지되면 졸음 상태로 판단하여 GPIO 16번 핀의 능동부저를 울리는 예제입니다.
# 웹캠 번호와 부저 GPIO 핀 번호는 실제 연결 환경에 맞게 조정해야 합니다.
