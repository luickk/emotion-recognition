import csv
import os
import glob
import numpy as np
import dlib
import pickle
import cv2
import sys
from imutils import face_utils
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from utils.data import *


def main():
    dataSetDir = 'data/MPI_selected/**'
    files_chunk_size = 60
    i = 0
    c = 0
    x = []
    y = []

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')
    
    classes = getClassesForDataSet(dataSetDir)

    print("classes exracted: ")
    print(classes)

    for filename in glob.iglob(dataSetDir, recursive=True):
        if os.path.isfile(filename): # filter dirs
            completeClass = filename.split('/')[3]
            img = cv2.imread(filename, cv2.IMREAD_COLOR)
            img = detect_face(img, detector, predictor)
            if type(img) is np.ndarray:
                i += 1
                img = cv2.resize(img, (256, 256))
                y.append(str(completeClass))
                x.append(img)
            else:
                print('Did not find any faces!')

            if i >= files_chunk_size:
                c += 1
                y = np.array(y)
                x = np.array(x)
                
                x_final, y_final = label_categorisation(x, y, classes)

                file_loc = 'data/raw_MPI_selected/'+str(c)+'.npy'
                if not x_final.shape[0] <= 1:

                    data = np.array([[x_final], y_final])

                    np.save(file_loc, data)

                    print('Saved to', file_loc)

                i = 0
                x = []
                y = []

def detect_face(img, detector, predictor):
    rects = detector(img, 0)
    roi_color = []
    for (i, rect) in enumerate(rects):
        shape = predictor(img, rect)
        shape = face_utils.shape_to_np(shape)

        (x, y, w, h) = face_utils.rect_to_bb(rect)

        roi_color = img[y:y+h, x:x+w]

    return roi_color

if __name__ == '__main__':
    main()
