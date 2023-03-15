# 🖥️ SE101 Project (Team: COSRX)

<img src="https://user-images.githubusercontent.com/45187177/214395225-df2ae1b8-75a9-4170-8828-cd1ff3026ab4.png" alt="SE101 Project Banner" width="1015"/>

![rpos_version](https://img.shields.io/badge/Raspberry%20Pi%20OS-5.15-red.svg)
![python](https://img.shields.io/badge/Python-3.11-blue.svg)

👥 Hudson K, Arjun W, Daniel M, and Rawsab S

## ⚙️ Requirements

> See InitialiseDB for instructions on how to set up database.


Install required libraries:
```
sudo apt-get install build-essential \
    cmake \
    gfortran \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    liblapack-dev \
    libatlas3-base \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy

sudo apt-get clean

sudo apt-get install libopenblas-dev
```

Install the **dlib Python library**:
```
sudo pip3 install dlib
```

Install the **Python face recognition library** (https://github.com/ageitgey/face_recognition):
```
sudo pip3 install --no-cache-dir face_recognition
```

Install the **imutils Python library**:
```
pip install imutils
```

Create **a "dataset" folder** before running any of the Python files.

## 📸 Capturing user images
Open the UserManager.py file and change the variable "name" to the name of the user. Create a folder under "datasets" with the same name.
Run the UserManager.py file and press space to take a photo. Take about 10 photos of each user.

