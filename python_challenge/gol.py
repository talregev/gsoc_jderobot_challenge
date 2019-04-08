import numpy as np
import json
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib


class Board:
    def __init__(self):
        self.board = np.array([[]])
        self.is_print = False
        self.LIVE_CELL_COLOR = "green"
        self.DEAD_CELL_COLOR = "white"

    def __str__(self):
        return self.board.__str__()

    def create(self, N, M):
        self.board = np.zeros((N, M), dtype=int)
        win = GridWindow(N, M)
        win.LIVE_CELL_COLOR = self.LIVE_CELL_COLOR
        win.DEAD_CELL_COLOR = self.DEAD_CELL_COLOR
        win.set_position(Gtk.WindowPosition.CENTER)
        win.set_type_hint(Gdk.WindowTypeHint.MENU)
        win.connect("delete-event", Gtk.main_quit)
        win.show_all()
        Gtk.main()

    def load(self, json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
        ui = data["ui"]
        if(ui == "console"):
            console = data["console"]
            self.is_print = console["isPrint"]
            input_file = console["inputFile"]
            self.read(input_file)
        if(ui == "gui"):
            gui = data["gui"]
            self.LIVE_CELL_COLOR = gui["cellLiveColor"]
            self.DEAD_CELL_COLOR = gui["cellDeadColor"]
            N, M = gui["gridSize"]
            self.create(N, M)


    def read(self, path):
        self.board = np.array([[]], dtype=int)
        is_first = True
        file = open(path, "r")
        for line in file:
            line_array = list(line.rstrip())
            row = np.array([line_array], dtype=int)
            if(is_first):
                self.board = np.append(self.board, row, axis=1)
                is_first = False
                continue
            self.board = np.append(self.board, row, axis=0)
        if(self.is_print):
            print(self.board)
            print('')

    def step(self):
        self.board = step(self.board)
        if(self.is_print):
            print(self.board)
            print('')

    def steps(self, num_steps):
        for i in range(num_steps):
            self.step()


class GridWindow(Gtk.Window):
    def __init__(self, N, M):

        self.LIVE_CELL_COLOR = "green"
        self.DEAD_CELL_COLOR = "white"
        self.N = N
        self.M = M

        Gtk.Window.__init__(self, title="Conway's Game of Life")
        grid = Gtk.Grid()
        self.add(grid)
        self.labels = np.empty((N, M), dtype=object)
        self.board  = np.zeros((N, M), dtype=int)

        for i in range(N):
            for j in range(M):
                label = Gtk.Label("        ")
                color = Gdk.color_parse(self.DEAD_CELL_COLOR)
                rgba = Gdk.RGBA.from_color(color)
                label.override_background_color(0, rgba)
                event_box = Gtk.EventBox()
                event_box.add(label)
                event_box.connect("button-press-event", self._on_click, i, j)
                self.labels[i][j] = label
                grid.attach(event_box, j, i, 1, 1)

        self.button = Gtk.Button(label="Start")
        self.button.connect("clicked", self.start)
        grid.attach(self.button, 0, N, 3, 1)
        self.is_start = False
        self.num_iter = 0

        button = Gtk.Button(label="Clear")
        button.connect("clicked", self.clear)
        grid.attach(button, 4, N, 3, 1)

        self.iter_label = Gtk.Label("Iteration 0")
        grid.attach(self.iter_label, int(M/2), N, 3, 1)

    def start(self, widget):
        self.is_start = not self.is_start
        if(self.is_start):
            self.button.set_label("Stop")
            self.step()
        else:
            self.button.set_label("Start")

    def clear(self, widget):
        if (not self.is_start):
            self.board = np.zeros((self.N, self.M), dtype=int)
            self.num_iter = 0
            self.update()

    def update(self):
        for i in range(self.N):
            for j in range(self.M):
                is_alive = self.board[i][j]
                cell_label = self.labels[i][j]
                self.set_color(cell_label, is_alive)
        self.iter_label.set_text("Iteration " + str(self.num_iter))

    def step(self):
        if(self.is_start):
            self.board = step(self.board)
            self.num_iter = self.num_iter + 1
            self.update()
            GLib.timeout_add_seconds(1, self.step)

        return False

    def set_color(self, cell_label ,is_alive):
        if (is_alive):
            color = Gdk.color_parse(self.LIVE_CELL_COLOR)
            rgba = Gdk.RGBA.from_color(color)
            cell_label.override_background_color(0, rgba)
        else:
            color = Gdk.color_parse(self.DEAD_CELL_COLOR)
            rgba = Gdk.RGBA.from_color(color)
            cell_label.override_background_color(0, rgba)

    def _on_click(self, widget, event, i, j):
        if(not self.is_start):
            is_alive   = self.board [i][j]
            cell_label = self.labels[i][j]
            is_alive = not is_alive
            self.board[i][j] = is_alive
            self.set_color(cell_label, is_alive)


def calc_live(board, i, j):
    N, M = board.shape
    if (i < 0 or i == N or j < 0 or j == M):
        return 0
    return board[i][j]


def sum_live_cell(board, i, j):
    sum_live = \
        calc_live(board, i-1, j-1) + \
        calc_live(board, i-1, j  ) + \
        calc_live(board, i-1, j+1) + \
        calc_live(board, i  , j-1) + \
        calc_live(board, i  , j+1) + \
        calc_live(board, i+1, j-1) + \
        calc_live(board, i+1, j  ) + \
        calc_live(board, i+1, j+1)
    return sum_live


def step(board):
    N, M = board.shape
    next_board = np.zeros((N, M), dtype=int)
    for i in range(N):
        for j in range(M):
            live = sum_live_cell(board, i, j)
            # Cell is a live! (It alive!)
            if(board[i][j] == 1):
                # Any live cell with fewer than two live neighbours dies, as if by underpopulation
                # Any live cell with more than three live neighbours dies, as if by overpopulation
                if(live < 2 or live > 3):
                    next_board[i][j] = 0

                # Any live cell with two or three live neighbours lives on to the next generation
                else:
                    next_board[i][j] = 1
            # Cell is dead
            else:
                # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction
                if(live == 3):
                    next_board[i][j] = 1
    return next_board
