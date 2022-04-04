import csv
import os
import sys
import subprocess
import filecmp
functitle=[]
funcvalue=[]
statetitle=[]
statevalue=[]
pq=0
g=0
with open('functionResult.csv', 'w') as csvfile1, open('statementResult.csv','w') as csvfile2 :
    spamwriter1 = csv.writer(csvfile1, delimiter=',')
    spamwriter2 = csv.writer(csvfile2, delimiter=',')
    fp1=open("universe");
    i=0
    for l1 in fp1:
        os.system("gcc -fprofile-arcs -ftest-coverage tcas.c")	
        os.system("./a.out "+l1)
        i=i+1
        k=1
        os.system("gcov tcas.c")  
        fp2=open("tcas.c.gcov");
        for line1 in fp2:
            try:    
                flag=line1.split(":")[0];
                if "-" in flag:
                    continue
                elif "#####" in flag:
                    statevalue.append("0")
                    statetitle.append(k)
                    k=k+1
                else: 
                    statevalue.append("1")
                    statetitle.append(k)
                    k=k+1
            except:
                print ("exiting")		
                exit(1)
        p=filecmp.cmp("/home/jitendra/Desktop/Fault_Localization/tcas_2.0/tcas/outputs/t"+str(i), "/home/jitendra/Desktop/Fault_Localization/tcas_2.0/tcas/Outputs_V1/t"+str(i)) 
        if p==True:
            statevalue.append(int('0'))
            funcvalue.append(int('0'))
        else:
            statevalue.append(int('1'))
            funcvalue.append(int('1'))
        if pq==0:
            functitle.append("Result")
            statetitle.append("Result")
            spamwriter1.writerow(functitle)
            spamwriter2.writerow(statetitle)
            pq=1
        if len(funcvalue)>1:
            spamwriter1.writerow(funcvalue)
            funcvalue=[]
        else:
            funcvalue=[]
        if len(statevalue)>1:
            spamwriter2.writerow(statevalue)
            statevalue=[]
        else:
            statevalue=[]



