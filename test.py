import random
from adofailib.parser import *
from adofailib.vfx.decoration import *

def getrand(): return (random.random() - 0.5) * 2

adofaiParser = ADOFAIParser("test.adofai")
adofaiLevel = adofaiParser.getLevel()

# Generate Level
adofaiLevel.disable("TrackDisappearAnimation")
adofaiLevel.disable("TrackAppearAnimation")

for action in adofaiLevel.data["actions"]:
    if action["eventType"] == "AnimateTrack":
        action["trackDisappearAnimation"] = "None"
        action["trackAnimation"] = "None"

tileInit = 120
tileAppearAnimation = -2
tileDisappearAnimation = 8
for i in range(adofaiLevel.length):
    adofaiLevel.moveTrack(i + 1, range = -1, duration = 4 * adofaiLevel[i + 1]["bpmScale"], ease = Easing("InQuart"), opacity = 1000, rotation = -20, position = [getrand() * 1.5, -3], scale = [80, 80], angleOffset = 180 * tileDisappearAnimation * adofaiLevel[i + 1]["bpmScale"])

    adofaiLevel.moveTrack(i + 1, range = 0, duration = 0, ease = Easing("Linear"), opacity = 0, rotation = 15, position = [0.2, 0.6], angleOffset = -180 * tileInit * adofaiLevel[i + 1]["bpmScale"])
    adofaiLevel.moveTrack(i + 1, range = 0, duration = 4 * adofaiLevel[i + 1]["bpmScale"], ease = Easing("OutQuart"), opacity = 100, rotation = 0, position = [0, 0], angleOffset = -180 * tileAppearAnimation * adofaiLevel[i + 1]["bpmScale"])

adofaiParser.save(adofaiLevel, "test2.adofai")

# Beats Ahead Calculation
adofaiParser.reload()
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

tileInit = 120
tileAppearAnimation = trackAppearAnim[0]
tileDisappearAnimation = 0
for i in range(adofaiLevel.length):
    if i + 1 in trackAppearAnim:
        adofaiLevel.setBPMScalePoint(adofaiLevel[i + 1]["bpm"])
        tileAppearAnimation = trackAppearAnim[i + 1]
    
    adofaiLevel.moveTrack(i + 1, range = -1, duration = 4 * adofaiLevel[i + 1]["bpmScale"], ease = Easing("InQuart"), opacity = 0, rotation = -20, position = [getrand() * 1.5, -3], scale = [80, 80], angleOffset = 180 * tileDisappearAnimation * adofaiLevel[i + 1]["bpmScale"])

    adofaiLevel.moveTrack(i + 1, range = 0, duration = 0, ease = Easing("Linear"), opacity = 0, rotation = 15, position = [0.2, 0.6], angleOffset = -180 * tileInit)
    adofaiLevel.moveTrack(i + 1, range = 0, duration = 4 * adofaiLevel[i + 1]["bpmScale"], ease = Easing("OutQuart"), opacity = 100, rotation = 0, position = [0, 0], angleOffset = -180 * tileAppearAnimation * adofaiLevel[i + 1]["bpmScale"])

adofaiParser.save(adofaiLevel, "test3.adofai")