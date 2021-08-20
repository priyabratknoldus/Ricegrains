#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 18:45:05 2021

@author: Priyabrata Sahoo
"""
import numpy as np
from tensorflow import keras
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing import image
from tensorflow.keras.models import load_model
from PIL import Image
import cv2
import matplotlib.pyplot as plt
from countwheatgrains import  count



class ricegrains:
    def __init__(self,filename):
        self.filename =filename

# This functions helps to upload the image on the ui front and helps to convert the image to required format so that the image could be predicted
    def predictionricegrains(self):
        # load model
        model = load_model('wheatgrains20New.h5',compile=False)

        # summarize model
        #model.summary()

        imagename = '/home/knoldus/Downloads/rice-quality-analysis-master (1)/Rice-Grain-Image-Classification-master/static/inputImage.jpg'
        #imagename=self.filename
        test_image = image.load_img(imagename, target_size = (224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = model.predict_proba(test_image)
        print(result)

        # classes = ['good rice grains', 'bad rice grains']
        # label_name = {classes[i]: result[i] for i in range(len(result))}

# if result is having value greater that .8 then it will predict good rice grains or else it will predict bad rice grains
        if result[0][0] >=.5:
            Prediction = 'BROKEN GRAINS'
            return [{"image": Prediction},count(),result]
        elif result[0][1] >= 0.5:
            Prediction = 'Damaged'
            return [{"image": Prediction},count(),result]
        elif result[0][2] >= 0.5:
            Prediction = 'ForeignMatters'
            return [{"image": Prediction},count(),result]
        elif result[0][3] >= 0.5:
            Prediction = 'Healthy'
            return [{"image": Prediction},count(),result]
        elif result[0][4] >= 0.5:
            Prediction = 'IMature'
            return [{"image": Prediction},count(),result]
        elif result[0][5] >= 0.5:
            Prediction = 'Potiya'
            return [{"image": Prediction},count(),result]
        elif result[0][6] >= 0.5:
            Prediction = 'Shrivled'
            return [{"image": Prediction},count(),result]
        elif result[0][7] >= 0.5:
            Prediction = 'Weevilled'
            return [{"image": Prediction},count(),result]
        else:
            print(" Need to upload the new  wheat grain image")





