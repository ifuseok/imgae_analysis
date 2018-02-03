from math import sqrt
import numpy as np
'''
class
FindPosition : 포즈 사진 읽어들어와서 처리하는 클래스
__init__
    position : 좌표가 저장된 리스트들이 저장된 리스트
    img : 이미지가 저장된 리스트
    per_posit : 반드시 포함되어야 할 기준들 번호 defalut 코,양쪽어깨
perfect_bool : 하나의 좌표 리스트를 받았을 때 원하는 position이 다 있다면 True 아니면 False
    position_list : 사진에 대한 포즈 좌표가 적힌 리스트 하나
    position_want : 원하는 포지션 위치가 담긴 리스트
    bol_area :
perfect_index : 원하는 position 다 포함된 사진만 뽑아내기
position_index : 찾고싶은 위치 적인 리스트 인덱스

'''

'''
해야 할 것!
좌표 순서 기록
0 : 코 
1 : 목
2 : 왼쪽어깨
3 : 왼팔꿈치
4 : 왼손
5 : 오른쪽어깨
6 : 오른쪽팔꿈치
7 : 오른쪽손
8 : 왼골반
9 : 왼무릎
10 : 왼발
11 : 오른골반
12 : 오른무릎
13 : 오른발
14 : 왼눈
15 : 왼귀
16 : 오른눈
17 : 오른귀
코랑 어깨가 반드시 있고
왼어깨랑 오른쪽 어깨 차이가 젤 큰 거를 가져온다
'''

class FindPosition :
    def __init__(self,position,img):
        self.position = position
        self.img = img
        div_position = []
        for po in position : #좌표 담긴 리스트 받아서 각 좌표마다 몇 명 잡아냈는지 확인하는 리스트
            po_list = []
            person = int(len(po) / 18)
            for n in range(person):
                start = n * 18
                end = 18 + (n * 18)
                po_list.append(po[start:end])
            div_position.append(po_list)  #각 사진 마다 인식된 사람하나 하나하나 마다 리스트 만들어서 할당
        self.div_position = div_position

    def perfect_bool(self, position_list, position_want,metric):
        bol_area = []
        for i in position_want:
            bol = (position_list[i] != (0, 0))
            bol_area.append(bol)
        if metric == "all":
            return all(bol_area) # 전부다 존재하는거
        elif metric == "any" :
            return any(bol_area) # 한 개 라도 있다면

    def perfect_case(self,per_posit = [0,2,5],metric = "all"):
        per_case = self.div_position[:] # 각 리스트 안에 한 사진 좌표 정보가 담겨있음
        for pi,posit in enumerate(per_case) : #각 좌표 담긴 리스트 마다 코 랑 어깨 다있는 case 만 빼오기 = > default
            indexes = []
            for ix,po in enumerate(posit):
                detect = self.perfect_bool(po,per_posit,metric)
                if detect != True : # 다 있지 않다면 목록에서 제거
                    if len(posit)!=1: # 혹시나 1개 밖에 없는데 아 있지 않은 경우라면 일단 keep
                        indexes.append(ix)
            for index in sorted(indexes, reverse=True):
                del posit[index]
                    #posit.pop(ix-len(posit))
        return per_case


def dif_posit(per_case,a=2,b=5) :
    per_case2 = per_case.copy()
    for i,case in enumerate(per_case2) :
        dist = []
        for ca in case :
            x1,y1 = ca[a]
            x2,y2 = ca[b]
            d = sqrt((x1-x2)**2+(y1-y2)**2)
            dist.append(d)
        dist = np.array(dist ,dtype = np.float)
        dist =  dist/dist.max()
        indexes = []

        for ix,value in enumerate(dist):
            if value <0.8 :
                indexes.append(ix)
        for index in sorted(indexes,reverse=True):
            del case[index]
    return(per_case2)
## @ 하면 private 함수 쓸수 있음

