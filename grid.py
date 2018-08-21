import numpy as np
import sys
import copy
import pickle
import shutil

from scipy.ndimage import convolve
class cell:
    def __init__(self,x,y,alive=False,age=0):
        self.x=x
        self.y=y
        self.alive=alive
        self.age=age
    def get_older(self):
        self.age+=1

class grid:
    def __init__(self,H,W):
        self.H=H
        self.W=W
        self.last=np.zeros(shape=[H,W],dtype=np.int)
        self.last2=np.zeros(shape=[H,W],dtype=np.int)
        #self.cells=np.random.randint(0,2,size=[H,W],dtype=np.int)
        self.cells = np.zeros(shape=[H,W],dtype=np.int)
        self.nei=np.zeros(shape=[H,W],dtype=np.int)
        self.kernel=np.asarray([[1,1,1],[1,0,1],[1,1,1]])

    def random_int(self):
        self.last=np.zeros(shape=[self.H,self.W],dtype=np.int)
        self.last2=np.zeros(shape=[self.H,self.W],dtype=np.int)
        #self.cells=np.random.randint(0,2<<<<s,size=[H,W],dtype=np.int)
        self.cells = np.random.random_integers(0,1,size=[self.H,self.W])
        self.nei=np.zeros(shape=[self.H,self.W],dtype=np.int)

    def set_v(self,view):
        self.view=view

    def update(self):

        self.last=np.copy(self.cells)
        self.last2 = np.copy(self.last)
        self.nei=convolve(self.cells,self.kernel)
        dead=np.zeros_like(self.cells)
        alive=np.zeros_like(self.cells)
        dead[np.where(self.cells==0)]=1
        alive[np.where(self.cells==1)]=1
        self.cells=np.zeros_like(self.cells)
        self.cells[np.where(((self.nei>1 )& (self.nei<4))&(alive) |  (self.nei==3)&(dead))]=1

        self.last=self.cells+self.last
        self.last2=self.last+self.last2
        return

    def pretty(self):
        out=""
        for r in self.last:
            out += str(r).replace("0",u"\u2591").replace("2", u"\u2592").replace("1",u"\u2588").replace(" ","")
            out +="\n"

            #out += str(r).replace("0"," . ").replace("1", " # ")
        return out

    def pretty_grid(self):
        out=[]
        i = 0
        for r in self.last2:
            out.append([])
            for g in r:
                out[i].append(str(g).replace("0", u"\u2591").replace("1", u"\u2592").replace("2", u"\u2593").replace("3",u"\u2588").replace(" ",""))
            out[i].append("\n")

            i+=1

        return out

    def infos(self):
        pass
        #alive=np.ufunc.reduce(np.ufunc.)

    def show(self):
        out=str(self.cells).replace("0",u"\u2593").replace("1",u"\u2588")
        sys.stdout.write('\b'*len(out))
        sys.stdout.write('\r'+out)
        #sys.stdout.flush()

    def set_cell(self,x,y,value):
        if(self.cells[x,y]!=value):
            self.cells[x,y]=value
            self.last2[x,y]=value

    def clear(self):
        self.last=np.zeros(shape=[self.H,self.W],dtype=np.int)
        self.last2=np.zeros(shape=[self.H,self.W],dtype=np.int)
        #self.cells=np.random.randint(0,2,size=[H,W],dtype=np.int)
        self.cells = np.zeros(shape=[self.H,self.W],dtype=np.int)

    def load(self):

        fl=open("saved",'rb')
        g = pickle.load(fl)

        fl.close()
        return g

    def save(self):
        fl = open("saved",'wb')
        pickle.dump(self,fl,-1)
        fl.close()

    def flip_cell(self,x,y):

        self.cells[x,y]=(self.cells[x,y]+1)%2





def test():
    g = grid(10,10)
    for i in range(0,10):
        gf=g.pretty_grid()
        print(gf)
        g.update()
    g.save()
    g=g.load()
    gf=g.pretty_grid()
    print(gf)




#main()