import pygame
import os

class TileSystem:
    def __init__(self, cell_width, cell_height, tile_image_dir=None):
        self.tile_image_dir = tile_image_dir
        self.tile_edges = {
            'blank': [0, 0, 0, 0],
            'T': [0, 1, 1, 1]
        }

        self.tiles = []
        if self.tile_image_dir:
            for tile_image_name in self.tile_edges.keys():
                # Create tile and its rotated versions
                # Assuming unique tiles 
                # (flipped tiles are not unique, must be handled separately
                # e.g. 'left hand' and 'right hand' tiles are unique)
                tile_image_path = os.path.join(
                    self.tile_image_dir, tile_image_name + '.png'
                )
                tile_to_add = Tile(
                    tile_image_name, 
                    self.tile_edges[tile_image_name], 
                    tile_image_path,
                    cell_width, cell_height
                )
                tile_possibilities = {str(tile_to_add.edges): tile_to_add}
                for i in range(1, 4):
                    copied_tile = tile_to_add.make_copy()
                    copied_tile.rotate(i)
                    tile_possibilities[str(copied_tile.edges)] = copied_tile
                    
                self.tiles.extend(tile_possibilities.values())
        else:
            for tile_name in self.tile_edges.keys():
                tile_to_add = Tile(
                    tile_name, 
                    self.tile_edges[tile_name], 
                    None,
                    cell_width, cell_height
                )
                tile_possibilities = {str(tile_to_add.edges): tile_to_add}
                for i in range(1, 4):
                    copied_tile = tile_to_add.make_copy()
                    copied_tile.rotate(i)
                    tile_possibilities[str(copied_tile.edges)] = copied_tile
                    
                self.tiles.extend(tile_possibilities.values())


class Tile:

    def __init__(self, *args):
        # args: name, edges, image_path
        if len(args) == 0:
            self.name = ''
            self.edges = [0, 0, 0, 0]
            self.image = None
            self.image_rect = None
            self.size = None
        elif len(args) == 5:
            self.name = args[0]
            self.edges = args[1]
            self.size = (args[3], args[4])
            if args[2] is not None:
                self.image = pygame.image.load(args[2]).convert()
                self.image = pygame.transform.scale(self.image, self.size)
            else:
                def_tiles = TileSetDefault(self.size)
                match self.name:
                    case 'blank':
                        self.image = def_tiles.tile_surfaces[self.name]
                    case 'T':
                        self.image = def_tiles.tile_surfaces[self.name]
                    case _:
                        self.image = def_tiles.tile_surfaces['blank']
                self.image = pygame.transform.scale(self.image, self.size)
            self.image_rect = self.image.get_rect(topleft=(0, 0))
        else:
            raise Exception('Invalid number of arguments')

    def rotate(self, n: int):
        assert n in [1, 2, 3]
        self.edges = self.edges[n:] + self.edges[:n]
        self.image = pygame.transform.rotate(self.image, 90 * n)

    def is_equal(self, other):
        return self.edges == other.edges

    def make_copy(self):
        copied = Tile()
        if self.edges is not None:
            copied.name = self.name
            copied.edges = self.edges[:]
            copied.image = self.image.copy()
            copied.image_rect = self.image_rect.copy()
        return copied

class TileSetDefault:

    size = 5

    def __init__(self, *args):
        self.tile_surfaces = {}

        # blank 3x3 tile
        blank_surface = pygame.Surface((self.size, self.size))
        blank_surface.fill((255, 255, 255))

        # T-shaped 3x3 tile
        t_surface = pygame.Surface((self.size, self.size))
        t_surface.fill((255, 255, 255))
        t_surface.set_at((2, 3), (0, 0, 0))
        t_surface.set_at((2, 4), (0, 0, 0))
        t_surface.set_at((0, 2), (0, 0, 0))
        t_surface.set_at((1, 2), (0, 0, 0))
        t_surface.set_at((2, 2), (0, 0, 0))
        t_surface.set_at((3, 2), (0, 0, 0))
        t_surface.set_at((4, 2), (0, 0, 0))

        if len(args) == 0:
            blank_surface = pygame.transform.scale(blank_surface, (50, 50))
            t_surface = pygame.transform.scale(t_surface, (50, 50))
        elif len(args) == 1:
            if args[0] == None:
                blank_surface = pygame.transform.scale(blank_surface, (50, 50))
                t_surface = pygame.transform.scale(t_surface, (50, 50))
            else:
                blank_surface = pygame.transform.scale(blank_surface, args[0])
                t_surface = pygame.transform.scale(t_surface, args[0])
        else:
            raise Exception('Invalid number of arguments')
        

        self.tile_surfaces['blank'] = blank_surface
        self.tile_surfaces['T'] = t_surface

