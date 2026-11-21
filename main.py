import tkinter as tk
from environment import GridEnvironment


def main():
    root = tk.Tk()
    root.title("Terminator 2: Judgment Day Simulation")

    environment = GridEnvironment()

    canvas = tk.Canvas(
        root,
        width=environment.columns * environment.cell_size,
        height=environment.rows * environment.cell_size
    )

    canvas.pack(padx=10, pady=10)

    environment.draw(canvas)

    root.mainloop()


if __name__ == "__main__":
    main()