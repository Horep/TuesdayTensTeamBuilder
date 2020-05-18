import numpy as np

#Average Values For Normalisation
KillAvg=0.679
SurvAvg=0.317
RndsMultKillAvg=1.277
#Weights
#[Kill,Surv,MultKill,Damage,KAST,ClutchSucc]
W=np.array([1,0.7,1,0.1,0.15,0.2])
scalars=np.array([1,4,9,16,25])
def Adjustment(x,L,G):#L=2.03,G=1.004
    return L*G*(np.expm1(x))/(L+G*np.expm1(x))

def KillRating(kills,rounds):
    return kills/(rounds*KillAvg)

def SurvRating(deaths,rounds):
    return (rounds - deaths)/(rounds*SurvAvg)

def MultiKillRat(M_Kill,rounds):#M_Kill: matrix of number of each multikill [1k,...,5k]
    return (np.sum(M_Kill*scalars))/(RndsMultKillAvg*rounds)

def DamageRat(x):
    val=0
    
    if 0<=x<75:
        val = (x/75)**(2.26)
    elif 75<=x<120:
        val = 1.36 - ((x-120)/75)**2
    else:
        val = 1.36
    return val

def KAST(useful,rounds):
    return 2*useful/rounds

def ClutchSucc(M_V,NoClutchRounds):#M_V: matrix of 1vX's won [1v1,...,1v5]
    return (np.sum(M_V*scalars))/(NoClutchRounds)

def FillMatrix(kills,rounds,deaths,ADR,useful,M_Kill,M_V,NoClutchRounds):
    M=[KillRating(kills,rounds),
       SurvRating(deaths,rounds),
       MultiKillRat(M_Kill,rounds),
       DamageRat(ADR),
       KAST(useful,rounds),
       ClutchSucc(M_V,NoClutchRounds)]
    return np.array(M)

def PreRating(x,w):
    return (np.sum(x*w))/ np.sum(w)




    