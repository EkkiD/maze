import sys, pygame
from collections import deque
import random

pygame.init()

grid_size = grid_rows, grid_cols = 20, 25
square_pixels = 20
base_offset = 50

size = width, height = (2*base_offset)+(grid_cols*square_pixels), (2*base_offset)+(grid_rows*square_pixels)

black = 0,0,0
white = 255,255,255
grey  = 0x6E6D6Da
green = 0x008000
dark  = 0x302226
brightgreen = 0x00ff00
red = 0xff0000
    
north = 1
east = 2
south = 4
west = 8

untouched = 0
visited = 1
stacked = 2
current = 3

   
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

render_steps = True

class node(object):
    """ Stores data regarding the self.nodes:
            - which walls are up
            - visited flag"""

    def __init__(self, row, col):
        self.walls = north | south | east | west
        if col == 0:               self.walls = self.walls ^ west
        if col == grid_cols - 1:   self.walls = self.walls ^ east
        if row == 0:               self.walls = self.walls ^ north
        if row == grid_rows - 1:   self.walls = self.walls ^ south
        self.status = 0

    def TearDown(self, wall):
        self.walls = self.walls ^ wall

    def Erect(self, wall):
        self.walls = self.walls | wall

    def IsStanding(self, wall):
        return self.walls & wall

    def AreAllWallsUp(self, row, col):
        """ Return true if the node has all Walls up, 
            false otherwise """
        if  ((row < 0) or (row >= grid_rows)):
                return False
        if ((col < 0) and (col >= grid_col)):
                return False

        if ((row != 0) and not(self.IsStanding(north))):
            return False
        if ((row != grid_rows-1) and not(self.IsStanding(south))):
            return False
        if ((col != 0) and not(self.IsStanding(west) )):
            return False
        if ((col != grid_cols-1) and not(self.IsStanding(east))):
            return False

        return True
    

class maze(object):
    """This class handles all of the maze generation and solving functions.

    Should be treated as a singleton until I figure out this member variable thing.
    
    For now this class will also take care of rendering the maze. Not sure if this is the best design but we'll use it for now"""
    
    def __init__(self):
        self.nodes = [None] * grid_rows
        for i in range(grid_rows):
            self.nodes[i] = [None] * grid_cols

        # initialize the array as a valid grid.
        for i in range(grid_rows):
            for j in range(grid_cols):
                self.nodes[i][j] = node(i, j)
        
        self.cellStack = deque()
        self.solve_start = (0,0)
        self.solve_end  = (grid_rows-1,grid_cols-1)

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_c:
                        self.clearMaze() 
                    if event.key == pygame.K_d:
                        self.runAlgorithm(self.DFSGenerate)
                    elif event.key == pygame.K_p:
                        #TODO: Implement Prim's method
                        self.runAlgorithm(self.DFSGenerate)
                    elif event.key == pygame.K_r:
                        self.runAlgorithm(self.DFSGenerate)
                        #TODO: implement DFS recursive
                    elif event.key == pygame.K_s:
                        #TODO: implement solve
                        self.runAlgorithm(self.DFSSolve)

            font = pygame.font.Font(None, 18)
            text = font.render("d-DFS Generate      p-Prim's Generate     c-Clear     s-Solve", 1, white)
            textpos = text.get_rect()
            textpos.bottom = screen.get_rect().bottom - base_offset/2
            textpos.centerx = screen.get_rect().centerx
            screen.blit(text, textpos)
        
            pygame.display.flip()

    def checkQuit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

    def randomLoc(self):
        row = random.randint(0,grid_rows-1)
        col = random.randint(0,grid_cols-1)
        self.cellStack.append((row, col))
        return

    def clearMaze(self):
        return

    def clearStatus(self):
        for row  in self.nodes:
            for node in row:
                node.status = untouched
        return

    def runAlgorithm(self, algorithm):
        #start at a random location
        if algorithm == self.DFSSolve:
            self.cellStack.append(self.solve_start)
        else:
            self.randomLoc()
        algorithm()
        self.DrawScreen()
        self.clearStatus()
        return

    def DrawScreen(self): 
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        #draw the outer border
        border_rect = (base_offset, base_offset, (grid_cols*square_pixels), (grid_rows*square_pixels))
        pygame.draw.rect(screen, grey, border_rect, 2)
    
        for row in range(grid_rows):
            for col in range(grid_cols):
                off_x = base_offset + col * square_pixels
                off_y = base_offset + row * square_pixels

                node = self.nodes[row][col]
                
                if node.IsStanding(north):
                    assert row > 0, "Can't draw north of row 0"
                    assert self.nodes[row-1][col].IsStanding(south), "Node %d, %d should have 'south' set"  % (row-1, col)
                    pygame.draw.line(screen, white, (off_x+2, off_y), (off_x+square_pixels-2, off_y), 2)

                if node.IsStanding(west):
                    assert col > 0, "Can't draw west of col 0"
                    assert self.nodes[row][col-1].IsStanding(east), "Node %d, %d should have 'east' set"  % (row, col-1)
                    pygame.draw.line(screen, white, (off_x, off_y+2), (off_x, off_y+square_pixels-2), 2)

                if node.status == stacked:
                    self.FillSquare((row, col), dark)

                if node.status == current:
                    self.FillSquare((row, col), green)

                if (row, col) == self.solve_start:
                    self.FillSquare((row, col), brightgreen)

                if (row, col) == self.solve_end:
                    self.FillSquare((row, col), red)

        pygame.display.flip()
        clock.tick(40)

    def FillSquare(self, loc, color):
        row = loc[0]
        col = loc[1]
        off_x = base_offset + col * square_pixels
        off_y = base_offset + row * square_pixels
        rect = (off_x+4, off_y+4,  square_pixels - 6, square_pixels - 6)
        pygame.draw.rect(screen, color, rect)

    def DFSGenerate(self):
        while True:
            try:
                top = self.cellStack.pop()
                row = top[0] 
                col = top[1]
                node = self.nodes[row][col]
                node.status = visited
                neighbors = []
                if (node.IsStanding(north)) and self.nodes[row-1][col].AreAllWallsUp(row-1, col):
                    neighbors.append(north)
    
                if (node.IsStanding(south)) and self.nodes[row+1][col].AreAllWallsUp(row+1, col):
                    neighbors.append(south)
    
                if (node.IsStanding(west)) and self.nodes[row][col-1].AreAllWallsUp(row, col-1):
                    neighbors.append(west)
    
                if (node.IsStanding(east)) and self.nodes[row][col+1].AreAllWallsUp(row, col+1):
                    neighbors.append(east)
    
                if(neighbors.__len__() == 0):
                    top = self.cellStack.pop()
                    self.nodes[top[0]][top[1]].status = current
                    self.cellStack.append(top)
                    if render_steps:
                        self.DrawScreen()
                    continue 
    
                index = random.randint(0,neighbors.__len__()-1)
                direction = neighbors[index]
    
                if(direction & north):
                    assert self.nodes[row-1][col].IsStanding(south), \
                                    "Node %d, %d should have 'south' set"  % (row-1, col)
                    self.nodes[row-1][col].TearDown(south)
                    node.TearDown(north)
                    new_loc = (row-1, col)
    
                elif(direction & south):
                    assert self.nodes[row+1][col].IsStanding(north), \
                                    "Node %d, %d should have 'north' set"  % (row+1, col)
                    self.nodes[row+1][col].TearDown(north)
                    node.TearDown(south)
                    new_loc = (row+1, col)
    
                elif(direction & east):
                    assert self.nodes[row][col+1].IsStanding(west), \
                                    "Node %d, %d should have 'east' set"  % (row, col+1)
                    self.nodes[row][col+1].TearDown(west)
                    node.TearDown(east)
                    new_loc = (row, col+1)
    
                elif(direction & west):
                    assert self.nodes[row][col-1].IsStanding(east), \
                                    "Node %d, %d should have 'south' set"  % (row, col+1)
                    self.nodes[row][col-1].TearDown(east)
                    node.TearDown(west)
                    new_loc = (row, col-1)
    
                node.status = stacked
                self.cellStack.append(top)
                self.cellStack.append(new_loc)
                self.nodes[new_loc[0]][new_loc[1]].status = current
                if render_steps: 
                    self.DrawScreen()
            except IndexError, e:
                # Once the stack is empty, we are done.
                break
        return  

    def DFSSolve(self):
        while True:
            try:
                top = self.cellStack.pop()
                if top == self.solve_end:
                    return
                row = top[0] 
                col = top[1]
                node = self.nodes[row][col]
                node.status = visited
                neighbors = []
                if  (row > 0) and (not node.IsStanding(north)) and self.nodes[row-1][col].status == untouched:
                    neighbors.append(north)
    
                if  (row < grid_rows-1) and (not node.IsStanding(south)) and self.nodes[row+1][col].status == untouched:
                    neighbors.append(south)
    
                if (col > 0) and (not node.IsStanding(west)) and self.nodes[row][col-1].status == untouched:
                    neighbors.append(west)
    
                if (col < grid_cols-1) and (not node.IsStanding(east)) and self.nodes[row][col+1].status == untouched:
                    neighbors.append(east)
    
                if(neighbors.__len__() == 0):
                    top = self.cellStack.pop()
                    self.nodes[top[0]][top[1]].status = current
                    self.cellStack.append(top)
                    self.DrawScreen();
                    continue 
    
                index = random.randint(0,neighbors.__len__()-1)
                direction = neighbors[index]
    
                if(direction & north):
                    new_loc = (row-1, col)
    
                elif(direction & south):
                    new_loc = (row+1, col)
    
                elif(direction & east):
                    new_loc = (row, col+1)
    
                elif(direction & west):
                    new_loc = (row, col-1)
    
                node.status = stacked
                self.cellStack.append(top)
                self.cellStack.append(new_loc)
                self.nodes[new_loc[0]][new_loc[1]].status = current
                 
                self.DrawScreen()
            except IndexError, e:
                # Once the stack is empty, we are done.
                break
        return
        



if __name__ == "__main__":
    myMaze = maze()
    myMaze.run()

