#!/usr/bin/python3

#Implements Conways Game of Life
#https://mathworld.wolfram.com/GameofLife.html


#Key points
#Uses an agent based model where the 'cell' manages all changes to local state
#The cell class expects to be in a square grid (for the neighbor calculations)
#The gol class implements the game state, can update it, and can draw it to screen


class cell:

    def __init__(self, x, y, state = None):
        import random

        self._x = x
        self._y = y
        self._revision = 0
        self._previous_state = None

        if state is None:
            self._state = random.choice([True, False])
        else:
            self._state = bool(state)

 
    def __bool__(self):
        return self._state


    def state(self, revision = None):
        #This method should allow for updating the cells in a parallel manor
        if revision is None:
            return self._state
        elif revision == self._revision:
            return self._state
        elif revision == self._revision-1:
            return self._previous_state
        else:
            print("Cell state revision is more than 1 update off")
            exit()


    def update(self, grid, gridsize):
        self._neighbors = 0

        #Calculate neighborhood value
        for xpos in range(self._x-1,self._x+2):         #Must offset by '2' to get the desired result
            for ypos in range(self._y-1,self._y+2):

                col = (xpos + gridsize.x) % gridsize.x      #Wrap the board, use modulus math to restrict us to the grid size
                row = (ypos + gridsize.y) % gridsize.y

                if grid[col][row].state(self._revision) is True:
                    if (xpos == self._x) and (ypos == self._y):     #Don't add oneself the the neighbor count
                        continue
                    else:
                        self._neighbors += 1

        #Update state
        self._previous_state = self._state
        
        if self._neighbors <= 1:
            self._state = False     #Dies from loneliness (0-1)
        elif self._neighbors == 2:
            pass                    #Two neighbors = no change
        elif self._neighbors == 3:
            self._state = True      #Will always return true since dead cells become live with 3 neighbors
        elif self._neighbors >= 4:
            self._state = False     #Dies from overpopulation (4+)

        self._revision += 1




class gol:

    def __init__(self):
        from collections import namedtuple
        size = namedtuple('size','x, y')
        self._gridsize = size(30,60)       #X is the horizontal lines (cols), Y is vertical lines (rows)
        
        #Create a 'grid' (list of lists) of 'cell' class objects and init them with their x,y location
        self._grid = [[cell(x,y) for y in range(self._gridsize.y)] for x in range(self._gridsize.x)] 


    def __str__(self):
        output = ""
        for x in range(self._gridsize.x):
            output += ''.join(['\u2588' if self._grid[x][y].state() is True else ' ' for y in range(self._gridsize.y)]) + '\n'

        return(output)


    def update(self):
        #Calls the cell.update() method on each position in the grid
        [[self._grid[posx][posy].update(self._grid, self._gridsize) for posy in range(self._gridsize.y)] for posx in range(self._gridsize.x)]


    def draw(self):
        #There is a lot of room for improvements in this method

        #Use pyplot to draw a representation of the grid
        from matplotlib import pyplot, colors
        colormap = colors.ListedColormap(["white","black"])

        #Convert the grid bool values into float values then use .imshow() to visualize data
        fgrid = [[1.0 if self._grid[x][y].state() is True else 0.0 for y in range(self._gridsize.y)] for x in range(self._gridsize.x)]
        pyplot.imshow(fgrid, cmap = colormap)

        pyplot.pause(.05)
        pyplot.cla() #required otherwise the render speed will slow down over time
        

    def is_stable(self):
        #Compares all cells state to previous_state -- if no values change return True and exit 
        #Also need a way to detect stable oscillation end states

        #TODO ~implement
        return False




if __name__ == '__main__':

    import time

    #Instantiate the game
    game = gol()

    count = 0
    while True:
        game.update()
        game.draw()
        count += 1

        #if game.is_stable():
        #    break

        if count == 1000:
            break

    #Print the final state to console
    print(game)

    #Pause here to leave the last draw() state on the screen
    print("Breakpoint reached, will delay 10 seconds before closing plot window")
    time.sleep(10)
