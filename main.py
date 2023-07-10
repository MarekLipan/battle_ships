import tkinter as tk
import json

# Constants
PLAYER_COLORS = ["green", "yellow", "purple", "red", "royalblue1"]
SHIP_POSITIONS_FILE = "ship_positions_1.json"


class BattleshipGame:
    def __init__(self, player):
        self.player = player
        self.grid_size = 10

        self.root = tk.Toplevel()
        self.root.title(f"Player {player + 1} - {PLAYER_COLORS[player]}")

        self.canvas_width = self.grid_size * 40 + 70
        self.canvas_height = self.grid_size * 40 + 70

        self.canvas = tk.Canvas(
            self.root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg=PLAYER_COLORS[player],
        )
        self.canvas.pack()

        self.grid = [
            [None for _ in range(self.grid_size)] for _ in range(self.grid_size)
        ]
        self.ships = []

        self.load_ship_positions()
        self.create_grid()

        self.canvas.bind("<Button-1>", self.handle_click)

    def load_ship_positions(self):
        try:
            with open(SHIP_POSITIONS_FILE, "r") as file:
                ship_positions = json.load(file)
                self.ships = ship_positions.get("ships", [])
        except FileNotFoundError:
            self.ships = []

        for ship in self.ships:
            ship["alive"] = len(ship["positions"])

    def create_grid(self):
        # Create column names
        for col in range(self.grid_size):
            x = 70 + col * 40
            y = 30
            self.canvas.create_text(x, y, text=chr(65 + col), font="Helvetica 18 bold")

        # Create row names and grid cells
        for row in range(self.grid_size):
            # Create row names
            x = 30
            y = 70 + row * 40
            self.canvas.create_text(x, y, text=str(row + 1), font="Helvetica 18 bold")

            for col in range(self.grid_size):
                x1 = 50 + col * 40
                y1 = 50 + row * 40
                x2 = x1 + 40
                y2 = y1 + 40
                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="gray", outline="black"
                )
                self.grid[row][col] = rect

    def handle_click(self, event):
        col = (event.x - 50) // 40
        row = (event.y - 50) // 40

        for ship in self.ships:
            if [row, col] in ship["positions"] and ship["player"] == self.player:
                self.canvas.itemconfig(
                    self.grid[row][col], fill=PLAYER_COLORS[self.player]
                )
                self.canvas.create_line(
                    col * 40 + 50,
                    row * 40 + 50,
                    (col + 1) * 40 + 50,
                    (row + 1) * 40 + 50,
                    fill="black",
                )
                self.canvas.create_line(
                    col * 40 + 50,
                    (row + 1) * 40 + 50,
                    (col + 1) * 40 + 50,
                    row * 40 + 50,
                    fill="black",
                )
                # update status
                ship["alive"] -= 1
                self.blacken_sunk_ships()
                self.blacken_defeated_player()

                return

        self.canvas.itemconfig(self.grid[row][col], fill="light blue")

    def blacken_sunk_ships(self):
        for ship in self.ships:
            if ship["alive"] == 0:
                for r, c in ship["positions"]:
                    self.canvas.itemconfig(self.grid[r][c], fill="black")
                self.ships.remove(ship)
        return

    def blacken_defeated_player(self):
        ships_alive = 0
        for ship in self.ships:
            if ship["player"] == self.player:
                ships_alive += 1

        if ships_alive == 0:
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    self.canvas.itemconfig(self.grid[row][col], fill="black")
        return


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Battleship Game")

    for player in range(5):
        game = BattleshipGame(player)

    root.mainloop()
