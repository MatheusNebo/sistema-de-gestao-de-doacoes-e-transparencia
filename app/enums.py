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