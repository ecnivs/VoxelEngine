from meshes.quad_mesh import QuadMesh
from settings import *

class Water:
    """
    Represents the water surface in the game world.

    Attributes:
        app (App): The main application instance.
        mesh (QuadMesh): The quad mesh used to render the water surface.
    """
    def __init__(self, app):
        """
        Initializes the water surface.

        Args:
            app (App): The main application instance.
        """
        self.app = app
        self.mesh = QuadMesh(app)  # Quad mesh for rendering water

    def render(self):
        """
        Renders the water surface.
        """
        self.mesh.render()

