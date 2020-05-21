import itertools
import numpy as np
from timeit import default_timer as timer
from CSGORankListProducer import RandomTeam
from TeamSort import Fairness, getKey, TeamValue

start = timer()


def GenTeamsFairness(P):
    d = 10000  # Dummy variable, needs to be large
    P = sorted(list(P), reverse=True, key=getKey)  # Sorts P
    # Generates list of all combinations of player list.
    Y = list(itertools.combinations(P, 5))

    # Iterates through all combinations to find smallest difference in metric
    for i in range(0, 126):
        A = Y[i]
        B = Y[-i-1]
        if abs(TeamValue(A) - TeamValue(B)) < d:
            d = abs(TeamValue(A) - TeamValue(B))
            A_dum = A
            B_dum = B

    A_Val = TeamValue(A_dum) / 5
    B_Val = TeamValue(B_dum) / 5
    A_dum = sorted(list(A_dum), reverse=True, key=getKey)
    B_dum = sorted(list(B_dum), reverse=True, key=getKey)

    sNap_A = [P[1], P[3], P[5], P[7], P[9]]
    sNap_B = [P[0], P[2], P[4], P[6], P[8]]
    Val_As = TeamValue(sNap_A) / 5
    Val_Bs = TeamValue(sNap_B) / 5

    TaF_A = [P[0], P[2], P[5], P[6], P[9]]
    TaF_B = [P[1], P[3], P[4], P[7], P[8]]
    Val_At = TeamValue(TaF_A) / 5
    Val_Bt = TeamValue(TaF_B) / 5

    Ville_A = [P[0], P[3], P[5], P[7], P[9]]
    Ville_B = [P[1], P[2], P[4], P[6], P[8]]
    Val_Av = TeamValue(Ville_A) / 5
    Val_Bv = TeamValue(Ville_B) / 5

    MyFairness = Fairness(A_Val, B_Val)
    sNapFairness = Fairness(Val_As, Val_Bs)
    TaF_Fairness = Fairness(Val_At, Val_Bt)
    Ville_Fairness = Fairness(Val_Av, Val_Bv)

    return MyFairness, sNapFairness, TaF_Fairness, Ville_Fairness


iterations = 10**7
t = []
for i in range(0, iterations):
    t.append(GenTeamsFairness(RandomTeam()))

t = np.array(t)
MySum = np.round(t.sum(axis=0)/iterations, 2)
MyStDev = np.round(t.std(axis=0), 2)
MyMin = np.round(t.min(axis=0), 2)
MyMax = np.round(t.max(axis=0), 2)
names = ["hOREP", "sNap", "TaF", "Ville"]
print("Over", iterations, "Random teams:")
for i in names:
    print(i+str("'s"), "Method-")
    print("Average Fairness  =", MySum[names.index(i)], "%")
    print("Standard Deviation=", MyStDev[names.index(i)], "%")
    print()

end = timer()
print("Time taken=", round(end - start, 2), "seconds.")
