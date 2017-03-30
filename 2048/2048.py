from sys import exit
import numpy as np
import subprocess

class Board(object):
    
    def __init__(self):
        self.board_state=np.zeros((4,4),dtype=np.int)
        self.move_turns=0
        self.game_on=False
        self.game_scores=0

    # Show the board in array
    def show_board(self):
        subprocess.call("cls", shell = True)
        print 'w,a,s,d control the move direction, press o exit the game'
        for i in range(4):
            print '%4s %4s %4s %4s'%(self.board_state[i][0] if self.board_state[i][0]!=0 else ' ',
                                     self.board_state[i][1] if self.board_state[i][1]!=0 else ' ',
                                     self.board_state[i][2] if self.board_state[i][2]!=0 else ' ',
                                     self.board_state[i][3] if self.board_state[i][3]!=0 else ' ')
                  
    def start(self):
        self.game_on=True
        # randomly set two different position into 2
        init_index=np.random.randint(0,16,size=2)
        while init_index[0]==init_index[1]:
            init_index=np.random.randint(0,16,size=2)
        init_row=init_index/4
        init_col=init_index%4
        self.board_state[[init_row],[init_col]]=2
        self.show_board()
        # start game
        while self.game_on==True:
            a=raw_input('Your move: ')
            ex_state=self.board_state.copy()  # save the state of previous board
            if a in ['w','W']:
                self.up_move()
            elif a in ['a','A']:
                self.left_move()
            elif a in ['d','D']:
                self.right_move()
            elif a in ['s','S']:
                self.down_move()
            elif a in ['o','O']:
                exit()
            else:
                subprocess.call("cls", shell = True)
                self.show_board()
                continue
            same_mat=ex_state==self.board_state
            if False in same_mat:           # If move action change the old state, add new number in random free space
                # If there is no space for new number, get result as over
                zero_pos=np.argwhere(self.board_state==0)
                # merge 2 within 500 turns
                if self.move_turns<500:
                    sl_num=np.random.randint(0,len(zero_pos))
                    self.board_state[zero_pos[sl_num][0]][zero_pos[sl_num][1]]=2
                else:                                                           # merge 4 after 500 turns
                    sl_num=np.random.randint(0,len(zero_pos))
                    self.board_state[zero_pos[sl_num][0]][zero_pos[sl_num][1]]=4                    
                self.move_turns+=1
            self.show_board()
            self.game_on=self.go_on()
       
       # judge if game is over      
    def go_on(self):
        if 0 in self.board_state:
            return True
        for rw in range(4):
            for cl in range(4):
                if rw<3 and self.board_state[rw][cl]==self.board_state[rw+1][cl]:
                    return True
                if cl<3 and self.board_state[rw][cl]==self.board_state[rw][cl+1]:
                    return True
        print "Game over"
        return False
         
    # merge neighbour same numbers into 1
    def merge_up(self):
        for cl in range(4):
            for rw in range(3):
                if self.board_state[rw][cl]==self.board_state[rw+1][cl]:
                    self.board_state[rw][cl]*=2
                    self.board_state[rw+1][cl]=0
    
    # shift zeros in the back of col
    def align_up(self):
        for cl in range(4):
            for rw in range(3):
                if self.board_state[rw][cl]==0:
                    i=rw+1
                    while i<=3:
                        if self.board_state[i][cl]!=0:
                            self._swap(i,cl,rw,cl)
                            break
                        i+=1
                        
    def up_move(self):
        self.align_up()
        self.merge_up()
        self.align_up()
        
    def merge_down(self):
        for cl in range(4):
            for rw in range(3,0,-1):
                if self.board_state[rw][cl]==self.board_state[rw-1][cl]:
                    self.board_state[rw][cl]*=2
                    self.board_state[rw-1][cl]=0
                    
    def align_down(self):
        for cl in range(4):
            for rw in range(3,0,-1):
                if self.board_state[rw][cl]==0:
                    i=rw-1
                    while i>=0:
                        if self.board_state[i][cl]!=0:
                            self._swap(i,cl,rw,cl)
                            break   
                        i-=1
    
    def down_move(self):
        self.align_down()
        self.merge_down()
        self.align_down()
        
    # Take the advantage of transpose to apply the same process to left and right move
    def left_move(self):
        self.board_state=self.board_state.T
        self.up_move()
        self.board_state=self.board_state.T   
        
    def right_move(self):
        self.board_state=self.board_state.T
        self.down_move()
        self.board_state=self.board_state.T                  
                    
    def _swap(self,r1,c1,r2,c2):
        tem=self.board_state[r1][c1]
        self.board_state[r1][c1]=self.board_state[r2][c2]
        self.board_state[r2][c2]=tem
        
if __name__=="__main__":
    well_board=Board()
    print "Start Game!"
    well_board.start()
