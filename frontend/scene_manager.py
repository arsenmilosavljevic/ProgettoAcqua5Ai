from frontend.scenes.intro_scene import IntroScene

class SceneManager:

    def __init__(self):
        self.scene = IntroScene(self)

    def change(self,new_scene):
        self.scene = new_scene

    def update(self,events,state):
        self.scene.update(events,state)

    def draw(self,screen,state):
        self.scene.draw(screen,state)