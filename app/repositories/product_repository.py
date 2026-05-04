from sqlalchemy.orm import Session
from app.models.product import Product
from sqlalchemy.exc import SQLAlchemyError

class ProductRepository:

    def create(self, db: Session, data):
        product = Product(**data.model_dump())
        db.add(product)

        try:
            db.commit()
            db.refresh(product)
            return product
        
        except SQLAlchemyError:
            db.rollback()
            raise

    def get_all(self, db: Session):
        return db.query(Product).all()

    def get_by_id(self, db: Session, product_id: int):
        return db.query(Product).filter(
            Product.product_id == product_id
        ).first()

# abordagem ORM tradicional em entidades de baixa complexidade
    def update(self, db: Session, product_id: int, data):
        product = self.get_by_id(db, product_id)

        if not product:
            return None

        for key, value in data.model_dump().items():
            setattr(product, key, value)

        db.commit()
        db.refresh(product)
        return product

    def delete(self, db: Session, product_id: int):
        product = self.get_by_id(db, product_id)

        if not product:
            return None

        db.delete(product)
        db.commit()
        return product