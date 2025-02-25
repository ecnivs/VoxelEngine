from settings import *

class Frustum:
    """
    Implements frustum culling for chunk visibility optimization. 
    Determines whether a chunk is within the camera's view frustum.
    """

    def __init__(self, camera):
        """
        Initializes the frustum culling system.

        Parameters:
            camera: The Camera object that defines the player's view.
        """
        self.cam: Camera = camera  # Reference to the camera
        self.factor_y = 1.0 / math.cos(half_y := V_FOV * 0.5)  # Precompute Y-axis frustum factor
        self.tan_y = math.tan(half_y)  # Tangent of the vertical FOV

        self.factor_x = 1.0 / math.cos(half_x := H_FOV * 0.5)  # Precompute X-axis frustum factor
        self.tan_x = math.tan(half_x)  # Tangent of the horizontal FOV

    def is_on_frustum(self, chunk):
        """
        Checks if a chunk is within the camera's view frustum.

        Uses a bounding sphere method to approximate the chunk's visibility.

        Parameters:
            chunk: The chunk object to check.

        Returns:
            bool: True if the chunk is visible, False otherwise.
        """
        sphere_vec = chunk.center - self.cam.position  # Vector from camera to chunk center

        # Check if chunk is within the near and far planes
        sz = glm.dot(sphere_vec, self.cam.forward)
        if not (NEAR - CHUNK_SPHERE_RADIUS <= sz <= FAR + CHUNK_SPHERE_RADIUS):
            return False

        # Check vertical (Y) frustum bounds
        sy = glm.dot(sphere_vec, self.cam.up)
        dist = self.factor_y * CHUNK_SPHERE_RADIUS + sz * self.tan_y
        if not (-dist <= sy <= dist):
            return False

        # Check horizontal (X) frustum bounds
        sx = glm.dot(sphere_vec, self.cam.right)
        dist = self.factor_x * CHUNK_SPHERE_RADIUS + sz * self.tan_x
        if not (-dist <= sx <= dist):
            return False

        return True  # Chunk is within the frustum
