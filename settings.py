from numba import njit
import numpy as np
import glm
import math

# OpenGL settings
MAJOR_VER, MINOR_VER = 3, 3  # OpenGL version
DEPTH_SIZE = 24  # Depth buffer precision
NUM_SAMPLES = 1  # Antialiasing sample count

# Resolution settings
WIN_RES = glm.vec2(1600, 900)  # Window resolution
FPS = 120  # Target frames per second

# World generation seed
SEED = 16  # Random seed for procedural generation

# Ray casting settings
MAX_RAY_DIST = 6  # Maximum distance for ray tracing (used for voxel selection)

# Chunk settings
CHUNK_SIZE = 48  # Size of a chunk (width, height, depth)
H_CHUNK_SIZE = CHUNK_SIZE // 2  # Half of the chunk size
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE  # Area of a chunk (XZ plane)
CHUNK_VOL = CHUNK_AREA * CHUNK_SIZE  # Volume of a chunk
CHUNK_SPHERE_RADIUS = H_CHUNK_SIZE * math.sqrt(3)  # Bounding sphere radius for chunk frustum culling

# World dimensions
WORLD_W, WORLD_H = 20, 2  # World width and height in chunks
WORLD_D = WORLD_W  # World depth (same as width)
WORLD_AREA = WORLD_W * WORLD_D  # Total number of chunks in XZ plane
WORLD_VOL = WORLD_AREA * WORLD_H  # Total number of chunks in the world

# World center coordinates
CENTER_XZ = WORLD_W * H_CHUNK_SIZE  # XZ center of the world
CENTER_Y = WORLD_H * H_CHUNK_SIZE  # Y center of the world

# Camera settings
ASPECT_RATIO = WIN_RES.x / WIN_RES.y  # Aspect ratio based on window resolution
FOV_DEG = 50  # Field of View in degrees
V_FOV = glm.radians(FOV_DEG)  # Vertical Field of View in radians
H_FOV = 2 * math.atan(math.tan(V_FOV * 0.5) * ASPECT_RATIO)  # Horizontal Field of View
NEAR = 0.1  # Near clipping plane distance
FAR = 2000.0  # Far clipping plane distance
PITCH_MAX = glm.radians(90)  # Maximum pitch (to prevent camera flipping)

# Player settings
PLAYER_SPEED = 0.007  # Player movement speed
PLAYER_ROT_SPEED = 0.003  # Player rotation speed
PLAYER_POS = glm.vec3(CENTER_XZ, CHUNK_SIZE, CENTER_XZ)  # Initial player position
MOUSE_SENSITIVITY = 0.001  # Mouse sensitivity for camera movement

# Background color (RGB)
BG_COLOR = glm.vec3(0.58, 0.83, 0.99)  # Sky blue

# Voxel texture IDs
SAND = 1
GRASS = 2
DIRT = 3
STONE = 4
SNOW = 5
LEAVES = 6
WOOD = 7

# Terrain height levels
SNOW_LVL = 54  # Snow level height
STONE_LVL = 49  # Stone level height
DIRT_LVL = 40  # Dirt level height
GRASS_LVL = 8   # Grass level height
SAND_LVL = 7    # Sand level height (beach areas)

# Tree generation settings
TREE_PROBABILITY = 0.02  # Probability of tree spawning on a grass block
TREE_WIDTH, TREE_HEIGHT = 4, 8  # Tree dimensions
TREE_H_WIDTH, TREE_H_HEIGHT = TREE_WIDTH // 2, TREE_HEIGHT // 2  # Half dimensions

# Water settings
WATER_LINE = 5.6  # Height at which water is rendered
WATER_AREA = 5 * CHUNK_SIZE * WORLD_W  # Area covered by water bodies

# Cloud settings
CLOUD_SCALE = 25  # Scale factor for cloud size
CLOUD_HEIGHT = WORLD_H * CHUNK_SIZE * 2  # Cloud altitude
