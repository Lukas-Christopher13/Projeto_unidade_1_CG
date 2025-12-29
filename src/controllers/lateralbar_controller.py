from src.models.gl_window_model import gl_window_model
from src.controllers.edit_shape_controller import EditShapeController
from src.controllers.view_mode_controller import ViewModeController

class LateralBarController:
    def __init__(self, view, gl_window_controller, model):
        self.view = view
        self.model = model
        self.gl_window_controller = gl_window_controller

        self.view_mode_controller = ViewModeController(self.view.view_mode_view, gl_window_controller, None)
        self.edit_shape_controller = EditShapeController(self.view.edit_shape_view, None)

        gl_window_model.add_listener(self)

        self.view.listbox.bind("<<ListboxSelect>>", self.select_shape)
        
    def update(self):
        self.view.listbox.delete(0, "end")
        for id, valor in enumerate(gl_window_model.shapes):
            self.view.listbox.insert("end", str(id))

    def select_shape(self, shape):
        select = self.view.listbox.curselection()
        if select:
            indice = select[0]
            valor = int(self.view.listbox.get(indice))
            gl_window_model.set_selected(valor)
        