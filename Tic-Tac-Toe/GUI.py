from tic_tac_toe_AI import min_max_ai
from tkinter import *
from tkinter import Tk,messagebox
from threading import Thread
from time import sleep as nap

class GUI(min_max_ai):
    def __init__(self,root):
        super().__init__()
        
        self.title = 'X-O AI'
        self.root = root
        self.root.configure(bg='#95a5a6')
        self.root.title(self.title)
        self.width,self.height = 455,500
        self.head_bg ="#486684" #7f8c8d
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.minsize(self.width,self.height)
        self.minutes,self.seconds = 0,0 # time 
        self.moving_height = 0
        self.wrong_red = "#ffa59e"
        self.right_blue = "#bdebff"
        self.selected_yellow = "#ddffc2"

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
        
        self.Game_name = Label(self.head_top,font=('arial',30,'italic',UNDERLINE),padx=10,bg=self.head_bg,fg='#81fcae',text=f"X-O AI")
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
        self.canvas = Label(master,bg='#95a5a6')
        self.canvas.place(y=self.moving_height+10,x=35,width =self.width)
        self.moving_height += 350
        # creating grid
        for row in range(self.side):
            for col in range(self.side):
                tile_num = f"{row}{col}"
                default = self.grid[row][col].upper()
                text_value = "   " if default == "" else default
                btn = Button(master=self.canvas,name=str(tile_num),
                            font=('arial',32,'bold'),text = text_value, 
                            borderwidth = 2,highlightthickness = 1,
                            bg = "white",relief="solid")    
                btn.config(height=1,width=3) #fix disapearin tiles issue
                btn.grid(row=row,column=col,ipadx = 20, ipady = 10,sticky=N+S+E+W)
                btn.bind("<Button-1>", self.mouse_click)
        
        self.grid_ele = self.canvas.winfo_children()

    def bottom(self,master):
        # this cointain 2 buttons new game - AI solve it
        bottom = Label(master,bg = self.head_bg)
        bottom.place(y= self.moving_height + 10,height = self.height - self.moving_height , width = self.width)

        self.new_gird = Button(bottom,font=('arial',20,'bold'),padx=10,relief=GROOVE,text="New Board",command = self.new_setup)
        self.new_gird.place(x= 10,y=10)
        self.AI_btn = Button(bottom,font=('arial',20,'bold'),padx=10,relief=GROOVE,bg = self.wrong_red,text="Exit",command = lambda : self.root.destroy())
        self.AI_btn.place(x= 250,y=10,width = 190 )

    def mouse_click(self,e):
        ''' listen the event and update the box with value '''
        # human click
        indexs = str(e.widget).rsplit(".",1)[1]
        row,col = int(indexs[0]),int(indexs[1])
        if self.grid[row][col] == '':
            win,possition,index = self.update_board(row,col,self.human)
            if win:
                # print(self.human,win,possition,index)
                self.show_win(possition,index,self.human)
                return
            
        # let ai play 
        if sum([i.count("") for i in self.grid]) == 0 :
            # show no more moves it a tie 
            response = messagebox.askyesno(self.title, "It is Tie!!\n New game ?")
            if response :
                self.new_setup()
                return 
            else :
                exit()

        move = self.best_move(self.ai)
        if self.grid[move['i']][move['j']] == '':
            win,possition,index = self.update_board(move['i'],move['j'],self.ai,BG='#eefc81')
            if win:
                # print(self.ai,win,possition,index)
                self.show_win(possition,index,self.ai)

    def show_win(self,possition,index,player):
        """
        show who wins
        and update the colour to blue
        """
        # print(possition,index,player)
        if possition == 'row':
            for ele in self.grid_ele:
                name = str(ele).rsplit('.',1)[1]
                if int(name[0]) == index:
                    ele["background"] = '#5cabff'
        elif possition == 'col':
            for ele in self.grid_ele:
                name = str(ele).rsplit('.',1)[1]
                if int(name[1]) == index:
                    ele["background"] = '#5cabff'
        elif possition == 'dig':
            if index == 0 : # element 00 11 22
                for ele in self.grid_ele:
                    name = str(ele).rsplit('.',1)[1]
                    row,col = int(name[0]),int(name[1])
                    if row == col:
                        ele["background"] = '#5cabff'
            else : # index = 1, elements -02 11 20 
                for ele in self.grid_ele:
                    name = str(ele).rsplit('.',1)[1]
                    row,col = int(name[0]),int(name[1])
                    if (row,col) in [(1,1),(0,2),(2,0)]:
                        ele["background"] = '#5cabff'

        if player :
            message = f"AI wins the Game 😎😎"
        else :
            message = f"Human wins the Game !! Impossible🤔"

        res = messagebox.askyesno(self.title, message+'\nNew Game?')
        if res :
            self.new_setup()

    def update_board(self,row,col,player,BG='#81fcae'):
        # nap(0.1) # for animation but tkinter is not so great for this use also lag some time
        name = f"{row}{col}"
        for i in self.grid_ele:
            if name == str(i).rsplit('.',1)[1]:
                self.grid[row][col] = player
                i['bg'] = BG
                i['text'] = player.upper()
            i.update()
        return self.is_win(player)

    def new_setup(self):
        """CLEAR AND UPDATE THE BOARD"""
        # remove board
        self.canvas.pack_forget()
        self.grid = [["","",""] for _ in range(self.side)]
        self.moving_height = 60
        # board
        self.board_grid(self.root)

    @classmethod
    def executor(cls):
        # runner for the gui
        root = Tk()
        gui = cls(root)
        # gui.runner()
        root.mainloop()

if __name__ == "__main__":
    GUI.executor()
