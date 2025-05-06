from kinetic import Kinetic
from steamdeck import SteamDeck


class Platform:
    def __init__(self, deck: SteamDeck, nKinetics=1):
        self.deck = deck
        self.kinetic_0 = Kinetic(0)

        # for i in range(nKinetics):
        #     setattr(self, f'kinetic_{i}', Kinetic(i))

