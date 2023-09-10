import hashlib
from adofailib.vfx.easing import Easing
from adofailib.vfx.color import Color
from adofailib.vfx.hitbox import ADOFAIFailHitBox

class ADOFAIDecoration:
    _deco_id = 0

    def __init__(
        self, path: str, tile: int = 0, # Basic Settings
        relative: str = "Tile", pivotOffset: list[float] = [0, 0], position: list[float] = [0, 0], rotation: float = 0, scale: list[float] = [100, 100], tiling: list[int] = [1, 1], # Transform Settings
        depth: int = -1, parallax: list[float] = [0, 0], color: Color = Color.WHITE, opacity: float = 100, # Movement & Color Settings
        tags: list[str] = [], locked: bool = False, imageSmoothing: bool = True, failHitBox: ADOFAIFailHitBox = None # Extra Settings
    ):
        self.path = path
        self.tile = tile

        self.relative = relative
        self.pivotOffset = pivotOffset
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.tiling = tiling

        self.depth = depth
        self.parallax = parallax
        self.color = color
        self.opacity = opacity

        self.tags = tags
        self.locked = locked
        self.imageSmoothing = "Enabled" if imageSmoothing else "Disabled"
        self.failHitBoxStatus = "Enabled" if failHitBox != None else "Disabled"
        self.failHitBox = failHitBox if failHitBox != None else ADOFAIFailHitBox()

        self.id = ADOFAIDecoration._deco_id
        ADOFAIDecoration._deco_id += 1

        self.tags.append(f"_generated_{self._getId()}")
        self.events = []

    def _getId(self) -> str:
        return hashlib.sha384(str(self.id).encode()).hexdigest()

    def move(
        self, tile: int = 0, duration: float = 0, angleOffset: float = 0, # Timings Options
        file: str = None, position: tuple[float] = (None, None), rotation: float = None, scale: tuple[float] = (None, None), opacity: float = None, color: Color = None, # Moving Options
        ease: Easing = Easing.Linear, eventTag: list[str] = [], # Extra Options
    ):
        moveEvent = ADOFAIDecoration.global_move(tile, duration, angleOffset, file, position, rotation, scale, opacity, color, ease, [f"_generated_{self._getId()}"], eventTag)
        self.events.append(moveEvent)
        return moveEvent

    @staticmethod
    def global_move(
        tile: int = 0, duration: float = 0, angleOffset: float = 0, # Timings Options
        file: str = None, position: tuple[float] = (None, None), rotation: float = None, scale: tuple[float] = (None, None), opacity: float = None, color: Color = None, # Moving Options
        ease: Easing = Easing.Linear, tag: list[str] = [], eventTag: list[str] = [], # Extra Options
    ):
        result = {"eventType": "MoveDecorations", "floor": tile, "duration": duration, "angleOffset": angleOffset}
        if file != None: result["decorationImage"] = file
        if position != (None, None): result["positionOffset"] = list(position)
        if rotation != None: result["rotationOffset"] = rotation
        if scale != (None, None): result["scale"] = list(scale)
        if opacity != None: result["opacity"] = opacity
        if color != None: result["color"] = color.toHex()
        result["ease"] = ease.type
        result["tag"] = " ".join(list(map(str, tag)))
        result["eventTag"] = " ".join(list(map(str, eventTag)))

        return result
    
    def convert(self) -> dict:
        return {
            "floor": self.tile, "eventType": "AddDecoration", "locked": self.locked, "decorationImage": self.path, 
            "position": self.position, "pivotOffset": self.pivotOffset, "rotation": self.rotation, "relativeTo": self.relative, "scale": self.scale, "tile": self.tiling,
            "color": self.color.toHex(), "opacity": self.opacity, "depth": self.depth, "parallax": self.parallax, "tag": " ".join(list(map(str, self.tags))),
            "failHitBox": self.failHitBoxStatus, "failHitBoxType": self.failHitBox.shape, "failHitBoxScale": self.failHitBox.scale, "failHitBoxOffset": self.failHitBox.offset, "failHitBoxRotation": self.failHitBox.rotation
        }
