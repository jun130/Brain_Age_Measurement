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
    cortical = temporal = frontal = parietal = occipital = 0
    f= open(file_name,'r') 
   
    
    while True :
        line = f.readline()
        line_cnt+=1 
       
        part = line.split()
        if line_cnt in (61, 65, 66, 68, 74, 75, 89, 92, 93) :
            temporal += float(part[4])
            
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
            cortical = part[4]
            
            '''
            print("temp =" + str(temporal)+"\n", "front =" + str(frontal)+"\n", 
            "parietal =" + str(parietal)+"\n", "occipital =" + str(occipital)+"\n",
            "cortical =" + str(cortical))
            '''

            db_row.append([int(file_name[3:6]),file_name[-14:-12], str(temporal), str(frontal),
             str(parietal), str(occipital), str(cortical)])
            
            
            '''
            for i in range(len(db_row)) :
                db_row[i] += te[i]
                print(db_row[i])
            '''
            f.close()
            break
        
        if line == '' :
            
            f.close()
            break

'''
file_path = list_stat[0]
#file_path = "C:\\Users\\lsj\\Desktop\\python\\source\\IXI_origin2.csv"


print(file_path)
df = pd.DataFrame()

f= open(file_path,'r') 
'''
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
        if int(row[0]) == int(list_stat[index][3:6]) : 
            # 파일명과 서브젝트가 일치하는 경우 
            '''
            temp_list.extend(row[0])
            temp_list.extend(row[1])
            temp_list.extend(row[-1])
            '''

            temp_list.append([row[1], row[-1][:-1]])
            
            db_row[index]  += temp_list[0]
            db_row[index+1]  += temp_list[0]
            print(db_row[index])
            print(db_row[index+1])

            # excel의 row, stat의 data 결합
            index+=2  
            
        else :
            # 파일명과 서브젝트가 일치하지 않는 경우
            while True :
                if(int(row[0]) < int(list_stat[index][3:6])) :
                    break
                index+=2

                

    #elif row[0] != '' || row[1] != '' || row[-1] !+ ''#비어있는 경우 db insert 안함 
    if len(row[-1]) != 1 :
        #print(row[0], row[1], row[-91]) 
        print("") 
    
    
    
    #print(line, end='')
    
    
    #user_name = item[item.index("WEIGHT")+1]
'''
for i in range(len(db_row)) :
    db_row[i] += te[i]
    print(db_row[i])
'''
    #print(line, end='')
