import urwid
import numpy as np
import grid
global widget
global g
global sf
global prog
global sta
import sys
speed=0.1
PAUSED=False
palette = [
    ('inside', 'black', 'dark green','standout'),
    #('better','black','green'),
    ('streak', 'dark green', 'black'),
    ('bg', 'dark green', 'black'),]

class Model():
    def __init__(self,world):
        self.speed=0.1
        self.paused=False
        self.world=world

    def set_speed(self,sp):
        self.speed=sp




class Cool_grid(urwid.Text):
    def __init__(self,txt,gr):
        urwid.Text.__init__(self,txt,align="left")
        self.gr=gr
        #self.gr : grid.grid


    def mouse_event(self,size, event, button, col, row, focus):

        if(row < self.gr.H and col < self.gr.W and button==1):
            self.gr.set_cell(row,col,1)

        if(row < self.gr.H and col < self.gr.W and button==3):
            self.gr.set_cell(row,col,0)

    def load(self,path=None):

        self.gr=self.gr.load()
        self.gr.update()
        sf = self.gr.pretty_grid()
        self.base_widget.set_text(('streak', sf))


    def save(self,path=None):
        self.gr.save()



class progress_slider(urwid.ProgressBar):
    #normalizzare a larghezza containre
    def __init__(self,txt):
        urwid.ProgressBar.__init__(self,'bg','inside',500,980)

    def update(self):
        global speed
        self.set_completion(1000-speed*1000)

        #self.set_text(('streak',"SPEED: "+str(speed)))
        #self.set_text(('streak',"SPEED: "+u"\u2592"*(20-int(speed*20)+1)))


class status(urwid.Text):
    def __init__(self,txt=None):
        self.stat=['|','/','-','\\','|']
        self.index=0
        urwid.Text.__init__(self,self.stat[self.index])

    def update(self):
        self.index=(self.index+1)%(len(self.stat)-1)
        self.set_text(('streak',self.stat[self.index]))


def callback(_loop,_data):
    global widget
    global prog
    global sta
    if not PAUSED:
        widget.gr.update()
        sta.update()
    #_loop:urwid.MainLoop

        # _loop.screen.get_input()get
    _loop.screen.set_input_timeouts(0.1,0.1,0.1)

    sf = widget.gr.pretty_grid()
    widget.base_widget.set_text(('streak', sf))



    _loop.set_alarm_in(speed,callback)
    return

def handle_click(cl_event,gr):
    cords=[0,0]
    gr.flip_cell(cords[1],cords[0])
    return

def unhandled_input(key):
    global speed
    global prog
    #speed inversa
    if key=="+":
        speed_up_simulation()
    if key=="-":
        slow_down_simulation()
    prog.update()

def speed_up_simulation(dt=None):
    global speed
    if speed>0.02:
        speed-=0.01
    else:
        speed=0.02

def slow_down_simulation(dt=None):
    global speed
    if speed<1.0:
        speed+=0.05
    else:
        speed=1.0

def get_buttons():

    def sw(_):
        global PAUSED
        PAUSED= not PAUSED
    def quit(_):
        exit()

    def clear_grid(_):
        global widget
        widget.gr.clear()

    def randomize(_):
        global widget
        widget.gr.random_int()
        widget.gr.update()

    def load(_):
        global widget

        widget.load()

    def save(_):
        global widget
        widget.save()

    pause=urwid.Button("PAUSE",on_press=sw)
    ex = urwid.Button("EXIT",on_press=quit)
    clear=urwid.Button("CLEAR",on_press=clear_grid)
    rand = urwid.Button("RANDOMIZE",on_press=randomize)
    place=urwid.Button("LOAD",on_press=load)
    lace = urwid.Button("SAVE", on_press=save)
    spm=urwid.Button("SPEED +",on_press=speed_up_simulation)
    spl=urwid.Button("SPEED -",on_press=slow_down_simulation)
    butts=[pause,ex,clear,rand,place,lace,spm,spl]
    stylized_butts=[]
    for b in butts:
        stylized_butts.append(urwid.AttrMap(b,'inside'))
    container = urwid.GridFlow(stylized_butts,20,2,2,align="center")
    container=urwid.LineBox(container)

    return container

def build_view():
    global sf
    global widget
    global g
    infoBox=urwid.Text("Conway's Game Of Life.\n Use + and - to speed up or slow down the simulation\n You can 'turn on' cells with your left click and 'kill' them with the right one")
    infoBox=urwid.LineBox(infoBox)
    infoBox=urwid.AttrMap(infoBox,'bg')
    widget=Cool_grid(('bg',""),g)
    prog=progress_slider(('inside',"#####"))
    #prog=urwid.ProgressBar('inside','inside',50,100)
    sta = status()
    prog.update()
    but=get_buttons()
    loader = urwid.Edit("path to file : ")
    load_tile=urwid.LineBox(loader)
    pil = urwid.Pile([sta]+[prog]+[but]+[infoBox]+[load_tile])
    col = urwid.Columns([('weight',3,widget),('weight',1.5,pil)],2)
    ln = urwid.LineBox(col,"Conway's GOL")
    mapa = urwid.AttrMap(ln, 'bg')
    fill = urwid.Filler(ln,'middle')
    return fill,widget,sta,prog

def main():
    #TODO RIFARE CON MODEL CONTROLLER
    global g
    global sf
    global widget
    global sta
    global prog

    g = grid.grid(40,120)
    ml = Model(g)
    fill,widget,sta,prog = build_view()


    main_loop = urwid.MainLoop(fill, palette,unhandled_input=unhandled_input)
    main_loop.set_alarm_in(1, callback,user_data=ml)
    main_loop.run()



main()