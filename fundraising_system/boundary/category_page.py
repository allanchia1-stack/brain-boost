class CategoryPage:
    def __init__(self, controller):
        self.controller = controller

    def create_category(self, name):
        return self.controller.create_category(name)

    def view_categories(self):
        return self.controller.view_categories()