import numpy as np

class BaseMesh:
    """
    A base class for managing OpenGL mesh objects.

    This class provides a structure for handling vertex buffer objects (VBOs),
    shader programs, and vertex array objects (VAOs) used in rendering.

    Attributes:
        ctx: The OpenGL context, initialized externally.
        program: The shader program used for rendering the mesh.
        vbo_format (str): The data format of the vertex buffer (e.g., "3f 3f" for positions and colors).
        attrs (tuple[str, ...]): Attribute names corresponding to the vertex format.
        vao: The vertex array object used for rendering.
    """

    def __init__(self):
        """
        Initializes the base mesh with default attributes.
        """
        self.ctx = None  # OpenGL context, set externally
        self.program = None  # Shader program, must be assigned before rendering
        self.vbo_format = None  # Format of vertex buffer data (e.g., "3f 3f")
        self.attrs: tuple[str, ...] = None  # Attribute names for vertex data
        self.vao = None  # Vertex array object

    def get_vertex_data(self) -> np.array:
        """
        Abstract method to retrieve vertex data.

        This method should be implemented in subclasses to return the vertex data.

        Returns:
            np.array: The vertex data array.
        """
        raise NotImplementedError("Subclasses must implement `get_vertex_data`.")

    def get_vao(self):
        """
        Generates and returns a Vertex Array Object (VAO) using the vertex data.

        This method initializes the VBO, binds it to the shader program, and
        creates the VAO.

        Returns:
            The generated VAO.
        """
        vertex_data = self.get_vertex_data()  # Retrieve vertex data from subclass implementation
        vbo = self.ctx.buffer(vertex_data)  # Create a buffer for vertex data
        vao = self.ctx.vertex_array(
            self.program, [(vbo, self.vbo_format, *self.attrs)], skip_errors=True
        )
        return vao

    def render(self):
        """
        Renders the mesh by drawing the VAO.

        This method assumes that the VAO is properly initialized and bound.
        """
        if self.vao:
            self.vao.render()
        else:
            raise RuntimeError("VAO is not initialized. Call `get_vao()` before rendering.")

