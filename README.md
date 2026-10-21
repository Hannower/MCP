# 🔌 MCP Supabase Server (RAG Bridge)

> Servidor baseado no **Model Context Protocol (MCP)** para permitir que Agentes de IA consultem dados relacionais e vetoriais de documentos fiscais armazenados no **Supabase**.

---

## 🎯 Objetivo

Este projeto atua como uma ponte padronizada de comunicação (via protocolo MCP e transporte `stdio`) entre assistentes de inteligência artificial (como Antigravity, Claude Desktop ou Cursor) e a base de dados PostgreSQL/pgvector gerenciada pelo pipeline RAG.

Com este conector, o Agente de IA ganha a ferramenta (tool) necessária para inspecionar, auditar e recuperar trechos de notas fiscais diretamente da tabela `rag_chunks`.

---

## 🏗️ Arquitetura

```
[ Agente de IA (Antigravity) ]
            │
            │ (stdio / MCP Protocol)
            ▼
[ Servidor MCP Local (server.py) ]
            │
            │ (Conexão Direta / psycopg2)
            ▼
[ Banco Supabase PostgreSQL ]
            └── Tabela: rag_chunks (Documentos RAG)
```

---

## 📂 Estrutura de Arquivos

```text
mcp-supabase-server/
├── .venv/               # Ambiente virtual Python isolado
├── .env                 # Credenciais de conexão (ignorado pelo git)
├── .env.example         # Exemplo de configuração das variáveis
├── .gitignore           # Filtro de arquivos sensíveis e temporários
├── server.py            # Servidor FastMCP com a ferramenta de consulta
└── README.md            # Documentação do projeto
```

---

## ⚙️ Pré-requisitos

1. **Python 3.10+** instalado.
2. Projeto RAG configurado com tabelas criadas no **Supabase**.
3. String de conexão PostgreSQL do Supabase (`postgresql://...`).

---

## 🚀 Instalação e Configuração

### 1. Criar e Ativar o Ambiente Virtual

No diretório do projeto:

**No Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**No Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar Dependências

Com a `.venv` ativada, execute:

```bash
python -m pip install -r requeriments.txt
python -m pip install "mcp<2"
```

> ⚠️ **Importante:** Este projeto usa a API `mcp.server.fastmcp` da versão 1.x do pacote `mcp`. A versão 2.x mudou a API e quebra a importação do arquivo `server.py`.

### 3. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com a string de conexão direta do Supabase (sem `?pgbouncer=true` para uso com `psycopg2`):

```env
DATABASE_URL=postgresql://postgres.SEU_PROJETO:SUA_SENHA@SEU_HOST:PORT/postgres
```

Se você tiver uma URL do pooler do Supabase com `?pgbouncer=true`, prefira usar a string direta do session-mode ou a URL sem esse parâmetro para evitar problemas na conexão.

### 4. Executar o servidor MCP

Na raiz do projeto, com a `.venv` ativada:

```bash
python server.py
```

Esse comando inicia o servidor MCP em modo `stdio`, pronto para ser registrado em clientes como Antigravity, Cursor ou Claude Desktop.

---

## 🛠️ Ferramentas Disponíveis no MCP

| Ferramenta | Descrição | Parâmetros |
| :--- | :--- | :--- |
| `listar_chunks_rag` | Consulta trechos de notas fiscais armazenados no Supabase | `limite` (int, padrão: 3) |

---

## 🔌 Conexão com o Antigravity / Clientes MCP

Para registrar este servidor no cliente MCP (ex.: no arquivo `settings.json` do VS Code / Antigravity), use um trecho como este:

```json
{
  "antigravity.mcpServers": {
    "mcp-supabase": {
      "command": "C:\\Users\\SEU_USUARIO\\Documents\\MCP\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\SEU_USUARIO\\Documents\\MCP\\server.py"
      ]
    }
  }
}
```

Exemplo real com o diretório atual do projeto:

```json
{
  "antigravity.mcpServers": {
    "mcp-supabase": {
      "command": "C:\\Users\\hannowermonteiro0649\\Documents\\MCP\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\hannowermonteiro0649\\Documents\\MCP\\server.py"
      ]
    }
  }
}
```

> **Dica:** No Windows, use barras duplas (`\\`) nos caminhos do JSON. Se o cliente exigir uma chave diferente, mantenha o mesmo `command` e `args` do servidor local.

---

## 💬 Exemplo de Uso com o Agente

Após recarregar o cliente com o servidor registrado, você pode solicitar ao Agente:

> *"Use a ferramenta `listar_chunks_rag` para verificar quais notas fiscais e itens estão registrados no banco do Supabase."*