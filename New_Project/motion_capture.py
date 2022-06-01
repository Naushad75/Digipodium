import cv2
import os
from cvzone.PoseModule import PoseDetector
from Database import Base, create_engine, Capture
from sqlalchemy.orm import sessionmaker



def motion_capture():
    cap = cv2.VideoCapture(0)

    detector = PoseDetector()
    posList = []
    while True:
        _, img = cap.read()
        img = detector.findPose(img)
        lmList, bboxInfo = detector.findPosition(img)

        if bboxInfo:
            lmString = ''
            for lm in lmList:
                lmString += f'{lm[1]},{img.shape[0]-lm[2]},{lm[3]},'

            posList.append(lmString)
        
        cv2.putText(img, "Press 's' to save the recording",(10,60),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
        cv2.imshow('Image', img)
        key = cv2.waitKey(1)
        if key == ord('s'):
            save_motion(posList,"webcam")
        if key == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()

def motion_capture_video(videofile):
    cap = cv2.VideoCapture(videofile)
    filename = os.path.basename(videofile)
    name,ext = os.path.splitext(filename)
    detector = PoseDetector()
    posList = []
    while True:
        success, img = cap.read()
        if not success:
            save_motion(posList,name)
            break
        img = detector.findPose(img)
        lmList, bboxInfo = detector.findPosition(img)

        if bboxInfo:
            lmString = ''
            for lm in lmList:
                lmString += f'{lm[1]},{img.shape[0]-lm[2]},{lm[3]},'

            posList.append(lmString)
        print(len(posList))
        cv2.putText(img, "Press 's' to save the recording",(10,60),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
        cv2.imshow('Image', img)
        key = cv2.waitKey(1)
        if key == ord('s'):
            save_motion(posList,name)
            break
        if key == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()

def save_motion(posList,name):
    if not os.path.exists("motion_data"):
        os.mkdir("motion_data")
    filename = f"motion_data/{name}_capture.txt"
    with open(filename,'w') as f:
        f.writelines(["%s\n" % item for item in posList])
        db = open_db()
        c = Capture(filename=filename)
        db.add(c)
        db.commit()
        db.close()

def open_db():
    engine = create_engine('sqlite:///animation.sqlite3')
    Session = sessionmaker(bind=engine)
    sess = Session()
    return sess

if __name__ == "__main__":
    motion_capture()