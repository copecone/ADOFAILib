import json
from adofailib import level

class ADOFAIParser:
    def __init__(self, path: str):
        self.path = path
        self.file = open(path, "r", encoding="utf-8")

        self.content = ""
        self.parsed = {"parsed": False}

        self._parse()
    
    def _parse(self):
        self.content = self.file.read()
        if self.content[0] == u'\ufeff':
            self.content = self.content[1:]

        self.content = self.content.replace(", },\n", "},\n")
        self.parsed = json.loads(self.content)

    def getLevel(self):
        return level.ADOFAILevel(self.parsed)
    
    @staticmethod
    def getDefaultWith(data: dict):
        angleData = [0 for _ in range(10)]
        if "angleData" in data:
            angleData = data["angleData"]
        
        settings = {
            "requiredMods": [], # Mod Settings
		    "version": 12, # ADOFAI Level File Version
		    "artist": "", "specialArtistType": "None", "artistPermission": "", "song": "", "author": "", # Basic Level Settings
		    "previewImage": "", "previewIcon": "", "previewIconColor": "003f52", "previewSongStart": 0, "previewSongDuration": 10, # Preview Settings
		    "seizureWarning": "Disabled", # Warning Settings
		    "levelDesc": "", "levelTags": "", "artistLinks": "", "difficulty": 1, # Level Desc Settings
		    "songFilename": "", # Music File
		    "bpm": 100, "volume": 100, "offset": 0, "pitch": 100, # Music Settings
		    "hitsound": "Kick", "hitsoundVolume": 100, # Hitsound Settings
		    "countdownTicks": 4, "separateCountdownTime": "Enabled", # Level Countdown Settings
		    "trackColor": "debb7b", "secondaryTrackColor": "ffffff", "trackStyle": "Standard", "trackGlowIntensity": 100, # Track Color Settings
		    "trackColorType": "Single", "beatsAhead": 3, "trackDisappearAnimation": "None", "beatsBehind": 4, "trackAnimation": "None", "trackColorAnimDuration": 2, "trackColorPulse": "None", "trackPulseLength": 10, # Track Animation Settings
		    "backgroundColor": "000000", "showDefaultBGIfNoImage": "Enabled", "bgImage": "", "bgImageColor": "ffffff", # Background Settings
            "parallax": [100, 100], "bgDisplayMode": "FitToScreen", "lockRot": "Disabled", "loopBG": "Disabled", "unscaledSize": 100, # Background Extra Settings
		    "relativeTo": "Player", "position": [0, 0], "rotation": 0, "zoom": 100, "pulseOnFloor": "Enabled", "startCamLowVFX": "Disabled",
		    "bgVideo": "", "loopVideo": "Disabled", "vidOffset": 0, # Video Background Settings
		    "floorIconOutlines": "Disabled", "stickToFloors": "Enabled", # Floor Settings
		    "planetEase": "Linear", "planetEaseParts": 1, "planetEasePartBehavior": "Mirror", # Planet Settings
		    "legacyFlash": False, "legacyCamRelativeTo": False, "legacySpriteTiles": False, # Legacy Settings
            "customClass": "", # Useless Dev Settings
	    }

        if "settings" in data:
            settings = data["settings"]

        actions = []
        if "actions" in data:
            actions = data["actions"]

        decorations = []
        if "decorations" in data:
            decorations = data["decorations"]

        return {"angleData": angleData, "settings": settings, "actions": actions, "decorations": decorations}
    
    def save(self, level: level.ADOFAILevel, path: str = None):
        self.file.close()
        level.genData()

        if path == None:
            self.file = open(self.path, "w", encoding="utf-8")
        else:
            self.file = open(path, "w", encoding="utf-8")

        self.file.write(json.dumps(self.getDefaultWith(level.data), sort_keys = True, indent = 4))
        self.file.close()

    def reload(self):
        self.file = open(self.path, "r", encoding="utf-8")
        
        self.content = ""
        self.parsed = {"parsed": False}

        self._parse()
