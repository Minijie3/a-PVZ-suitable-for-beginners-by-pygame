import image
import time
import data_object

class Object(image.Image):
    def __init__(self, id, img_pos):
        self.indextime = 0
        self.postime = 0
        self.summontime = time.time()
        self.id = id
        self.hassummon = self.get_Data()['HAS_SUMMON']
        self.hp = self.get_Data()['HP']
        self.attack = self.get_Data()['ATTACK']
        super(Object,self).__init__(
            self.get_Data()['PATH'],
            self.get_Data()['INDEX'],
            self.get_Data()['INDEX_CNT'],
            self.get_Data()['SIZE'],
            img_pos,
        )

    def get_Data(self):
        return data_object.data[self.id]

    def get_postime(self):
        return self.get_Data()['POS_TIME']
    
    def get_indextime(self):
        return self.get_Data()['INDEX_TIME']
    
    def get_summontime(self):
        return self.get_Data()['SUMMON_TIME']
    
    def CheckCanLoot(self):
        return self.get_Data()['CAN_LOOT']
    
    def get_price(self):
        return self.get_Data()['PRICE']
    
    def get_type(self):
        return self.get_Data()['TYPE']

    #The pic may not be kinetic, just provide a judgement.
    def CheckPos(self):
        #What should be attention is that time.time() != 0 at the beginning.
        if time.time() - self.postime <= self.get_postime():
            return False
        else:
            self.postime = time.time()
            return True

    def CheckIndex(self):
        if time.time() - self.indextime <= self.get_indextime():
            return
        else:
            self.indextime = time.time()
            self.index += 1
            if self.index == self.indexcount:
                self.index = 0
            self.UpdateIndex(self.index)
            #This guarantee that even if indexcount == 0, you can still use Checkindex() due to the existance of UpdateImage.
                
    def CheckSummon(self):
        if time.time() - self.summontime <= self.get_summontime():
            return False
        else:
            self.summontime = time.time()
            return True

    def Summon(self):
        pass
    def Move(self):
        pass

    def update(self):
        self.CheckIndex()
        self.Move()