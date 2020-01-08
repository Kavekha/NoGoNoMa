from random import randint

from map_builders.builder_map import MetaMapbuilder
from gmap.gmap_enums import TileType


class DiagonalTilePathCleaner(MetaMapbuilder):
    def build_meta_map(self, build_data):
        gmap = build_data.map
        for i, tile in enumerate(gmap.tiles):
            if tile == TileType.FLOOR:
                """We check if x + 1, y + 1 (i + 1 + gmap.width) is not map belt
                If it's not, we check if it's a floor. If it is, we have a potential diagonal floor
                We check then if x + 1 tile and y + 1 tile are wall.
                If both are wall: then we have a diagonal floor
                We do a randint(0, 1) and choose one of the tile to make it a floor."""

                south_east_tile = i + 1 + gmap.width
                if gmap.is_constructible_tile(south_east_tile):
                    south_wall = i + gmap.width
                    east_wall = i + 1
                    if gmap.tiles[south_wall] == TileType.WALL and gmap.tiles[east_wall] == TileType.WALL:
                        if randint(0, 1) == 1:
                            gmap.tiles[south_wall] = TileType.FLOOR
                        else:
                            gmap.tiles[east_wall] = TileType.FLOOR
