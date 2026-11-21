
import tkinter as tk


class GridEnvironment:
    def __init__(self, rows=20, columns=20, cell_size=30):
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size

        self.terrain = [
            ["ground" for _ in range(columns)]
            for _ in range(rows)
        ]

        self.create_environment()

    def create_environment(self):
        for row in range(2, 7):
            for col in range(3, 7):
                self.terrain[row][col] = "building"

        for row in range(3, 8):
            for col in range(12, 16):
                self.terrain[row][col] = "building"

        for row in range(12, 16):
            for col in range(2, 6):
                self.terrain[row][col] = "building"

        for row in range(13, 18):
            for col in range(13, 17):
                self.terrain[row][col] = "building"

        for col in range(self.columns):
            self.terrain[9][col] = "road"

        for row in range(self.rows):
            self.terrain[row][9] = "road"

        for row in range(7, 10):
            for col in range(16, 19):
                self.terrain[row][col] = "restricted"

        for row in range(15, 18):
            for col in range(7, 10):
                self.terrain[row][col] = "hazard"

        for row in range(1, 4):
            for col in range(17, 19):
                self.terrain[row][col] = "safe"

    def in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.columns

    def is_walkable(self, row, col):
        if not self.in_bounds(row, col):
            return False

        return self.terrain[row][col] not in ("building", "restricted")

    def can_move(self, current_position, target_position):
        current_row, current_col = current_position
        target_row, target_col = target_position

        if not self.is_walkable(current_row, current_col):
            return False

        if not self.is_walkable(target_row, target_col):
            return False

        distance = (
            abs(target_row - current_row)
            + abs(target_col - current_col)
        )

        return distance == 1

    def get_neighbours(self, row, col):
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        neighbours = []

        for row_change, col_change in directions:
            new_row = row + row_change
            new_col = col + col_change

            if self.is_walkable(new_row, new_col):
                neighbours.append((new_row, new_col))

        return neighbours

    def get_terrain(self, row, col):
        if not self.in_bounds(row, col):
            return None

        return self.terrain[row][col]

    def draw(self, canvas):
        colors = {
            "ground": "#D9E2D0",
            "road": "#777777",
            "building": "#455A64",
            "restricted": "#C65D5D",
            "hazard": "#E5A83B",
            "safe": "#77BFA3"
        }

        for row in range(self.rows):
            for col in range(self.columns):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                terrain_type = self.terrain[row][col]

                canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=colors[terrain_type],
                    outline="#B0B0B0"
                )


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Terminator 2 Simulation Environment")

    environment = GridEnvironment()

    canvas = tk.Canvas(
        root,
        width=environment.columns * environment.cell_size,
        height=environment.rows * environment.cell_size
    )

    canvas.pack(padx=10, pady=10)
    environment.draw(canvas)

    root.mainloop()