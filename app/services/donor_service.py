from fastapi import HTTPException
from app.enums import DonorType
from app.repositories.donor_repository import DonorRepository


class DonorService:

    def __init__(self):
        self.repository = DonorRepository()

    def create_donor(self, db, data):
        self._validate_pf_pj(data)
        return self.repository.create(db, data)

    def list_donors(self, db):
        return self.repository.get_all(db)

    def get_donor(self, db, donor_id):
        return self.repository.get_by_id(db, donor_id)

    def update_donor(self, db, donor_id, data):
        
        # Busca o donor atual para validar mudança de tipo
        current_donor = self.repository.get_by_id(db, donor_id)
        if not current_donor:
            raise HTTPException(status_code=404, detail="Doador não encontrado")
        
        self._validate_pf_pj_update(data, current_donor)
        return self.repository.update(db, donor_id, data)

    def delete_donor(self, db, donor_id):
        return self.repository.delete(db, donor_id)

    def _validate_pf_pj(self, data):
        if data.donor_type == DonorType.PF:
            if not data.name or not data.cpf:
                raise HTTPException(
                    status_code=400,
                    detail="Pessoa física exige nome e CPF"
                )

        elif data.donor_type == DonorType.PJ:
            if not data.company_name or not data.cnpj:
                raise HTTPException(
                    status_code=400,
                    detail="Pessoa jurídica exige razão social e CNPJ"
                )

    def _validate_pf_pj_update(self, data, current_donor=None):

        self._validate_immutable_fields(current_donor, data)

        # Validação de mudança de tipo
        if current_donor and data.donor_type and data.donor_type != current_donor.donor_type:
            raise HTTPException(
                status_code=400,
                detail="Não é permitido alterar o tipo de doador após a criação"
            )

        if data.donor_type is None:
            return

        if data.donor_type == DonorType.PF and data.company_name:
            raise HTTPException(
                status_code=400,
                detail="Pessoa física não deve possuir razão social"
            )

        if data.donor_type == DonorType.PJ and data.name:
            raise HTTPException(
                status_code=400,
                detail="Pessoa jurídica não deve possuir nome pessoal"
            )

        if data.cpf and data.cpf != current_donor.cpf:
            raise HTTPException(
                status_code=400,
                detail="CPF não pode ser alterado"
        )

        if data.cnpj and data.cnpj != current_donor.cnpj:
            raise HTTPException(
                status_code=400,
                detail="CNPJ não pode ser alterado"
        )

        