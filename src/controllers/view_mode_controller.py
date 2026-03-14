from src.components.cohen_sutherland_popup_frame import CohenSutherlandClipFrame


class ViewModeController:
    def __init__(self, view, gl_window_controller,  model):
        self.view = view
        self.model = model
        self.gl_window_controller = gl_window_controller

        self.view.set_controller(self)

    def open_line_clip_popup(self):
        clip_frame = CohenSutherlandClipFrame(
            self.view,
            title="Recorte de Reta - Cohen-Sutherland",
            w=980,
            h=720
        )
        clip_frame.open_popup()
        self.view.wait_window(clip_frame.popup)
        