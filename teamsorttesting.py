import itertools
import numpy as np
import matplotlib.pyplot as plt

from random import randint
from timeit import default_timer as timer
from CSGORankListProducer import RandomTeam
from TeamSort import Fairness, getKey, TeamValue

start = timer()
shitlist = []


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
    sNap_a = []
    sNap_b = []
    players = [P[0], P[1], P[2], P[3], P[4], P[5], P[6], P[7], P[8], P[9]]
    # AB
    sNap_a.append(players.pop(0))
    sNap_b.append(players.pop(0))

    for i in range(4):
        if getKey(sNap_a[0]) > getKey(sNap_b[0]):
            # BA
            sNap_b.append(players.pop(0))
            sNap_a.append(players.pop(0))
        else:
            if randint(0, 1):
                # AB
                sNap_a.append(players.pop(0))
                sNap_b.append(players.pop(0))
            else:
                # BA
                sNap_b.append(players.pop(0))
                sNap_a.append(players.pop(0))

    Val_As = TeamValue(sNap_a) / 5
    Val_Bs = TeamValue(sNap_b) / 5

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
    if MyFairness < 70:
        shitlist.append(P)

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
    print(i+str("s"), "Method-")
    print("Average Fairness  =", MySum[names.index(i)], "%")
    print("Standard Deviation=", MyStDev[names.index(i)], "%")
    print()


labels = ("hOREP", "sNap", "TaF", "Ville")
size = 3
fig, ax = plt.subplots()
ax.boxplot(t, notch=False, sym=".")
plt.title(label=str(iterations)+" iterations")
plt.ylabel("Fairness %")
plt.xticks(np.arange(len(labels))+1, labels)
plt.ylim(0, 100)
plt.savefig("TeamSortData.png", dpi=1500)
plt.show()

fig, axs = plt.subplots(4, sharex=True, figsize=(10, 10))
binNum = 50
axs[0].set_xlim([0, 100])
axs[0].hist(t[:, 0], bins=binNum, color="blue", density=True,
            edgecolor='black', linewidth=1.2)
axs[0].set_title("hOREP")
axs[1].hist(t[:, 1], bins=binNum, color="orange", density=True,
            edgecolor='black', linewidth=1.2)
axs[1].set_title("sNap")
axs[2].hist(t[:, 2], bins=binNum, color="purple", density=True,
            edgecolor='black', linewidth=1.2)
axs[2].set_title("TaF")
axs[3].hist(t[:, 3], bins=binNum, color="green", density=True,
            edgecolor='black', linewidth=1.2)
axs[3].set_title("Ville")
axs[3].set_xlabel("Fairness %")
plt.savefig("TeamSortData2.png", dpi=500)
plt.show()
end = timer()
print("Time taken=", round(end - start, 2), "seconds.")
