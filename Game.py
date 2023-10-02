from __future__ import absolute_import
from imgui.integrations.pygame import PygameRenderer
import OpenGL.GL as gl
import imgui
import pygame
import sys
from graphics import Graphics
import graphics
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






def main():
    pygame.init()
    Gamelogic.initializegame()
    clock=pygame.time.Clock()
    size = 1500, 1000

    pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)

    imgui.create_context()
    impl = PygameRenderer()

    io = imgui.get_io()
    Graphics.io = io
    io.display_size = size
    for i in range(1,100):
        Graphics.Fonts['Helvetica'][str(i)]=io.fonts.add_font_from_file_ttf("Helvetica.ttf", i)
    impl.refresh_font_texture()
    pygame.mixer.music.load('Sounds/background.mp3')
    pygame.mixer.music.play(-1, 5.0)




    # initialize variables here
    fpslist=[]

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type ==pygame.KEYDOWN and event.key==pygame.K_F11:
                pygame.display.toggle_fullscreen()
            impl.process_event(event)
        impl.process_inputs()

        imgui.new_frame()
        # add imgui stuff here
        Graphics.creategui()
        Gamelogic.frameaction()
        imgui.set_next_window_size(105, 50)
        imgui.set_next_window_position(Graphics.widthfactor*1200, Graphics.heightfactor*500)
        Gamelogic.io = io
        imgui.begin('fps', False)
        fpslist.append(round(clock.get_fps()))
        if len(fpslist)>100:
            fpslist=fpslist[-100:]
        imgui.text(f'FPS:{round(sum(fpslist) / len(fpslist))}')
        imgui.end()

        pygame.mixer.music.set_volume(Gamelogic.musicvolume)




        gl.glClearColor(*[e/255 for e in graphics.Themes[Graphics.theme]['mainbackground']], 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()
        clock.tick(Gamelogic.fps)




if __name__ == "__main__":
    main()
