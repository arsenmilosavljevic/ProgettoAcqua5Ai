from backend.GlobalManager import GlobalManager

class GameState:

    def __init__(self):

        self.year = GlobalManager.INSTANCE.time.year

        self.water_a = 100
        self.water_b = 100

        self.humor_a = 100      # <-- aggiunto
        self.humor_b = 100      # <-- aggiunto

        self.dam_built = False
        self.request_done = False
        self.war = False

        self.intro_choice = None  # <-- aggiunto