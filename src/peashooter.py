import objectbase
import peabullet
from const import *

class peashooter(objectbase.Object):
    def __init__(self, id, img_pos):
        super().__init__(id, img_pos)
        self.cnt = 0
    def CheckSummon(self):# Here happened a strange bug while wrting so I use a cnt.
        if self.index == 8 and self.cnt == 0:
            self.cnt += 1
            return True
        elif self.index == 0:
            self.cnt = 0
        else:
            return False

    def Summon(self):
        judgement = self.CheckSummon()
        if judgement:
            return peabullet.peabullet(NORM_PEABULLET_ID, (self.pos[0] + 80, self.pos[1] + 35))
        else:
            return None
        
        