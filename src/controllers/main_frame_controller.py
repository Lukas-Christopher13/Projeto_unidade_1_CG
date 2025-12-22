from src.views.main_frame_view import MainFrameView
from src.controllers.lateralbar_controller import LateralBarController
from src.utils.windowtk import WindowTk

class MainFrameController:
    def __init__(self, root):
        self.view = MainFrameView(root, self)

        self.lateral_bar_controller = LateralBarController(self.view.lateral_bar_view, None)

        self.main_frame_model = None

    def run(self):
        self.view.gl_window.animate = 1
        self.view.gl_window.mainloop()



