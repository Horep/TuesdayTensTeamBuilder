import itertools
from CSGORankListProducer import RandomTeam
import numpy as np
from TeamSort import Fairness,getKey,TeamValue



#Iterates through all permutations to find smallest difference in metric
#d is the smallest difference found at ith iteration

def GenTeams(P):
    d=10000 #dummy variable, needs to be large
    P=sorted(list(P),reverse=True,key=getKey)#Sorts P
    #Generates list of all permutations of player list.
    Y=list(itertools.combinations(P,5))
    
    #Iterates through all permutations to find smallest difference in metric
    #d is the smallest difference found at ith iteration
    for i in range(0,126):
        A=Y[i]
        B=Y[-i-1]
        if abs(TeamValue(A)-TeamValue(B))<d:
            d=abs(TeamValue(A)-TeamValue(B))
            A_dum=A
            B_dum=B
    
    A_Val=TeamValue(A_dum)/5
    B_Val=TeamValue(B_dum)/5
    A_dum=sorted(list(A_dum),reverse=True,key=getKey)
    B_dum=sorted(list(B_dum),reverse=True,key=getKey)
    sNap_A=[P[1],P[3],P[5],P[7],P[9]]
    sNap_B=[P[0],P[2],P[4],P[6],P[8]]   
    Val_As=TeamValue(sNap_A)/5
    Val_Bs=TeamValue(sNap_B)/5
    return Fairness(A_Val,B_Val),Fairness(Val_As,Val_Bs)


iterations=100
t=[]
for i in range(0,iterations):
    t.append(GenTeams(RandomTeam()))
    
t=np.array(t)

MySum=t.sum(axis=0)/iterations