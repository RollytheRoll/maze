from grafik import Line, Point
import time
import random

class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line, "white")

        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, "white")

        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line,"white")

        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line,"white")

    def draw_move(self, to_cell, undo=False):
        half_length = abs(self._x2 - self._x1) // 2
        x_center = half_length + self._x1
        y_center = half_length + self._y1

        half_length2 = abs(to_cell._x2 - to_cell._x1) // 2
        x_center2 = half_length2 + to_cell._x1
        y_center2 = half_length2 + to_cell._y1

        fill_color = "red"
        if undo:
            fill_color = "gray"

        line = Line(Point(x_center, y_center), Point(x_center2, y_center2))
        self._win.draw_line(line, fill_color)

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed= None,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited(self.num_cols,self.num_rows)

    def _create_cells(self):
        self._cells = []

        for col in range(self.num_cols):
            column = []
            for row in range(self.num_rows):
                cell = Cell(self.win)
                column.append(cell)
            self._cells.append(column)

        for col in range(self.num_cols):
            for row in range(self.num_rows):
                self._draw_cell(col, row)

    def _draw_cell(self, i, j):
        if self.win is None:
            return
        cell = self._cells[i][j]

        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y

        cell.draw(x1, y1, x2, y2)
        self._animate()
    
    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        entrance_cell.has_top_wall = False
        self._draw_cell(0,0)

        exit_cell = self._cells[self.num_cols -1][self.num_rows -1]
        exit_cell.has_bottom_wall = False
        self._draw_cell(self.num_cols -1, self.num_rows -1)

    def _break_walls_r(self,i,j):
        current_cell = self._cells[i][j]
        current_cell.visited = True

        while True:
            directions = []

            if i > 0 and not self._cells[i - 1][j].visited:  # left
                directions.append(("left", i - 1, j))
            if i < self.num_cols - 1 and not self._cells[i + 1][j].visited:  # right
                directions.append(("right", i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:  # up
                directions.append(("up", i, j - 1))
            if j < self.num_rows - 1 and not self._cells[i][j + 1].visited:  # down
                directions.append(("down", i, j + 1))
            
            if len(directions) == 0:
                self._draw_cell(i,j)
                return
            
            direction, next_i, next_j = random.choice(directions)
            next_cell = self._cells[next_i][next_j]

            if direction == "left":
                current_cell.has_left_wall = False
                next_cell.has_right_wall = False
            elif direction == "right":
                current_cell.has_right_wall = False
                next_cell.has_left_wall = False
            elif direction == "up":
                current_cell.has_top_wall = False
                next_cell.has_bottom_wall = False
            elif direction == "down":
                current_cell.has_bottom_wall = False
                next_cell.has_top_wall = False

            self._break_walls_r(next_i,next_j)

    def _reset_cells_visited(self, i, j):
        for col in range(i):
            for row in range(j):
                self._cells[col][row].visited = False

    def solve(self):
        if self._solve_r(0,0) is True:
            return True
        else:
            return False
        
    def _solve_r(self, i, j):
        self._animate()

        current = self._cells[i][j]
        current.visited = True

        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True
        

        if i > 0 and not self._cells[i - 1][j].visited and not self._cells[i - 1][j].has_right_wall:  # left
            current.draw_move(self._cells[i - 1][j])
            if self._solve_r(i-1,j) is True:
                return True
            else:
                current.draw_move(self._cells[i - 1][j],True)
        
        if i < self.num_cols - 1 and not self._cells[i + 1][j].visited and not self._cells[i + 1][j].has_left_wall:  # right
            current.draw_move(self._cells[i + 1][j])
            if self._solve_r(i+1,j) is True:
                return True
            else:
                current.draw_move(self._cells[i + 1][j],True)

        if j > 0 and not self._cells[i][j - 1].visited and not self._cells[i][j - 1].has_bottom_wall:  # up
            current.draw_move(self._cells[i][j - 1])
            if self._solve_r(i,j-1) is True:
                return True
            else:
                current.draw_move(self._cells[i][j - 1],True)

        if j < self.num_rows - 1 and not self._cells[i][j + 1].visited and not self._cells[i][j + 1].has_top_wall:  # down
            current.draw_move(self._cells[i][j + 1])
            if self._solve_r(i,j+1):
                return True
            else:
                current.draw_move(self._cells[i][j + 1],True)
        
        return False
    