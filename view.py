import urwid

class View():

    def __init__(self,state,g):

        infoBox = urwid.Text(
            "Conway's Game Of Life.\n Use + and - to speed up or slow down the simulation\n You can 'turn on' cells with your left click and 'kill' them with the right one")
        infoBox = urwid.LineBox(infoBox)
        infoBox = urwid.AttrMap(infoBox, 'bg')
        self.widget = Cool_grid(('bg', ""), g)
        self.prog = progress_slider(('inside', "#####"))
        # prog=urwid.ProgressBar('inside','inside',50,100)
        self.sta = status()
        self.speed=0.05
        self.prog.update(self.speed)
        self.pause=False
        but = self.get_buttons()
        loader = urwid.Edit("path to file : ")
        load_tile = urwid.LineBox(loader)
        pil = urwid.Pile([self.sta] + [self.prog] + [but] + [infoBox] + [load_tile])
        col = urwid.Columns([('weight', 3, self.widget), ('weight', 1.5, pil)], 2)
        ln = urwid.LineBox(col, "Conway's GOL")
        #mapa = urwid.AttrMap(ln, 'bg')
        self.fill = urwid.Filler(ln, 'middle')

        self.palette=[('inside', 'black', 'dark green','standout'),('streak', 'dark green', 'black'), ('bg', 'dark green', 'black'),]

    def callback(self,_loop, _data):

        if not self.pause:
            self.widget.gr.update()
            self.sta.update()
        # _loop:urwid.MainLoop

        # _loop.screen.get_input()get
        _loop.screen.set_input_timeouts(0.1, 0.1, 0.1)

        sf = self.widget.gr.pretty_grid()
        self.widget.base_widget.set_text(('streak', sf))

        _loop.set_alarm_in(self.speed, self.callback)
        return

    def speed_up_simulation(self):
        if self.speed > 0.01:
            self.speed -= 0.01
        else:
            self.speed = 0.01

    def slow_down_simulation(self):
        if self.speed < 0.5:
            self.speed += 0.05
        else:
            self.speed = 0.5

    def get_buttons(self):
        def sw(_):
            self.pause = not self.pause

        def quit(_):
            exit()

        def clear_grid(_):

            self.widget.gr.clear()

        def randomize(_):

            self.widget.gr.random_int()
            self.widget.gr.update()

        def load(_):


            self.widget.load()

        def save(_):

            self.widget.save()

        pause = urwid.Button("PAUSE", on_press=sw)
        ex = urwid.Button("EXIT", on_press=quit)
        clear = urwid.Button("CLEAR", on_press=clear_grid)
        rand = urwid.Button("RANDOMIZE", on_press=randomize)
        place = urwid.Button("LOAD", on_press=load)
        lace = urwid.Button("SAVE", on_press=save)
        spm = urwid.Button("SPEED +", on_press=self.speed_up_simulation)
        spl = urwid.Button("SPEED -", on_press=self.slow_down_simulation)
        butts = [pause, ex, clear, rand, place, lace, spm, spl]
        stylized_butts = []
        for b in butts:
            stylized_butts.append(urwid.AttrMap(b, 'inside'))
        container = urwid.GridFlow(stylized_butts, 20, 2, 2, align="center")
        container = urwid.LineBox(container)

        return container

    def unhandled_input(self,key):
        if key == "+":
            self.speed_up_simulation()
        if key == "-":
            self.slow_down_simulation()
        self.prog.update(self.speed)

class progress_slider(urwid.ProgressBar):
    #normalizzare a larghezza containre
    def __init__(self,txt):
        urwid.ProgressBar.__init__(self,'bg','inside',500,970)
    def update(self,sp):
        self.set_completion(990-sp*1980)


class status(urwid.Text):
    def __init__(self,txt=None):
        self.stat=['|','/','-','\\','|']
        self.index=0
        urwid.Text.__init__(self,self.stat[self.index])

    def update(self):
        self.index=(self.index+1)%(len(self.stat)-1)
        self.set_text(('streak',self.stat[self.index]))

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