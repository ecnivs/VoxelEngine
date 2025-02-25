from settings import *

class ShaderProgram:
    """
    Handles the initialization and management of OpenGL shader programs used in the application.
    It loads, compiles, and links shader programs, assigns texture units, and updates uniform values.
    """
    def __init__(self, app):
        """
        Initializes the shader programs and assigns required uniform values.

        Parameters:
            app: The main application instance, providing context for rendering.
        """
        self.app = app
        self.ctx = app.ctx # OpenGL rendering context
        self.player = app.player # Reference to player object (camera)

        # Load shader programs
        self.chunk = self.get_program(shader_name='chunk')
        self.voxel_marker = self.get_program(shader_name='voxel_marker')
        self.water = self.get_program('water')
        self.clouds = self.get_program('clouds')

        # Set initial uniform values
        self.set_uniforms_on_init()

    def set_uniforms_on_init(self):
        """Sets initial values for uniform variables in the shaders."""
        # Chunk shader uniforms
        self.chunk['m_proj'].write(self.player.m_proj)  # Projection matrix
        self.chunk['m_model'].write(glm.mat4())  # Model matrix (identity matrix)
        self.chunk['u_texture_array_0'] = 1  # Assign texture array unit
        self.chunk['bg_color'].write(BG_COLOR)  # Background color
        self.chunk['water_line'] = WATER_LINE  # Water level reference

        # Voxel marker shader uniforms
        self.voxel_marker['m_proj'].write(self.player.m_proj)
        self.voxel_marker['m_model'].write(glm.mat4())
        self.voxel_marker['u_texture_0'] = 0  # Assign texture unit

        # Water shader uniforms
        self.water['m_proj'].write(self.player.m_proj)
        self.water['u_texture_0'] = 2  # Assign texture unit
        self.water['water_area'] = WATER_AREA  # Define water area dimensions
        self.water['water_line'] = WATER_LINE  # Define water level

        # Clouds shader uniforms
        self.clouds['m_proj'].write(self.player.m_proj)
        self.clouds['center'] = CENTER_XZ  # Cloud movement center reference
        self.clouds['bg_color'].write(BG_COLOR)  # Background color for clouds
        self.clouds['cloud_scale'] = CLOUD_SCALE  # Cloud scaling factor

    def update(self):
        """Updates the view matrix in all shaders to reflect camera movements."""
        self.chunk['m_view'].write(self.player.m_view)
        self.voxel_marker['m_view'].write(self.player.m_view)
        self.water['m_view'].write(self.player.m_view)
        self.clouds['m_view'].write(self.player.m_view)

    def get_program(self, shader_name):
        """
        Loads and compiles the vertex and fragment shaders, then links them into a shader program.

        Parameters:
            shader_name: The base name of the shader files (without extension).
        Returns:
            A compiled and linked shader program.
        """
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        # Compile and link the shader program
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
