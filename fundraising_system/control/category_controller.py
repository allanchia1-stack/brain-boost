from entity.category import Category


class CategoryController:
    def __init__(self, datastore):
        self.datastore = datastore

    def create_category(self, name):
        category_id = self.datastore.generate_id("C", self.datastore.categories)
        category = Category(category_id, name)
        self.datastore.categories.append(category)
        return category

    def view_categories(self):
        return self.datastore.categories

    def update_category(self, category_id, new_name):
        for category in self.datastore.categories:
            if category.category_id == category_id:
                category.name = new_name
                return category
        return None

    def delete_category(self, category_id):
        for category in self.datastore.categories:
            if category.category_id == category_id:
                self.datastore.categories.remove(category)
                return True
        return False