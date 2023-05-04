class ZigAtSymbol(str):
    def __new__(cls, s, from_parser=False):
        s = str(s)
        return super().__new__(cls, s)
    def __repr__(self):
        return "@\"{}\"".format(self)
    

    
