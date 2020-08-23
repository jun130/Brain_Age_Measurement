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
for file_name in list_stat :
    #print(file_name)
    
    line_cnt = 0 
    cortical = temporal = frontal = parietal = occipital = 0.0
    f= open(file_name,'r') 
   
    
    while True :
        line = f.readline()
        line_cnt+=1 
       
        part = line.split()

        if line_cnt in (61, 65, 66, 68, 74, 75, 89, 92, 93) :
            temporal += float(part[4]) # part[4] is part of thickness
            
        if line_cnt in (62, 63, 71, 73, 76, 77, 78, 79, 83, 85, 86, 87, 91) :    
            frontal += float(part[4])
            
        if line_cnt in (67, 69, 81, 82, 84, 88, 90) :   
            parietal += float(part[4])
        
        if line_cnt in (64, 70, 72, 80) :
            occipital += float(part[4])
        
        if line_cnt == 94 :
            temporal = round(temporal/9.0, 3)
            frontal = round(frontal/13.0, 3)
            parietal = round(parietal/7.0, 3)
            occipital = round(occipital/4.0, 3)
            cortical = round(float(part[4])/1.0,3)

            db_row.append([str(int(file_name[3:6])),file_name[-14:-12], str(temporal), str(frontal),
             str(parietal), str(occipital), str(cortical)])
            
            f.close()
            break
        
        if line == '' :
            
            f.close()
            break



import pymysql
 
# MySQL Connection 연결
conn = pymysql.connect(host='221.142.100.2', port=3456, user='guest', password= '540528',
                       db='patientdb')
 
# Connection 으로부터 Cursor 생성
curs = conn.cursor()
 
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
            print(db_row[index])
            print(db_row[index+1])
            
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
                index+=2

    if len(row[-1]) != 1 :

        print("") 


# Connection 닫기
conn.close()