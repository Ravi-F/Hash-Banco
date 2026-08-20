import math

from app.models import Bucket


class IndiceHashEstatico:
    def __init__(self, fr, nr, tamanho_pagina):
        self.fr = fr  # Fator de bloco / Tamanho do bucket
        self.nr = nr  # Total de tuplas
        self.tamanho_pagina = tamanho_pagina
        self.num_paginas = math.ceil(nr / tamanho_pagina) if tamanho_pagina > 0 else 0

        # NB > NR / FR (Adicionado um fator de carga de ~20% para eficiência)
        self.nb = max(13, int(nr * 1.5) | 1)
        self.buckets = [Bucket(fr) for _ in range(self.nb)]

        self.colisoes = 0
        self.overflows = 0

    def funcao_hash(self, chave):
        # Algoritmo de Hash Polinomial (DJB2 adaptado)
        h = 5381
        for char in chave:
            h = ((h << 5) + h) + ord(char)
        return h % self.nb

    def inserir(self, chave, id_pagina):
        idx = self.funcao_hash(chave)
        bucket = self.buckets[idx]

        if len(bucket.entradas) > 0:
            self.colisoes += 1

        houve_overflow = bucket.inserir(chave, id_pagina)
        if houve_overflow:
            self.overflows += 1

    def buscar(self, chave):
        idx = self.funcao_hash(chave)
        bucket = self.buckets[idx]
        custo_paginas = 1  # Acesso ao bucket/página

        curr = bucket
        while curr:
            for item_chave, id_pag in curr.entradas:
                if item_chave == chave:
                    return id_pag, custo_paginas
            curr = curr.overflow
            if curr:
                custo_paginas += 1  # Leitura extra de bucket em overflow

        return None, custo_paginas
