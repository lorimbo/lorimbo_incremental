from __future__ import absolute_import
from imgui.integrations.pygame import PygameRenderer
import OpenGL.GL as gl
import imgui
import pygame
import sys
from graphics import Graphics
from Game_logic import Gamelogic

# color library
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (127, 0, 255)
orange = (255, 100, 0)
grey = (105, 105, 105)
teal = (173, 216, 230)
brown = (139, 69, 19)
aasdsa= 0






def main():
    pygame.init()
    Gamelogic.initializegame()
    size = 1500, 1000

    pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)

    imgui.create_context()
    impl = PygameRenderer()

    io = imgui.get_io()
    io.display_size = size
    Graphics.new_font = io.fonts.add_font_from_file_ttf("orange kid.ttf", 35)
    impl.refresh_font_texture()

    # initialize variables here

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            impl.process_event(event)
        impl.process_inputs()

        imgui.new_frame()
        # add imgui stuff here
        Graphics.creategui()
        Gamelogic.frameaction()


        gl.glClearColor(119/255, 136/255, 153/255, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()


if __name__ == "__main__":
    main()
