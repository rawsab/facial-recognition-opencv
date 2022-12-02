import cv2
import numpy as np
import os
import time
from picamera2 import Picamera2
import face_recognition
import imutils
import pickle
import espeakng
from Logger import *
from datetime import datetime

# pass a cv2 image and encodings to compare to
def facialRecognitionLoop(frame, speaker, knownEncodings):
        currentname = "Unknown"

        # finds faces in frame
        boxes = face_recognition.face_locations(frame)
        # computes embeddings of frame
        tempEncodings = face_recognition.face_encodings(frame, boxes)
        names = []

        # loop over the new embeddings and compare to our knowns
        for tempEncoding in tempEncodings:
            # attempt to match each face in the input image to our known encodings
            for knownEncoding in knownEncodings:
                matches = face_recognition.compare_faces(knownEncoding["encodings"], tempEncoding)
                name = "Unknown" #if face is not recognized, then print Unknown

                # check to see if we have found a match
                if True in matches:
                    # finds count of recognized faces
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}
                    for i in matchedIdxs:
                        name = knownEncoding["name"]
                        counts[name] = counts.get(name, 0) + 1

                    # finds the name of the face with the most matches
                    name = max(counts, key=counts.get)

                    # if someone in the dataset is identified, print their name on the screen
                    if currentname != name:
                        currentname = name
                        print(currentname)
                        speaker.say("Welcome " + currentname)
                        logAuthUser(currentname)
                        noticed = True
                    # if a user is not recognised, save photo of them and write new unauthorised user log
                    else:     
                        img_name = user_dir + "/unrecognised_{}.jpg".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        cv2.imwrite(img_name, frame)
                        print("{} written!".format(img_name))
                        

                # update the list of names
                if name != 'Unknown':
                    names.append(name)
        return (boxes, names)

# use if you want to run it independently
def runFaceRecognition():
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    cam.set(cv2.CAP_PROP_FPS, 30)

    speaker = espeakng.Speaker()
    print("[INFO] Initializing camera...")

    exitLoop = False

    
    print("[INFO] Loading encodings + face detector...")
    filePaths = os.listdir("/home/daniel/CosRX/FaceRecognition/CurrentVersion")
    knownEncodings = []
    
    for  filePath in filePaths:
        if filePath.endswith('.pickle'):
            data = pickle.loads(open(filePath, "rb").read())
            knownEncodings.append(data)

    exitLoop = False

    # loop over frames from the video stream -- remove or True for single execution
    while not exitLoop or True:
        ret, frame = cam.read()
        if not ret:
            print("\n[ERROR] Unable to receive frames. Exiting...")
            break
        exitLoop = facialRecognitionLoop(frame, speaker, knownEncodings)
    # cleanup
    cam.release()
    cv2.destroyAllWindows()