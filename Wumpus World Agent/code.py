import random


class WumpusWorldAgent:
    def __init__(self, n, arrows, env_file):
        self.n = n
        self.grid = [[' ' for _ in range(n)] for _ in range(n)]
        self.visited = [[False for _ in range(n)] for _ in range(n)]
        self.direction = 'right'
        self.current_pos = (0, 0)
        self.arrows = arrows
        self.has_gold = False
        self.is_alive = True
        self.score = 0
        self.env_file = env_file

    def initialize_grid(self):
        with open(self.env_file, 'r') as file:
            lines = file.readlines()

        # Process pit, gold, and wumpus locations
        for line in lines[2:]:
            parts = line.strip().split()
            location_type = parts[0]
            row = int(parts[1]) - 1
            col = int(parts[2]) - 1

            if location_type == 'p':
                self.grid[row][col] = 'P'  # Mark pit location
            elif location_type == 'g':
                self.grid[row][col] = 'G'  # Mark gold location
            elif location_type == 'w':
                self.grid[row][col] = 'W'  # Mark wumpus location

    def move_up(self):
        if not self.is_alive or self.has_gold:
            return

        x, y = self.current_pos
        if x - 1 >= 0:
            self.current_pos = (x - 1, y)
            self.score -= 1
            print(f'Moved up to position: {self.current_pos}')
        else:
            print('Cannot move up in that direction!')

        self.check_events()

    def move_down(self):
        if not self.is_alive or self.has_gold:
            return

        x, y = self.current_pos
        if x + 1 < self.n:
            self.current_pos = (x + 1, y)
            self.score -= 1
            print(f'Moved down to position: {self.current_pos}')
        else:
            print('Cannot move down in that direction!')

        self.check_events()

    def move_left(self):
        if not self.is_alive or self.has_gold:
            return

        x, y = self.current_pos
        if y - 1 >= 0:
            self.current_pos = (x, y - 1)
            self.score -= 1
            print(f'Moved left to position: {self.current_pos}')
        else:
            print('Cannot move left in that direction!')

        self.check_events()

    def move_right(self):
        if not self.is_alive or self.has_gold:
            return

        x, y = self.current_pos
        if y + 1 < self.n:
            self.current_pos = (x, y + 1)
            self.score -= 1
            print(f'Moved right to position: {self.current_pos}')
        else:
            print('Cannot move right in that direction!')

        self.check_events()

    def shoot_arrow(self):
        if not self.is_alive or self.arrows == 0:
            return

        x, y = self.current_pos
        if self.direction == 'right':
            for j in range(y + 1, self.n):
                if self.grid[x][j] == 'W':
                    self.grid[x][j] = ' '
                    self.score -= 10
                    print('You killed the Wumpus!')
                    return
                elif self.grid[x][j] == 'P':
                    break
        elif self.direction == 'down':
            for i in range(x + 1, self.n):
                if self.grid[i][y] == 'W':
                    self.grid[i][y] = ' '
                    self.score -= 10
                    print('You killed the Wumpus!')
                    return
                elif self.grid[i][y] == 'P':
                    break
        elif self.direction == 'left':
            for j in range(y - 1, -1, -1):
                if self.grid[x][j] == 'W':
                    self.grid[x][j] = ' '
                    self.score -= 10
                    print('You killed the Wumpus!')
                    return
                elif self.grid[x][j] == 'P':
                    break
        elif self.direction == 'up':
            for i in range(x - 1, -1, -1):
                if self.grid[i][y] == 'W':
                    self.grid[i][y] = ' '
                    self.score -= 10
                    print('You killed the Wumpus!')
                    return
                elif self.grid[i][y] == 'P':
                    break

        self.arrows -= 1
        self.score -= 1
        print('No wumpus in sight!')

    def check_breeze(self):
        x, y = self.current_pos
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return any(self.grid[i][j] == 'P' for i, j in neighbors if 0 <= i < self.n and 0 <= j < self.n)

    def check_stench(self):
        x, y = self.current_pos
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return any(self.grid[i][j] == 'W' for i, j in neighbors if 0 <= i < self.n and 0 <= j < self.n)

    def check_events(self):
        x, y = self.current_pos
        if self.grid[x][y] == 'W':
            self.is_alive = False
            self.score -= 100
            print('You were killed by the Wumpus!')
        elif self.grid[x][y] == 'G':
            self.grid[x][y] = ' '  # Remove the gold from the grid
            self.has_gold = True
            self.score += 150
            print('You found the gold!')
            print('Congratulations! You won the game!')
            print(f'Final Score: {self.score}')
            return
        else:
            breeze = self.check_breeze()
            stench = self.check_stench()
            if breeze:
                print('There is a breeze nearby.')
            if stench:
                print('There is a stench nearby.')

        if self.has_gold:
            print('You already have the gold!')
            print(f'Final Score: {self.score}')
            return

    def play(self):
        self.initialize_grid()

        while not self.has_gold and self.is_alive:
            command = input("Enter your command (u: move up, d: move down, l: move left, r: move right, s: shoot arrow): ").lower()

            if command == 'u':
                self.move_up()
            elif command == 'd':
                self.move_down()
            elif command == 'l':
                self.move_left()
            elif command == 'r':
                self.move_right()
            elif command == 's':
                self.shoot_arrow()
            else:
                print('Invalid command!')

        if not self.has_gold and not self.is_alive:
            print('Game over! You lost.')
            print(f'Final Score: {self.score}')
        else:
            print(f'Final Score: {self.score}')
# Example usage
env_file = 'env1.txt'
agent = WumpusWorldAgent(20, 5, env_file)
agent.play()