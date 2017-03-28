from sys import exit
import numpy as np
import subprocess

class Board(object):
    
    def __init__(self):
        self.game_on=True
        self.step=0
        self.board_screen=np.array([[" "," "," "],[" "," "," "],[" "," "," "]])
        self.board_state=np.array([[0,0,0],[0,0,0],[0,0,0]])
        self.player_turn=False
        self.exist_index=[]
        
    # The player move   
    def player_move(self, pos):
        if pos in self.exist_index:
            print "Incorrect input!"
            exit()
        row,col=self.parse(pos)
        if self.player_turn==True:
            self.board_state[row][col]=1
            self.player_turn=False
            self.step=self.step+1
            self.show_board()
            self.check_game()
        self.pc_move()
        
    
    # The computer move, randomly choose the spare region  
    def pc_move(self):
        if self.player_turn==False:
            #find the spare region
            rows,cols=np.nonzero(self.board_state)
            if len(rows)==0:
                pass
            else:
                for i in range(len(rows)):
                    self.exist_index.append((rows[i])*3+cols[i]+1)
            #Randomly pick one position
            pre_index=np.random.randint(1,9)
            while pre_index in self.exist_index:
                pre_index=np.random.randint(8)
                
            print pre_index
            row,col=self.parse(pre_index)
            self.board_state[row][col]=-1
            self.player_turn=True    
            self.step=self.step+1
            self.show_board()
            self.check_game()
    
    # Show the board
    def show_board(self):
        subprocess.call("cls", shell = True)
        for m in range(3):
            for n in range(3):
                if self.board_state[m][n]==1:
                    self.board_screen[m][n]="X"
                elif self.board_state[m][n]==-1:
                    self.board_screen[m][n]='O'
        for i in range(3):
            print self.board_screen[i]
        print ''
                
    # Check if there is a winner or game over
    def check_game(self):
        row_count=self.board_state.sum(axis=0)
        col_count=self.board_state.sum(axis=1)
        n11=self.board_state[1][1]
        n00=self.board_state[0][0]
        n22=self.board_state[2][2]
        n02=self.board_state[0][2]
        n20=self.board_state[2][0]
        cross_count=np.array([n00+n11+n22,n20+n11+n02])
        count_pool=np.concatenate((row_count,col_count,cross_count),axis=0)
        if 3 in count_pool:
            print 'You Win!'
            self.game_on=False
            exit()
        if -3 in count_pool:
            print 'Computer Win!'
            self.game_on=False
            exit()
        if self.step==9:
            print 'Game is over, no one win!'
            self.game_on=False
            exit()
    
    # parse the specific position based on index(1~9)
    def parse(self, player_in):
        row=player_in/3
        col=player_in%3
        if col==0:
            row=row-1
        col=col-1
        return row,col
        
if __name__=="__main__":
    well_board=Board()
    print "Start Game, your opponent turn!"
    well_board.pc_move()
    while well_board.game_on==True:
        print "Your turn!"
        well_board.player_move(int(input()))
    