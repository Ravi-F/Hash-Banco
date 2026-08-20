from pathlib import Path

import time
import tkinter as tk
import customtkinter as ctk

from app.indice_hash import IndiceHashEstatico
from app.models import Pagina

# Configurações visuais do CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class SistemaHashApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Índice Hash Estático")
        self.geometry("1100x750")

        self.palavras = []
        self.paginas = []
        self.indice = None
        self.carregar_dados()

        self.criar_interface()

    def carregar_dados(self):
        # Tenta carregar o arquivo local data/words.txt
        caminho = Path(__file__).resolve().parent.parent / "data" / "words.txt"
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                self.palavras = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            # Fallback para execução de testes rápidos se o arquivo não existir
            self.palavras = [f"palavra_{i}" for i in range(100000)]

    def criar_interface(self):
        # Layout principal em Grid (Esquerda: Controles/Estatísticas, Direita: Visualizações)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Painel Esquerdo
        frame_esquerda = ctk.CTkFrame(self, width=320, corner_radius=10)
        frame_esquerda.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(frame_esquerda, text="Configurações do Índice", font=("Arial", 16, "bold")).pack(pady=10)

        ctk.CTkLabel(frame_esquerda, text="Tamanho da Página (tuplas/pág):").pack(anchor="w", padx=15)
        self.entry_tam_pagina = ctk.CTkEntry(frame_esquerda, placeholder_text="Ex: 500")
        self.entry_tam_pagina.insert(0, "1000")
        self.entry_tam_pagina.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(frame_esquerda, text="Tamanho do Bucket (FR):").pack(anchor="w", padx=15)
        self.entry_fr = ctk.CTkEntry(frame_esquerda, placeholder_text="Ex: 10")
        self.entry_fr.insert(0, "10")
        self.entry_fr.pack(fill="x", padx=15, pady=5)

        self.btn_construir = ctk.CTkButton(frame_esquerda, text="Construir Índice", command=self.construir_indice)
        self.btn_construir.pack(fill="x", padx=15, pady=15)

        ctk.CTkFrame(frame_esquerda, height=2, fg_color="gray").pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(frame_esquerda, text="Operações de Busca", font=("Arial", 16, "bold")).pack(pady=10)

        ctk.CTkLabel(frame_esquerda, text="Chave de Busca (Palavra):").pack(anchor="w", padx=15)
        self.entry_busca = ctk.CTkEntry(frame_esquerda, placeholder_text="Digite uma palavra")
        self.entry_busca.pack(fill="x", padx=15, pady=5)

        self.btn_buscar_hash = ctk.CTkButton(frame_esquerda, text="Buscar via Índice Hash", command=self.buscar_hash, state="disabled")
        self.btn_buscar_hash.pack(fill="x", padx=15, pady=5)

        self.btn_table_scan = ctk.CTkButton(frame_esquerda, text="Executar Table Scan", command=self.executar_table_scan, state="disabled", fg_color="darkorange", hover_color="orange")
        self.btn_table_scan.pack(fill="x", padx=15, pady=5)

        # Painel de Estatísticas
        ctk.CTkFrame(frame_esquerda, height=2, fg_color="gray").pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(frame_esquerda, text="Estatísticas do Sistema", font=("Arial", 16, "bold")).pack(pady=5)

        self.lbl_stats = ctk.CTkLabel(frame_esquerda, text="Construa o índice para exibir métricas.", justify="left", font=("Consolas", 11))
        self.lbl_stats.pack(fill="both", expand=True, padx=15, pady=5)

        # Painel Direito (Resultados e Exibição de Páginas)
        frame_direita = ctk.CTkFrame(self, corner_radius=10)
        frame_direita.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        frame_direita.grid_rowconfigure(1, weight=1)
        frame_direita.grid_columnconfigure(0, weight=1)

        # Resultado da Pesquisa
        self.frame_resultado = ctk.CTkFrame(frame_direita, fg_color="#2b2b2b", corner_radius=8)
        self.frame_resultado.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.lbl_resultado = ctk.CTkLabel(self.frame_resultado, text="Aguardando consultas...", font=("Arial", 13))
        self.lbl_resultado.pack(padx=10, pady=10)

        # Abas para Visualizar as Páginas
        self.tabview = ctk.CTkTabview(frame_direita)
        self.tabview.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.tab_pag1 = self.tabview.add("Primeira Página")
        self.tab_pag_last = self.tabview.add("Última Página")

        self.txt_pag1 = ctk.CTkTextbox(self.tab_pag1, font=("Consolas", 12))
        self.txt_pag1.pack(fill="both", expand=True)

        self.txt_pag_last = ctk.CTkTextbox(self.tab_pag_last, font=("Consolas", 12))
        self.txt_pag_last.pack(fill="both", expand=True)

    def construir_indice(self):
        import math

        try:
            tam_pag = int(self.entry_tam_pagina.get())
            fr = int(self.entry_fr.get())
        except ValueError:
            self.lbl_resultado.configure(text="Erro: Informe valores numéricos válidos.")
            return

        nr = len(self.palavras)
        if nr == 0:
            self.lbl_resultado.configure(text="Erro: Arquivo de palavras vazio ou não encontrado.")
            return

        # 1. Paginamento
        self.paginas = []
        num_paginas = math.ceil(nr / tam_pag)

        for i in range(num_paginas):
            pag = Pagina(i)
            pag.tuplas = self.palavras[i * tam_pag : (i + 1) * tam_pag]
            self.paginas.append(pag)

        # 2. Exibição da primeira e última página na UI
        self.txt_pag1.delete("1.0", tk.END)
        self.txt_pag1.insert("1.0", f"--- PÁGINA 0 (Total de tuplas: {len(self.paginas[0].tuplas)}) ---\n\n")
        self.txt_pag1.insert(tk.END, "\n".join(self.paginas[0].tuplas))

        self.txt_pag_last.delete("1.0", tk.END)
        self.txt_pag_last.insert("1.0", f"--- PÁGINA {num_paginas - 1} (Total de tuplas: {len(self.paginas[-1].tuplas)}) ---\n\n")
        self.txt_pag_last.insert(tk.END, "\n".join(self.paginas[-1].tuplas))

        # 3. Construção do Índice Hash
        self.indice = IndiceHashEstatico(fr, nr, tam_pag)

        inicio = time.perf_counter()
        for pag in self.paginas:
            for chave in pag.tuplas:
                self.indice.inserir(chave, pag.id_pagina)
        tempo_construcao = (time.perf_counter() - inicio) * 1000

        # Cálculo de Métricas
        tx_colisao = (self.indice.colisoes / nr) * 100
        tx_overflow = (self.indice.overflows / nr) * 100

        stats_txt = (
            f"Total de Tuplas (NR): {nr:,}\n"
            f"Total Páginas (NP): {num_paginas:,}\n"
            f"Num. Buckets (NB): {self.indice.nb:,}\n"
            f"Capacidade/Bucket (FR): {fr}\n"
            f"---------------------------\n"
            f"Taxa de Colisões: {tx_colisao:.2f}%\n"
            f"Taxa de Overflows: {tx_overflow:.2f}%\n"
            f"Tempo Construção: {tempo_construcao:.2f}ms"
        )
        self.lbl_stats.configure(text=stats_txt)
        self.lbl_resultado.configure(text="Índice construído com sucesso! Pronto para realizar buscas.")

        self.btn_buscar_hash.configure(state="normal")

    def buscar_hash(self):
        chave = self.entry_busca.get().strip()
        if not chave or not self.indice:
            return

        inicio = time.perf_counter()
        pag_id, custo_io = self.indice.buscar(chave)
        tempo_hash = (time.perf_counter() - inicio) * 1000

        if pag_id is not None:
            msg = (
                f"[BUSCA HASH] Registo Encontrado!\n"
                f"Chave: '{chave}' | Localizado na Página: {pag_id}\n"
                f"Custo estimado de I/O: {custo_io} página(s) lida(s) | Tempo: {tempo_hash:.4f} ms"
            )
            self.btn_table_scan.configure(state="normal")
        else:
            msg = f"[BUSCA HASH] A chave '{chave}' NÃO foi encontrada na tabela.\nCusto I/O: {custo_io} páginas lidas | Tempo: {tempo_hash:.4f} ms"
            self.btn_table_scan.configure(state="disabled")

        self.tempo_hash_ultimo = tempo_hash
        self.lbl_resultado.configure(text=msg)

    def executar_table_scan(self):
        chave = self.entry_busca.get().strip()
        if not chave:
            return

        inicio = time.perf_counter()
        pag_encontrada = None
        custo_io = 0

        for pag in self.paginas:
            custo_io += 1
            if chave in pag.tuplas:
                pag_encontrada = pag.id_pagina
                break

        tempo_scan = (time.perf_counter() - inicio) * 1000
        diferenca_tempo = tempo_scan - getattr(self, "tempo_hash_ultimo", 0)

        if pag_encontrada is not None:
            msg = (
                f"[TABLE SCAN] Registro Encontrado!\n"
                f"Chave: '{chave}' | Localizado na Página: {pag_encontrada}\n"
                f"Custo de I/O (Table Scan): {custo_io} páginas lidas | Tempo: {tempo_scan:.4f} ms\n"
                f"Diferença (Table Scan - Hash): +{diferenca_tempo:.4f} ms"
            )
        else:
            msg = f"[TABLE SCAN] Chave não encontrada. Percorridas {custo_io} páginas."

        self.lbl_resultado.configure(text=msg)
