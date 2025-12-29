class ViewModeController:
    def __init__(self, view, gl_window_controller,  model):
        self.view = view
        self.model = model
        self.gl_window_controller = gl_window_controller

        self.view.set_controller(self)
        