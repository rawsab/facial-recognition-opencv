import os
import cv2
from picamera2 import Picamera2
import numpy as np
from PIL import Image
import face_recognition
import pickle
from imutils import paths
from Logger import *

def trainAllUsers():
    imagePaths = list(paths.list_images("dataset"))

    # initialize the list of known encodings and known names
    knownEncodings = []
    knownNames = []

    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        print("Image path: " + imagePath);
        # extract the person name from the image path
        print("[INFO] processing image {}/{}".format(i + 1,
            len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]

        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB)
        print(imagePath)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb,
            model="hog")

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            knownEncodings.append(encoding)
            knownNames.append(name)

    # dump the facial encodings + names to disk
    print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open("encodings.pickle", "wb")
    f.write(pickle.dumps(data))
    f.close()

def trainUser(name):
    imagePaths = os.listdir("dataset/" + name)

    knownEncodings = []


    for  imagePath in imagePaths:
        imagePath = 'dataset/'+name +'/'+imagePath
        print(imagePath)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb,
            model="hog")

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            knownEncodings.append(encoding)
            
        print("[INFO] serializing encodings...")
        data = {"encodings": knownEncodings, "name": name}
        f = open(name+"_encodings.pickle", "wb")
        f.write(pickle.dumps(data))
        f.close()

# Use this to add new user
def addNewUser(name):
    USERS_DIR = "dataset/"
    user_id = input("Enter user name and press <return> ")
    userDir = USERS_DIR+user_id.strip()
    # Create user folder if it does not exist
    MAX_CAPTURES = 30
    if not os.path.exists(userDir):
        os.makedirs(userDir)
        takePhotos(name,userDir, MAX_CAPTURES)
    else:
        print("User already exists.")


def removeUser(name):
    removeAuthUser(name)
    os.remove(name+'_encodings.pickle')
    for image in os.listdir('dataset/'+name):
        os.remove('dataset/'+name + '/' + image)
    os.rmdir('dataset/'+name)

def takePhotos(name,user_dir, maxCaptures):
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    cam.set(cv2.CAP_PROP_FPS, 30)

    img_counter = 0;
    while img_counter<=maxCaptures:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("press space to take a photo", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = user_dir + "/image_{}.jpg".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
    
    newAuthUser(name, user_dir)
    
    cam.release()
    cv2.destroyAllWindows()
    trainUser(name);
