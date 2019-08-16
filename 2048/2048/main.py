__version__ = '1.3.2'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, OptionProperty, ObjectProperty
from kivy.graphics import Color, BorderImage
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.utils import platform
from kivy.factory import Factory
from random import choice, random

from proj2 import *

platform = platform()
app = None

if platform == 'android':
    # Support for Google Play
    import gs_android
    leaderboard_highscore = 'CgkI0InGg4IYEAIQBg'
    achievement_block_32 = 'CgkI0InGg4IYEAIQCg'
    achievement_block_64 = 'CgkI0InGg4IYEAIQCQ'
    achievement_block_128 = 'CgkI0InGg4IYEAIQAQ'
    achievement_block_256 = 'CgkI0InGg4IYEAIQAg'
    achievement_block_512 = 'CgkI0InGg4IYEAIQAw'
    achievement_block_1024 = 'CgkI0InGg4IYEAIQBA'
    achievement_block_2048 = 'CgkI0InGg4IYEAIQBQ'
    achievement_block_4096 = 'CgkI0InGg4IYEAIQEg'
    achievement_100x_block_512 = 'CgkI0InGg4IYEAIQDA'
    achievement_1000x_block_512 = 'CgkI0InGg4IYEAIQDQ'
    achievement_100x_block_1024 = 'CgkI0InGg4IYEAIQDg'
    achievement_1000x_block_1024 = 'CgkI0InGg4IYEAIQDw'
    achievement_10x_block_2048 = 'CgkI0InGg4IYEAIQEA'
    achievements = {
        32: achievement_block_32,
        64: achievement_block_64,
        128: achievement_block_128,
        256: achievement_block_256,
        512: achievement_block_512,
        1024: achievement_block_1024, 
        2048: achievement_block_2048,
        4096: achievement_block_4096}

    from kivy.uix.popup import Popup
    class GooglePlayPopup(Popup):
        pass

else:
    achievements = {}

## BEGIN FP GLUE -- ############################################################

def get_tabuleiro(game):
  t = cria_tabuleiro()
  tabuleiro_actualiza_pontuacao(t, game.score)

  for i in range(4):
    for j in range(4):
        coord = cria_coordenada(i + 1, j + 1)
        if isinstance(game.grid[j][i], Number):
          tabuleiro_preenche_posicao(t, coord, game.grid[j][i].number)
        else:
          tabuleiro_preenche_posicao(t, coord, 0)
  return t

def set_tabuleiro(game, t):
  for i in range(4):
    for j in range(4):
      coord = cria_coordenada(i + 1, j + 1)
      value = tabuleiro_posicao(t, coord)

      if game.grid[j][i] != None:
        game.grid[j][i].destroy()

      if value == 0:
        game.grid[j][i] = None
      else:
        game.spawn_number_at(j, i, value) 
  game.score = tabuleiro_pontuacao(t)
  game.reposition()

## END FP STUFF ################################################################

class ButtonBehavior(object):
    # XXX this is a port of the Kivy 1.8.0 version, the current android versino
    # still use 1.7.2. This is going to be removed soon.
    state = OptionProperty('normal', options=('normal', 'down'))
    last_touch = ObjectProperty(None)
    def __init__(self, **kwargs):
        self.register_event_type('on_press')
        self.register_event_type('on_release')
        super(ButtonBehavior, self).__init__(**kwargs)

    def _do_press(self):
        self.state = 'down'

    def _do_release(self):
        self.state = 'normal'

    def on_touch_down(self, touch):
        if super(ButtonBehavior, self).on_touch_down(touch):
            return True
        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y):
            return False
        if self in touch.ud:
            return False
        touch.grab(self)
        touch.ud[self] = True
        self.last_touch = touch
        self._do_press()
        self.dispatch('on_press')
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            return True
        if super(ButtonBehavior, self).on_touch_move(touch):
            return True
        return self in touch.ud

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return super(ButtonBehavior, self).on_touch_up(touch)
        assert(self in touch.ud)
        touch.ungrab(self)
        self.last_touch = touch
        self._do_release()
        self.dispatch('on_release')
        return True

    def on_press(self):
        pass

    def on_release(self):
        pass


class Number(Widget):
    number = NumericProperty(2)
    scale = NumericProperty(.1)
    colors = {
        2: get_color_from_hex('#eee4da'),
        4: get_color_from_hex('#ede0c8'),
        8: get_color_from_hex('#f2b179'),
        16: get_color_from_hex('#f59563'),
        32: get_color_from_hex('#f67c5f'),
        64: get_color_from_hex('#f65e3b'),
        128: get_color_from_hex('#edcf72'),
        256: get_color_from_hex('#edcc61'),
        512: get_color_from_hex('#edc850'),
        1024: get_color_from_hex('#edc53f'),
        2048: get_color_from_hex('#edc22e'),
        4096: get_color_from_hex('#ed702e'),
        8192: get_color_from_hex('#ed4c2e')}

    def __init__(self, **kwargs):
        super(Number, self).__init__(**kwargs)
        anim = Animation(scale=1., d=0, t='out_quad')
        anim.bind(on_complete=self.clean_canvas)
        anim.start(self)

    def clean_canvas(self, *args):
        self.canvas.before.clear()
        self.canvas.after.clear()

    def move_to_and_destroy(self, pos):
        self.destroy()
        #anim = Animation(opacity=0., d=.25, t='out_quad')
        #anim.bind(on_complete=self.destroy)
        #anim.start(self)

    def destroy(self, *args):
        self.parent.remove_widget(self)

    def move_to(self, pos):
        if self.pos == pos:
            return
        Animation(pos=pos, d=.1, t='out_quad').start(self)

    def on_number(self, instance, value):
        if platform == 'android':
            if value in achievements:
                app.gs_unlock(achievements[value])
            if value == 512:
                app.gs_increment(achievement_100x_block_512)
                app.gs_increment(achievement_1000x_block_512)
            elif value == 1024:
                app.gs_increment(achievement_100x_block_1024)
                app.gs_increment(achievement_1000x_block_1024)
            elif value == 2048:
                app.gs_increment(achievement_10x_block_2048)


class Game2048(Widget):

    cube_size = NumericProperty(10)
    cube_padding = NumericProperty(10)
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Game2048, self).__init__()
        self.grid = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]]

        # bind keyboard
        Window.bind(on_key_down=self.on_key_down)
        Window.on_keyboard = lambda *x: None

        self.restart()

    def on_key_down(self, window, key, *args):
        moved = False
        if key == 273:
            moved = self.move_topdown(True, from_keyboard=True)
        elif key == 274:
            moved = self.move_topdown(False, from_keyboard=True)
        elif key == 276:
            moved = self.move_leftright(False, from_keyboard=True)
        elif key == 275:
            moved = self.move_leftright(True, from_keyboard=True)
        elif key == 27 and platform == 'android':
            from jnius import autoclass
            PythonActivity = autoclass('org.renpy.android.PythonActivity')
            PythonActivity.mActivity.moveTaskToBack(True)
            return True
        self.check_end()

    def rebuild_background(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0xbb / 255., 0xad / 255., 0xa0 / 255.)
            BorderImage(pos=self.pos, size=self.size, source='data/round.png')
            Color(0xcc / 255., 0xc0 / 255., 0xb3 / 255.)
            csize = self.cube_size, self.cube_size
            for ix, iy in self.iterate_pos():
                BorderImage(pos=self.index_to_pos(ix, iy), size=csize,
                source='data/round.png')


    def reposition(self, *args):
        self.rebuild_background()
        # calculate the size of a number
        l = min(self.width, self.height)
        padding = (l / 4.) / 8.
        cube_size = (l - (padding * 5)) / 4.
        self.cube_size = cube_size
        self.cube_padding = padding

        for ix, iy, number in self.iterate():
            number.size = cube_size, cube_size
            number.pos = self.index_to_pos(ix, iy)

    def iterate(self):
        for ix, iy in self.iterate_pos():
            child = self.grid[ix][iy]
            if child:
                yield ix, iy, child

    def iterate_pos(self):
        for ix in range(4):
            for iy in range(4):
                yield ix, iy

    def index_to_pos(self, ix, iy):
        padding = self.cube_padding
        cube_size = self.cube_size
        return [
            (self.x + padding) + ix * (cube_size + padding),
            (self.y + padding) + iy * (cube_size + padding)]

    def spawn_number_at(self, ix, iy, value):
        number = Number(
                size=(self.cube_size, self.cube_size),
                pos=self.index_to_pos(ix, iy),
                number=value)
        self.grid[ix][iy] = number
        self.add_widget(number)

    def on_touch_up(self, touch):
        v = Vector(touch.pos) - Vector(touch.opos)
        if v.length() < dp(20):
            return

        # detect direction
        dx, dy = v
        if abs(dx) > abs(dy):
            self.move_leftright(dx > 0)
        else:
            self.move_topdown(dy > 0)
        return True

    def move_leftright(self, right, from_keyboard):
        t = get_tabuleiro(self)
        ot = copia_tabuleiro(t)
        if right:
          jogada = 'E'
        else:
          jogada = 'W'

        tabuleiro_reduz(t, jogada)

        if not tabuleiros_iguais(ot, t):
          preenche_posicao_aleatoria(t)
          set_tabuleiro(self, t)
          return True

        return False

    def move_topdown(self, top, from_keyboard):
        t = get_tabuleiro(self)
        ot = copia_tabuleiro(t)
        if top:
          jogada = 'S'
        else:
          jogada = 'N'

        tabuleiro_reduz(t, jogada)

        if not tabuleiros_iguais(ot, t):
          preenche_posicao_aleatoria(t)
          set_tabuleiro(self, t)
          return True

        return False

    def check_end(self):
        if not self.have_available_moves():
            self.end()
            return True
        return False

    def have_available_moves(self):
        return not tabuleiro_terminado(get_tabuleiro(self))

    def end(self):
        end = self.ids.end.__self__
        self.remove_widget(end)
        self.add_widget(end)
        text = 'Game\nover!'
        for ix, iy, cube in self.iterate():
            if cube.number == 2048:
                text = 'WIN !'
        self.ids.end_label.text = text
        Animation(opacity=1., d=.5).start(end)
        app.gs_score(self.score)

    def restart(self):
        self.score = 0
        for ix, iy, child in self.iterate():
            child.destroy()
        self.grid = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]]
        t = cria_tabuleiro()
        preenche_posicao_aleatoria(t)
        preenche_posicao_aleatoria(t)
        set_tabuleiro(self, t)
        self.ids.end.opacity = 0


class Game2048App(App):
    use_kivy_settings = False

    def build_config(self, config):
        if platform == 'android':
            config.setdefaults('play', {'use_google_play': '0'})

    def build(self):
        global app
        app = self

        if platform == 'android':
            self.use_google_play = self.config.getint('play', 'use_google_play')
            if self.use_google_play:
                gs_android.setup(self)
            else:
                Clock.schedule_once(self.ask_google_play, .5)
        else:
            # remove all the leaderboard and achievement buttons
            scoring = self.root.ids.scoring
            scoring.parent.remove_widget(scoring)

    def gs_increment(self, uid):
        if platform == 'android' and self.use_google_play:
            gs_android.increment(uid, 1)

    def gs_unlock(self, uid):
        if platform == 'android' and self.use_google_play:
            gs_android.unlock(uid)

    def gs_score(self, score):
        if platform == 'android' and self.use_google_play:
            gs_android.leaderboard(leaderboard_highscore, score)

    def gs_show_achievements(self):
        if platform == 'android':
            if self.use_google_play:
                gs_android.show_achievements()
            else:
                self.ask_google_play()

    def gs_show_leaderboard(self):
        if platform == 'android':
            if self.use_google_play:
                gs_android.show_leaderboard(leaderboard_highscore)
            else:
                self.ask_google_play()

    def ask_google_play(self, *args):
        popup = GooglePlayPopup()
        popup.open()

    def activate_google_play(self):
        self.config.set('play', 'use_google_play', '1')
        self.config.write()
        self.use_google_play = 1
        gs_android.setup(self)

    def on_pause(self):
        if platform == 'android':
            gs_android.on_stop()
        return True

    def on_resume(self):
        if platform == 'android':
            gs_android.on_start()

    def _on_keyboard_settings(self, *args):
        return

if __name__ == '__main__':
    Factory.register('ButtonBehavior', cls=ButtonBehavior)
    Game2048App().run()
