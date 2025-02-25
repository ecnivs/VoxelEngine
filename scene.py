from settings import *
import moderngl as mgl
from world import World
from world_objects.voxel_marker import VoxelMarker
from world_objects.water import Water
from world_objects.clouds import Clouds

class Scene:
    """Manages the overall scene, including world generation, environmental elements, and rendering logic."""
    def __init__(self, app):
        """
        Initializes the scene with essential components.

        Parameters:
            app: The main application instance, providing context and settings.
        """
        self.app = app
        self.world = World(self.app)  # The main voxel-based world
        self.voxel_marker = VoxelMarker(self.world.voxel_handler)  # Selection highlight for voxels
        self.water = Water(app)  # Water rendering object
        self.clouds = Clouds(app)  # Cloud rendering object

    def update(self):
        """Updates all scene components, including the world, voxel marker, and environmental elements."""
        self.world.update()
        self.voxel_marker.update()
        self.clouds.update()

    def render(self):
        """
        Renders the scene in the correct order, ensuring proper visibility and optimizations.

        1. Renders the world (chunks).
        2. Disables back-face culling for non-solid elements (clouds, water).
        3. Renders clouds and water.
        4. Re-enables back-face culling for performance optimization.
        5. Renders the voxel selection marker.
        """
        self.world.render()

        # Disable culling to render transparent objects correctly
        self.app.ctx.disable(mgl.CULL_FACE)
        self.clouds.render()
        self.water.render()
        self.app.ctx.enable(mgl.CULL_FACE)

        # Render voxel selection marker
        self.voxel_marker.render()
