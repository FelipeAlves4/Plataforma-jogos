from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle

# Importar os jogos
from guess_game import start_guess_game
from battle_game import start_battle_game
from treasure_game import start_treasure_game


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Adiciona um fundo gradiente
        with self.canvas.before:
            Color(0.1, 0.1, 0.3, 1)  # Cor de fundo (azul escuro)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)
        
        # Título
        title = Label(
            text="Selecione um jogo",
            font_size=32,
            color=(1, 1, 1, 1),  # Cor branca
            size_hint=(1, 0.2)
        )
        layout.add_widget(title)

        # Botão do Jogo da Adivinhação
        btn_game1 = Button(
            text="🎯 Jogo da Adivinhação",
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            size_hint=(1, 0.2),
            background_normal="",  # Remove o fundo padrão
            background_down=""
        )
        btn_game1.bind(on_press=lambda x: start_guess_game())
        layout.add_widget(btn_game1)

        # Botão do Batalha Naval
        btn_game2 = Button(
            text="⚓ Batalha Naval",
            background_color=(0.1, 0.7, 0.5, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            size_hint=(1, 0.2),
            background_normal="",
            background_down=""
        )
        btn_game2.bind(on_press=lambda x: start_battle_game())
        layout.add_widget(btn_game2)

        # Botão do Caça ao Tesouro
        btn_game3 = Button(
            text="💎 Caça ao Tesouro",
            background_color=(1, 0.5, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            size_hint=(1, 0.2),
            background_normal="",
            background_down=""
        )
        btn_game3.bind(on_press=lambda x: start_treasure_game())
        layout.add_widget(btn_game3)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos


class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.current = 'main_menu'
        return sm


if __name__ == '__main__':
    GameApp().run()
