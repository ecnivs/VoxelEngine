from settings import *
from meshes.cube_mesh import CubeMesh

class VoxelMarker:
    """
    Represents a visual marker for voxel selection in the world.

    Attributes:
        app (App): The main application instance.
        handler (VoxelHandler): Manages voxel interactions and selection.
        position (glm.vec3): The world position of the selected voxel.
        m_model (glm.mat4): Model matrix for transformation.
        mesh (CubeMesh): The mesh used to render the voxel marker.
    """
    def __init__(self, voxel_handler):
        """
        Initializes the voxel marker.

        Args:
            voxel_handler (VoxelHandler): Handles voxel interactions.
        """
        self.app = voxel_handler.app
        self.handler = voxel_handler
        self.position = glm.vec3(0)  # Default position
        self.m_model = self.get_model_matrix()
        self.mesh = CubeMesh(self.app)  # Cube mesh for rendering the marker

    def update(self):
        """Updates the marker's position to match the selected voxel."""
        if self.handler.voxel_id:  # If a voxel is selected
            self.position = self.handler.voxel_world_pos  # Update position

    def set_uniform(self):
        """Updates the shader's model matrix for rendering."""
        self.mesh.program['m_model'].write(self.get_model_matrix())

    def get_model_matrix(self):
        """
        Computes the transformation matrix for positioning the voxel marker.

        Returns:
            glm.mat4: The transformation matrix.
        """
        return glm.translate(glm.mat4(), glm.vec3(self.position))

    def render(self):
        """Renders the voxel marker if a voxel is selected."""
        if self.handler.voxel_id:
            self.set_uniform()
            self.mesh.render()
