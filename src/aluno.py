class Aluno:
    def __init__(self, nome, cpf, data_nascimento, status):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.status = status

    def __repr__(self):
        return f"Aluno(nome='{self.nome}', cpf='{self.cpf}',data_nascimento='{self.data_nascimento}', status='{self.status}')"
