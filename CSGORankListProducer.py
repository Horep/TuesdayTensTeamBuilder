from random import randint

RankNumList = {
    0: "S1",
    1: "S2",
    2: "S3",
    3: "S4",
    4: "SE",
    5: "SEM",
    6: "GN1",
    7: "GN2",
    8: "GN3",
    9: "GNM",
    10: "MG1",
    11: "MG2",
    12: "MGE",
    13: "DMG",
    14: "LE",
    15: "LEM",
    16: "SMFC",
    17: "GE",
    18: "Lvl10"
    }


def RandomTeam():
    EndArray = []
    for i in range(0, 10):
        EndArray.append(RankNumList.get(randint(0, 18)))
    return EndArray
