import pygame as pg
from camera import Camera
from settings import *

class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        self.app = app
        super().__init__(position, yaw, pitch)

    def update(self):
        self.keyboard_control()
        self.mouse_control()
        super().update()

    def handle_event(self, event):
        voxel_handler = self.app.scene.world.voxel_handler

        if event.type == pg.MOUSEBUTTONDOWN:   
            if event.button == 1:
                voxel_handler.remove_voxel()
            if event.button == 3:
                voxel_handler.add_voxel()

        if event.type == pg.KEYDOWN:
            if pg.K_1 <= event.key <= pg.K_7:
                if voxel_handler.new_voxel_id != event.key - pg.K_0:
                    voxel_handler.new_voxel_id = event.key - pg.K_0

    def mouse_control(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_x <= 0 or mouse_x >= WIN_RES.x - 1 or mouse_y <= 0 or mouse_y >= WIN_RES.y - 1:
            pg.mouse.set_pos(WIN_RES.x // 2, WIN_RES.y // 2)
        else:
            if mouse_dx:
                self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
            if mouse_dy:
                self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.app.delta_time
        if key_state[pg.K_LSHIFT] and key_state[pg.K_w]:
            self.move_forward(vel * 2)
        elif key_state[pg.K_w]:
            self.move_forward(vel)
        if key_state[pg.K_s]:
            self.move_back(vel)
        if key_state[pg.K_d]:
            self.move_right(vel)
        if key_state[pg.K_a]:
            self.move_left(vel)
        if key_state[pg.K_SPACE]:
            self.move_up(vel)
        if key_state[pg.K_LCTRL]:
            self.move_down(vel)
