import os
import pygame
import random
import tiles


class Cell:
    def __init__(self, cell_id, options):
        self.cell_id = cell_id
        self.tile = None
        self.options = options[:]
    
    def is_collapsed(self):
        return self.tile is not None or self.options is None


    def remove_option(self, tile, my_dir):
        i_to_remove = set()
        for i, option in enumerate(self.options):
            if  (my_dir == 'below' and option.edges[2] != tile.edges[0]) or \
                (my_dir == 'above' and option.edges[0] != tile.edges[2]) or \
                (my_dir == 'right' and option.edges[1] != tile.edges[3]) or \
                (my_dir == 'left'  and option.edges[3] != tile.edges[1]):
                i_to_remove.add(i)
        for i in sorted(i_to_remove, reverse=True):
            self.options.pop(i)
        if not self.options:
            self.options = None


class Game:
    def __init__(self, screen: pygame.Surface):
        
        self.GRID_WIDTH = 40
        self.GRID_HEIGHT = 30
        
        self.screen = screen
        self.cell_height = self.screen.get_height() / self.GRID_HEIGHT
        self.cell_width = self.screen.get_width() / self.GRID_WIDTH
        tile_system = tiles.TileSystem(
            (self.cell_width // tiles.TileSetDefault.size) * tiles.TileSetDefault.size, 
            (self.cell_height // tiles.TileSetDefault.size) * tiles.TileSetDefault.size)
        self.tiles = tile_system.tiles
        self.grid = [
            Cell(i, self.tiles) for i in range(self.GRID_WIDTH * self.GRID_HEIGHT)
        ]
        
        
        # self.randomize_grid() # For testing

    def update_neighbor_options(self, cell):
        curr_cell_id = cell.cell_id
        curr_cell_row = curr_cell_id // self.GRID_WIDTH
        curr_cell_col = curr_cell_id % self.GRID_WIDTH
        if curr_cell_row > 0:
            # Update top neighbor
            top_neighbor = self.grid[curr_cell_id - self.GRID_WIDTH]
            if not top_neighbor.is_collapsed():
                top_neighbor.remove_option(cell.tile, 'below')
        if curr_cell_row < self.GRID_HEIGHT - 1:
            # Update bottom neighbor
            bottom_neighbor = self.grid[curr_cell_id + self.GRID_WIDTH]
            if not bottom_neighbor.is_collapsed():
                bottom_neighbor.remove_option(cell.tile, 'above')
        if curr_cell_col > 0:
            # Update left neighbor
            left_neighbor = self.grid[curr_cell_id - 1]
            if not left_neighbor.is_collapsed():
                left_neighbor.remove_option(cell.tile, 'right')
        if curr_cell_col < self.GRID_WIDTH - 1:
            # Update right neighbor
            right_neighbor = self.grid[curr_cell_id + 1]
            if not right_neighbor.is_collapsed():
                right_neighbor.remove_option(cell.tile, 'left')


    def collapse_grid(self):
        sorted_by_lowest_options = sorted(
            filter(lambda cell: not cell.is_collapsed(), self.grid),
            key=lambda cell: len(cell.options)
        )
        if len(sorted_by_lowest_options) == 0:
            print('Grid is collapsed.')
            return
        len_lowest_options = len(sorted_by_lowest_options[0].options)
        cells_w_lowest_options = list(
            filter(lambda cell: len(cell.options) == len_lowest_options, 
                   sorted_by_lowest_options)
        )
        choice_to_collapse = random.choice(cells_w_lowest_options)
        choice_to_collapse.tile = random.choice(choice_to_collapse.options)
        choice_to_collapse.options.clear()
        self.update_neighbor_options(choice_to_collapse)
        

    def draw(self):
        
        self.collapse_grid()
        # print([cell.tile.edges for cell in self.grid if cell.tile is not None])

        # Draw grid
        self.screen.fill((0, 0, 0))
        for j in range(self.GRID_HEIGHT):
            for i in range(self.GRID_WIDTH):
                curr_cell = self.grid[i + j * self.GRID_WIDTH]
                if curr_cell.tile is None:
                    continue
                curr_cell.tile.image_rect.topleft = (
                    int(i * self.cell_height), 
                    int(j * self.cell_width))
                self.screen.blit(
                    curr_cell.tile.image, 
                    curr_cell.tile.image_rect)

    
    def randomize_grid(self):
        # Random grid (for testing)
        for j in range(self.GRID_HEIGHT):
            for i in range(self.GRID_WIDTH):
                random_tile = random.choice(self.tiles).make_copy()
                random_tile.image_rect.topleft = (
                    int(i * self.cell_height), 
                    int(j * self.cell_width))
                self.grid[i + j * self.GRID_WIDTH].tile = random_tile
