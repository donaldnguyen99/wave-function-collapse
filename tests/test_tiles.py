import sys
sys.path.append('..')
from tiles import Tile
import pygame
import pytest

@pytest.fixture(scope='class', autouse=True)
def pygame_setup_teardown():
    pygame.init()
    pygame.display.set_mode((800, 600))
    
    yield

    pygame.quit()

class TestTile:
    def test_empty_tile_init(self):
        tile = Tile()
        assert tile.name == ''
        assert tile.edges == [0, 0, 0, 0]
        assert tile.image is None
        assert tile.image_rect is None

    def test_tile_init_5_args(self):
        tile = Tile('test', [1, 2, 3, 4], 'tiles/T.png', 10, 10)
        assert tile.name == 'test'
        assert tile.edges == [1, 2, 3, 4]
        assert tile.image is not None
        assert tile.image_rect is not None

    def test_tile_rotate(self):
        tile = Tile('test', [1, 2, 3, 4], 'tiles/T.png', 10, 10)
        tile.rotate(1)
        assert tile.edges == [2, 3, 4, 1]

    def test_tile_make_copy(self):
        tile = Tile('test', [1, 2, 3, 4], 'tiles/T.png', 10, 10)
        tile2 = tile.make_copy()
        tile2.rotate(1)
        assert tile2.image is not tile.image
        assert tile2.edges != tile.edges
        assert tile2.image_rect is not tile.image_rect