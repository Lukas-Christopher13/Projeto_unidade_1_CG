from src.views.main_frame_view import MainFrameView
from src.controllers.gl_window_controller import GlWindowController
from src.controllers.lateralbar_controller import LateralBarController

class MainFrameController:
    def __init__(self, root):
        self.view = MainFrameView(root, self)

        self.gl_window_controller = GlWindowController(self.view.gl_window_view)
        self.lateral_bar_controller = LateralBarController(self.view.lateral_bar_view, self.gl_window_controller, None)

        self.main_frame_model = None

    def show_transform_screen(self, reset_scene=True):
        self.lateral_bar_controller.show_transform_screen(reset_scene=reset_scene)

    def show_line_algorithm_screen(self, name: str, algorithm):
        self.lateral_bar_controller.show_line_algorithm_screen(name, algorithm)

    def show_circle_algorithm_screen(self, name: str, algorithm):
        self.lateral_bar_controller.show_circle_algorithm_screen(name, algorithm)

    def run(self):
        self.view.gl_window_view.mainloop()

