from settings import *
import moderngl as mgl
import pygame as pg
import sys
from shader_program import ShaderProgram
from scene import Scene
from player import Player
from textures import Textures

class VoxelEngine:
    """The core engine class responsible for initializing and running the voxel rendering engine."""
    def __init__(self):
        """Initializes the engine, sets up the OpenGL context, and configures the display."""
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)

        # Create an OpenGL-enabled display window
        pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()

        # Enable depth testing, back-face culling, and blending for rendering
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.gc_mode = 'auto' # Enable automatic garbage collection for OpenGL objects

        self.clock = pg.time.Clock()
        self.delta_time = 0 # Time between frames
        self.time = 0 # Elapsed time in seconds

        # Lock mouse to window and hide cursor
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.is_running = True
        self.on_init()

    def on_init(self):
        """Initializes game components such as textures, player, shader program, and scene."""
        self.textures = Textures(self)
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)

    def update(self):
        """Updates game logic, including player movement, shaders, and scene objects."""
        self.player.update()
        self.shader_program.update()
        self.scene.update()

        # Update timing values
        self.delta_time = self.clock.tick(FPS) # Limit FPS and get frame duration
        self.time = pg.time.get_ticks() * 0.001 # Get elapsed time in seconds
        pg.display.set_caption(f'{self.clock.get_fps() :.0f}') # Update window title with FPS

    def render(self):
        """Clears the screen and renders the scene."""
        self.ctx.clear(color=BG_COLOR)
        self.scene.render()
        pg.display.flip() # Swap buffers to display the frame

    def handle_events(self):
        """Handles user input events such as quitting and player interactions."""
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False
            self.player.handle_event(event=event)

    def run(self):
        """The main game loop that processes events, updates logic, and renders frames."""
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()

        # Clean up resources and exit
        pg.quit()
        sys.exit()

if __name__ == '__main__':
    app = VoxelEngine()
    app.run()
