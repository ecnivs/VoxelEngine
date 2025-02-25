from settings import *
from meshes.base_mesh import BaseMesh

class CubeMesh(BaseMesh):
    """
    A class representing a cube mesh used for voxel markers.
    This class extends BaseMesh and constructs a simple cube mesh with texture coordinates.
    """
    def __init__(self, app):
        """
        Initialize the CubeMesh instance.

        Parameters:
            app: The main application instance providing context and shader programs.
        """
        super().__init__()
        self.app = app
        self.ctx = self.app.ctx
        self.program = self.app.shader_program.voxel_marker

        self.vbo_format = '2f2 3f2'  # Format specifying texture and position attributes
        self.attrs = ('in_tex_coord_0', 'in_position',)
        self.vao = self.get_vao()

    @staticmethod
    def get_data(vertices, indices):
        """
        Generate vertex data from the provided vertices and indices.

        Parameters:
            vertices (list of tuples): List of vertex positions.
            indices (list of tuples): List of index tuples defining triangle faces.

        Returns:
            np.ndarray: Flattened array of vertex data formatted as float16.
        """
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='float16')

    def get_vertex_data(self):
        """
        Generate vertex data for the cube mesh, including texture coordinates.

        Returns:
            np.ndarray: Combined vertex and texture coordinate data.
        """
        # Define cube vertices
        vertices = [
            (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1),
            (0, 1, 0), (0, 0, 0), (1, 0, 0), (1, 1, 0)
        ]
        # Define cube indices for faces
        indices = [
            (0, 2, 3), (0, 1, 2),
            (1, 7, 2), (1, 6, 7),
            (6, 5, 4), (4, 7, 6),
            (3, 4, 5), (3, 5, 0),
            (3, 7, 4), (3, 2, 7),
            (0, 6, 1), (0, 5, 6)
        ]
        vertex_data = self.get_data(vertices, indices)

        # Define texture coordinate vertices
        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [
            (0, 2, 3), (0, 1, 2),
            (0, 2, 3), (0, 1, 2),
            (0, 1, 2), (2, 3, 0),
            (2, 3, 0), (2, 0, 1),
            (0, 2, 3), (0, 1, 2),
            (3, 1, 2), (3, 0, 1),
        ]
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)

        # Combine texture and vertex data
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        return vertex_data

