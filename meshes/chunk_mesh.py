from meshes.base_mesh import BaseMesh
from meshes.chunk_mesh_builder import build_chunk_mesh

class ChunkMesh(BaseMesh):
    """
    Represents the mesh for a chunk in the world.

    This class handles the generation and management of a chunk’s vertex data,
    binding it to the appropriate shader program and rendering it using OpenGL.

    Attributes:
        app: The main application instance, providing access to the OpenGL context.
        chunk: The chunk associated with this mesh.
        ctx: The OpenGL rendering context.
        program: The shader program used for rendering the chunk.
        vbo_format (str): The format of the vertex buffer data.
        format_size (int): The total size of the vertex attributes.
        attrs (tuple[str, ...]): The attributes corresponding to the vertex format.
        vao: The vertex array object used for rendering the chunk.
    """

    def __init__(self, chunk):
        """
        Initializes the chunk mesh.

        Args:
            chunk: The chunk for which this mesh is being created.
        """
        super().__init__()
        self.app = chunk.app  # Reference to the main application
        self.chunk = chunk  # The chunk associated with this mesh
        self.ctx = self.app.ctx  # OpenGL rendering context
        self.program = self.app.shader_program.chunk  # Shader program for chunks

        # Define vertex buffer format
        self.vbo_format = '1u4'  # Single unsigned 4-byte integer
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())  # Compute attribute size
        self.attrs = ('packed_data',)  # Vertex attribute names

        # Generate the initial VAO
        self.vao = self.get_vao()

    def rebuild(self):
        """
        Rebuilds the chunk mesh.

        This method regenerates the vertex array object (VAO) when the chunk data changes.
        """
        self.vao = self.get_vao()

    def get_vertex_data(self):
        """
        Generates vertex data for the chunk mesh.

        Calls the `build_chunk_mesh` function to construct the mesh data based on the chunk’s voxel data.

        Returns:
            np.array: The generated vertex data for the chunk mesh.
        """
        mesh = build_chunk_mesh(
            chunk_voxels=self.chunk.voxels,
            format_size=self.format_size,
            chunk_pos=self.chunk.position,
            world_voxels=self.chunk.world.voxels
        )
        return mesh
