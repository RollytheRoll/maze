import unittest
from cell import Cell,Maze
from grafik import *

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_create_cells_large(self):
        num_cols = 16
        num_rows = 12
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_entrance_and_exit_break(self):
        num_cols = 16
        num_rows = 12
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(False,m1._cells[0][0].has_top_wall)
        self.assertEqual(False, m1._cells[m1.num_cols -1][m1.num_rows -1].has_bottom_wall)
    
    def test_visited(self):
        num_cols = 16
        num_rows = 12
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)

        for col in range(num_cols):
            for row in range(num_rows):
                self.assertEqual(m1._cells[col][row].visited, False)

    
if __name__ == "__main__":
    unittest.main()