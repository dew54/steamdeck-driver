class Kinetic:
    def __init__(self, index=0):
        self.index = index
        
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.x = 0
        self.y = 0
        self.z = 0

        self.VRoll = 0
        self.VPitch = 0
        self.VYaw = 0
        self.VX = 0
        self.VY = 0
        self.VZ = 0

        self.ARoll = 0
        self.APitch = 0
        self.AYaw = 0
        self.AX = 0
        self.AY = 0
        self.AZ = 0

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
    