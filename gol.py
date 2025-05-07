#!/usr/bin/env python3
"""
Conway's Game of Life

Runs a simulation of Conway's Game of Life using a Tkinter GUI.
Utilizes NumPy for efficient computation.
"""

import argparse
import tkinter as tk
import numpy as np
import random


class GameOfLifeBoard:
    """Handles the state and evolution of the Game of Life grid."""

    def __init__(self, width: int, height: int):
        """
        Initializes the Game of Life board.

        Args:
            width: Number of columns.
            height: Number of rows.
        """
        self.width = width
        self.height = height

        self.board = np.zeros((self.height, self.width), dtype=np.uint8)
        self.cache_board = np.zeros_like(self.board)
        self.next_board = np.zeros_like(self.board)

    def toggle_cell(self, x: int, y: int):
        """
        Toggles the state of a cell (alive ↔ dead).

        Args:
            x: Column index.
            y: Row index.
        """
        self.board[y, x] = 1 - self.board[y, x]

    def step(self):
        """
        Computes the next generation based on Conway's rules.
        """
        neighbors = (
            np.roll(self.board, 1, axis=0) +
            np.roll(self.board, -1, axis=0) +
            np.roll(self.board, 1, axis=1) +
            np.roll(self.board, -1, axis=1) +
            np.roll(np.roll(self.board, 1, axis=0), 1, axis=1) +
            np.roll(np.roll(self.board, 1, axis=0), -1, axis=1) +
            np.roll(np.roll(self.board, -1, axis=0), 1, axis=1) +
            np.roll(np.roll(self.board, -1, axis=0), -1, axis=1)
        )

        survive = (self.board == 1) & ((neighbors == 2) | (neighbors == 3))
        birth = (self.board == 0) & (neighbors == 3)

        self.next_board[:] = 0
        self.next_board[survive | birth] = 1
        self.board, self.next_board = self.next_board, self.board


class GameOfLifeRenderer:
    """Manages the Tkinter GUI for displaying and interacting with the game."""

    def __init__(self, board: GameOfLifeBoard, cell_size: int, update_delay: int):
        """
        Initializes the GUI renderer.

        Args:
            board: Instance of GameOfLifeBoard.
            cell_size: Size of each cell in pixels.
            update_delay: Delay between frames in milliseconds.
        """
        self.board = board
        self.cell_size = cell_size
        self.update_delay = update_delay
        self.is_running = False

        self.root = tk.Tk()
        self.root.title("Conway's Game of Life")

        canvas_width = board.width * cell_size
        canvas_height = board.height * cell_size
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height)
        self.canvas.pack()

        self.colors = [
            "#213b4a", "#2c4655", "#2c7b55", "#53b357",
            "#7ada5a", "#2d5e56", "#8beb67"
        ]

        self.rectangles = [
            [self.canvas.create_rectangle(
                col * cell_size,
                row * cell_size,
                (col + 1) * cell_size,
                (row + 1) * cell_size,
                fill=self.colors[0],
                outline=self.colors[1]
            ) for col in range(board.width)]
            for row in range(board.height)
        ]

        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)

        self.schedule_next_frame()

    def on_left_click(self, event):
        """Toggles the clicked cell."""
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        self.board.toggle_cell(col, row)
        self.draw_board()

    def on_right_click(self, event):
        """Toggles simulation run/pause."""
        self.is_running = not self.is_running

    def schedule_next_frame(self):
        """Schedules the next animation frame."""
        self.root.after(self.update_delay, self.update_frame)

    def update_frame(self):
        """Advances the simulation and redraws the board."""
        if self.is_running:
            self.board.step()
        self.draw_board()
        self.schedule_next_frame()

    def draw_board(self):
        """Draws the current board state."""
        changes = np.argwhere(self.board.board != self.board.cache_board)
        for row, col in changes:
            color = self.colors[random.randint(2, len(self.colors) - 1)] if self.board.board[row, col] else self.colors[0]
            self.canvas.itemconfig(self.rectangles[row][col], fill=color)
        self.board.cache_board = self.board.board.copy()

    def run(self):
        """Starts the Tkinter event loop."""
        self.root.mainloop()


def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Conway's Game of Life in Python with Tkinter and NumPy.",
        epilog="Example: python gol.py --width 256 --height 64 --cell-size 8 --delay 16 --random-cell 64 --h-line 2 --v-line 1"
    )

    parser.add_argument("--width", type=int, default=16, help="Grid width in cells.")
    parser.add_argument("--height", type=int, default=16, help="Grid height in cells.")
    parser.add_argument("--cell-size", type=int, default=32, help="Cell size in pixels.")
    parser.add_argument("--delay", type=int, default=32, help="Frame delay in ms.")
    parser.add_argument("--random-cell", type=int, default=4, help="Number of random live cells.")
    parser.add_argument("--h-line", type=int, default=0, help="Number of random horizontal lines.")
    parser.add_argument("--v-line", type=int, default=1, help="Number of random vertical lines.")

    return parser.parse_args()


def populate_board(board: GameOfLifeBoard, args):
    """Populates the board based on command-line arguments."""
    max_cells = board.width * board.height
    args.random_cell = min(args.random_cell, max_cells - 1)
    args.h_line = min(args.h_line, board.height - 1)
    args.v_line = min(args.v_line, board.width - 1)

    if args.random_cell > 0:
        cells = set()
        while len(cells) < args.random_cell:
            cells.add((random.randint(0, board.width - 1), random.randint(0, board.height - 1)))
        for x, y in cells:
            board.board[y, x] = 1

    if args.h_line > 0:
        lines = random.sample(range(board.height), k=args.h_line)
        for y in lines:
            board.board[y, 1:-1] = 1

    if args.v_line > 0:
        lines = random.sample(range(board.width), k=args.v_line)
        for x in lines:
            board.board[1:-1, x] = 1


def main():
    """Main entry point."""
    input("\n\nConway's\n   ______                        ____  ____   __    _ ____\n  / ____/___ _____ ___  ___     / __ \\/ __/  / /   (_) __/__\n / / __/ __ `/ __ `__ \\/ _ \\   / / / / /_   / /   / / /_/ _ \\\n/ /_/ / /_/ / / / / / /  __/  / /_/ / __/  / /___/ / __/  __/\n\\____/\\__,_/_/ /_/ /_/\\___/   \\____/_/    /_____/_/_/  \\___/\n\nExample usage:\npython gol.py --width 256 --height 64 --cell-size 8 --delay 16 --random-cell 64 --h-line 2 --v-line 1\n\n- Left-click on a cell toggle its state.\n- Right-click on the view to toggle play/pause.\n- Press [Enter] when you are ready.")

    args = parse_args()

    args.width = max(args.width, 1)
    args.height = max(args.height, 1)
    args.cell_size = max(args.cell_size, 1)
    args.delay = max(args.delay, 1)

    board = GameOfLifeBoard(args.width, args.height)
    renderer = GameOfLifeRenderer(board, args.cell_size, args.delay)

    populate_board(board, args)
    renderer.draw_board()
    renderer.run()


if __name__ == "__main__":
    main()