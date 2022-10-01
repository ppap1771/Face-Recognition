import cv2
import numpy as np
import face_recognition
import os
import sys


def searchName(name):
    with open('encode.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name in nameList:
            return True
        else:
            return False


def fetchEncoding(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def enterUser(name, registered, id):
    with open('encode.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            f.writelines(f'\n{name},{registered},{id}')


def confirmReg(name):
    with open('encode.csv', 'r') as f:
        myDataList = f.readlines()
        flag = 0
        for line in myDataList:
            entry = line.split(',')
            if entry[0] == name:
                flag = 1
                break
            else:
                flag = 0
        if flag == 1:
            return True
        else:
            return False


def compareEncodings(image):
    small_image = cv2.cvtColor(cv2.resize(image, (0, 0), None, 0.25, 0.25), cv2.COLOR_BGR2RGB)

    face = face_recognition.face_locations(small_image)
    encode = face_recognition.face_encodings(small_image, face)

    match = face_recognition.compare_faces(encodingComp, encode[0])
    face_dis = face_recognition.face_distance(encodingComp, encode[0])
    match_index = np.argmin(face_dis)

    if match[match_index]:
        print("[!] The user is registered under another name.")
        return True
    else:
        return False


if __name__ == '__main__':
    try:
        path = './auth_face'
        images = []
        classNames = []
        myList = os.listdir(path)

        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])

        encodingComp = fetchEncoding(images)
        nameAuth = input('[:] Enter your name > ')
        IDAuth = input('[:] Enter your ID > ')

        cap = cv2.VideoCapture(0)

        if searchName(nameAuth):
            try:
                while True:
                    success, img = cap.read()
                    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

                    facesCurFrame = face_recognition.face_locations(imgS)
                    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

                    flag = 1
                    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                        try:
                            matches = face_recognition.compare_faces(encodingComp, encodeFace)
                            faceDis = face_recognition.face_distance(encodingComp, encodeFace)
                            matchIndex = np.argmin(faceDis)
                            if matches[matchIndex]:
                                print("[+] Identified as " + nameAuth)
                                y1, x2, y2, x1 = faceLoc
                                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                                cv2.putText(img, 'Identity confirmed: ', (50, 30), cv2.FONT_HERSHEY_COMPLEX, 1,
                                            (255, 0, 0),
                                            2)
                                cv2.putText(img, nameAuth, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1,
                                            (255, 255, 255),
                                            2)
                                flag = 1
                            else:
                                cv2.putText(img, 'Identity could not be confirmed! ', (50, 30),
                                            cv2.FONT_HERSHEY_COMPLEX, 1,
                                            (255, 0, 0), 2)
                                flag = 0

                        except Exception as e:
                            print(f"[-] ERROR: {e}")
                            sys.exit(0)

                    if flag == 0:
                        break

                    cv2.imshow('Webcam', img)
                    cv2.waitKey(5)

            except Exception as e:

                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                sys.exit(0)

               
        else:
            try:
                while True:
                    success, img = cap.read()
                    if not success:
                        print("Camera didnot open :(")
                    cv2.putText(img, "Press C to capture your image", (50, 30), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (255, 0, 0), 1)
                    cv2.imshow('Webcam', img)
                    
                    if cv2.waitKey(10) & 0xFF == ord('c'):
                        break

                del cap
                if not classNames:
                    cv2.imwrite(r'./auth_face/' + nameAuth+ "_" + IDAuth + '.png', img)
                    enterUser(nameAuth, True, IDAuth)
                else:
                    if not compareEncodings(img):
                        cv2.imwrite(r'./auth_face/' + nameAuth+ "_" + IDAuth + '.png', img)
                        enterUser(nameAuth, True, IDAuth)

                if confirmReg(nameAuth):
                    print("[+] User registered successfully !!")
                else:
                    print("[-] User could not be registered !!")

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                sys.exit(0)

    except Exception as e:
        print(f"[-] ERROR: {e}")
        sys.exit(0)
