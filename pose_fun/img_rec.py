import numpy as np
from math import sqrt
import cv2
import os

def case_classify(per_dict):
    case1 = dict()
    case2 = dict()
    case3 = dict()
    for key,values in per_dict.items():
        for index,value in enumerate(values):
            left = (value[8] != (0, 0))
            right = (value[11] != (0, 0))
            total = left or right
            if total == True:  # 골반이 하나있다면
                new_key = (key, index)
                case1.update({new_key: value})
            else:
                le = (value[2]==(0,0))
                ri = (value[5]==(0,0))
                new_key = (key, index)
                if (le or ri) == True:
                    case3.update({new_key: value})
                else:
                    case2.update({new_key: value})
    return case1,case2,case3

def dist(a,b) :
    x1,y1 = a
    x2,y2 = b
    d1 = (x1-x2)**2 + (y1-y2)**2
    d2 =sqrt(d1)
    return d2

def find_rectangle(img,case,metric) :
    assert isinstance(case,dict) , "cas Must be dictionary"
    assert isinstance(img, dict), "img Must be dictionary"
    case_rec = {}
    for key,values in case.items():
            # 사각형 윗 꼭지점 두개 구하기
        d = dist(values[2],values[5])
        d_2 = int(d/3)
        d_10 = int(d/1.2)
        x_l,y_l = values[2]
        x_r, y_r = values[5]
        y_sh = np.array([y_l,y_r]).min() - d_2 # 어깨 Y 좌표 키우기
        x_l = x_l - d_10
        x_r = x_r + d_10
        dd = abs(x_l-x_r)
        key_img = key[0]
        # 골반 부분과의 차이
        if metric == "perfect":
            down_posit = []
            down_posit.append(values[8])
            down_posit.append(values[11])
            down_posit = [x for x in down_posit if x != (0, 0)]
            down_posit.sort(key=lambda position: position[1], reverse=True)
            down_y = down_posit[0][1]
        if metric == "else":
            down_y = int(img[key_img].shape[0] * 0.9)
        h = int(abs(y_sh - down_y) * 1.3) # 사각형 높이
        x_l_dd = x_l + dd
        y_sh_h = y_sh + h
        if x_l_dd > img[key_img].shape[1] :
            x_l_dd = img[key_img].shape[1] -1 # x범위 밖일 경우
        if x_l < 0 : x_l = 0 #왼쪽 어깨좌표가 0보다 작아질 경우
        if y_sh_h > img[key_img].shape[0] :
            y_sh_h = img[key_img].shape[0] - 1
        case_rec.update({key : [(x_l,y_sh),(x_l_dd,y_sh_h)]})
    return case_rec


def show_rectengle(img_dict,case_rec,paths):
    for key in case_rec:
        cv2.rectangle(img_dict[key[0]], case_rec[key][0], case_rec[key][1], (0, 255, 0), 2)
        name = str(key[0]) + "_" + str(key[1]) + ".png"
        cv2.imwrite(os.path.join(paths, name), img_dict[key[0]])

def select_case(want_list,case,metric = "and"):
    assert isinstance(case,dict), "case file must be dictionary"
    assert isinstance(want_list,list) , "want_list must be list that retain pose position"
    result = {}
    for key in case:
        case_find = [(case[key][i]!=(0,0)) for i in want_list]
        if metric == "and": ## 전부다 있는 경우 추출
            if all(case_find) == True:
                result.update({key:case[key].copy()})
        elif metric == "any": ## 원하는 속성중 하나라도 있으면
            if any(case_find) == True:
                result.update({key: case[key].copy()})
        else :
            print(AttributeError , "metric must be 'and' or 'any'")
    return result

