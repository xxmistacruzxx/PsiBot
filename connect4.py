from asyncio.windows_events import NULL


class connect4:
    def __init__(self, width, height):
        #initialize width
        if width >= 4 & width < 10:
            self.width = width
        else:
            self.width = 7
        #initialize height
        if height >= 4:
            self.height = height
        else:
            self.height = 6
        
        #temp height and width lock
        self.height = 6
        self.width= 7

        self.turn = 1
        self.board = [[0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0]]
        self.moves = 0
        self.maxMoves = self.width * self.height

    def clear(self):
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j] = 0 
    
    def printboard(self):
        for i in range(self.height-1, -1, -1):
            for j in range(self.width):
                print(self.board[i][j], end=" ")
            print()
    
    # PARAMETERS:
    #   player: either 1 or 2, representing which player is trying to place a piece
    # RETURNS:
    #   -1 if the piece was unable to be played
    #   (hiterator, 0) if a piece was played, but nobody won
    #   (hiterator, 1) if a piece was played, and player 1 won
    #   (hiterator, 2) if a piece was played, and player 2 won
    #   (hiterator, -1) if a piece was played, and there are no more turns left (tie)
    def placepiece(self, player, col):
        hiterator = self.height
        while(hiterator != 0):
            if self.board[hiterator-1][col] == 0:
                hiterator -= 1
            else:
                break
        if hiterator == self.height:
            print("col is full")
            return -1
        else:
            self.board[hiterator][col] = player
            return (hiterator, self.checkwin(hiterator, col, player))

    def checkdir(self, row, col, player, horz, vert):
        try:
            count = 0
            for i in range(4):
                if self.board[row+(i*vert)][col+(i*horz)] != player:
                    break
                count += 1
            if count == 4:
                print("player " + str(player) + " wins!")
                return player
            else:
                return 0
        except:
            return 0

    # RETURNS:
    #   player if a win was found
    #   0 if no win was found
    def checkwin(self, row, col, player):
        arr = [0]*8
        dirs = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        for i in range(len(dirs)):
            arr[i] = self.checkdir(row, col, player, dirs[i][0], dirs[i][1])
        return max(arr)

# connect4game object for easier use in discord implementation
class connect4game:
    def __init__(self, player1id, player1name, player1user, messageid):
        self.game = connect4(7,6)
        self.player1id = player1id
        self.player1name = player1name
        self.player1user = NULL
        self.player2id = "null"
        self.player2name = "null"
        self.player2user = NULL
        self.curplayer = 1
        self.messageid = messageid
        self.started = False
    
    def placepiece(self, col):
        if col > self.game.width or col < 0:
            return
        lol = self.game.placepiece(self.curplayer, col)
        if self.curplayer == 1:
            self.curplayer = 2
        else:
            self.curplayer = 1
        return lol[1]

    def gametostring(self):
        temp = ""
        for i in range(self.game.height-1, -1, -1):
            for j in range(self.game.width):
                if self.game.board[i][j] == 0:
                    temp = temp + ":white_circle:"
                elif self.game.board[i][j] == 1:
                    temp = temp + ":blue_circle:"
                else:
                    temp = temp + ":red_circle:"
            temp = temp + "\n"
        temp = temp + ":one::two::three::four::five::six::seven:"
        return temp

    def printvars(self):
        print(self.game)
        print(self.player1id)
        print(self.player2id)
        print(self.curplayer)
        print(self.messageid)
        print(self.started)

        