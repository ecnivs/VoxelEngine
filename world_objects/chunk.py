from settings import *
from meshes.chunk_mesh import ChunkMesh
import random
from terrain_gen import *

class Chunk:
    """
    Represents a single chunk in the world, storing voxel data and rendering information.

    Attributes:
        app (App): The main application instance.
        world (World): The world instance this chunk belongs to.
        position (tuple): The position of the chunk in chunk coordinates.
        m_model (glm.mat4): The model matrix for transforming the chunk in the world.
        voxels (np.array): A 1D array storing voxel data for the chunk.
        mesh (ChunkMesh): The mesh representation of the chunk for rendering.
        is_empty (bool): Indicates if the chunk contains no solid voxels.
        center (glm.vec3): The center position of the chunk for frustum culling.
        is_on_frustum (function): Function reference to check if the chunk is within the camera's frustum.
    """
    def __init__(self, world, position):
        """
        Initializes the chunk with its position and world reference.

        Args:
            world (World): The world instance this chunk belongs to.
            position (tuple): The chunk's position in chunk coordinates.
        """
        self.app = world.app
        self.world = world
        self.position = position
        self.m_model = self.get_model_matrix()
        self.voxels: np.array = None
        self.mesh: ChunkMesh = None
        self.is_empty = True
        self.center = (glm.vec3(self.position) + 0.5) * CHUNK_SIZE  # Center for frustum culling
        self.is_on_frustum = self.app.player.frustum.is_on_frustum  # Frustum culling function

    def get_model_matrix(self):
        """
        Computes the model transformation matrix for the chunk.

        Returns:
            glm.mat4: The transformation matrix for the chunk.
        """
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model

    def set_uniform(self):
        """Sets the model matrix uniform in the shader program before rendering."""
        self.mesh.program['m_model'].write(self.m_model)

    def build_mesh(self):
        """Generates the mesh for the chunk based on its voxel data."""
        self.mesh = ChunkMesh(self)

    def render(self):
        """Renders the chunk if it is not empty and is within the camera's frustum."""
        if not self.is_empty and self.is_on_frustum(self):
            self.set_uniform()
            self.mesh.render()

    def build_voxels(self):
        """
        Generates the voxel data for the chunk.

        Returns:
            np.array: A 1D array containing voxel IDs for the chunk.
        """
        voxels = np.zeros(CHUNK_VOL, dtype='uint8')  # Initialize an empty voxel array
        cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE  # Get world-space coordinates
        self.generate_terrain(voxels, cx, cy, cz)  # Fill voxel data based on terrain generation
        if np.any(voxels):  # Check if the chunk contains any solid voxels
            self.is_empty = False
        return voxels

    @staticmethod
    @njit
    def generate_terrain(voxels, cx, cy, cz):
        """
        Generates terrain voxel data for the chunk based on world height.

        Args:
            voxels (np.array): The array storing voxel IDs.
            cx (int): The world X coordinate of the chunk.
            cy (int): The world Y coordinate of the chunk.
            cz (int): The world Z coordinate of the chunk.
        """
        for x in range(CHUNK_SIZE):
            wx = x + cx  # World X coordinate
            for z in range(CHUNK_SIZE):
                wz = z + cz  # World Z coordinate
                world_height = get_height(wx, wz)  # Get terrain height at this position
                local_height = min(world_height - cy, CHUNK_SIZE)  # Limit height to chunk bounds

                for y in range(local_height):
                    wy = y + cy  # World Y coordinate
                    set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height)  # Assign voxel type
