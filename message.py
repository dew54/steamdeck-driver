import msgpack
import base64

class Message:

    def __init__(self):
        self.state = {
            "index": 0,
            "roll": 0,
            "pitch": 0,
            "yaw": 0,
            "x": 0,
            "y": 0,
            "z": 0,
            "VRoll": 0,
            "VPitch": 0,
            "VYaw": 0,
            "VX": 0,
            "VY": 0,
            "VZ": 0,
            "ARoll": 0,
            "APitch": 0,
            "AYaw": 0,
            "AX": 0,
            "AY": 0,
            "AZ": 0
        }
    
    def packKinetic(self, kinetic):
        self.state["index"] = kinetic.index
        self.state["roll"] = kinetic.roll
        self.state["pitch"] = kinetic.pitch
        self.state["yaw"] = kinetic.yaw
        self.state["x"] = kinetic.x
        self.state["y"] = kinetic.y
        self.state["z"] = kinetic.z
        self.state["VRoll"] = kinetic.VRoll
        self.state["VPitch"] = kinetic.VPitch
        self.state["VYaw"] = kinetic.VYaw
        self.state["VX"] = kinetic.VX
        self.state["VY"] = kinetic.VY
        self.state["VZ"] = kinetic.VZ
        self.state["ARoll"] = kinetic.ARoll
        self.state["APitch"] = kinetic.APitch
        self.state["AYaw"] = kinetic.AYaw
        self.state["AX"] = kinetic.AX
        self.state["AY"] = kinetic.AY
        self.state["AZ"] = kinetic.AZ

        packed = msgpack.packb(self.state)

        base64_str = base64.b64encode(packed).decode('utf-8')
        return base64_str

        