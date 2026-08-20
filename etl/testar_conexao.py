from sqlalchemy import text

from conexao import criar_engine


engine = criar_engine()

with engine.connect() as conexao:
    banco_atual = conexao.execute(
        text("SELECT current_database()")
    ).scalar_one()

    tabela_encontrada = conexao.execute(
        text(
            "SELECT to_regclass("
            "'staging.resultados_financeiros'"
            ")"
        )
    ).scalar_one()

print(f"Conexão realizada com o banco: {banco_atual}")
print(f"Tabela encontrada: {tabela_encontrada}")