from settings import *
from meshes.cube_mesh import CubeMesh

class VoxelMarker:
    def __init__(self, voxel_handler):
        self.app = voxel_handler.app
        self.handler = voxel_handler
        self.position = glm.vec3(0)
        self.m_model = self.get_model_matrix()
        self.mesh = CubeMesh(self.app)

    def update(self):
        if self.handler.voxel_id:
            self.position = self.handler.voxel_world_pos

    def set_uniform(self):
        self.mesh.program['m_model'].write(self.get_model_matrix())

    def get_model_matrix(self):
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position))
        return m_model

    def render(self):
        if self.handler.voxel_id:
            self.set_uniform()
            self.mesh.render()
