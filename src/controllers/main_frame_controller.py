from src.views.main_frame_view import MainFrameView
from src.controllers.gl_window_controller import GlWindowController
from src.controllers.lateralbar_controller import LateralBarController
from src.controllers.context_menu_controller import ContextMenuController

class MainFrameController:
    def __init__(self, root):
        self.view = MainFrameView(root, self)

        self.gl_window_controller = GlWindowController(self.view.gl_window_view)
        self.lateral_bar_controller = LateralBarController(self.view.lateral_bar_view, None)
        self.context_menu_controller = ContextMenuController(self.view.context_menu_view)

        self.main_frame_model = None

    def run(self):
        self.view.gl_window_view.animate = 1
        self.view.gl_window_view.mainloop()



