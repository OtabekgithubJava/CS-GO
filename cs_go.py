from abc import ABC, abstractmethod
from os import system

system("cls")


class WeaponModel(ABC):
    @abstractmethod
    def __init__(self, name: str, damage: int, cost: float):
        pass


class PlayerModel(ABC):
    @abstractmethod
    def __init__(self, name: str):
        pass


class GameModel(ABC):
    @abstractmethod
    def __init__(self, map: str):
        pass

    @abstractmethod
    def addCounters(self, player):
        pass

    @abstractmethod
    def addTerrorist(self, player):
        pass

    @abstractmethod
    def buyWeapon(self, player, weapon):
        pass

    @abstractmethod
    def shoot(self, player1, player2):
        pass


class Weapon(WeaponModel):
    def __init__(self, name: str, damage: int, cost: float, type: str):
        self.name = name
        self.damage = damage
        self.cost = cost
        self.type = type

    def __str__(self):
        return f"""
name: {self.name}
damage: {self.damage}
cost: {self.cost}
type: {self.type}
"""


WEAPONS = {
    "knife": Weapon("knife", 100, 0, "knife"),
    "ak-47": Weapon("ak-47", 30, 2100, "avtomat"),
    "awp": Weapon("AWP", 100, 4000, "avtomat"),
    "deagle": Weapon("deagle", 20, 700, "pistol"),
    "P90": Weapon("P90", 10, 500, "pistol"),
    "shotgun": Weapon("shotgun", 35, 2150, "avtomat"),
}


class Player(PlayerModel):
    def __init__(self, name: str = "Player0"):
        self.name = name
        self.__health = 100
        self.__cash = 12000
        self.knife = WEAPONS["knife"]
        self.pistol = WEAPONS["P90"]
        self.gun = None
        self.activeWeapon = self.pistol

    def set_cash(self, price: float):
        self.__cash += price

    def get_cash(self) -> int:
        return self.__cash

    def set_health(self, damage: int):
        self.__health += damage

    def get_health(self) -> int:
        return self.__health

    def set_activeWeapon(self, weaponNum: int):
        if weaponNum == 1:
            self.activeWeapon = self.gun
        elif weaponNum == 2:
            self.activeWeapon = self.pistol
        elif weaponNum == 3:
            self.activeWeapon = self.knife

    def __str__(self):
        return f"""
name: "{self.name}"
health: {self.__health}%
cash: {self.__cash}$

activeWeapon {self.activeWeapon}
"""


class Game(GameModel):
    def __init__(self, map: str):
        self.map = map
        self.counters = []
        self.terrorists = []

    def addCounters(self, player: Player):
        player.type = "counter"
        self.counters.append(player)

    def addTerrorist(self, player: Player):
        player.type = "terrorist"
        self.terrorists.append(player)

    def buyWeapon(self, player: Player, weapon: Weapon):
        if player not in self.terrorists and player not in self.counters:
            return "Siz o'yinda emassiz"
        if player.get_cash() < weapon.cost:
            return "Pul yetarli emas."
        if player.get_health() <= 0:
            return "Keyingi o'yinda urinib ko'ring"

        player.set_cash(-weapon.cost)
        if weapon.type == "avtomat":
            player.gun = weapon
        if weapon.type == "pistol":
            player.pistol = weapon
        if weapon.type == "knife":
            player.knife = weapon

        player.activeWeapon = weapon

    def shoot(self, player1: Player, player2: Player, getWeapon: bool = False):
        if player1.type == player2.type:
            return "Sizlar bitta komandasiz"
        if player1.get_health() <= 0:
            return "Siz o'lgansiz"
        if player2.get_health() <= 0:
            return "Allaqachon o'lgan"
        player2.set_health(-player1.activeWeapon.damage)
        if player2.get_health() <= 0:
            player1.set_cash(500)
            if getWeapon:
                player1.gun = player2.gun if player2.gun else player1.gun
            player2.gun = None
            player2.pistol = WEAPONS["P90"]
            player2.knife = WEAPONS["knife"]


eshmat = Player("eshmat vor zakon")
toshmat = Player("toshmat")

game = Game("dust 2x2")
game.addCounters(eshmat)
game.addTerrorist(toshmat)
game.buyWeapon(eshmat, WEAPONS["deagle"])
game.shoot(eshmat, toshmat)
game.buyWeapon(toshmat, WEAPONS["awp"])
game.shoot(toshmat, eshmat)
print(game.shoot(toshmat, eshmat))

print(eshmat)
print(toshmat)