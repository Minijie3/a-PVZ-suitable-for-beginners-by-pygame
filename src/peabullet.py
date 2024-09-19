import objectbase
from const import *

class peabullet(objectbase.Object):
    def CheckPos_R(self):
        judgement = super(peabullet,self).CheckPos()
        if judgement:
            self.pos[0] += self.get_Data()['SPEED_R']
        else:
            return judgement
        
    def Move(self):
        self.CheckPos_R()