import os
from survive import settings

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define directions
SOUTH = 1
SOUTH_WEST = 2
WEST = 3
NORTH_WEST = 4
NORTH = 5
NORTH_EAST = 6
EAST = 7
SOUTH_EAST = 8

# Define other variables
CHARACTERS_DIRS = os.path.join(settings.BASE_DIR, 'static/images/chars/')