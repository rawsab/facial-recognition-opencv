from FaceRecognition import *
from UserManager import *



while(True):
    ans = input("1 for facial recognition, 2 for new user: ")
    if int(ans) == 1:
        runFaceRecognition()
    elif int(ans) == 2:
        addNewUser()
    else:
        break
