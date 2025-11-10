""""""
class PlayerStats:
    def __init__(self, name, player_class):
        self.name = name
        self.player_class = player_class
        self.level = 1
        self.experience = 0
        self.health = 100
        self.mana = 100
        self.stamina = 100

    def level_up(self):
        self.level += 1
        self.health += 10
        self.mana += 5
        self.stamina += 5
        print(f"{self.name} leveled up to level {self.level}!")

    def gain_experience(self, amount):
        """Gain experience and level up if threshold (100xp) is reached."""
        self.experience += amount
        if self.experience >= 100:  # Change threshold to be dynamic based on level
            self.experience -= 100
            self.level_up()
