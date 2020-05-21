import itertools

from CSGORankListProducer import RandomTeam


# Change to 1 for a detailed readout of values
ValReadOut = 0
# Change to 1 to produce comparison to sNap bot's method
ValCompare = 0

RankList = {
    "S1": 800,
    "S2": 800,
    "S3": 800,
    "S4": 800,
    "SE": 950,
    "SEM": 950,
    "GN1": 1050,
    "GN2": 1100,
    "GN3": 1150,
    "GNM": 1200,
    "MG1": 1250,
    "MG2": 1250,
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
    d = 10000  # dummy variable, needs to be large
    P = sorted(list(P), reverse=True, key=getKey)  # Sorts P

    # Generates list of all permutations of player list.
    Y = list(itertools.combinations(P, 5))

    # Iterates through all permutations to find smallest difference in metric
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
        sNap_A = [P[1], P[3], P[5], P[7], P[9]]
        sNap_B = [P[0], P[2], P[4], P[6], P[8]]
        print()
        print("sNap Bot Team A=", sNap_A)
        print("sNap Bot Team B=", sNap_B)
        Val_As = TeamValue(sNap_A) / 5
        Val_Bs = TeamValue(sNap_B) / 5
        print("Avg value of sNap A=", Val_As)
        print("Avg value of sNap B=", Val_Bs)
        print("Avg sNap value difference=", abs(Val_As - Val_Bs))
        print("sNap Fairness Metric=",
              str(round(Fairness(Val_As, Val_Bs))) + "%")

    return A_dum, B_dum
