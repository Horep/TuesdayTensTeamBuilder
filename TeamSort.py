import itertools
from random import randint
from CSGORankListProducer import RandomTeam


# Change to 1 for a detailed readout of values
ValReadOut = 1
# Change to 1 to produce comparison to sNap bot's method
ValCompare = 1

RankList = {
    "S1": 800,
    "S2": 825,
    "S3": 850,
    "S4": 875,
    "SE": 950,
    "SEM": 965,
    "GN1": 1050,
    "GN2": 1100,
    "GN3": 1150,
    "GNM": 1200,
    "MG1": 1250,
    "MG2": 1275,
    "MGE": 1400,
    "DMG": 1550,
    "LE": 1700,
    "LEM": 1850,
    "SMFC": 2000,
    "GE": 2150,
    "Lvl10": 2500
    }


def Fairness(x, y):  # Twice the "probablity" that x wins
    return 200/(1 + 10 ** ((abs(x - y))/400))


def getKey(item):  # Returns ELO value of rank
    return RankList[str(item)]


def TeamValue(x):  # Calculates value of team
    val = 0
    for i in range(0, 5):
        val = val + RankList.get(x[i])
    return val


def GenTeams(P):
    d = 10000  # Dummy variable, needs to be large
    P = sorted(list(P), reverse=True, key=getKey)  # Sorts P

    # Generates list of all combinations of player list.
    Y = list(itertools.combinations(P, 5))

    # Iterates through all combinations to find smallest difference in metric
    # d is the smallest difference found at ith iteration
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

    if ValReadOut == 1:
        print("Players=", P)
        print()
        print("Team A=", A_dum)
        print("Team B=", B_dum)
        print()
        print("Avg value of Team A=", A_Val)
        print("Avg value of Team B=", B_Val)
        print("Avg value difference=", d / 5)
        print()
        print("Fairness Metric=", str(round(Fairness(A_Val, B_Val))) + "%")

    if ValCompare == 1:
        sNap_a = []
        sNap_b = []
        players = P
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
        print()
        print("sNap Bot Team A=", sNap_a)
        print("sNap Bot Team B=", sNap_b)
        Val_As = TeamValue(sNap_a) / 5
        Val_Bs = TeamValue(sNap_b) / 5
        print("Avg value of sNap A=", Val_As)
        print("Avg value of sNap B=", Val_Bs)
        print("Avg sNap value difference=", abs(Val_As - Val_Bs))
        print("sNap Fairness Metric=",
              str(round(Fairness(Val_As, Val_Bs))) + "%")

    return A_dum, B_dum
