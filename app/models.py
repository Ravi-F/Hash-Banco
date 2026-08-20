class Pagina:
    def __init__(self, id_pagina):
        self.id_pagina = id_pagina
        self.tuplas = []

class Bucket:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.entradas = []  # Lista de tuplas: (chave, id_pagina)
        self.overflow = None

    def inserir(self, chave, id_pagina):
        if len(self.entradas) < self.capacidade:
            self.entradas.append((chave, id_pagina))
            return False  # Inserido sem gerar novo overflow
        else:
            if self.overflow is None:
                self.overflow = Bucket(self.capacidade)
            return self.overflow.inserir(chave, id_pagina) or True
