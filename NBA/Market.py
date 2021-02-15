from NBA.Game import Game
class Market:
    def __init__(self, details, game):
        self.marketId = details.get('market')
        super().__init__(game)