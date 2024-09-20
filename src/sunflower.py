import objectbase
import sunshine
from const import *

class sunflower(objectbase.Object):
    def Summon(self):
        judgement = self.CheckSummon()
        if judgement:
            return sunshine.sunshine_summon_sunflower(SUNSHINE_ID, ( self.pos[0] + 35, self.pos[1] + 10 ))
        else:
            return None