from kinetic import Kinetic


class Platform:
    def __init__(self, name, version, nKinetics=1):
        self.name = name
        self.version = version
        for i in range(nKinetics):
            setattr(self, f'kinetic_{i}', Kinetic(i))
