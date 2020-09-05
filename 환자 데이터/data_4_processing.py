import pandas as pd 
import os
from glob import glob

# 661번 stat 삭제 필요.

os.chdir("C:\\Users\\lsj\\Desktop\\python\\source\\IXI_aparc_stats\\stats") 
# 현재 workspace 변경

list_stat = glob("*.stats") 
# stats 로 끝나는 파일 리스트 추출 


db_row = []
te = []
kk = 0
summ = 0.0
mean = 0
for file_name in list_stat :
    #print(file_name)
    
    line_cnt = 0 
    cortical = temporal = frontal = parietal = occipital = 0.0

    f= open(file_name,'r') 
   
    surfarea = surf_temp = surf_fron = surf_pari = surf_occi = 0.0
    while True :
        line = f.readline()
        line_cnt+=1 
       
        part = line.split()
        
        if line_cnt == 21 :
            part = line.split(',')
            mean = round(float(part[3]),3)
        if line_cnt in (61, 65, 66, 68, 74, 75, 89, 92, 93) :
            temporal += float(part[2]) * float(part[4]) # part[4] is part of thickness
            surf_temp += float(part[2])
            
        if line_cnt in (62, 63, 71, 73, 76, 77, 78, 79, 83, 85, 86, 87, 91) :    
            frontal += float(part[2]) * float(part[4])
            surf_fron += float(part[2])
            
        if line_cnt in (67, 69, 81, 82, 84, 88, 90) :   
            parietal += float(part[2]) * float(part[4])
            surf_pari += float(part[2])
        
        if line_cnt in (64, 70, 72, 80) :
            occipital += float(part[2]) * float(part[4])
            surf_occi += float(part[2])
        
        if line_cnt == 94 :
            surfarea += surf_temp + surf_fron + surf_pari + surf_occi
            cortical = round((temporal + frontal + parietal + occipital)/surfarea,3)
            temporal = round(temporal/surf_temp, 3)
            frontal = round(frontal/surf_fron, 3)
            parietal = round(parietal/surf_pari, 3)
            occipital = round(occipital/surf_occi, 3)
            
            #print(round(float(mean)- cortical,3))
            summ += round(float(mean)- cortical,3)
            kk += 1
            db_row.append([str(int(file_name[3:6])),file_name[-14:-12], str(temporal), str(frontal),
             str(parietal), str(occipital), str(mean)])
            
            f.close()
            break
        
        if line == '' :
            
            f.close()
            break

print("표본 데이터 수 : " + str(float(kk))) 
print("오차 : " + str(summ/float(kk)) )

import pymysql
 
# MySQL Connection 연결
#conn = pymysql.connect(host='192.168.1.12', port=3456, user='guest', password= '540528',
#                       db='patientdb')
 
# Connection 으로부터 Cursor 생성
#curs = conn.cursor()
 
file_path = "C:\\Users\\lsj\\Desktop\\python\\source\\IXI_origin2.csv"
f= open(file_path,'r') 

line_cnt = 0 

index =0





while True :
    line = f.readline()
    row = line.split(',')
    line_cnt+=1 
    temp_list = []

    
    if line == '' :
        # 파일의 끝 
        print(index/2) # 파일 개수 체크.
        f.close()
        break

    if line_cnt > 1 :
        if int(row[0]) == int(list_stat[index][3:6]) and len(row[-1]) > 1:
            # 파일명과 서브젝트가 일치하는 경우 
 
            temp_list.append([row[1], str(float(row[-1][:-1]))])
            
            db_row[index]  += temp_list[0]
            db_row[index+1]  += temp_list[0]
            #print(db_row[index])
            #print(db_row[index+1])
            
            '''
            # SQL문 실행
            
            sql = "INSERT INTO inform(sub_id, hemi, temporal, frontal, parietal, occipital, cortical, sex, age) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            curs.execute(sql, db_row[index])
            
            curs.execute(sql, db_row[index+1])
            conn.commit()
            '''
           
            index+=2  
            
        else :
            # 파일명과 서브젝트가 일치하지 않는 경우
            while True :
                if(int(row[0]) < int(list_stat[index][3:6])) :
                    
                    break
                if(int(row[0]) == int(list_stat[index][3:6]) and len(row[-1]) > 1 ) :
                    
                    temp_list.append([row[1], str(float(row[-1][:-1]))])
                    db_row[index]  += temp_list[0]
                    db_row[index+1]  += temp_list[0]
                
                index+=2
                

    if len(row[-1]) != 1 :

        print("") 

import csv 

column = ['sub_id','hemi','temporal','frontal', 'parietal','occipital','cortical','sex','age']

with open('C:\\Users\\lsj\\Desktop\\python\\source\\sample_test.csv','w', newline='') as t:
     makewrite = csv.writer(t) 
     makewrite.writerow(column)
     for value in db_row:
         if(len(value) > 8 ) :
            makewrite.writerow(value)
# Connection 닫기
#conn.close()