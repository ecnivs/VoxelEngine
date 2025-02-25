from settings import *
from meshes.cloud_mesh import CloudMesh

class Clouds:
    """
    Represents a cloud system in the game world, handling rendering and animation.

    Attributes:
        app (App): The main application instance.
        mesh (CloudMesh): The mesh responsible for rendering the clouds.
    """
    def __init__(self, app):
        """
        Initializes the cloud system.

        Args:
            app (App): The main application instance.
        """
        self.app = app
        self.mesh = CloudMesh(app)  # Initialize the cloud mesh

    def update(self):
        """Updates the cloud shader with the current time for animation effects."""
        self.mesh.program['u_time'] = self.app.time  # Pass elapsed time for cloud movement

    def render(self):
        """Renders the clouds."""
        self.mesh.render()  # Draw the cloud mesh
