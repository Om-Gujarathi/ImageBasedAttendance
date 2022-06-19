import cv2
import numpy as np
import face_recognition
import os
from sheets import mark_attendance
import keyboard

path = 'imagesAttendance'
images = []
classnames = []

myList = os.listdir(path)
print(myList)

for stu in myList:
    curImg = cv2.imread(f'{path}/{stu}')
    images.append(curImg)
    classnames.append(os.path.splitext(stu)[0])

print(classnames)

attendance = ["Absent"] * len(classnames)


def findencodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodeList.append(face_recognition.face_encodings(img)[0])
    return encodeList


encodeKnown = findencodings(images)
print("Encoding Complete!")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

check = "Continue"

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceLocCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceLocCurFrame):
        matches = face_recognition.compare_faces(encodeKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            attendance[matchIndex] = "Present"
            name = classnames[matchIndex]
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

    cv2.imshow("WebCam", img)
    print(attendance)
    cv2.waitKey(10)

    if keyboard.is_pressed('x'):
        break

cap.release()
cv2.destroyAllWindows()
print(attendance)

mark_attendance(attendance)

print("Task Completed Sucessfully")
