# Hash-Banco

Aplicação de demonstração de um índice hash estático com interface gráfica.

**Requisitos**
- **Python**: 3.8+ (testado com 3.12)
- **Sistema**: Linux (Pop!_OS/Ubuntu recomendado)
- **Dependências de sistema**: `python3-tk` (fornece `tkinter` para GUIs)
- **Dependências Python**: `customtkinter`

**Instalação (recomendada: virtualenv)**
```bash
# instalar dependências de sistema (Pop!/Ubuntu)
sudo apt update
sudo apt install -y python3 python3-venv python3-pip python3-tk

# criar e ativar virtualenv no diretório do projeto
python3 -m venv .venv
source .venv/bin/activate

# instalar dependências Python
pip install --upgrade pip
pip install customtkinter
```

Se preferir não usar virtualenv, instale `customtkinter` globalmente com `pip install --user customtkinter`.

**Executar a aplicação**

Com o virtualenv ativado (ou com as dependências instaladas globalmente):
```bash
.venv/bin/python app.py
# ou
python3 app.py
```

**Verificações rápidas**
- Verificar se `tkinter` está disponível no ambiente Python:
```bash
.venv/bin/python -c "import tkinter; print('tkinter OK')"
```
- Se gerar erro `ModuleNotFoundError: No module named 'tkinter'`, instale `python3-tk` via `apt` (ou o gerenciador de pacotes da sua distribuição).

**Uso básico da interface**
- Ao abrir a janela, ajuste `Tamanho da Página` e `Tamanho do Bucket (FR)` se desejar. Valores padrão: `1000` e `10`.
- Clique em `Construir Índice` para gerar o índice a partir de `words.txt` (se o arquivo não existir, o programa gera uma lista de teste automática).
- Use `Chave de Busca` para procurar uma palavra via índice hash (`Buscar via Índice Hash`).
- Compare desempenho com `Executar Table Scan`.

**Arquivo de dados**
- `words.txt`: arquivo de texto com uma palavra por linha. Se presente, será utilizado como fonte de tuplas.

**Solução de problemas**
- Display não abre em servidor remoto: garanta encaminhamento X (`ssh -X`) ou use um servidor X virtual (ex.: `Xvfb`).
- Erro ao importar `customtkinter`: rode `pip install customtkinter` no ambiente ativo.

**Notas**
- A aplicação é uma demonstração educativa — o índice e buckets são mantidos em memória.
- Para testes com muitos dados, ajuste `Tamanho da Página` para controlar número de páginas geradas.