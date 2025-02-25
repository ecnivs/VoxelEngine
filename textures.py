import pygame as pg
import moderngl as mgl

class Textures:
    """Handles the loading and management of textures in the application."""
    def __init__(self, app):
        """
        Initializes the Textures class, loading various textures and assigning texture units.

        Parameters:
            app: The main application instance, providing context for rendering.
        """
        self.app = app
        self.ctx = app.ctx

        # load textures
        self.texture_0 = self.load('frame.png')
        self.texture_1 = self.load('water.png')
        self.texture_array_0 = self.load('tex_array_0.png', is_tex_array=True)

        # assign texture unit
        self.texture_0.use(location=0)
        self.texture_array_0.use(location=1)
        self.texture_1.use(location=2)

    def load(self, file_name, is_tex_array=False):
        """
        Loads a texture or texture array from a file.

        Parameters:
            file_name (str): The name of the texture file located in the 'assets' directory.
            is_tex_array (bool): Whether the texture should be treated as a texture array.

        Returns:
            The loaded texture object.
        """
        texture = pg.image.load(f'assets/{file_name}')
        texture = pg.transform.flip(texture, flip_x=True, flip_y=False)

        if is_tex_array:
            num_layers = 3 * texture.get_height() // texture.get_width()
            texture = self.app.ctx.texture_array(
                size=(texture.get_width(), texture.get_height() // num_layers, num_layers),
                components=4,
                data=pg.image.tostring(texture, 'RGBA')
            )
        else:
            texture = self.ctx.texture(
                size=texture.get_size(),
                components=4,
                data=pg.image.tostring(texture, 'RGBA', False)
            )
        # Set texture properties
        texture.anisotropy = 32.0
        texture.build_mipmaps()
        texture.filter = (mgl.NEAREST, mgl.NEAREST)

        return texture
