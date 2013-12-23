#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""CLASSE D'UNE ENTITÉ POUR LA BASE D'UNE CLASSE DE MONSTRE AVEC AI"""
"APPRESS BEGINNING GAME DEVELOPMENT - CHAPTER 6"

###########################################
#### Importation fonction et modules : ####
###########################################

import sys
sys.path.append('/home/pampi/Documents/Git/Cours-Python/Livre/BeginningGameDevelopmentWithPygame/Stock')
from vector2d import Vector2D
import pygame
from pygame.locals import *
from random import randint

##############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : ####
##############################################################################


class State:
    """Base class for the states"""
    def __init__(self, name):
        self.name = name

    def do_actions(self):
        pass

    def check_conditions(self):
        pass

    def entry_actions(self):
        pass

    def exit_actions(self):
        pass


class StateMachine:
    """Base class for the state machine"""
    def __init__(self):
        self.state = {}  # store the states
        self.active_state = None  # Active state

    def add_state(self, state):
        """Add a state to the internal dico"""
        self.state[state.name] = state

    def think(self):
        """Load the active state actions and conditions"""
        if self.active_state is None:
            return
        self.active_state.do_actions()
        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)

    def set_state(self, new_state_name):
        """Change the current state and perform exit/entry actions"""
        if self.active_state is not None:
            self.active_state.exit_actions()  # Close last state

        self.active_state = self.state[new_state_name]
        self.active_state.entry_actions()  # Change entity stats


class World:
    """Entities living World"""
    def __init__(self):
        self.entities = {}  # All entities
        self.entity_id = 0  # last entity id

        # Draw the nest
        self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
        self.background.fill((255, 255, 255))
        pygame.draw.circle(self.background, (200, 255, 200), NEST_POSITION,
                           int(NEST_SIZE))

    def add_entity(self, entity):
        """Add a new entity to the world"""
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self, entity):
        """Remove an entity"""
        del self.entities[entity.id]

    def get_entity(self, entity_id):
        """Find an entity with it id"""
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None

    def process(self, time_passed):
        """Launch entity thinking and movement"""
        time_passed_seconds = time_passed / 1000
        for entity in list(self.entities.values()):
            entity.process(time_passed_seconds)

    def render(self, surface):
        """Draw the background and all the entities"""
        surface.blit(self.background, (0, 0))
        for entity in list(self.entities.values()):
            entity.render(surface)

    def get_close_entity(self, name, location, range=100):
        """Find other entities in a range around"""
        location = Vector2D(*location)
        for entity in list(self.entities.values()):
            if entity.name == name:
                distance = location.get_distance(entity.location)
                if distance < range:
                    return entity
        return None


class GameEntity:
    """Base class for entity development"""
    def __init__(self, world, name, image):
        self.world = world
        self.name = name
        self.image = image
        self.location = Vector2D(0, 0)
        self.destination = Vector2D(0, 0)
        self.speed = 0
        self.brain = StateMachine()  # Entity brain
        self.id = 0

    def render(self, surface):
        """Posting the entity to the center instead top corner.
           We do this because the entities will be treated as circles
           with a point and a radius which will simplify the math when we need
           to detect interactions with other entities"""
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x-w/2, y-h/2))

    def process(self, time_passed):
        """time_passed in seconde"""
        self.brain.think()

        if self.speed > 0 and self.location != self.destination:
            vec_to_destination = self.destination - self.location
            distance_to_destination = vec_to_destination.get_magnitude()
            heading = vec_to_destination.normalized()
            # Avoid exceeding the destination
            travel_distance = min(distance_to_destination,
                                  time_passed * self.speed)
            self.location += travel_distance * heading


class Ant(GameEntity):
    """Create a new ant inthe world based on GameEntity class"""
    def __init__(self, world, image):
        super().__init__(world, "ant", image)
        # GameEntity.__init__(self, world, "ant", image)

        # Instance of each states
        exploring_state = AntStateExploring(self)
        seeking_state = AntStateSeeking(self)
        delivering_state = AntStateDelivering(self)
        hunting_state = AntStateHunting(self)

        # Add the states to the state machine (self.brain)
        self.brain.add_state(exploring_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(delivering_state)
        self.brain.add_state(hunting_state)

        self.carry_image = None

    def carry(self, image):
        """Ant carring something"""
        self.carry_image = image

    def drop(self, surface):
        """Ant drop something  ---> blit out and reset the carry_image"""
        if self.carry_image:
            x, y = self.location
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x-w, y-h/2))
            self.carry_image = None

    def render(self, surface):
        """Render the ant on the screen with or without a carry object"""
        # Call the render function of the base class
        GameEntity.render(self, surface)

        # Extra code to render the 'carry' image
        if self.carry_image:
            x, y = self.location
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x-w, y-h/2))


class Leaf(GameEntity):
    """Create a new leaf into the world"""
    def __init__(self, world, image):
        super().__init__(world, "leaf", image)
        # GameEntity.__init__(self, world, "leaf", image)


class Spider(GameEntity):
    """Create a new spider into the world"""
    def __init__(self, world, image):
        super().__init__(world, "spider", image)
        # GameEntity.__init__(self, world, "spider", image)

        # Dead spider
        self.dead_image = pygame.transform.flip(image, 0, 1)

        self.health = 25
        self.speed = 50 + randint(-20, 20)

    def bitten(self):
        """Spider is dangerous beat it !"""
        self.health -= 1
        if self.health <= 0:
            self.speed = 0
            self.image = self.dead_image
        # Speed up to run away
        self.speed = 170

    def render(self, surface):
        """Display the spider and it's heath bar"""
        GameEntity.render(self, surface)

        # Draw the heath bar
        x, y = self.location
        w, h = self.image.get_size()
        # Bar just bellow the spider
        bar_x = x - 12
        bar_y = y + h/2
        surface.fill((255, 0, 0), (bar_x, bar_y, 25, 4))
        surface.fill((0, 255, 0), (bar_x, bar_y, self.health, 4))

    def process(self, time_passed):
        """time_passed in secondes"""
        x, y = self.location
        if x > SCREEN_SIZE[0] + 2:
            self.world.remove_entity(self)
            return
        GameEntity.process(self, time_passed)


class AntStateExploring(State):
    """Exploring the World"""
    def __init__(self, ant):
        super().__init__(EXPLORING)
        # State.__init__(self, EXPLORING)
        # Ant manipulated
        self.ant = ant

    def random_destination(self):
        """New random destination"""
        w, h = SCREEN_SIZE
        self.ant.destination = Vector2D(randint(0, w), randint(0, h))

    def do_action(self):
        """Change direction every 20 calls"""
        if randint(1, 20) == 1:
            self.random_destination()

    def check_conditions(self):
        """Check conditions to change state (seeking and hunting)"""
        leaf = self.ant.world.get_close_entity("leaf", self.ant.location)
        if leaf is not None:
            self.ant.leaf_id = leaf.id
            return SEEKING

        spider = self.ant.world.get_close_entity("spider",
                                                 NEST_POSITION, NEST_SIZE)
        if spider is not None:
            self.ant.spider_id = spider.id
            return HUNTING

        return None

    def entry_actions(self):
        """Change entity stats"""
        self.ant.speed = 120 + randint(-30, 30)
        self.random_destination()


class AntStateSeeking(State):
    """Capture the leaf"""
    def __init__(self, ant):
        super().__init__(SEEKING)
        # State.__init__(self, SEEKING)

        self.ant = ant
        self.leaf_id = None

    def check_conditions(self):
        """Check conditions to change state (delivring and exploring)"""
        leaf = self.ant.world.get_entity(self.ant.leaf_id)
        if leaf is None:
            return EXPLORING

        if self.ant.location.get_distance(leaf.location) < 5.0:
            self.ant.carry(leaf.image)
            self.ant.world.remove_entity(leaf)
            return DELIVERING

        return None

    def entry_actions(self):
        """Change entity stats"""
        leaf = self.ant.world.get_entity(self.ant.leaf_id)
        if leaf is not None:
            self.ant.destination = leaf.location
            self.ant.speed = 160 + randint(-20, 20)


class AntStateDelivering(State):
    """Delivre the leaf"""
    def __init__(self, ant):
        super().__init__(DELIVERING)
        # State.__init__(self, DELIVERING)

        self.ant = ant

    def check_conditions(self):
        """Check conditions to change state (exploring)"""
        if Vector2D(*NEST_POSITION).get_distance(self.ant.location) < NEST_SIZE:
            if randint(1, 10) == 1:
                self.ant.drop(self.ant.world.background)
                return EXPLORING

        return None

    def entry_actions(self):
        """Change entity stats"""
        self.ant.speed = 60  # Slow ant
        # Variant nest destination (change position under the nest)
        random_offset = Vector2D(randint(-20, 20), randint(-20, 20))
        self.ant.destination = Vector2D(*NEST_POSITION) + random_offset


class AntStateHunting(State):
    """Hunt spiders"""
    def __init__(self, ant):
        super().__init__(HUNTING)
        # State.__init__(self, HUNTING)

        self.ant = ant
        self.got_kill = False  # Spider alive

    def do_actions(self):
        spider = self.ant.world.get_entity(self.ant.spider_id)
        if spider is None:
            return

        self.ant.destination = spider.location

        if self.ant.location.get_distance(spider.location) < 15.:

            # Give the spider a fighting chance to avoid being killed!
            if randint(1, 5) == 1:
                spider.bitten()

            # If the spider is dead, move it back to the nest
                if spider.health <= 0:
                    self.ant.carry(spider.image)
                    self.ant.world.remove_entity(spider)
                    self.got_kill = True

    def check_conditions(self):
        """Check conditions to change the state (delivring and exploring)"""
        if self.got_kill:
            return DELIVERING

        spider = self.ant.world.get_entity(self.ant.spider_id)
        # Spider already kill
        if spider is None:
            return EXPLORING

        # Spider too far
        if spider.location.get_distance(NEST_POSITION) > NEST_SIZE * 3:
            return EXPLORING

        return None

    def entry_actions(self):
        """Change entity states"""
        self.speed = 160. + randint(0, 50)

    def exit_actions(self):
        """Reinitialize the dead spider flag"""
        self.got_kill = False


def run():
    """Start the game"""
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    world = World()
    w, h = SCREEN_SIZE
    clock = pygame.time.Clock()
    ant_image = pygame.image.load("Stock/ant.png").convert_alpha()
    leaf_image = pygame.image.load("Stock/leaf.png").convert_alpha()
    spider_image = pygame.image.load("Stock/spider.png").convert_alpha()

    # Add entities
    for ant_no in range(ANT_COUNT):
        ant = Ant(world, ant_image)
        ant.location = Vector2D(randint(0, w), randint(0, h))
        ant.brain.set_state(EXPLORING)
        world.add_entity(ant)

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        time_passed = clock.tick(30)

        if randint(1, 10) == 1:
            leaf = Leaf(world, leaf_image)
            leaf.location = Vector2D(randint(0, w), randint(0, h))
            world.add_entity(leaf)

        if randint(1, 100) == 1:
            spider = Spider(world, spider_image)
            spider.location = Vector2D(-50, randint(0, h))
            spider.destination = Vector2D(w + 50, randint(0, h))
            world.add_entity(spider)

        world.process(time_passed)
        world.render(screen)
        pygame.display.update()


###############################
#### Programme principal : ####
###############################

EXPLORING = "exploring"
HUNTING = "hunting"
SEEKING = "seeking"
DELIVERING = "delivring"
SCREEN_SIZE = (1200, 900)
NEST_POSITION = (int(SCREEN_SIZE[0] / 2), int(SCREEN_SIZE[1] / 2))
ANT_COUNT = 180
NEST_SIZE = 200.

if __name__ == '__main__':
    run()
