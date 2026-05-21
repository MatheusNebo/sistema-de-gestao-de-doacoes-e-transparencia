import enum


class DonorType(str, enum.Enum):
    PF = "PF"
    PJ = "PJ"

    def label(self):
        labels = {
            "PF": "Pessoa Física",
            "PJ": "Pessoa Jurídica"
        }
        return labels.get(self.value)


class DonationType(str, enum.Enum):
    FOOD = "food"
    FINANCIAL = "financial"

    def label(self):
        labels = {
            "food": "Doação de Alimentos",
            "financial": "Doação Financeira"
        }
        return labels.get(self.value)


class UnitType(str, enum.Enum):
    KG = "kg"
    G = "g"
    UN = "un"
    L = "l"
    ML = "ml"
    FARDO = "fardo"
    CAIXA = "caixa"

    def label(self):
        labels = {
            "kg": "Quilograma",
            "g": "Grama",
            "un": "Unidade",
            "l": "Litro",
            "ml": "Mililitro",
            "fardo": "Fardo",
            "caixa": "Caixa"
        }
        return labels.get(self.value)


class UserRole(str, enum.Enum):
    admin = "admin"
    voluntario = "voluntario"


class MovementType(str, enum.Enum):
    ENTRADA = "entrada"
    SAIDA = "saida"
    PERDA = "perda"

    def label(self):
        labels = {
            "entrada": "Entrada",
            "saida": "Saída",
            "perda": "Perda"
        }
        return labels.get(self.value)


class MovementSource(str, enum.Enum):
    DOACAO = "doacao"
    DISTRIBUICAO = "distribuicao"
    AJUSTE = "ajuste"

    def label(self):
        labels = {
            "doacao": "Doação",
            "distribuicao": "Distribuição",
            "ajuste": "Ajuste"
        }
        return labels.get(self.value)