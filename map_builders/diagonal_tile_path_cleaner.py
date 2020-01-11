from random import randint

from map_builders.builder_map import MetaMapbuilder
from gmap.gmap_enums import TileType


class DiagonalTilePathCleaner(MetaMapbuilder):
    def build_meta_map(self, build_data):
        gmap = build_data.map
        diagonals = [- 1 - gmap.width, 1 - gmap.width, gmap.width + 1, gmap.width - 1]  # nw, ne, se, sw
        cardinals = [-1, - gmap.width, 1, gmap.width]   # west, north, east, south

        for i, tile in enumerate(gmap.tiles):
            if tile == TileType.FLOOR:
                # Pour chaque diagonal autour de i et si cette diagonale est constructible.
                for diagonal in diagonals:
                    if not gmap.is_constructible_tile(i + diagonal):
                        continue
                    # on regarde les tuiles a chaque cardinal si elles sont construtibles.
                    cardinal_walls = 0
                    for cardinal in cardinals:
                        if not gmap.is_constructible_tile(i + cardinal):
                            cardinal_walls = 0
                            continue
                        if gmap.tiles[i + cardinal] == TileType.WALL:
                            cardinal_walls += 1
                        # si deux de suite sont des murs, alors cardinal doit être convertie en floor.
                        if cardinal_walls == 2:
                            gmap.tiles[i + cardinal] = TileType.FLOOR
                            cardinal_walls = 0
