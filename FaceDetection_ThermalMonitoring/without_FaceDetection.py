import cv2
import face_detection.face_detection as face_detection
import pytesseract
from multiprocessing import Process
import socket
import time


def get_my_ip_address(remote_server="google.com"):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((remote_server, 80))
        return s.getsockname()[0]


pytesseract.pytesseract.tesseract_cmd = r'D:\Programs\tesseract.exe'


def Video():
    # face_detector = face_detection.FaceDetector()
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    while not cap.isOpened():
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        cv2.waitKey(1000)
    while True:
        flag, frame = cap.read()
        # custom_config = r'--oem 3 --psm 6'
        sub_image = frame[5:25, 30: 78]
        text = pytesseract.image_to_string(sub_image, config='--psm 10 --oem 3 -c tessedit_char_whitelist=.0123456789')
        temp = str(text[0:4])
        if flag:
            f = open("data.txt", "w")
            str1 = "conf :" + "No" + ": temp :" + str(temp)
            f.write(str1)
            f.close()
            print("Human Detected with confidence : ", "No", ": Body Temp : ", temp)
            cv2.imshow('camera_feed', frame)
        else:
            cv2.waitKey(1000)
        k = cv2.waitKey(5)
        if k == 27:
            break
        time.sleep(.3)
    cv2.destroyAllWindows()


def share():
    tcpServerSocket = socket.socket()
    hostip = get_my_ip_address()
    print("IP Address : ", get_my_ip_address())
    port = 12345
    tcpServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServerSocket.bind((hostip, port))
    print(tcpServerSocket.getsockname())
    tcpServerSocket.listen(5)
    while True:
        print("Waiting for connection")
        clientSocket, addr = tcpServerSocket.accept()
        print('Connection address:', addr)
        f = open("data.txt", "r")
        str2 = 'Message from the server! ' + f.read() + "\n"
        clientSocket.send(str2.encode())
        clientSocket.close()
    tcpServerSocket.close()


if __name__ == "__main__":
    p1 = Process(target=Video)
    p1.start()
    p2 = Process(target=share)
    p2.start()
    p1.join()
    p2.join()
