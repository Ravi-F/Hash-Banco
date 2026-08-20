# Explicação do Código — `app.py`

Resumo rápido
- Aplicação GUI que demonstra um índice hash estático em memória para buscas por palavras.
- Interface construída com `customtkinter` sobre `tkinter`.

Arquitetura e componentes principais

- `Pagina`:
  - Representa uma página lógica contendo um conjunto de tuplas (aqui, palavras).
  - Atributos: `id_pagina`, `tuplas` (lista de strings).

- `Bucket`:
  - Representa um bucket do índice hash com capacidade fixa (`capacidade`).
  - Mantém `entradas` (lista de tuplas `(chave, id_pagina)`) e possivelmente uma cadeia `overflow` (encadeamento de buckets adicionais).
  - Método `inserir(chave, id_pagina)` insere enquanto houver espaço, caso contrário cria/encadeia overflow.

- `IndiceHashEstatico`:
  - Constrói e mantém os buckets: parâmetros principais `fr` (capacidade por bucket), `nr` (número de tuplas) e `tamanho_pagina`.
  - Calcula `nb` (número de buckets) com um fator de carga (garante ímpar mínimo de 13).
  - `funcao_hash(chave)`: hash tipo DJB2 adaptado; retorna índice `h % nb`.
  - `inserir(chave, id_pagina)`: envia para bucket pelo hash; conta colisões e overflows.
  - `buscar(chave)`: percorre bucket e seus `overflow` encadeados; retorna `(id_pagina, custo_paginas)` ou `(None, custo)`.

- `SistemaHashApp` (subclasse `ctk.CTk`):
  - Interface gráfica e fluxo da aplicação.
  - `carregar_dados()`: tenta ler `words.txt`; se não existir gera uma lista de teste grande.
  - `criar_interface()`: monta controles (configuração, busca, estatísticas) e painéis de visualização.
  - `construir_indice()`: realiza o paginamento (divide `palavras` em `Pagina`), popula `IndiceHashEstatico` inserindo cada chave com `id_pagina`, e calcula métricas (taxa de colisões/overflows, tempo de construção).
  - `buscar_hash()`: busca uma chave via índice, mede tempo e custo (número de páginas lidas); habilita `Table Scan` quando encontrado.
  - `executar_table_scan()`: varre todas as páginas sequencialmente (simula busca sem índice) e mede custo/tempo para comparação.

Fluxo de execução
1. Ao iniciar (`if __name__ == "__main__"`) a janela `SistemaHashApp` é criada e exibida (`mainloop`).
2. Usuário define `Tamanho da Página` e `FR` e clica em `Construir Índice`.
3. O código paginará os dados, exibirá a primeira/última página, construirá o índice na memória e mostrará métricas.
4. Buscas podem ser feitas via índice ou por `Table Scan` para comparar custo/tempo.

Pontos importantes / decisões de implementação
- O hash usa DJB2 (boa distribuição para strings simples) e aplica modulo por `nb`.
- Colisões são contadas quando um bucket já tem entradas; overflows são encadeados como novos `Bucket`.
- `nb` é calculado com um fator de carga (~20%) e garantido como ímpar mínimo (`max(13, ...) | 1`).
- O sistema carrega `words.txt` se existir, caso contrário gera dados de teste (útil para demonstração sem dependências externas).

Como estender / pontos de melhoria
- Persistência: gravar páginas/buckets em disco (simular I/O real).
- Remoção e re-hash dinâmico: atualmente o índice é estático após construção.
- Estatísticas mais detalhadas: profundidade média de overflow, ocupação por bucket, histograma de buckets.
- Otimização: substituir encadeamento por listas de overflow mais eficientes ou alocação em blocos.

Referências de arquivos
- Código principal: [app.py](app.py#L1)
- Dados de entrada (opcional): [words.txt](words.txt#L1)