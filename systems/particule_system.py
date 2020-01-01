from time import perf_counter

from bearlibterminal import terminal

from systems.system import System
from world import World
from ui_system.ui_enums import Layers
from components.particule_component import ParticuleLifetimeComponent
from components.position_component import PositionComponent
from components.renderable_component import RenderableComponent
from ui_system.render_camera import render_entities_camera
import config


class ParticuleSpawnSystem(System):
    def update(self, *args, **kwargs):
        for new_particule in ParticuleBuilder.requests_to_spawn():
            pos = PositionComponent(new_particule.x, new_particule.y)
            render = RenderableComponent(new_particule.glyph, new_particule.char_color,
                                         sprite=new_particule.sprite, render_order=Layers.PARTICULE)
            lifetime = ParticuleLifetimeComponent(new_particule.lifetime)
            World.create_entity(pos, render, lifetime)

        ParticuleBuilder.clear_requests()


class ParticuleRequest:
    def __init__(self, x, y, char_color, glyph, sprite, lifetime):
        self.x = x
        self.y = y
        self.char_color = char_color
        self.glyph = glyph
        self.sprite = sprite
        self.lifetime = lifetime


class ParticuleBuilder:
    _requests = []

    @staticmethod
    def request(x, y, char_color, glyph, sprite, lifetime=0.2):
        ParticuleBuilder._requests.append(ParticuleRequest(x, y, char_color, glyph, sprite, lifetime))

    @staticmethod
    def requests_to_spawn():
        return ParticuleBuilder._requests

    @staticmethod
    def clear_requests():
        ParticuleBuilder._requests.clear()


def cull_dead_particules(tick_time):
    # print(f'---cull dead particule : {tick_time}')
    dead_particules = []
    subjects = World.get_components(ParticuleLifetimeComponent)

    now = perf_counter()
    for entity, (particule, *args) in subjects:
        print(
            f'now : {now} : particule {entity}: {now - particule.start_time} vs {particule.lifetime}')
        if now - particule.start_time > particule.lifetime:
            print(f'DEAD!')
            dead_particules.append(entity)

    if dead_particules:
        for dead_particule in dead_particules:
            World.delete_entity(dead_particule)

        terminal.layer(Layers.PARTICULE.value)
        terminal.clear_area(0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        render_entities_camera()
        terminal.refresh()
