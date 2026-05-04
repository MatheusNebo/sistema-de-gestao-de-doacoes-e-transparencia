from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from sqlalchemy.exc import SQLAlchemyError

class InventoryRepository:

    def create(self, db: Session, data):
        inventory = Inventory(**data.model_dump())
        db.add(inventory)

        try:
            db.commit()
            db.refresh(inventory)
            return inventory

        except SQLAlchemyError:
            db.rollback()
            raise


    def get_all(self, db: Session):
        return db.query(Inventory).all()


    def get_by_id(self, db: Session, inventory_id: int):
        return db.query(Inventory).filter(
            Inventory.inventory_id == inventory_id
        ).first()


    # abordagem otimizada em entidades de alto volume
    def update(self, db: Session, inventory_id: int, data):
        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            return self.get_by_id(db, inventory_id)

        try:
            db.query(Inventory).filter(
                Inventory.inventory_id == inventory_id
            ).update(update_data, synchronize_session=False)

            db.commit()

            return self.get_by_id(db, inventory_id)

        except SQLAlchemyError:
            db.rollback()
            raise


    def delete(self, db: Session, inventory_id: int):
        inventory = self.get_by_id(db, inventory_id)

        if not inventory:
            return None

        try:
            db.delete(inventory)
            db.commit()
            return inventory

        except SQLAlchemyError:
            db.rollback()
            raise