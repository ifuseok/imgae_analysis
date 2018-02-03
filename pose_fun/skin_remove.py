import cv2

import numpy as np
import os
import sys
os.sys.path.append("C:/Users\LeeWonSeok\주피터 파일")
import scripts
import skin_detector

class Skin:

    def __init__(self,img_dict,rec_dict,):
        assert isinstance(img_dict,dict), "image variable must be dict"
        assert isinstance(rec_dict, dict), "rectangle position variable must be dict"
        self.img_dict = img_dict
        self.rec_dict = rec_dict

    def remove(self):
        img = self.img_dict.copy()
        rec = self.rec_dict.copy()
        self.new_list = {}

        for key in rec:
            x1,y1 = rec[key][0]
            x2,y2 = rec[key][1]
            img_copy = img[key[0]].copy()
            a,b,c = img[key[0]][y1:y2,x1:x2].shape
            mask = skin_detector.process(img_copy[y1:y2,x1:x2])
            img_copy[y1:y2,x1:x2] = cv2.bitwise_and(img_copy[y1:y2,x1:x2],img_copy[y1:y2,x1:x2],mask=~mask)

            """
            for k in range(c):
                for i in range(a):
                    for j in range(b):
                        if mask[i,j] != 0:
                            img_copy[i,j,k]=0
            """
            self.new_list.update({key:img_copy})
        return self.new_list

    def write(self,path):
        for key in self.new_list:
            a,b=key
            c = str(a)+"_" + str(b)
            cv2.imwrite(os.path.join(path,c+".png"),self.new_list[key])
