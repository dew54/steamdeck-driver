from roboPlatform import Platform

class MechanumPlatform(Platform):
    def __setattr__(self, name, value):
        return super().__setattr__(name, value)