from settings import *
from meshes.base_mesh import BaseMesh

class QuadMesh(BaseMesh):
    """
    A simple quad mesh used for rendering water surfaces.
    This class extends `BaseMesh` to create a flat quad mesh with texture coordinates and position attributes.
    """
    def __init__(self, app):
        """
        Initialize the QuadMesh.

        Parameters:
            app: The application instance, providing context and shader programs.
        """
        super().__init__()
        self.app = app

        self.ctx = self.app.ctx
        self.program = self.app.shader_program.water
        self.vbo_format = '2u1 3u1'  # Defines the vertex buffer format
        self.attrs = ('in_tex_coord', 'in_position')
        self.vao = self.get_vao()

    def get_vertex_data(self):
        """
        Generate vertex data for the quad mesh.

        Returns:
            np.ndarray: An array containing interleaved texture coordinates and positions.
        """
        vertices = np.array([
            (0, 0, 0), (1, 0, 1), (1, 0, 0),
            (0, 0, 0), (0, 0, 1), (1, 0, 1)
        ], dtype='uint8')

        tex_coords = np.array([
            (0, 0), (1, 1), (1, 0),
            (0, 0), (0, 1), (1, 1)
        ], dtype='uint8')

        vertex_data = np.hstack([tex_coords, vertices])
        return vertex_data
