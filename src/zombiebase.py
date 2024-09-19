import objectbase

class zombiebaseob(objectbase.Object):
    def __init__(self, id, img_pos):
        super().__init__(id, img_pos)
        self.eat_flag = False

    def CheckPos_L(self):
        judgement = super(zombiebaseob,self).CheckPos()
        if judgement:
            self.pos[0] -= self.get_Data()['SPEED_L']
        else:
            #Sometimes this class may be inherited, so return.
            return judgement
        
    def Move(self):
        if not self.eat_flag:
            self.CheckPos_L()

    def draw(self, DS):
        if self.pos[0] >= 200:
            super().draw(DS)