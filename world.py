from settings import *
from world_objects.chunk import Chunk
from voxel_handler import VoxelHandler

class World:
    """ Represents the voxel-based world, managing chunks and voxel data."""
    def __init__(self, app):
        """
        Initializes the world with chunks, voxel data, and a voxel handler.

        Parameters:
            app: Reference to the main application.
        """
        self.app = app
        self.chunks = [None for _ in range(WORLD_VOL)]
        self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype='uint8')
        self.build_chunks()
        self.build_chunk_mesh()
        self.voxel_handler = VoxelHandler(self)

    def update(self):
        """Updates the world, particularly handling voxel interactions."""
        self.voxel_handler.update()

    def build_chunks(self):
        """Initializes and generations all chunks in the world."""
        for x in range(WORLD_W):
            for y in range(WORLD_H):
                for z in range(WORLD_D):
                    chunk = Chunk(self, position=(x, y, z))
                    chunk_index = x + WORLD_W * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk
                    self.voxels[chunk_index] = chunk.build_voxels()
                    chunk.voxels = self.voxels[chunk_index]

    def build_chunk_mesh(self):
        """Builds the mesh for each chunk, enabling rendering."""
        for chunk in self.chunks:
            chunk.build_mesh()

    def render(self):
        """Renders all chunks in the world."""
        for chunk in self.chunks:
            chunk.render()
