
w = 288
h = w
d = w
numBlocks = 4
blockSize = 0.4 * (w // (numBlocks))
fullBlockWidth = (w // (numBlocks)) / 2
stride = w // (numBlocks)

board = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
         ["6", ".", ".", "1", "9", "5", ".", ".", "."],
         [".", "9", "8", ".", ".", ".", ".", "6", "."],
         ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
         ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
         ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
         [".", "6", ".", ".", ".", ".", "2", "8", "."],
         [".", ".", ".", "4", "1", "9", ".", ".", "5"],
         [".", ".", ".", ".", "8", ".", ".", "7", "9"]]

board = [["4", ".", ".", "."],
         [".", ".", ".", "1"],
         [".", "4", "2", "."],
         ["2", ".", ".", "."]]

finalBoard = [[None for col in row] for row in board]

add_library('PeasyCam')

def setup():
    global board
    background(22, 25, 28)

    size(800, 800, OPENGL)
    cam = PeasyCam(this, 500)
    board = map2d(num2vec, board)

    # board = [[[(x,y,d)
    #            for d in range(4)]
    #           for y in range(4)]
    #          for x in range(4)]

def num2vec(ent):
    """Turn sudoku board into vectors of True/False."""
    if ent != ".":
        vec = [False] * numBlocks
        vec[int(ent) - 1] = True
    else:
        vec = [True] * numBlocks
    return vec

def map2d(fn, array):
    return [[fn(entry) for entry in row] for row in array]


def draw():
    global finalBoard
    # lights()
    #directionalLight(255, 255, 255, 1, 1, 1)
    background(255)
    fill(0)
    box(10)
    reCent = stride * (numBlocks) / 2
    translate(-reCent, -reCent, reCent)

    #directionalLight(255, 255, 255, 1, -1, 1)
    for row in range(numBlocks):
        for col in range(numBlocks):
            possibleValues = board[row][col]
            if sum(possibleValues) == 1:
                sol = [i for i, x in
                       enumerate(list(possibleValues)) if x][0]
                finalBoard[row][col] = sol+1
            else:
                sol = None

            for depth in range(numBlocks):
                # y, , z = row * stride, col * stride, depth * stride
                posVal = board[row][col][depth]

                if posVal == True:
                    c1 = 210 * (posVal)
                    c2 = 100 * (posVal)
                    c3 = 100 * (posVal)
                    a = 150
                else:
                    c1 = 100
                    c2 = 100
                    c3 = 100
                    a = 50
                colorDict = {0: [0, 0, 0],
                             1: [200, 100, 0],
                             2: [100, 200, 100],
                             3: [200, 200, 200]}

                #clr = [0+25*posVal[0], 0+50*posVal[1], 0+75*posVal[2]]
                if sol is not None:
                    if depth == sol:
                        # Green for solution
                        c1 = 0
                        c2 = 150
                        c3 = 0
                        a = 255
                    else:
                        a = 50
                fill(c1, c2, c3,
                     #(distVal) *
                     a
                     )
                #fill(0, (1-distAdj) * 100)
                noStroke()
                pushMatrix()
                #s = 2 * noiseVal ** 2
                translate(fullBlockWidth + col * stride,
                          fullBlockWidth + row * stride,
                          -fullBlockWidth - depth * stride)
                textSize(10)
                #text('xi:'+str(xi)+', yi:'+str(yi)+', zi:'+str(zi), 0, 0)
                box(blockSize)
                popMatrix()

    buffer = 20
    # Draw boundaries
    pushMatrix()
    #translate(-blockWidth, -blockWidth, blockWidth)
    stroke(0, 0, 0, 200)
    fill(0)
    # box(blockSize)
    strokeWeight(10)
    # box(100)
    line(0, 0, 0, 300, 0, 0)
    line(0, 0, 0, 0, 300, 0)
    line(300, 0, 0, 300, 300, 0)
    line(0, 300, 0, 300, 300, 0)

    strokeWeight(2)
    for i in range(1, numBlocks):
        stroke(0, 0, 0, 50)
        line(0, stride * i, 0, 300, stride * i, 0)
        line(stride * i, 0, 0, stride * i, 300, 0)

    for i in range(int(sqrt(numBlocks)), numBlocks, int(sqrt(numBlocks))):
        stroke(0, 0, 0, 150)
        line(0, stride * i, 0, 300, stride * i, 0)
        line(stride * i, 0, 0, stride * i, 300, 0)

    for row in range(numBlocks):
        for col in range(numBlocks):
            sol = finalBoard[row][col]
            if sol is not None:
                textSize(20)
                textAlign(CENTER, CENTER)
                text(str(sol), fullBlockWidth + col * stride,
                     fullBlockWidth + row * stride,
                     0)

    popMatrix()
    
    # Update solution

def solve(self):
    """
    1. add all the cells with definite values to queue, and for
    each one exclude other cell values in same col/row/block
    2. once there are none of those left, look at
    """
    allCells = {(i,j) for i in range(self.size) for j in range(self.size)}

    # Initialize queue with solved cells
    solved = self.getIdx(map2d(lambda x: sum(map(int,x)) == 1, self.board))
    queue = [x for x in solved]
    unsolved = allCells - set(solved)
    self.printBoard()

    i = 1
    while i > 0:
        print('Queue: {}'.format(queue))
        # Propagate constraints for solved cells
        print('Propating Constraints...')
        while len(queue) > 0:
            idx = queue.pop(0)
            print(idx)
            boardTemp = self.updateVec(idx)
            self.board = boardTemp
            print('Updated')


            for idx in unsolved:
                vec = self.board[idx[0]][idx[1]]
                if sum(map(int,vec)) == 1:
                    print('New solution! -> {}'.format(idx))
                    queue.append(idx)
                    unsolved = unsolved - {idx}
                    solved.append(idx)
        self.printBoard()
        i -= 1
    print('Solved!')

def updateVec(self, idx):
    # TODO: could also OR the solved vectors of column/row/block
    # together and then take the Intersection and Not
    #self.board[x,y] = self.board[x,y] & np.logical_not(vec)
    boardTemp = [[u for u in v] for v in self.board]

    x, y = idx[0], idx[1]
    num = int(self.vec2num(boardTemp[x][y]))

    colsToChange = list(set(range(self.size)) - {y})
    rowsToChange = list(set(range(self.size)) - {x})

    # Fix row, set all other columns to False

    for col in colsToChange:
        boardTemp[x][col][num-1] = False

    for row in rowsToChange:
        boardTemp[row][y][num-1] = False

    # Get id's of block cells
    for blockIdx in self.getBlock(x,y):
        boardTemp[blockIdx[0]][blockIdx[1]][num-1] = False

    assert all(map2d(any, boardTemp)), "contradiction"
    # TODO: change so only change if works
    # Update final board
    self.finalBoard[x][y] = str(num)
    return boardTemp


def getIdx(self, board):
    """Get the indices of True entries of boolean-masked board."""
    return [(i,j) for i, row in enumerate(board)
            for j, entry in enumerate(row) if entry]


def getBlock(self,i,j):
    """Get indices in same block."""
    size = self.blocksize
    i0 = (i // size)*size
    j0 = (j // size)*size

    block = [(u,v) for u in range(i0, i0 + size)
                for v in range(j0, j0 + size)]
    block.remove((i,j))
    return block

def getCol(self,i,j):
    """Get indices in same column."""
    col = [(x,j) for x in range(self.size)]
    col.remove((i,j))
    return col

def getRow(self,i,j):
    """Get indices in same row."""
    row = [(i,x) for x in range(self.size)]
    row.remove((i,j))
    return row

# def num2vec(self,ent):
#     """Turn sudoku board into vectors of True/False."""
#     if ent != ".":
#         vec = [False]*self.size
#         vec[int(ent)-1] = True
#     else:
#         vec = [True]*self.size
#     return vec

def vec2num(self, vec):
    """Turn True/False vector into corresponding number"""
    if sum(map(int,vec)) == 1:
        return str([i for i, x in enumerate(list(vec)) if x][0] + 1)
        #return str(np.where(vec)[0][0]+1)
    else:
        return ' '

    
    
    
    
