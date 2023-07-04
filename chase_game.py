import sys
import time
import heapq


class BoardObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player = None
        self.enemy = None
        self.prize = False
        self.block = None


class Player:
    def __init__(self, name):
        self.name = name
        self.x = None
        self.y = None


class Enemy:
    def __init__(self, name):
        self.name = name
        self.x = None
        self.y = None


class Block:
    def __init__(self, name):
        self.name = name
        self.x = None
        self.y = None


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[BoardObject(x, y) for y in range(height)] for x in range(width)]
        self.players = []
        self.enemies = []
        self.prize = None
        self.blocks = []

    def add_player(self, player, x, y):
        for p in self.players:
            self.board[p.x][p.y].player = None
        self.players = [player]
        player.x = x
        player.y = y
        self.board[x][y].player = player

    def add_enemy(self, enemy, x, y):
        for e in self.enemies:
            self.board[e.x][e.y].enemy = None
        self.enemies = [enemy]
        enemy.x = x
        enemy.y = y
        self.board[x][y].enemy = enemy

    def add_prize(self, x, y):
        self.board[x][y].prize = True
        self.prize = (x, y)

    def add_block(self, block, x, y):
        self.board[x][y].block = block
        self.blocks.append(block)

    def get_player_location(self, player):
        return player.x, player.y

    def get_enemy_location(self, enemy):
        return enemy.x, enemy.y

    def get_prize_location(self):
        return self.prize

    def print_board(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y].prize:
                    print("$", end=" ")  # $ represents the prize
                elif self.board[x][y].player:
                    print("P", end=" ")  # P represents the player
                elif self.board[x][y].enemy:
                    print("E", end=" ")  # E represents the enemy
                elif self.board[x][y].block:
                    print("X", end=" ")  # X represents the block
                else:
                    print(".", end=" ")  # . represents an empty cell
            print()

#manhattan_distance
def calculate_manhattan_distance(start, goal):
    return abs(goal[0] - start[0]) + abs(goal[1] - start[1])


def a_star_search(board, start, goal):
    queue = [(0, start)]
    visited = set()
    path = {}
    g_score = {start: 0}
    f_score = {start: calculate_manhattan_distance(start, goal)}

    while queue:
        _, current = heapq.heappop(queue)

        if current == goal:
            final_path = []
            while current in path:
                final_path.append(current)
                current = path[current]
            return final_path[::-1]

        visited.add(current)

        neighbors = get_valid_neighbors(board, current)
        for neighbor in neighbors:
            neighbor_g_score = g_score[current] + 1
            if neighbor in g_score and neighbor_g_score >= g_score[neighbor]:
                continue

            path[neighbor] = current
            g_score[neighbor] = neighbor_g_score
            f_score[neighbor] = neighbor_g_score + calculate_manhattan_distance(neighbor, goal)

            if neighbor not in visited:
                heapq.heappush(queue, (f_score[neighbor], neighbor))

    return None


# get_valid_neighbors: This function returns a list of valid neighboring positions for a given position on the board.

# the function checks the boundaries of the board to determine the valid neighboring positions by checking x,y.
def get_valid_neighbors(board, position):
    x, y = position
    neighbors = []

    if x > 0 and not board.board[x - 1][y].block and (x - 1, y) != board.get_prize_location():
        neighbors.append((x - 1, y))
    if x < board.width - 1 and not board.board[x + 1][y].block and (x + 1, y) != board.get_prize_location():
        neighbors.append((x + 1, y))
    if y > 0 and not board.board[x][y - 1].block and (x, y - 1) != board.get_prize_location():
        neighbors.append((x, y - 1))
    if y < board.height - 1 and not board.board[x][y + 1].block and (x, y + 1) != board.get_prize_location():
        neighbors.append((x, y + 1))

    return neighbors


# move_player: This function moves the player in the specified direction on the board. It checks for boundary conditions and updates the player's position accordingly.
def move_player(board, player, direction):
    player_location = board.get_player_location(player)
    if player_location is None:
        return None

    x, y = player_location
    if direction == "up":
        if x > 0 and not board.board[x - 1][y].block:
            x -= 1
        else:
            print("Invalid direction or blocked path. Please try again.")
            return None
    elif direction == "down":
        if x < board.width - 1 and not board.board[x + 1][y].block:
            x += 1
        else:
            print("Invalid direction or blocked path. Please try again.")
            return None
    elif direction == "left":
        if y > 0 and not board.board[x][y - 1].block:
            y -= 1
        else:
            print("Invalid direction or blocked path. Please try again.")
            return None
    elif direction == "right":
        if y < board.height - 1 and not board.board[x][y + 1].block:
            y += 1
        else:
            print("Invalid direction or blocked path. Please try again.")
            return None

    board.add_player(player, x, y)
    return x, y


def move_enemy(board, enemy, player_location):
    enemy_location = board.get_enemy_location(enemy)
    if enemy_location is None:
        return None

    path = a_star_search(board, enemy_location, player_location)
    if not path:
        return None

    for i, step in enumerate(path):
        time.sleep(2)
        x, y = step
        if board.board[x][y].block or (x, y) == board.get_prize_location():
            break
        board.add_enemy(enemy, x, y)
        print("Enemy next movement:", path[:i + 1])

    return x, y

counter_Enemy=0
counter_Player=0
# check_game_status: This function checks the game status based on the current positions of the player, enemy, and prize. It returns "You lose!" if the player and enemy occupy the same position, "You win!" if the player reaches the prize, and None if the game is still in progress.
def check_game_status(board, player_location, enemy_location, counter_Enemy, counter_Player):
    if player_location == enemy_location:
        counter_Enemy += 1
        return "You lose!", counter_Enemy, counter_Player

    prize_location = board.get_prize_location()
    if player_location == prize_location:
        counter_Player += 1
        return "You win!", counter_Enemy, counter_Player

    return None, counter_Enemy, counter_Player

# play_game: This function initializes the game board, player, enemy, and prize. It then starts a game loop where it repeatedly prints the board, takes player input for the direction, moves the player, checks the game status, finds the enemy path, moves the enemy, and checks the game status again until the game is over.

def play_game1():
    global counter_Enemy, counter_Player
    board_width = 7
    board_height = 7
    board = Board(board_width, board_height)
    player = Player("Player")
    enemy = Enemy("Enemy")
    block1 = Block("BLOCK1")
    block2 = Block("BLOCK2")
    block3 = Block("BLOCK3")
    block4 = Block("BLOCK4")
    block5 = Block("BLOCK5")
    block6 = Block("BLOCK6")
    board.add_player(player, 0, 1)
    board.add_enemy(enemy, 6, 4)
    board.add_prize(4, 3)
    board.add_block(block1, 0, 4)
    board.add_block(block2, 6, 6)
    board.add_block(block3, 3, 3)
    board.add_block(block4, 2, 5)
    board.add_block(block5, 1, 2)
    board.add_block(block6, 2, 2)
    counter_Enemy = 0  # Initialize the enemy counter
    counter_Player = 0  # Initialize the player counter

    while True:
        board.print_board()

        # Get player direction from user
        direction = input("Enter player direction (up/down/left/right): ")

        # Move player and check game status
        move_player(board, player, direction)
        player_location = board.get_player_location(player)
        if player_location is None:
            print("Invalid move. Please try again.")
            continue

        game_status, _, _ = check_game_status( board, player_location, board.get_enemy_location(enemy), counter_Enemy, counter_Player )

        if game_status:
            if "win" in game_status.lower():
                counter_Player += 1
            elif "lose" in game_status.lower():
                counter_Enemy += 1
            print("Player:", counter_Player, "Enemy:", counter_Enemy)
            print(game_status)
            break

        # Print entire enemy path
        enemy_path = a_star_search(board, board.get_enemy_location(enemy), player_location)
        print("Enemy Path:", enemy_path)

        # Move enemy one cell
        if enemy_path:
            move_enemy(board, enemy, enemy_path[0])
        else:
            print("Enemy cannot reach the player. You win!")
            break

        enemy_location = board.get_enemy_location(enemy)
        if enemy_location is None:
            print("Enemy cannot reach the player. You win!")
            break

        game_status, _, _ = check_game_status(
            board, player_location, board.get_enemy_location(enemy), counter_Enemy, counter_Player
        )

        if game_status:
            if "lose" in game_status.lower():
                counter_Enemy += 1
            print("Player:", counter_Player, "Enemy:", counter_Enemy)
            print(game_status)
            break
def play_game2():
    global counter_Enemy, counter_Player
    board_width = 7
    board_height = 7
    board = Board(board_width, board_height)
    player = Player("Player")
    enemy = Enemy("Enemy")
    block1=Block("BLOCK1")
    block2= Block("BLOCK2")
    block3 = Block("BLOCK3")
    block4 = Block("BLOCK4")
    block5 = Block("BLOCK5")
    block6 = Block("BLOCK6")
    board.add_player(player, 0, 0)
    board.add_enemy(enemy, 3, 4)
    board.add_prize(3, 3)
    board.add_block(block1, 0, 4)
    board.add_block(block2, 6, 6)
    board.add_block(block3, 5, 3)
    board.add_block(block4, 6, 5)
    board.add_block(block5, 1, 2)
    board.add_block(block6, 4, 2)
    counter_Enemy = counter_Enemy  # Initialize the enemy counter
    counter_Player = counter_Player  # Initialize the player counter

    while True:
        board.print_board()

        # Get player direction from user
        direction = input("Enter player direction (up/down/left/right): ")

        # Move player and check game status
        move_player(board, player, direction)
        player_location = board.get_player_location(player)
        if player_location is None:
            print("Invalid move. Please try again.")
            continue

        game_status, _, _ = check_game_status(
            board, player_location, board.get_enemy_location(enemy), counter_Enemy, counter_Player
        )

        if game_status:
            if "win" in game_status.lower():
                counter_Player += 1
            elif "lose" in game_status.lower():
                counter_Enemy += 1
            print("Player:", counter_Player, "Enemy:", counter_Enemy)
            print(game_status)
            break

        # Print entire enemy path
        enemy_path = a_star_search(board, board.get_enemy_location(enemy), player_location)
        print("Enemy Path:", enemy_path)

        # Move enemy one cell
        if enemy_path:
            move_enemy(board, enemy, enemy_path[0])
        else:
            print("Enemy cannot reach the player. You win!")
            break

        enemy_location = board.get_enemy_location(enemy)
        if enemy_location is None:
            print("Enemy cannot reach the player. You win!")
            break

        game_status, _, _ = check_game_status(
            board, player_location, board.get_enemy_location(enemy), counter_Enemy, counter_Player
        )

        if game_status:
            if "lose" in game_status.lower():
                counter_Enemy += 1
            print("Player:", counter_Player, "Enemy:", counter_Enemy)
            print(game_status)
            break

def play_game3():
    global counter_Enemy, counter_Player
    board_width = 7
    board_height = 7
    board = Board(board_width, board_height)
    player = Player("Player")
    enemy = Enemy("Enemy")
    block1 = Block("BLOCK1")
    block2 = Block("BLOCK2")
    block3 = Block("BLOCK3")
    block4 = Block("BLOCK4")
    block5 = Block("BLOCK5")
    block6 = Block("BLOCK6")
    board.add_player(player, 1, 5)
    board.add_enemy(enemy, 5, 4)
    board.add_prize(6, 3)
    board.add_block(block1, 0, 2)
    board.add_block(block2, 2, 6)
    board.add_block(block3, 5, 3)
    board.add_block(block4, 2, 6)
    board.add_block(block5, 1, 2)
    board.add_block(block6, 4, 4)
    counter_Enemy = counter_Enemy  # Initialize the enemy counter
    counter_Player = counter_Player  # Initialize the player counter

    while True:
        board.print_board()

        # Get player direction from user
        direction = input("Enter player direction (up/down/left/right): ")

        # Move player and check game status
        move_player(board, player, direction)
        player_location = board.get_player_location(player)
        if player_location is None:
            print("Invalid move. Please try again.")
            continue

        game_status, _, _ = check_game_status(
            board, player_location, board.get_enemy_location(enemy), counter_Enemy, counter_Player)

        if game_status:
            if "win" in game_status.lower():
                counter_Player += 1
            elif "lose" in game_status.lower():
                counter_Enemy += 1
            print("Player:", counter_Player, "Enemy:", counter_Enemy)
            print(game_status)
            break

        # Print entire enemy path
        enemy_path = a_star_search(board, board.get_enemy_location(enemy), player_location)
        print("Enemy Path:", enemy_path)

        # Move enemy one cell
        if enemy_path:
            move_enemy(board, enemy, enemy_path[0])
        else:
            print("Enemy cannot reach the player. You win!")
            break

        enemy_location = board.get_enemy_location(enemy)
        if enemy_location is None:
            print("Enemy cannot reach the player. You win!")
            break

        game_status, _, _ = check_game_status(
            board, player_location, board.get_enemy_location(enemy), counter_Enemy, counter_Player)

        if game_status:
            if "lose" in game_status.lower():
                counter_Enemy += 1
            print("Player:", counter_Player, "Enemy:", counter_Enemy)
            print(game_status)
            break



print("lets play !!!")
time.sleep(2)
play_game1()
time.sleep(2)
print("lets do it again")
time.sleep(2)
play_game2()
time.sleep(2)
print("lets do for the last time")
time.sleep(2)
play_game3()









