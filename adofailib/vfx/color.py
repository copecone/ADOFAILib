class Color:
    def __init__(self, *args):
        if len(args) == 1:
            colorTuple = Color.convertHex(args[0])

            self.red = colorTuple[0]
            self.green = colorTuple[1]
            self.blue = colorTuple[2]
            self.alpha = colorTuple[3]
        else:
            self.red = args[0]
            self.green = args[1]
            self.blue = args[2]
            if len(args) > 3:
                self.alpha = args[3]
            else: self.alpha = 255

    @staticmethod
    def convertHex(hexstr: str):
        result = []
        if hexstr.startswith("#"): hexstr = hexstr[1:]

        for i in (0, 2, 4):
            result.append(int(hexstr[i:i+2], 16))

        if len(hexstr) > 6:
            result.append(int(hexstr[6:8], 16))
        else: result.append(255)

        return tuple(result)
    
    def toHex(self):
        return "{:02x}{:02x}{:02x}{:02x}".format(self.red, self.green, self.blue, self.alpha)
    
Color.WHITE = Color("#ffffffff")