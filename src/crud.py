import sqlite3
from banco import get_connection

# CREATE 
def create_aluno(aluno):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO alunos (nome, cpf, data_nascimento, status)
        VALUES (?, ?, ?, ?)
    """, (aluno.nome, aluno.cpf, aluno.data_nascimento, aluno.status))
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return novo_id

def read_alunos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alunos")
    alunos = cursor.fetchall()
    conn.close()
    return alunos


def read_aluno_by_id(aluno_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alunos WHERE id = ?", (aluno_id,))
    aluno = cursor.fetchone()
    conn.close()
    return aluno


def update_aluno(aluno_id, novos_dados):
    conn = get_connection()
    cursor = conn.cursor()

    campos = []
    valores = []
    for campo, valor in novos_dados.items():
        campos.append(f"{campo} = ?")
        valores.append(valor)

    valores.append(aluno_id)

    sql = f"UPDATE alunos SET {', '.join(campos)} WHERE id = ?"
    cursor.execute(sql, valores)
    conn.commit()
    conn.close()


def delete_aluno(aluno_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
    conn.commit()
    conn.close()


def read_alunos():
    return [
        (1, "Ana Silva", "123.456.789-00", "2000-01-10", "Ativo"),
        (2, "Bruno Costa", "987.654.321-00", "1999-06-25", "Inativo"),
        (3, "Carlos Lima", "555.111.222-33", "2001-09-13", "Ativo"),
    ]
