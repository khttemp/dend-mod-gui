def load():
    global gameList
    global LS
    global BS
    global CS
    global RS
    global SS

    gameList = [
        "Shining Stage",
        "Rising Stage",
        "Climax Stage",
        "Burning Stage",
        "Lightning Stage",
    ]

    LS = len(gameList) - 1
    BS = len(gameList) - 2
    CS = len(gameList) - 3
    RS = len(gameList) - 4
    SS = len(gameList) - 5
