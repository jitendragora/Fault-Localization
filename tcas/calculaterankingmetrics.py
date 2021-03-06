# -*- coding: utf-8 -*-
"""CalculateRankingMetrics.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HYZZRCjIxLTpuXZiapu4eaGe_HMggRMg
"""

import pandas as pd
import numpy as np
import math
import os
import csv

df_train=pd.read_csv('statementResult_tcas_tcasMutantLine72_V4.csv')
df_train.head()

y = np.array([df_train['Result']]).T
y = y.tolist()
#print(y)
df_train.drop(['Result'],1 )
x = df_train.values.tolist()
#print(x)
total_test_cases = len(y)
total_failed=np.count_nonzero(y)
total_passed=total_test_cases-total_failed
print("Total Passed Test Cases are: {} , and Total Failed Test Cases are: {}".format(total_passed, total_failed))

def tarantula(nsuccess, nfailure):
    try:
        cef = nfailure
        cnf = total_failed-nfailure
        cep = nsuccess
        cnp = total_passed-nsuccess
        sus_score = float(float(cef)/float(cef+cnf))/float((float(cef)/float(cef+cnf))+(float(cep)/float(cep+cnp)))
        return sus_score
    except ZeroDivisionError:
        return -999999

def oPowerP(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    op = cef - (cep/float(cep+cnp+1))
    return op

def bigO(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    if cnf > 0:
      return -1
    return cnp

def oPowerD(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    od = (cep-(cef/float(cef+cnf+1)))
    return od

def kulczynski1(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = cef/float(cnf+cep)
        return ans
    except ZeroDivisionError:
        return -999999

def kulczynski2(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = ((cef/float(cnf+cef))+(cef/float(cef+cep)))/2
        return ans
    except ZeroDivisionError:
        return -999999

def jaccard(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = cef/float(total_failed + cep)
        return ans
    except ZeroDivisionError:
        return -999999

def ochiai(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = float(cef)/float(math.sqrt( (cef+cnf)*(cef+cep) ))
        return ans
    except ZeroDivisionError:
        return -999999

def ample(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = abs(cef/float(cef*cep) - cep/float(cep*cnp))
        return ans
    except ZeroDivisionError:
        return -999999

def ample2(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = float(cef/total_failed)-float(cep/total_passed)
        return ans
    except ZeroDivisionError:
        return -999999

def wong1(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    ans = float(cef)
    return ans

def wong2(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    ans = float(cef-cep)
    return ans

def wong3(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    h = 0
    if cef<=2:
      h = cep
    elif cep in range(3, 11):
      h = float(2 + float((cep-2)/10))
    else:
      h = float(2.8 + float((cep-10)/1000))
    ans = float(cef-h)
    return ans

def wong3Dash(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    if cef+cep==0:
      h = -1000
    else:
      h = wong3(nsuccess, nfailure)
    ans = float(cef-h)
    return ans

def gp13(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = cef*(1 + 1/float(2*cep +cef) )
        return ans
    except ZeroDivisionError:
        return -999999

def cbiInc(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = cef/float(cef+cep) - float(total_failed/total_test_cases)
        return ans
    except ZeroDivisionError:
        return -999999

def cbiLog(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    cbiInc_ans = cbiInc(nsuccess, nfailure)
    #NOT ZeroDivisionError
    if cbiInc_ans != -999999:
      if total_failed > 0 and cef>0:
        try:
            ans =  2/( 1/(cbiInc_ans) + float(math.log(total_failed)/math.log(cef)) )
            return ans
        except ZeroDivisionError:
            return -999999
    else:
      return cbiInc_ans

def cbiSqrt(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    cbiInc_ans = cbiInc(nsuccess, nfailure)
    if cbiInc_ans != -999999: #NOT ZeroDivisionError
      try:
          ans =2/float( 1/(cbiInc_ans) + math.sqrt(total_failed)/math.sqrt(cef) )
          return ans
      except ZeroDivisionError:
        return -999999
    else:
      return cbiInc_ans

def sorensenDice(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = (2*cef)/float(2*cef + cnf + cep)
        return ans
    except ZeroDivisionError:
        return -999999

def russellAndRao(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    ans = float(cef/total_test_cases)

def m1(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = (cef+cnp)/float(cnf+cep)
        return ans
    except ZeroDivisionError:
        return -999999

def m2(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = cef/float(cef+cnp+2*(cnf+cep))
        return ans
    except ZeroDivisionError:
        return -999999

def m3(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    ans = 2*(cef+cnp)/total_test_cases
    return ans

def lee(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    ans = float(cef+cnp)
    return ans

def rogersAndTanimoto(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = (cef+cnp)/float(cef+cnp+2*(cnf+cep))
        return ans
    except ZeroDivisionError:
        return -999999

def goodman(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = (2*cef-cnf-cep)/float(2*cef+cnf+cep)
        return ans
    except ZeroDivisionError:
        return -999999

def simpleMatching(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    ans = float((cef+cnp)/total_test_cases)
    return ans

def hamann(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    ans = float((cef+cnp-cnf-cep)/total_test_cases)
    return ans

def euclid(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    ans = float(math.sqrt(cef + cnp))
    return ans

def hamming(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    ans = float(cef + cnp)
    return ans

def rogot1(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = 1/2*(cef/float(cef+cep) + cnp/float(2*cnp+cnf+cep))
        return ans
    except ZeroDivisionError:
        return -999999

def rogot2(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = 1/4*(cef/float(cef+cep) + cef/total_failed + cnp/total_passed + cnp/float(cnp+cnf))
        return ans
    except ZeroDivisionError:
        return -999999

def binary(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    if cnf>0:
      return 0
    else:
      return 1

def gower1(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    ans = float(cef-(cnf+cep)+cnp)/total_test_cases
    return ans

def gower2(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = (cef+cnp)/float(cef+cnp+0.5*(cnf+cep))
        return ans
    except ZeroDivisionError:
        return -999999

def gower3(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = ((cef*cnp)-(cnf*cep))/float((cef*cnp)+(cnf*cep))
        return ans
    except ZeroDivisionError:
        return -999999

def addedValue(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = cef/float(max(cef+cep, total_failed))
        return ans
    except ZeroDivisionError:
        return -999999

def manhattan(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    ans = 1-float((cep+cnf)/total_test_cases)
    return ans

def braun(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = cef/float(cef+cep)
        return ans
    except ZeroDivisionError:
        return -999999

def levandowsky(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = cef/(total_failed+cep)
        return ans
    except ZeroDivisionError:
        return -999999

def simpson(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = float(cef/total_failed)
        return ans
    except ZeroDivisionError:
        return -999999

def dice(nsuccess, nfailure):
    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    try:
        ans = 2*cef/float(total_failed+cep)
        return ans
    except ZeroDivisionError:
        return -999999

Tarantula=[]
Tarantula.append("Tarantula")

OToThePowerP = []
OToThePowerP.append("OToThePowerP")

BigO = []
BigO.append("BigO")

OToThePowerD = []
OToThePowerD.append("OToThePowerD")

Kulczynski1=[]
Kulczynski1.append("Kulczynski1")

Kulczynski2=[]
Kulczynski2.append("Kulczynski2")

Jaccard = []
Jaccard.append("Jaccard")

Ochiai = []
Ochiai.append("Ochiai")

Ample = []
Ample.append("Ample")

Ample2 = []
Ample2.append("Ample2")

Wong1 = []
Wong1.append("Wong1")

Wong2 = []
Wong2.append("Wong2")

Wong3 = []
Wong3.append("Wong3")

Wong3Dash = []
Wong3Dash.append("Wong3Dash")

GP13 = []
GP13.append("GP13")

CbiInc = []
CbiInc.append("CbiInc")

CbiLog = []
CbiLog.append("CbiLog")

CbiSqrt = []
CbiSqrt.append("CbiSqrt")

SorensenDice = []
SorensenDice.append("SorensenDice")

RussellAndRao = []
RussellAndRao.append("RussellAndRao")

M1 = []
M1.append("M1")

M2 = []
M2.append("M2")

M3 = []
M3.append("M3")

Lee = []
Lee.append("Lee")

RogersAndTanimoto = []
RogersAndTanimoto.append("RogersAndTanimoto")

Goodman = []
Goodman.append("Goodman")

SimpleMatching = []
SimpleMatching.append("SimpleMatching")

Hamann = []
Hamann.append("Hamann")

Euclid = []
Euclid.append("Euclid")

Hamming = []
Hamming.append("Hamming")

Rogot1 = []
Rogot1.append("Rogot1")

Rogot2 = []
Rogot2.append("Rogot2")

Binary = []
Binary.append("Binary")

Gower1 = []
Gower1.append("Gower1")

Gower2 = []
Gower2.append("Gower2")

Gower3 = []
Gower3.append("Gower3")

AddedValue = []
AddedValue.append("AddedValue")

Manhattan = []
Manhattan.append("Manhattan")

Braun = []
Braun.append("Braun")

Levandowsky = []
Levandowsky.append("Levandowsky")

Simpson = []
Simpson.append("Simpson")

Dice = []
Dice.append("Dice")

for i in range(0,len(x[0])):
    nsuccess=0
    nfailure=0
    for j in range(0,len(y)):
        #print x[j][i],y[j][0]
        if x[j][i]==1 and y[j][0]==0:
            nsuccess=nsuccess+1
        elif x[j][i]==1 and y[j][0]==1:
            nfailure=nfailure+1

    cef = nfailure
    cnf = total_failed-nfailure
    cep = nsuccess
    cnp = total_passed-nsuccess
    
    '''print("Count of statements Executed by failed Test Cases is: "+str(cef))
    print("Count of statements NOT Executed by failed Test Cases is: "+str(cnf))
    print("Count of statements Executed by Passed Test Cases is: "+str(cep))
    print("Count of statements Not Executed by Passed Test Cases is: "+str(cnp))
    print("")'''


    Tarantula.append(tarantula(nsuccess, nfailure))
    OToThePowerP.append(oPowerP(nsuccess, nfailure))
    BigO.append(bigO(nsuccess, nfailure))
    OToThePowerD.append(oPowerD(nsuccess, nfailure))
    Kulczynski1.append(kulczynski1(nsuccess, nfailure))
    Kulczynski2.append(kulczynski2(nsuccess, nfailure))
    
    Jaccard.append(jaccard(nsuccess, nfailure))
    Ochiai.append(ochiai(nsuccess, nfailure))
    Ample.append(ample(nsuccess, nfailure))
    Ample2.append(ample2(nsuccess, nfailure))
    Wong1.append(wong1(nsuccess, nfailure))
    Wong2.append(wong2(nsuccess, nfailure))
    Wong3.append(wong3(nsuccess, nfailure))
    Wong3Dash.append(wong3Dash(nsuccess, nfailure))

    GP13.append(gp13(nsuccess, nfailure))
    CbiInc.append(cbiInc(nsuccess, nfailure))
    CbiLog.append(cbiLog(nsuccess, nfailure))
    CbiSqrt.append(cbiSqrt(nsuccess, nfailure))

    SorensenDice.append(sorensenDice(nsuccess, nfailure))
    RussellAndRao.append(russellAndRao(nsuccess, nfailure))
    M1.append(m1(nsuccess, nfailure))
    M2.append(m2(nsuccess, nfailure))
    M3.append(m3(nsuccess, nfailure))
    Lee.append(lee(nsuccess, nfailure))

    RogersAndTanimoto.append(rogersAndTanimoto(nsuccess, nfailure))
    Goodman.append(goodman(nsuccess, nfailure))
    SimpleMatching.append(simpleMatching(nsuccess, nfailure))
    Hamann.append(hamann(nsuccess, nfailure))
    Euclid.append(euclid(nsuccess, nfailure))
    Hamming.append(hamming(nsuccess, nfailure))
    Rogot1.append(rogot1(nsuccess, nfailure))
    Rogot2.append(rogot2(nsuccess, nfailure))
    Binary.append(binary(nsuccess, nfailure))
    Gower1.append(gower1(nsuccess, nfailure))
    Gower2.append(gower2(nsuccess, nfailure))
    Gower3.append(gower3(nsuccess, nfailure))
    AddedValue.append(addedValue(nsuccess, nfailure))
    Manhattan.append(manhattan(nsuccess, nfailure))
    Braun.append(braun(nsuccess, nfailure))
    Levandowsky.append(levandowsky(nsuccess, nfailure))
    Simpson.append(simpson(nsuccess, nfailure))
    Dice.append(dice(nsuccess, nfailure))

#getting parent directory
cwd = os.getcwd()
p=0
i=-1
while i>= (-len(cwd)) :
    #print(cwd[i])
    if cwd[i]=='/' :
        p=p+1
    if p==1 :
        break
    i=i-1
parent_directory=cwd[:i]
print(parent_directory)

csvfile=open("RankingMetricsScore_tcasMutantLine72_V4.csv", "a+")
spamwriter1 = csv.writer(csvfile, delimiter=',')
spamwriter1.writerow(Tarantula)
spamwriter1.writerow(OToThePowerP)
spamwriter1.writerow(BigO)
spamwriter1.writerow(OToThePowerD)
spamwriter1.writerow(Kulczynski1)
spamwriter1.writerow(Kulczynski2)
spamwriter1.writerow(Jaccard)
spamwriter1.writerow(Ochiai)
spamwriter1.writerow(Ample)
spamwriter1.writerow(Ample2)
spamwriter1.writerow(Wong1)
spamwriter1.writerow(Wong2)
spamwriter1.writerow(Wong3)
spamwriter1.writerow(Wong3Dash)
spamwriter1.writerow(GP13)
spamwriter1.writerow(CbiInc)
spamwriter1.writerow(CbiLog)
spamwriter1.writerow(CbiSqrt)
spamwriter1.writerow(SorensenDice)
spamwriter1.writerow(RussellAndRao)
spamwriter1.writerow(M1)
spamwriter1.writerow(M2)
spamwriter1.writerow(M3)
spamwriter1.writerow(Lee)
spamwriter1.writerow(RogersAndTanimoto)
spamwriter1.writerow(Goodman)
spamwriter1.writerow(SimpleMatching)
spamwriter1.writerow(Hamann)
spamwriter1.writerow(Euclid)
spamwriter1.writerow(Hamming)
spamwriter1.writerow(Rogot1)
spamwriter1.writerow(Rogot2)
spamwriter1.writerow(Binary)
spamwriter1.writerow(Gower1)
spamwriter1.writerow(Gower2)
spamwriter1.writerow(Gower3)
spamwriter1.writerow(AddedValue)
spamwriter1.writerow(Manhattan)
spamwriter1.writerow(Braun)
spamwriter1.writerow(Levandowsky)
spamwriter1.writerow(Simpson)
spamwriter1.writerow(Dice)

print("End")
