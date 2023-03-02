from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '900')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.core.window import Window

class MainWidget(GridLayout):

    tiles = []
    tiles_index = {}

    window = {"cols": 20, "rows": 20}
    window_x = 38.1*window["cols"]
    window_y = 30.1*window["rows"]

    clicked_button = {}

    who_plays = "O"

    menu = []
    score = {"O": 0, "X": 0}
    winning_tiles = []

    game_over = False
    game_over_click = False

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.cols = self.window["cols"]
        self.rows = self.window["rows"]
        self.init_menu()
        self.init_tiles(0)
        if self.is_desktop:
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

    def is_desktop(self):
        if platform in ("linux", "win", "macosx"):
            return True
        else:
            return False

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard.unbind(on_key_up=self.on_keyboard_up)
        self._keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        pass

    def on_keyboard_up(self, keyboard, keycode):
        pass

    def on_touch_down(self, touch):
        if self.game_over == True:
            self.clicked_button = {}
            self.winning_tiles = []

            button_count = self.window["cols"] * (self.window["rows"] - 1)
            for i in range(0, button_count):
                self.tiles[i].text = str(i)
                self.tiles[i].color = (1, 1, 1, .6)
                self.tiles[i].font_size = 0
                self.tiles[i].background_normal = ""
                self.tiles[i].background_color = (1, 1, 1, .4)
            self.game_over = False
        elif self.game_over == False and self.game_over_click == True:
            self.game_over_click = False

        return super(GridLayout, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        pass

    def init_menu(self):
        if len(self.menu) >= 1:
            for i in range(0, self.cols):
                self.remove_widget(self.menu[i])
            self.menu = []

        for i in range(0, self.cols):
            if i == 0:
                self.menu.append(Label(text="X:", font_size=20))
            elif i == 1:
                self.menu.append(Label(text=str(self.score["X"]), font_size=20))
            elif i == self.cols-2:
                self.menu.append(Label(text="O:", font_size=20))
            elif i == self.cols-1:
                self.menu.append(Label(text=str(self.score["O"]), font_size=20))
            elif i == self.cols//2-1:
                self.menu.append(Label(text="Playing: ", font_size=20))
            elif i == self.cols//2:
                self.menu.append(Label(text=self.who_plays, font_size=20))
            else:
                self.menu.append(Label())
            self.add_widget(self.menu[i])

    def init_tiles(self, clicked):
        button_count = self.window["cols"] * (self.window["rows"] - 1)
        x = 0
        y = 0
        for i in range(0, button_count):
            self.tiles.append(Button(text=str(i),color=(1, 1, 1, .6), font_size=0, background_normal="", background_color=(1, 1, 1, .4)))
            self.add_widget(self.tiles[i])
            self.tiles[i].bind(on_press=self.press)

            self.tiles_index[i] = {}
            self.tiles_index[i]["x"] = x
            self.tiles_index[i]["y"] = y

            x += 1
            if x >= self.cols:
                y += 1
                x = 0

    def highlight_win_tiles(self):
        button_count = self.window["cols"] * (self.window["rows"] - 1)
        for i in range(0, button_count):
            if i in self.winning_tiles:
                self.tiles[i].color  = (0, 0, 0, 1)
            elif i not in self.winning_tiles:
                self.tiles[i].background_color = (1, 1, 1, .1)
                self.tiles[i].color = (1, 1, 1, .6)

    def check_win(self, player):
        if len(self.winning_tiles) >= 3:
            self.score[player] += 1
            self.menu[1].text = str(self.score["X"])
            self.menu[self.cols-1].text = str(self.score["O"])
            self.game_over = True
            self.game_over_click = True
            self.highlight_win_tiles()
            return True
        else:
            self.winning_tiles = []


    def check_all_directions(self, tile):
        column = self.tiles_index[tile]["x"]
        row = self.tiles_index[tile]["y"]

        button_count = self.window["cols"] * (self.window["rows"] - 1)
        player = self.clicked_button[tile]

        # check horizontal
        for i in range(0, self.cols):
            if self.game_over == False:
                check_number = row*self.cols + i
                if check_number in self.clicked_button:
                    if self.clicked_button[check_number] == player:
                        self.winning_tiles.append(check_number)
                    else:
                        self.winning_tiles = []
                else:
                    self.check_win(player)

        # vertical
        for i in range(0, self.rows):
            if self.game_over == False:
                check_number = column + i*self.cols
                if check_number in self.clicked_button:
                    if self.clicked_button[check_number] == player:
                        self.winning_tiles.append(check_number)
                    else:
                        self.winning_tiles = []
                else:
                    self.check_win(player)

        # from left down to the top right
        lowest_left = column * (self.cols-1) + tile
        for i in range(0, self.cols):
            if self.game_over == False:
                check_number = lowest_left - i*(self.cols-1)
                if check_number in self.clicked_button and check_number >= 0:
                    if self.clicked_button[check_number] == player:
                        self.winning_tiles.append(check_number)
                    else:
                        self.check_win(player)
                else:
                    self.check_win(player)

        # from top left to the down right
        lowest_right = tile + (self.cols - column - 1) * (self.cols+1)
        for i in range(0, self.cols):
            if self.game_over == False:
                check_number = lowest_right - i*(self.cols+1)
                if check_number in self.clicked_button and check_number >= 0:
                    if self.clicked_button[check_number] == player:
                        self.winning_tiles.append(check_number)
                    else:
                        self.check_win(player)
                else:
                    self.check_win(player)

    def press(self, instance):
        if instance.text == "X" or instance.text == "O":
            return False
        else:
            if self.game_over_click == False :
                clicked = int(instance.text)
                self.clicked_button[clicked] = self.who_plays
                self.tiles[clicked].text = self.who_plays
                self.tiles[clicked].font_size = 20

                self.tiles[clicked].color = (0, 0, 0, 1)
                self.tiles[clicked].background_normal = ""
                if self.who_plays == "X":
                    self.tiles[clicked].background_color = (.7, 0, 0, 1)
                else:
                    self.tiles[clicked].background_color = (0, .7, 0, 1)

                self.check_all_directions(clicked)

                if self.who_plays == "O":
                    self.who_plays = "X"
                else:
                    self.who_plays = "O"
                self.menu[self.cols//2].text = self.who_plays
                self.width = self.window_x
                self.height = self.window_y
                # self.init_menu()
                # self.init_tiles(clicked)

class CrissCross(App):
    pass

CrissCross().run()
