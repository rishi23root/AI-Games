from Sudoku import sudoku
from tkinter import *
from tkinter import Tk,simpledialog
from threading import Thread
from time import sleep as nap

class GUI(sudoku):
    def __init__(self,root):
        super().__init__()
        self.root = root
        self.root.title('Sudoku AI')
        self.width,self.height = 455,600
        self.head_bg ="#486684" #7f8c8d
        self.root.geometry(f"{self.width}x{self.height}")
        self.minutes,self.seconds = 0,0 # time 
        self.moving_height = 0
        self.wrong_red = "#ffa59e"
        self.right_blue = "#bdebff"
        self.selected_yellow = "#ddffc2"
        # for users use self.question grid
        self.default_indexes = []
        for row in range(self.side):
            for col in range(self.side):
                if self.question[row][col] :
                    self.default_indexes.append([row,col])

        # head
        self.head(self.root)
        
        # clock in thread 😎.
        self.time_thread = Thread(target = lambda : self.clock() , daemon=True)
        self.time_thread.start()
        
        # board
        self.board_grid(self.root)

        # bottom_btns
        self.bottom(self.root)

    def head(self,master):
        self.moving_height += 60

        self.head_top = Label(master,bg = self.head_bg)
        self.head_top.place(height = self.moving_height, width = self.width)

        # clock - time update every second 
        self.time_value = Label(self.head_top,font=('arial',30,'bold'),padx=10,bg=self.head_bg,fg='white',text=f"{str(self.minutes).zfill(2)}:{str(self.seconds).zfill(2)}")
        self.time_value.pack(side=RIGHT)
        
        self.Game_name = Label(self.head_top,font=('arial',30,'italic',UNDERLINE),padx=10,bg=self.head_bg,fg='#81fcae',text=f"Sudoku AI")
        self.Game_name.pack(side=LEFT)

    def clock(self):
        # we need to make how much time is passed so -> every sec add 1 in clock and divide it by 60       
        while True:
            # update every second # update the value here till the window exits it will run
            nap(1)
            self.seconds += 1
            if self.seconds == 60 : 
                self.minutes += 1  
                self.seconds = 0
            if self.minutes == 60 : self.minutes,self.seconds = 0,0 # reset the clock afer one hours
            
            time = f"{str(self.minutes).zfill(2)}:{str(self.seconds).zfill(2)}"
            self.time_value['text'] = time
                
    def board_grid(self,master):
        # use to render the grid and let user enter values
        # take 455 X 455 width and height +10 for border and all 
        self.canvas = Label(master,bg='#95a5a6')
        self.canvas.place(y=self.moving_height,width =self.width, height=self.width + 8)
        self.moving_height += self.width + 8 
        # creating grid
        for row in range(9):
            for col in range(9):
                tile_num = f"{row}{col}"
                default = self.question[row][col]
                text_value = "  " if default == 0 else str(default) 
                # btn = Button(master=canvas,name=str(tile_num),
                #             font=('arial',18,'bold'),text = text_value, 
                #             borderwidth = 1,highlightthickness = 2,
                #             background = "white",relief="solid") 
                # btn.grid(row=row,column=col,ipadx = 7, ipady =0,sticky=N+S+E+W)
                btn = Label(master=self.canvas,name=str(tile_num),
                            font=('arial',21,'bold'),text = text_value, 
                            borderwidth = 1,highlightthickness = 5,
                            bg = "white",relief="solid") 
                btn.grid(row=row,column=col,ipadx = 10, ipady = 2,sticky=N+S+E+W)
                btn.bind("<Button-1>", self.mouse_click)
        
        self.grid_ele = self.canvas.winfo_children()
    
    def check_possible(self,row,col,num):
        num = int(num)
        # row != rows and  col != cols because we dont want to compare element from it self 
        if num == 0 : return False
        # default nums
        if [row,col] in self.default_indexes : return False
        # row
        for cols in range(self.side): # to range in the row length
            if self.question[row][cols] == num and col != cols : return False

        # reading each cell 
        # for rows in self.question: 
        for rows in range(self.side):
            if self.question[rows][col] == num and row != rows :return False
        
        # for the box 
        row_range = row//self.side_small * self.side_small
        col_range = col//self.side_small * self.side_small
        for rows in range(row_range,row_range+self.side_small):
            for cols in range(col_range,col_range+self.side_small):
                if self.question[rows][cols] == num and rows != row and cols != col :
                    return False
        return True

    def mouse_click(self,e):
        # select a box and make it coloured blue if it is right else red
        indexs = str(e.widget).rsplit(".",1)[1]
        row,col = int(indexs[0]),int(indexs[1])
        # return if it is the default position
        if [row,col] in self.default_indexes : return
        # amd make it empty if it is not the default
        else : e.widget.configure(text = ' ')

        # listen for value keyboard key press (1-10] 
        e.widget.configure(bg = self.selected_yellow)   # seleted
        a = simpledialog.askstring(title="Enter Digit",prompt="What will be the Value ?")
        try :
            if a in [""," ","  "] : raise
            a = int(a.strip())
            if a not in range(1,10) : return
        except : return
        finally : e.widget.configure(background = "white")

        e.widget.configure(text = str(a))
        self.question[row][col] = a
        if not self.check_possible(row,col,a) : e.widget.configure(background = self.wrong_red)
        else : e.widget.configure(background = self.right_blue)

        # check the whole grid for error from any other elements  
        for i in self.grid_ele:
            name = str(i).rsplit('.',1)[1]
            row,col = int(name[0]),int(name[1])
            val_str = i["text"]
            val = int(val_str) if val_str != ' ' else 0
            
            if [row,col] in self.default_indexes : continue
            # update the clour of that element 
            
            if self.question[row][col] != 0:
                if not self.check_possible(row,col,val) : 
                    print(self.check_possible(row,col,val),row,col,val)
                    i["background"] = self.wrong_red
                else : i["background"] = self.right_blue
            i.update()

    def bottom(self,master):
        # this cointain 2 buttons new game - AI solve it
        bottom = Label(master,bg = self.head_bg)
        bottom.place(y= self.moving_height,height = self.height - self.moving_height, width = self.width)

        self.new_gird = Button(bottom,font=('arial',20,'bold'),padx=10,relief=GROOVE,text="New Board",command = self.new_setup)
        self.new_gird.place(x= 10,y=10)
        self.AI_btn   = Button(bottom,font=('arial',20,'bold'),padx=10,relief=GROOVE,text="AI solution",command = self.Ai_solve)
        self.AI_btn.place(x= 250,y=10 )

    def Ai_solve(self):
        # for visual effects
        self.new_gird["state"] = "disabled"
        self.AI_btn["state"] = "disabled"
        self.solve()
        self.new_gird["state"] = "normal"
        self.AI_btn["state"] = "normal"

    def update_cell(self,row,col,val):
        # redefine funtion for animation in grid
        '''Take index of the row and col and value to update useful in inheretance'''
        name = f"{row}{col}"
        # nap(0.1) # for animation but tkinter is not so great for this use also lag some time
        # print(row,col)
        for i in self.grid_ele:
            if name == str(i).rsplit('.',1)[1]:
                self.grid[row][col] = val
                if val : i['bg'] = '#81fcae'
                else : 
                    i['bg'] = 'white'
                    val = " "
                i['text'] = val
                i.update()
                return

    def new_setup(self):
        # remove board
        self.canvas.pack_forget()

        self.grid = self.sudoku_genrator()
        self.question = [ a[:] for a in self.grid[:]]
        self.moving_height = 60
        self.default_indexes = []
        for row in range(self.side):
            for col in range(self.side):
                if self.question[row][col] :
                    self.default_indexes.append([row,col])
        # print(self.default_indexes)
        
        # board
        self.board_grid(self.root)

    @classmethod
    def runner(cls):
        # runner for the gui
        root = Tk()
        gui = cls(root)
        root.mainloop()


if __name__ == "__main__":
    GUI.runner()


