import json
from adofailib.vfx import *
from adofailib.vfx.easing import Easing
from adofailib.vfx.decoration import ADOFAIDecoration
from adofailib.vfx.color import Color

class ADOFAILevel:
    chartActions = [
        "Twirl", "SetSpeed", "Hold", "Pause", # Basic Chart Actions
        "EditorComment", "Bookmark", "SetPlanetRotation", "ScaleRadius", "ScalePlanets", "PositionTrack" # Extra Chart Actions
    ]

    def __init__(self, data: dict):
        self.data = data
        self.length = len(self.data["angleData"])
        self.defaultBPM = self.data["settings"]["bpm"]
        self.defaultBPMForScale = self.defaultBPM
        self._deco = []

        self.makeCache()

    def makeCache(self):
        self._actionCache = {}
        for action in self.data["actions"]:
            if "floor" in action:
                if action["floor"] in self._actionCache:
                    self._actionCache[action["floor"]].append(action)
                else: self._actionCache[action["floor"]] = [action]

        currentBPM = self.data["settings"]["bpm"]
        self._bpmCache = [currentBPM]

        for index, angle in enumerate(self.data["angleData"]):
            if index + 1 in self._actionCache:
                for action in self._actionCache[index + 1]:
                    if action["eventType"] == "SetSpeed":
                        if action["speedType"] == "Bpm": currentBPM = action["beatsPerMinute"]
                        if action["speedType"] == "Multiplier": currentBPM *= action["bpmMultiplier"]
            
            self._bpmCache.append(currentBPM)
    
    def getChartData(self) -> dict:
        angleData = self.data["angleData"]
        settings = self.data["settings"]

        actions = []
        for action in self.data["actions"]:
            if action["eventType"] in ADOFAILevel.chartActions:
                actions.append(action)

        return {"angleData": angleData, "settings": settings, "actions": actions}
    
    def removeVFX(self):
        self.data = self.getChartData()

    def disable(self, target):
        if target == "TrackDisappearAnimation":
            self.data["settings"]["trackDisappearAnimation"] = "None"
            self.data["settings"]["beatsBehind"] = 0
        if target == "TrackAppearAnimation":
            self.data["settings"]["trackAnimation"] = "None"
            self.data["settings"]["beatsAhead"] = 0

    def genData(self):
        if "decorations" not in self.data:
            self.data["decorations"] = []
        
        for deco in self._deco:
            self.data["decorations"].append(deco.convert())
            for event in deco.events:
                self.data["actions"].append(event)

    def addDecoration(self, decoration: decoration.ADOFAIDecoration):
        self._deco.append(decoration)

    def moveTrack(
        self, tile: int = 0, range: tuple[int] = (0, 0), gap: int = 0, # Range Settings
        duration: float = 0, angleOffset: float = 0, # Timing Settings
        opacity: float = None, scale: list[float] = [None, None], rotation: float = None, position: list[float] = [None, None], # Move Settings
        ease: Easing = Easing.Linear, eventTag: list[str] = []
    ):
        if type(range) == int:
            range = [range, range]

        result = {
            "floor": tile, "eventType": "MoveTrack", "startTile": [range[0], "ThisTile"], "endTile": [range[1], "ThisTile"], "gapLength": gap,
            "duration": duration, "angleOffset": angleOffset, "ease": ease.type, "eventTag": " ".join(list(map(str, eventTag)))
        }

        if opacity != None: result["opacity"] = opacity
        if scale != [None, None]: result["scale"] = scale
        if position != [None, None]: result["positionOffset"] = position
        if rotation != None: result["rotationOffset"] = rotation

        self.data["actions"].append(result)

    def moveDecoration(
        self, tile: int = 0, duration: float = 0, angleOffset: float = 0, # Timings Options
        file: str = None, position: tuple[float] = (None, None), rotation: float = None, scale: tuple[float] = (None, None), opacity: float = None, color: Color = None, # Moving Options
        ease: Easing = Easing.Linear, tag: list[str] = [], eventTag: list[str] = [], # Extra Options
    ):
        decoMove = ADOFAIDecoration.global_move(tile, duration, angleOffset, file, position, rotation, scale, opacity, color, ease, tag, eventTag)
        self.data["actions"].append(decoMove)
        return decoMove

    def setBPMScalePoint(self, bpm):
        self.defaultBPMForScale = bpm

    def __getitem__(self, key):
        return {"bpm": self._bpmCache[key], "bpmScale": self._bpmCache[key] / self.defaultBPMForScale}

