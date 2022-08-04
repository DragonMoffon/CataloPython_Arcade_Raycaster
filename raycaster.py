import math
from PIL import Image
from dataclasses import dataclass
import arcade.gl as gl
from array import array
import numpy as np

import arcade

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
TEX_SIZE = 64

WORLD_LIST = ((1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2),
              (1, 1, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 0, 2, 3, 2),
              (1, 0, 0, 0, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 2, 0, 2),
              (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 2),
              (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2),
              (1, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 0, 0, 0, 2, 0, 2),
              (1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 0, 2),
              (1, 0, 1, 1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2),
              (1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2),
              (1, 0, 0, 1, 0, 1, 1, 2, 0, 2, 2, 0, 0, 2, 0, 2, 2),
              (1, 1, 0, 0, 0, 0, 1, 2, 0, 0, 0, 2, 0, 2, 0, 0, 2),
              (1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2))

WORLD_LIST_2 = ((1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2),
                (2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
                (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2),
                (2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
                (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2),
                (2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1),
                (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2),
                (2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
                (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2),
                (2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
                (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2),
                (1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2))

wall_tex = []
for t_x in range(TEX_SIZE):
    texture = arcade.load_texture("brick_chonk.png", t_x * 10, 0, 10, TEX_SIZE*10)
    wall_tex.append(texture)
wall_tex_2 = []
for t_x in range(TEX_SIZE):
    texture = arcade.load_texture("glowy_chonk.png", t_x * 10, 0, 10, TEX_SIZE*10)
    wall_tex_2.append(texture)
textures = (tuple(wall_tex), tuple(wall_tex_2))

image_1 = Image.open("brick.png")
image_2 = Image.open("glowy wall.png")

image_1 = image_1.convert("RGB")
image_2 = image_2.convert("RGB")

tex_1 = []
tex_2 = []
for t_x in range(TEX_SIZE):
    tex_1.append([])
    tex_2.append([])
    for t_y in range(TEX_SIZE):
        tex_1[t_x].append(image_1.getpixel((TEX_SIZE - t_x - 1, TEX_SIZE - t_y - 1)))
        tex_2[t_x].append(image_2.getpixel((t_x, t_y)))

texture = (tex_1, tex_2)


@dataclass
class Pixels:
    buffer: gl.Buffer
    vao: gl.geometry


class RayCastWindow(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "RAY CAST")
        arcade.set_background_color(arcade.color.BLACK)
        self.background = arcade.load_texture("background.png")
        self.colors = [((28, 146, 109), (26, 112, 82)), ((109, 28, 146), (89, 8, 126))]
        self.world_map = tuple(WORLD_LIST_2)
        self.lists = (WORLD_LIST, WORLD_LIST_2)
        self.world_index = 1
        self.world_map = self.lists[self.world_index]

        self.ctx.enable_only()

        self.run = False
        self.move = 0

        self.blast_dir_x = 0
        self.blast_dir_y = 0
        self.blast_pos_x = 0
        self.blast_pos_y = 0
        self.blast_spawn = 0

        self.pos_x = 4
        self.pos_y = 2

        self.pitch = 0
        self.pos_z = 0
        self.jump = 0
        self.resolution = 1

        self.dir_x = 1
        self.dir_y = 0

        self.plane_x = 0
        self.plane_y = 0.66

        self.walls = []
        self.pixels = None
        self.cast_through = []
        self.tex_height = TEX_SIZE

        self.move_speed = 0
        self.rotation_speed = 0

        self.change_x = 0
        self.change_y = 0

        self.rotation_change = 0

        self.pressed = True
        self.tab = False

        self.walls = arcade.SpriteList()
        for x in range(SCREEN_WIDTH + 60):
            sprite = arcade.Sprite(center_x=x, center_y=SCREEN_HEIGHT/2)
            self.walls.append(sprite)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        if self.walls[0].texture is not None:
            self.walls.draw()
            pass

        if self.tab:
            for y in range(17):
                for x in range(12):
                    map_xy = self.world_map[x][y]
                    text = str(map_xy)
                    if x == math.floor(self.pos_x) and y == math.floor(self.pos_y):
                        arcade.draw_text(text, x * 10 + 5, y * 10 + 5, arcade.color.RADICAL_RED)
                    elif map_xy:
                        arcade.draw_text(text, x * 10 + 5, y * 10 + 5, arcade.color.DARK_GRAY)
                    elif (x, y) in self.cast_through:
                        arcade.draw_text(text, x * 10 + 5, y * 10 + 5, arcade.color.YELLOW)
                    else:
                        arcade.draw_text(text, x * 10 + 5, y * 10 + 5, arcade.color.GRAY)

    def on_update(self, delta_time: float):
        def _gen_wall_data():
            self.cast_through = []
            x = 0
            while x <= SCREEN_WIDTH + 60:
                camera_x = 2 * (x / SCREEN_WIDTH) - 1
                ray_dir_x = self.dir_x + self.plane_x * camera_x
                ray_dir_y = self.dir_y + self.plane_y * camera_x

                map_x = math.floor(self.pos_x)
                map_y = math.floor(self.pos_y)

                if ray_dir_y == 0:
                    delta_dist_x = 0
                elif ray_dir_x == 0:
                    delta_dist_x = 1
                else:
                    delta_dist_x = abs(1 / ray_dir_x)

                if ray_dir_x == 0:
                    delta_dist_y = 0
                elif ray_dir_y == 0:
                    delta_dist_y = 1
                else:
                    delta_dist_y = abs(1 / ray_dir_y)

                if ray_dir_x < 0:
                    step_x = -1
                    side_dist_x = (self.pos_x - map_x) * delta_dist_x
                else:
                    step_x = 1
                    side_dist_x = (map_x + 1 - self.pos_x) * delta_dist_x

                if ray_dir_y < 0:
                    step_y = -1
                    side_dist_y = (self.pos_y - map_y) * delta_dist_y
                else:
                    step_y = 1
                    side_dist_y = (map_y + 1 - self.pos_y) * delta_dist_y

                hit = False
                side = 1

                c_map = self.world_map
                while not hit:
                    if side_dist_x < side_dist_y:
                        side_dist_x += delta_dist_x
                        map_x += step_x
                        side = 0
                    else:
                        side_dist_y += delta_dist_y
                        map_y += step_y
                        side = 1

                    if (map_x, map_y) not in self.cast_through:
                        self.cast_through.append((map_x, map_y))

                    if c_map[map_x][map_y] == 3:
                        c_map = self.lists[1 - self.world_index]
                    elif c_map[map_x][map_y]:
                        hit = True

                if side:
                    perp_wall_dist = ((map_y - self.pos_y + ((1 - step_y) / 2)) / ray_dir_y)
                else:
                    perp_wall_dist = ((map_x - self.pos_x + ((1 - step_x) / 2)) / ray_dir_x)

                line_height = math.floor(SCREEN_HEIGHT / perp_wall_dist)

                if not side:
                    wall_x = self.pos_y + (perp_wall_dist * ray_dir_y)
                else:
                    wall_x = self.pos_x + (perp_wall_dist * ray_dir_x)
                wall_x -= math.floor(wall_x)

                line_start = (SCREEN_WIDTH / 2) - (line_height / 2)
                line_end = (SCREEN_WIDTH/2) + (line_height / 2)
                tex_x = math.floor(wall_x * TEX_SIZE)
                if side == 0 and ray_dir_x > 0:
                    tex_x = TEX_SIZE - tex_x - 1
                elif side == 1 and ray_dir_y < 0:
                    tex_x = TEX_SIZE - tex_x - 1

                tex_num = self.world_map[map_x][map_y] - 1
                sprite = self.walls[x - 1]
                sprite.texture = textures[tex_num][tex_x]
                sprite.height = line_height
                x += self.resolution

        if self.change_x or self.change_y:
            if self.run:
                check_x = math.floor(self.pos_x + (self.change_x * 5))
                check_y = math.floor(self.pos_y + (self.change_y * 5))
                if not self.world_map[check_x][check_y]:
                    self.pos_x += self.change_x * 5
                    self.pos_y += self.change_y * 5
                    self.pressed = True
                elif self.world_map[check_x][check_y] == 3:
                    self.pos_x += self.change_x * 5
                    self.pos_y += self.change_y * 5
                    self.pressed = True
                    self.world_map = self.lists[1-self.world_index]
                    self.world_index = 1-self.world_index
            else:
                check_x = math.floor(self.pos_x + self.change_x)
                check_y = math.floor(self.pos_y + self.change_y)
                if not self.world_map[check_x][check_y]:
                    self.pos_x += self.change_x
                    self.pos_y += self.change_y
                    self.pressed = True
                elif self.world_map[check_x][check_y] == 3:
                    self.pos_x += self.change_x
                    self.pos_y += self.change_y
                    self.pressed = True
                    self.world_map = self.lists[1-self.world_index]
                    self.world_index = 1-self.world_index

        if self.rotation_change:
            rot_change = self.rotation_change * delta_time
            old_dir_x = self.dir_x
            self.dir_x = old_dir_x * math.cos(rot_change) - self.dir_y * math.sin(rot_change)
            self.dir_y = old_dir_x * math.sin(rot_change) + self.dir_y * math.cos(rot_change)
            old_plane_x = self.plane_x
            self.plane_x = old_plane_x * math.cos(rot_change) - self.plane_y * math.sin(rot_change)
            self.plane_y = old_plane_x * math.sin(rot_change) + self.plane_y * math.cos(rot_change)
            print(self.dir_x * self.plane_x + self.dir_y * self.plane_y)
            self.pressed = True
            self.change_x = self.dir_x * self.move_speed * self.move
            self.change_y = self.dir_y * self.move_speed * self.move

        self.pressed = True
        if self.pressed:
            _gen_wall_data()

            self.pressed = False

        self.move_speed = 1 * delta_time
        self.rotation_speed = math.radians(360/2.7564353243)

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.UP:
            self.change_x = self.dir_x * self.move_speed
            self.change_y = self.dir_y * self.move_speed
            self.pressed = True
            self.move = 1
        elif key == arcade.key.DOWN:
            self.change_x = -self.dir_x * self.move_speed
            self.change_y = -self.dir_y * self.move_speed
            self.pressed = True
            self.move = -1
        elif key == arcade.key.LEFT:
            self.rotation_change = -self.rotation_speed
            self.pressed = True
        elif key == arcade.key.RIGHT:
            self.rotation_change = self.rotation_speed
            self.pressed = True
        elif key == arcade.key.TAB and self.tab:
            self.tab = False
        elif key == arcade.key.LSHIFT:
            self.run = True
        elif key == arcade.key.TAB:
            self.tab = True
        elif key == arcade.key.W:
            self.pitch -= 5
        elif key == arcade.key.S:
            self.pitch += 5
        elif key == arcade.key.SPACE:
            self.jump = 15
        elif key == arcade.key.KEY_1:
            self.world_map = tuple(WORLD_LIST)
            self.pressed = True
        elif key == arcade.key.KEY_2:
            self.world_map = tuple(WORLD_LIST_2)
            self.pressed = True
        elif key == arcade.key.ESCAPE:
            self.close()

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.UP and self.change_x != -self.dir_x:
            self.change_x = 0
            self.change_y = 0
            self.move = 0
        elif key == arcade.key.DOWN and self.change_x != self.dir_x:
            self.change_x = 0
            self.change_y = 0
            self.move = 0
        elif key == arcade.key.LEFT and self.rotation_change < 0:
            self.rotation_change = 0
        elif key == arcade.key.RIGHT and self.rotation_change > 0:
            self.rotation_change = 0
        elif key == arcade.key.LSHIFT:
            self.run = False


def main():
    window = RayCastWindow()
    window.center_window()
    arcade.run()


if __name__ == "__main__":
    main()
