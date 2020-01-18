from bearlibterminal import terminal

from world import World
from ui_system.ui_enums import Layers
from ui_system.render_functions import get_item_display_name
from components.position_components import PositionComponent
from components.name_components import NameComponent
from components.hidden_component import HiddenComponent
from components.character_components import AttributesComponent
from components.pools_component import Pools
from ui_system.interface import Interface
from ui_system.render_functions import print_shadow
from ui_system.render_camera import get_map_coord_with_mouse_when_zooming, get_map_coord_with_zoom


class Tooltip:
    def __init__(self):
        self.lines = list()

    def add(self, string):
        self.lines.append(string)

    @property
    def width(self):
        best = 0
        for line in self.lines:
            if len(line) > best:
                best = len(line)
        return best

    @property
    def height(self):
        return len(self.lines)

    def render(self, x, y):
        terminal.layer(Layers.TOOLTIP.value)
        for i, line in enumerate(self.lines):
            print_shadow(x, y + i, line)


def draw_tooltip():
    current_map = World.fetch('current_map')

    # mouse x,y on screen
    mouse_pos_x = terminal.state(terminal.TK_MOUSE_X)
    mouse_pos_y = terminal.state(terminal.TK_MOUSE_Y)
    # mouse x, y relative to map, taken "out of map" margin into account
    mouse_map_pos_x, mouse_map_pos_y = get_map_coord_with_mouse_when_zooming()
    # the mouse is on this map coords. May be out of bound!
    mouse_on_map_x = get_map_coord_with_zoom(mouse_map_pos_x)
    mouse_on_map_y = get_map_coord_with_zoom(mouse_map_pos_y)

    if 1 > mouse_on_map_x or mouse_on_map_x > Interface.map_screen_width - 1\
            or 1 > mouse_on_map_y or mouse_on_map_y > Interface.map_screen_height - 1:
        return

    if current_map.visible_tiles[current_map.xy_idx(mouse_map_pos_x, mouse_map_pos_y)]:
        # est ce qu'on doit bien reconstruire le tooltip?
        old_tooltip, old_mouse_x, old_mouse_y = World.fetch('tooltip')
        tooltip = list()
        subjects = World.get_components(NameComponent, PositionComponent)
        for entity, (name, position) in subjects:
            if World.get_entity_component(entity, HiddenComponent):
                continue
            if mouse_map_pos_x == position.x and mouse_map_pos_y == position.y:
                tooltip.append(entity)

        # identique, on ne change rien.
        if tooltip == old_tooltip and mouse_map_pos_x == old_mouse_x and mouse_map_pos_y == old_mouse_y:
            return

        # nouveaux tooltips!
        World.insert('tooltip', (tooltip, mouse_map_pos_x, mouse_map_pos_y))
        terminal.layer(Layers.TOOLTIP.value)
        terminal.clear_area(0, 0, Interface.screen_width, Interface.screen_height)

        if not tooltip:
            return

        tip_boxes = list()
        for entity in tooltip:
            tip = Tooltip()
            tip.add(get_item_display_name(entity))

            # level
            level = World.get_entity_component(entity, Pools)
            if level:
                tip.add(f'Level : {level.level}')
            # attributes
            attributes = World.get_entity_component(entity, AttributesComponent)
            if attributes:
                description = ''
                if attributes.might.bonus_value > 3:
                    description += "Strong. "
                if attributes.might.bonus_value < 3:
                    description += "Weak. "
                if attributes.body.bonus_value > 3:
                    description += "Healthy. "
                if attributes.body.bonus_value < 3:
                    description += "Unhealthy. "
                if attributes.quickness.bonus_value > 3:
                    description += "Agile. "
                if attributes.quickness.bonus_value < 3:
                    description += "Clumsy. "
                if attributes.wits.bonus_value > 3:
                    description += "Smart. "
                if attributes.wits.bonus_value < 3:
                    description += "Stupid. "
                if not description:
                    description = "Quite average."
                tip.add(description)

            # Status effects
            from components.status_effect_components import DurationComponent, StatusEffectComponent
            subjects = World.get_components(NameComponent, DurationComponent, StatusEffectComponent)
            for effect, (effect_named, effect_duration, effect_status) in subjects:
                if effect_status.target == entity:
                    tip.add(f'{effect_named.name} ({effect_duration.turns})')

            tip_boxes.append(tip)

        # render left or right of mouse
        arrow_y = mouse_pos_y
        print(f'mouse pos x {mouse_pos_x}, interface screen: {Interface.screen_width // 2}')
        if mouse_pos_x < Interface.screen_width // 2:
            arrow = '→'
            arrow_x = mouse_pos_x - (1 * Interface.zoom)
        else:
            arrow = '←'
            arrow_x = mouse_pos_x + (1 * Interface.zoom)
        terminal.layer(Layers.TOOLTIP.value)
        terminal.color('white')
        print_shadow(arrow_x, arrow_y, arrow)

        total_tip_height = 0
        for tooltip in tip_boxes:
            total_tip_height += tooltip.height

        y = mouse_pos_y - (total_tip_height // 2)
        while y + (total_tip_height // 2) > Interface.screen_height:
            y -= 1

        for tooltip in tip_boxes:
            if mouse_pos_x < Interface.screen_width // 2:
                x = mouse_pos_x - (Interface.zoom + tooltip.width)
            else:
                x = mouse_pos_x + 1 + Interface.zoom
            tooltip.render(x, y)
            y += tooltip.height
        terminal.refresh()
