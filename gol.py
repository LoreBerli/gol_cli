import urwid
import numpy as np
import grid
import sys
import view

class Model():
    def __init__(self,world):
        self.speed=0.1
        self.paused=False
        self.world=world

    def set_speed(self,sp):
        self.speed=sp


def handle_click(cl_event,gr):
    cords=[0,0]
    gr.flip_cell(cords[1],cords[0])
    return

def main():

    g = grid.grid(40,120)
    ml = Model(g)
    vw=view.View(ml,g)

    main_loop = urwid.MainLoop(vw.fill, vw.palette,unhandled_input=vw.unhandled_input)
    main_loop.set_alarm_in(1, vw.callback,user_data={"mod":ml,"vw":vw})
    main_loop.run()



main()