from src.models.gl_window_model import singleton
from src.controllers.edit_shape_controller import EditShapeController

class LateralBarController:
    def __init__(self, view, model):
        self.model = model
        self.view = view

        self.edit_shape_controller = EditShapeController(self.view.edit_shape_view, None)

        singleton.add_listener(self)

        self.view.listbox.bind("<<ListboxSelect>>", self.select_shape)
        
    def update(self):
        self.view.listbox.delete(0, "end")
        for id, valor in enumerate(singleton.shapes):
            self.view.listbox.insert("end", str(id))

    def select_shape(self, shape):
        select = self.view.listbox.curselection()
        if select:
            indice = select[0]
            valor = int(self.view.listbox.get(indice))
            singleton.set_selected(valor)
        