class RenderService:
    _view = None

    @classmethod
    def register_view(cls, view):
        cls._view = view

    @classmethod
    def request_render(cls):
        if cls._view:
            cls._view.request_render()