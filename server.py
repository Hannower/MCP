import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

# Substitua pela sua string de conexão real do Supabase
DATABASE_URL = os.getenv("DATABASE_URL");

# Inicializa o servidor MCP
mcp = FastMCP("SupabaseRAG")

@mcp.tool()
def listar_chunks_rag(limite: int = 3) -> str:
    """Consulte esta ferramenta para ler os trechos de documentos (chunks) armazenados no banco de dados do Supabase."""
    try:
        # Estabelece conexão direta com o PostgreSQL do Supabase
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Busca amostras na tabela que foi populada pela ingestão
        cursor.execute("SELECT * FROM rag_chunks LIMIT %s;", (limite,))
        linhas = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if not linhas:
            return "A tabela rag_chunks está vazia ou não foi encontrada."
            
        resultado = "Dados encontrados no Supabase:\n\n"
        for linha in linhas:
            resultado += f"{str(linha)}\n---\n"
            
        return resultado
        
    except Exception as e:
        return f"Erro de conexão com o banco de dados: {str(e)}"

if __name__ == "__main__":
    # O Antigravity se comunicará com este servidor via entrada e saída padrão (stdio)
    mcp.run_stdio_async()