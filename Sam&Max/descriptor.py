#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""HOW TO UNDERTAND DESCRIPTORS AND PATTERN OBSERVER"""
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


class SignalDescriptor(object):
    # class attribute : can be call from inside or outside a class instance
    abonnements = {}

    @classmethod
    def previens_moi(cls, obj, attr, callback):
        # setdefault return dict values and create it if doesn't exist
        # add allows to add another element inside a set
        # Here a function reference is added to the set : it's a callback
        cls.abonnements.setdefault(obj, {}).setdefault(attr, set()).add(callback)

    def __init__(self, nom, valeur_initiale=None):
        self.nom = nom
        self.valeur = valeur_initiale

    def __get__(self, obj, objtype):
        # Before get value all functions are run
        # self.nom limits to functions inside abonnement[cls][cls.nom]
        # functions are store in a set
        for callback in self.abonnements.get(obj, {}).get(self.nom, ()):
            callback('get', obj, self.nom, self.valeur)
        return self.valeur

    def __set__(self, obj, valeur):
        # Before set value all functions are run
        # self.nom limits to functions inside abonnement[cls][cls.nom]
        # functions are store in a set
        for callback in self.abonnements.get(obj, {}).get(self.nom, ()):
            callback('set', obj, self.nom, self.valeur, valeur)
        self.valeur = valeur


class Joueur(object):

    credits = SignalDescriptor("credits", 0)
    tests = SignalDescriptor("tests", 0)
    outch = SignalDescriptor("tests", 288)


def monitorer_credits(action, obj, attribut, valeur_actuelle, nouvelle_valeur=None):
    if action == 'set':
        print("Les {} ont changé:".format(attribut))
    else:
        print("Les {} ont été consultés:".format(attribut))
    print(action, obj, attribut, valeur_actuelle, nouvelle_valeur)


#
#
# PATTERN OBSERVER
#
#
def evenement(nom):
    # Make sure list event can be call and initialize it
    evenement.abonnements = getattr(evenement, 'abonnements', {})

    # Call all callbacks of the event in parameter
    evenement.trigger = lambda e: [f(e) for f in evenement.abonnements[e]]

    # wrapper
    def decorateur(func):

        # Add decorated function as callback to this event
        evenement.abonnements.setdefault(nom, []).append(func)

        # Return function without changes
        return func

    return decorateur


@evenement('evenement1')
@evenement('evenement2')
def reagir_a_evenement(evenement):
    # Function must accept the event as argument
    print("Oh, evenement '%s' a eu lieu" % evenement)


@evenement('evenement1')
def moi_aussi(evenement, choco=33):
    # Can add more argument of course !!
    print("Cool, moi aussi j'ai reagit a l'evenement '%s'" % evenement)
    print(choco)

########################
#### Main Program : ####
########################

# perso = Joueur()
# print(SignalDescriptor.abonnements, perso.credits, type(perso.credits), "\n\n")

# # Add a callback to credit attribute
# SignalDescriptor.previens_moi(perso, 'credits', monitorer_credits)
# perso.credits  # GET
# print("--------")
# perso.credits = 22  # SET
# print("--------")
# perso.credits -= 10  # GET and SET
# print("--------")
# perso.credits += 10  # GET and SET
# print("\n\n")

# # Add callback to tests attribute
# SignalDescriptor.previens_moi(perso, 'tests', monitorer_credits)

# # Create two class attribute with the same name force to use the same functions
# # for these attributes (see get and set comments)
# print(perso.tests, perso.outch)

#
#
# PATTERN OBSERVER
#
#
evenement.trigger('evenement1')
evenement.trigger('evenement2')
print(evenement.abonnements)
