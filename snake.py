from tkinter import *
import tkinter.font as tkFont
from random import randint
class main():
    def __init__(self):
        self.root=Tk()
        self.setup()
        self.widget()
        self.snake_init()
        self.setup_bind()
        self.loop()
    def setup(self):
        self.root.title("Python貪食蛇")
        self.w=32
        self.h=32
        self.ms=20
        self.fs=2000
        self.lenth=24
        self.fruits=[]
        self.font=tkFont.Font(family="helvetica",size=6)
    def widget(self):
        self.pxs=[]
        for y in range(self.h):
            self.pxs.append([])
            for x in range(self.w):
                self.pxs[-1].append(Label(self.root,borderwidth=1,fg="white",bg="white",text="O",relief="solid",font=self.font))
                self.pxs[-1][-1].grid(row=y+1,column=x+1)
    def snake_init(self):
        self.direction=(0,1)
        self.head=(self.h//2,self.w//2)
        self.body=[self.head]
        for i in range(self.lenth-1):
            self.body.append((self.head[0]+self.direction[0]*-1,self.head[1]+self.direction[1]*-1))
    def setup_bind(self):
        self.root.bind("<w>",lambda x: self.change_direction("w"))
        self.root.bind("<s>",lambda x: self.change_direction("s"))
        self.root.bind("<a>",lambda x: self.change_direction("a"))
        self.root.bind("<d>",lambda x: self.change_direction("d"))
    def update(self):
        self.head=(self.head[0]+self.direction[0],self.head[1]+self.direction[1])
        try:
            self.change_px(self.head,"black")
        except (IndexError):
            if self.direction==(0,1):
                self.head=(self.head[0],0)
            elif self.direction==(0,-1):
                self.head=(self.head[0],self.w-1)
            elif self.direction==(1,0):
                self.head=(0,self.head[1])
            elif self.direction==(-1,0):
                self.head=(self.h-1,self.head[1])
            self.change_px(self.head,"black")
        if self.head in self.body:
            index=self.body.index(self.head)
            for element in self.body[index:]:
                self.change_px(element,"white")
            self.body=self.body[0:index]
            self.lenth=len(self.body)
        if self.head in self.fruits:
            print("+")
            self.lenth+=5
            self.fruits.remove(self.head)
        self.change_px(self.head,"black")
        self.body.insert(0,self.head)
        if len(self.body)>self.lenth:
            if self.body[-1] not in self.fruits:
                self.change_px(self.body[-1],"white")
            self.body.pop()
        self.root.after(self.ms,self.update)
    def change_direction(self,char):
        if char=="w" and self.direction!=(1,0):
            self.direction=(-1,0)
        elif char=="s" and self.direction!=(-1,0):
            self.direction=(1,0)
        elif char=="a" and self.direction!=(0,1):
            self.direction=(0,-1)
        elif char=="d" and self.direction!=(0,-1):
            self.direction=(0,1)
    def generate_fruit(self):
        fruit=(randint(0,self.h-1),randint(0,self.w-1))
        while fruit in self.fruits:
            fruit=(randint(0,self.h-1),randint(0,self.w-1))
        self.change_px(fruit,"red")
        self.fruits.append(fruit)
        self.root.after(self.fs,self.generate_fruit)
    def loop(self):
        self.root.after(self.ms,self.update)
        self.root.after(self.fs,self.generate_fruit)
        self.root.mainloop()
    def change_px(self,coords,color):
        self.pxs[coords[0]][coords[1]].config(fg=color,bg=color)
if __name__=="__main__":
    main()

