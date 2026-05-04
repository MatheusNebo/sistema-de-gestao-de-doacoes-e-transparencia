from app.repositories.inventory_repository import InventoryRepository

class InventoryService:

    def __init__(self):
        self.repository = InventoryRepository()

    def create_inventory(self, db, data):
        return self.repository.create(db, data)

    def list_inventories(self, db):
        return self.repository.get_all(db)

    def get_inventory(self, db, inventory_id):
        return self.repository.get_by_id(db, inventory_id)

    def update_inventory(self, db, inventory_id, data):
        return self.repository.update(db, inventory_id, data)

    def delete_inventory(self, db, inventory_id):
        return self.repository.delete(db, inventory_id)