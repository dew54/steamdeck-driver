class Kinetic:
    def __init__(self, index=None):
        self.index = index

        self.roll = None
        self.pitch = None
        self.yaw = None
        self.x = None
        self.y = None
        self.z = None

        self.VRoll = None
        self.VPitch = None
        self.VYaw = None
        self.VX = None
        self.VY = None
        self.VZ = None

        self.ARoll = None
        self.APitch = None
        self.AYaw = None
        self.AX = None
        self.AY = None
        self.AZ = None

    def updateAngle(self, roll, pitch, yaw):
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    def updateAngleV(self, VRoll, VPitch, VYaw):
        self.VRoll = VRoll
        self.VPitch = VPitch
        self.VYaw = VYaw

    def updateAngleA(self, ARoll, APitch, AYaw):
        self.ARoll = ARoll
        self.APitch = APitch
        self.AYaw = AYaw

    def updatePosition(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def updatePositionV(self, VX, VY, VZ):
        self.VX = VX
        self.VY = VY
        self.VZ = VZ    

    def updatePositionA(self, AX, AY, AZ):
        self.AX = AX
        self.AY = AY
        self.AZ = AZ

    def updateConfiguration(self, angles, positions):
        self.updateAngle(*angles)
        self.updatePosition(*positions)

    def updateVelocity(self, anglesV, positionsV):
        self.updateAngleV(*anglesV)
        self.updatePositionV(*positionsV)
    
    def updateAcceleration(self, anglesA, positionsA):
        self.updateAngleA(*anglesA)
        self.updatePositionA(*positionsA)
        
    def getAngle(self):
        return self.roll, self.pitch, self.yaw      
    
    def getAngleV(self):
        return self.VRoll, self.VPitch, self.VYaw
    
    def getAngleA(self):
        return self.ARoll, self.APitch, self.AYaw   
    
    def getPosition(self):
        return self.x, self.y, self.z
    
    def getPositionV(self):
        return self.VX, self.VY, self.VZ
    
    def getPositionA(self):
        return self.AX, self.AY, self.AZ
    