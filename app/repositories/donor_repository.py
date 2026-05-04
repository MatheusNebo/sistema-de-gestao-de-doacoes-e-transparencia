from sqlalchemy.orm import Session
from app.models.donor import Donor
from sqlalchemy.exc import SQLAlchemyError

class DonorRepository:

    def create(self, db: Session, data):
        donor = Donor(**data.model_dump())
        db.add(donor)

        try:
            db.commit()
            db.refresh(donor)
            return donor

        except SQLAlchemyError:
            db.rollback()
            raise

    def get_all(self, db: Session):
        return db.query(Donor).all()

    def get_by_id(self, db: Session, donor_id: int):
        return db.query(Donor).filter(
            Donor.donor_id == donor_id
        ).first()

    # abordagem otimizada em entidades de alto volume, update direto no banco, sem carregar objeto em memória
    def update(self, db: Session, donor_id: int, data):
        # pula campos não fornecidos (melhor para PATCH requests)
        update_data = data.model_dump(exclude_unset=True)
    
        if not update_data:
            return self.get_by_id(db, donor_id)
    
        # update direto no banco - evita loop Python e múltiplas operações
        db.query(Donor).filter(
        Donor.donor_id == donor_id
        ).update(update_data, synchronize_session=False)
    
        db.commit()
        return self.get_by_id(db, donor_id)

    def delete(self, db: Session, donor_id: int):
        donor = self.get_by_id(db, donor_id)

        if not donor:
            return None

        db.delete(donor)
        db.commit()
        return donor