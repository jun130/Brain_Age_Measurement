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
    all_list = []
    all_list.append(str(int(file_name[3:6])))
    all_list.append(file_name[-14:-12])
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
        if line_cnt > 60 :
            all_list.append(part[4])
        
            
            all_list.append(str(mean))
            kk += 1

            db_row.append(all_list)
            
            f.close()
            break
        
        if line == '' :
            
            f.close()
            break



import pymysql
 
# MySQL Connection 연결
#conn = pymysql.connect(host='192.168.1.12', port=3456, user='guest', password= '',
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
            print(1)
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

column = ['sub_id','hemi','bankssts','caudalanteriorcingulate', 'caudalmiddlefrontal','cuneus','entorhinal','fusiform','inferiorparietal',
'inferiortemporal','isthmuscingulate','lateraloccipital','lateralorbitofrontal', 'lingual','medialorbitofrontal','middletemporal','parahippocampal','paracentral',
'parsopercularis','parsorbitalis','parstriangularis','pericalcarine', 'postcentral','posteriorcingulate','precentral','precuneus','rostralanteriorcingulate', 
'rostralmiddlefrontal','superiorfrontal','superiorparietal','superiortemporal', 'supramarginal','frontalpole','temporalpole','transversetemporal','insula', 'cortical',
'sex','age']

with open('C:\\Users\\lsj\\Desktop\\python\\source\\sample_test.csv','w', newline='') as t:
     makewrite = csv.writer(t) 
     makewrite.writerow(column)
     for value in db_row:
         if(len(value) > 37 ) :
            makewrite.writerow(value)
# Connection 닫기
#conn.close()
