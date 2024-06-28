import pyxel


WIDTH = 1920
HEIGHT = 1080


class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="3D", fps=60, quit_key=pyxel.KEY_ESCAPE, display_scale=4)
        pyxel.run(self.update, self.draw)

    def update(self):
    	pass

    def draw(self):
        pyxel.cls(3)

App()