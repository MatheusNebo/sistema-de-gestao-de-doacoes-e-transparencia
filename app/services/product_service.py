from app.repositories.product_repository import ProductRepository

class ProductService:

    def __init__(self):
        self.repository = ProductRepository()

    def create_product(self, db, data):
        return self.repository.create(db, data)

    def list_products(self, db):
        return self.repository.get_all(db)

    def get_product(self, db, product_id):
        return self.repository.get_by_id(db, product_id)

    def update_product(self, db, product_id, data):
        return self.repository.update(db, product_id, data)

    def delete_product(self, db, product_id):
        return self.repository.delete(db, product_id)