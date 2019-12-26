from tkinter import *
from tkinter import messagebox
import tkinter.font as tkfont
import yaml
from random import randint
class main(object):
    def __init__(self):
        with open("config.yml","r",encoding="utf-8") as reader:
            self.config=yaml.load(reader,Loader=yaml.SafeLoader)
        self.root=Tk()
        self.setup()
        self.widget()
        self.scoreboard()
        self.snake()
        self.begin()
    def setup(self):
        self.w=self.config["game"]["width"]
        self.h=self.config["game"]["height"]
        self.speed=self.config["game"]["speed"]
        self.lenth=self.config["game"]["lenth"]
        self.fruitscore=self.config["game"]["fruitscore"]
        self.fruitfreq=self.config["game"]["fruitfreq"]
        self.scoreVar=StringVar()
        self.scoreVar.set("NULL")
        self.font=tkfont.Font(family=self.config["word"]["font"],size=self.config["word"]["size"])
        self.scorefont=tkfont.Font(family=self.config["word"]["font_2"],size=self.config["word"]["size_2"])
    def widget(self):
        self.root.title(self.config["word"]["title"])
        self.labels=[]
        for y in range(self.h):
            self.labels.append([])
            for x in range(self.w):
                self.labels[y].append(Label(self.root,text=self.config["word"]["intile"],font=self.font,borderwidth=1,relief="solid"))
                self.change_color((y,x),"nothing")
                self.labels[y][x].grid(row=y,column=x)
                #print("({},{})".format(y,x))
    def scoreboard(self):
        self.scorelabel=Label(self.root,textvariable=self.scoreVar,font=self.scorefont)
        self.scorelabel.config()
        self.scorelabel.grid(columnspan=self.w)
    def begin(self):
        self.scoreVar.set("按下空白鍵已開始")
        self.root.bind("<space>",lambda x: self.loop())
        self.root.mainloop()
    def snake(self):
        self.head=(self.h//2,self.w//2)
        self.body=[]
        self.fruits=[]
        self.direction=(0,1)
        self.direction_flag=True
    def loop(self):
        self.root.bind("<w>",lambda x: self.change_direction((-1,0)))
        self.root.bind("<s>",lambda x: self.change_direction((1,0)))
        self.root.bind("<a>",lambda x: self.change_direction((0,-1)))
        self.root.bind("<d>",lambda x: self.change_direction((0,1)))
        self.root.after(self.fruitfreq,self.genfruit)
        self.root.after(self.speed,self.update)
    def update(self):
        self.head=(self.head[0]+self.direction[0],self.head[1]+self.direction[1])
        self.direction_flag=True
        #print(self.head)
        try:
            self.change_color(self.head,"snake")
        except (IndexError):
            self.gameover()
        if self.head in self.body:
            self.gameover()
        self.body.insert(0,self.head)
        if len(self.body)>self.lenth:
            self.change_color(self.body[-1],"nothing")
            del self.body[-1]
        if self.head in self.fruits:
            self.lenth+=self.fruitscore
            print(self.lenth)
            self.fruits.remove(self.head)
        self.scoreVar.set("長度：{} cm".format(str(self.lenth)))
        self.root.after(self.speed,self.update)
    def change_color(self,coords,state):
        if coords[0]<0 or coords[1]<0:
            raise IndexError
        label=self.labels[coords[0]][coords[1]]
        color=self.config["color"][state]
        try:
            if label.snake_state=="fruit":
                if state=="snake":
                    label.config(fg=color,bg=color)
            else:
                label.config(fg=color,bg=color)
        except (AttributeError):
            label.snake_state=state
            label.config(fg=color,bg=color)
    def genfruit(self):
        fruit=(randint(0,self.h-1),randint(0,self.w-1))
        while fruit in self.fruits:
            fruit=(randint(0,self.h-1),randint(0,self.w-1))
        self.fruits.append(fruit)
        self.change_color(fruit,"fruit")
        self.root.after(self.fruitfreq,self.genfruit)
    def change_direction(self,direction):
        if direction != (self.direction[0]*-1,self.direction[1]*-1) and self.direction_flag==True:
            self.direction=direction
            self.direction_flag=False
    def gameover(self):
        messagebox.showinfo(self.config["word"]["title"],self.config["word"]["end"])
        self.root.quit()
if __name__=="__main__":
    main()