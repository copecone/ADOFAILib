import random
from adofailib.parser import *
from adofailib.vfx.decoration import *

def getrand(): return (random.random() - 0.5) * 2

adofaiParser = ADOFAIParser("test.adofai")
adofaiLevel = adofaiParser.getLevel()

adofaiLevel.disable("TrackDisappearAnimation")
adofaiLevel.disable("TrackAppearAnimation")

defaultBeatsAhead = adofaiLevel.data["settings"]["beatsAhead"]
if defaultBeatsAhead == 0:
    defaultBeatsAhead = 16

trackAppearAnim = {0: defaultBeatsAhead}

for action in adofaiLevel.data["actions"]:
    if action["eventType"] == "AnimateTrack":
        action["trackDisappearAnimation"] = "None"
        if action["trackAnimation"] != "None":
            trackAppearAnim[action["floor"]] = action["beatsAhead"]
            action["trackAnimation"] = "None"
        else:
            trackAppearAnim[action["floor"]] = trackAppearAnim[0]

tileInit = 240
tileAppearAnimation = trackAppearAnim[0]

tileDisappearAnimation = 0
for i in range(adofaiLevel.length):
    if i + 1 in trackAppearAnim:
        adofaiLevel.setBPMScalePoint(adofaiLevel[i + 1]["bpm"])
        tileAppearAnimation = trackAppearAnim[i + 1]

    adofaiLevel.moveTrack(i + 1, range = 0, duration = 0, ease = Easing("Linear"), opacity = 0, rotation = 15, position = [0.2, 0.6], scale = [100, 100], angleOffset = -180 * tileInit * adofaiLevel[i + 1]["bpmScale"])

    # adofaiLevel.moveTrack(i, range = 0, duration = 1, ease = Easing("OutQuad"), rotation = 360, scale = [100, 100])

    adofaiLevel.moveTrack(i + 1, range = 0, duration = 4 * adofaiLevel[i + 1]["bpmScale"], ease = Easing("OutQuart"), opacity = 100, rotation = 0, position = [0, 0], angleOffset = -180 * tileAppearAnimation * adofaiLevel[i + 1]["bpmScale"])
    adofaiLevel.moveTrack(i + 1, range = -1, duration = 4 * adofaiLevel[i + 1]["bpmScale"], ease = Easing("InQuart"), opacity = 0, rotation = -20, position = [getrand() * 1.5, -3], scale = [80, -80], angleOffset = 180 * tileDisappearAnimation * adofaiLevel[i + 1]["bpmScale"])

"""
detail = 16
ylength = 8

adofaiLevel.moveDecoration(1, duration = 4, position = [-8, -2], tag = ["justlinecircle"], ease=Easing("OutCirc"))
for i in range(100 * detail):
    scalei = 0 + i / detail / 8
    deco = ADOFAIDecoration("circle.png", tile = 5, parallax = [i / detail, i / detail], position = [0, ylength], scale = [scalei, scalei], tags = ["justlinecircle"], opacity = 2, depth = -1)
    adofaiLevel.addDecoration(deco)
"""

adofaiParser.save(adofaiLevel, "test2.adofai")