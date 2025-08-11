from roboPlatform import Platform
from kinetic import Kinetic

class MechanumPlatform(Platform):

    def updateKinetic(self, k_index=0):
        self.deck.poll()

        vx = -(self.deck.get_axis(0)/32000)
        vy = (self.deck.get_axis(1)/32000)
        vw = -(self.deck.get_axis(2)/32000)

        positionV = (vx, vy, 0)
        angleV = (0, 0, vw)
        self.kinetic_0.updateVelocity(angleV, positionV)

    def getKinetic(self):
        return self.kinetic_0
        