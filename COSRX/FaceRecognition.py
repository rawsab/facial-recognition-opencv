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

def getNames():
    temp = []
    with open(r'Names.txt', 'r') as fp:
        for line in fp:
            x = line[:-1]
            temp.append(x)
    return temp


def addName(name):
    names = getNames()
    names.append(name)
    with open(r'Names.txt', 'w') as fp:
        for n in names:
            fp.write("%s\n" % n)

def runFaceRecognition():
    speaker = espeakng.Speaker()
    print("[INFO] Initializing camera...")
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    cam.set(cv2.CAP_PROP_FPS, 30)
    exitLoop = False

    
    print("[INFO] Loading encodings + face detector...")
    filePaths = os.listdir("/home/daniel/NewCosRX/facial-recognition")
    knownEncodings = []
    
    for  filePath in filePaths:
        if filePath.endswith('.pickle'):
            data = pickle.loads(open(filePath, "rb").read())
            knownEncodings.append(data)

    exitLoop = False

    # loop over frames from the video stream -- remove or True for single execution
    while not exitLoop or True:
        currentname = "Unknown"
        
        # grab the frame from the threaded video stream
        ret, frame = cam.read()
        if not ret:
            print("\n[ERROR] Unable to receive frames. Exiting...")
            break

        # resize the frame to 320px (to speedup processing)
        # detect the face boxes
        # compute the facial embeddings for each face bounding box
        frame = imutils.resize(frame, width=320)
        boxes = face_recognition.face_locations(frame)
        tempEncodings = face_recognition.face_encodings(frame, boxes)
        names = []

        for tempEncoding in tempEncodings:
            # attempt to match each face in the input image to our known encodings
            for knownEncoding in knownEncodings:
                matches = face_recognition.compare_faces(knownEncoding["encodings"], tempEncoding)
                name = "Unknown" #if face is not recognized, then print Unknown

                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name = knownEncoding["name"]
                        counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    name = max(counts, key=counts.get)

                    # if someone in the dataset is identified, print their name on the screen
                    if currentname != name:
                        currentname = name
                        print(currentname)
                        logAuthUser(name)
                        exitLoop = True

                # update the list of names
                names.append(name)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # draw the predicted face name on the image - color is in BGR
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 255), 2)

        # display the image to our screen
        cv2.imshow("Facial Recognition is Running", frame)
        key = cv2.waitKey(1) & 0xFF

        # quit when 'esc' key is pressed
        if key == 27:
            break
        
    if exitLoop == True:
        speaker.say("Welcome " + currentname)
        time.sleep(3)

    # cleanup
    cam.release()
    cv2.destroyAllWindows()

