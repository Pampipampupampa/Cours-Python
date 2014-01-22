#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""MULTIPLE INHERITANCE : I HAVE A LOT OF MOTHER """
"SAM AND MAX"

########################################
#### Classes and Methods imported : ####
########################################

#####################
#### Constants : ####
#####################

#######################################
#### Classes, Methods, Functions : ####
#######################################


class Weapon(object):
    """Class to create new powerful weapons"""
    def __init__(self, nom, damage):
        self.nom = nom
        self.damage = damage

    def attack(self, target):
        if target.armor:
            damage = target.armor.defend(self.damage)
            target.health -= damage
        else:
            target.health -= self.damage
        if target.health < 0:
            target.health = 0
        print("{} health = {}".format(target.name, target.health))


class Armor(object):
    """Class to create awesome armors"""
    def __init__(self, nom, resistance):
        self.nom = nom
        self.resistance = resistance

    def defend(self, damage):
        damage = damage - self.resistance
        if damage < 0:
            return 0
        return damage


# Multiple inheritance : from weapon and armor
class ReprisalArmor(Armor, Weapon):
    """Class to create powerful and awesome weapon armored"""
    def __init__(self, nom, damage, resistance):
        Armor.__init__(nom, resistance)
        Weapon.__init__(nom, damage)


class PoisonWeapon(Weapon):
    """A dangerous weapon be careful with it"""
    def __init__(self, name, damage, poison):
        super().__init__(name, damage)
        self.poison = poison

    def attack(self, target):
        super().attack(target)
        target.health -= self.poison
        if target.health < 0:
            target.health = 0
        print("{} hit by poison, health = {}".format(target.name, target.health))


class Hero(object):
    """Class to create your hero"""
    def __init__(self, name, health, weapon=None, armor=None):
        self.name = name
        self.health = health
        self.weapon = weapon
        self.armor = armor

    def fight(self, target):
        print("{} attaque {}".format(self.name, target.name))
        while True:
            if self.weapon:
                self.weapon.attack(target)
            if target.health <= 0:
                break
            if target.weapon:
                target.weapon.attack(self)
            if self.health <= 0:
                break
        if self.health > 0:
            print("{} win and earns so much glory with this awesome fight".format(self.name))
        else:
            print("{} is just another loser ...".format(self.name))


########################
#### Main Program : ####
########################

# Create an hero and a prat
excalibur = Weapon("Excalibur", 500)
wood_stick = Weapon("Wood Stick", 2)
suit = Armor("Great Suit", 10)

hero = Hero("Arthur", 2000, excalibur)
morgana = Hero("Morgane", 2000, wood_stick, suit)

# Start fight
morgana.fight(hero)


# New fight with magic help
hero.health = 2000
morgana.health = 2000
morgana.weapon = PoisonWeapon("Basilic sword", 100, 500)

# Start fight
morgana.fight(hero)
