import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from crud import create_aluno, read_alunos, update_aluno, delete_aluno

import tkinter as tk
from tkinter import ttk, messagebox
from crud import create_aluno, read_alunos, update_aluno, delete_aluno


def criar_janela_principal():
    janela = tk.Tk()
    janela.title("Sistema de Alunos")
    janela.geometry("600x500")
    janela.configure(bg="#f0f0f0")

    
    tk.Label(janela, text="Nome:").pack()
    entrada_nome = tk.Entry(janela, width=40)
    entrada_nome.pack(pady=3)

    tk.Label(janela, text="CPF:").pack()
    entrada_cpf = tk.Entry(janela, width=40)
    entrada_cpf.pack(pady=3)

    tk.Label(janela, text="Data de Nascimento:").pack()
    dta_nascimento = tk.Entry(janela, width=40)
    dta_nascimento.pack(pady=3)

    tk.Label(janela, text="Status:").pack()
    entrada_status = tk.Entry(janela, width=40)
    entrada_status.pack(pady=3)

   
    colunas = ("id", "nome", "cpf", "data_nascimento", "status")
    tabela = ttk.Treeview(janela, columns=colunas, show="headings", height=10)

    for c in colunas:
        tabela.heading(c, text=c.title())
        tabela.column(c, width=120 if c != "id" else 60, anchor="center")

    tabela.pack(pady=10, fill="both", expand=True)


    def limpar_campos():
        entrada_nome.delete(0, tk.END)
        entrada_cpf.delete(0, tk.END)
        dta_nascimento.delete(0, tk.END)
        entrada_status.delete(0, tk.END)

    def carregar_lista():
        for item in tabela.get_children():
            tabela.delete(item)
        try:
            for a in read_alunos():  
                tabela.insert("", "end", values=(a[0], a[1], a[2], a[3], a[4]))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar lista: {e}")

    def cadastrar():
        nome = entrada_nome.get().strip()
        cpf = entrada_cpf.get().strip()
        data = dta_nascimento.get().strip()
        status = entrada_status.get().strip()
        if not (nome and cpf and data and status):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return
        try:
            create_aluno(nome, cpf, data, status)
            messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
            carregar_lista()
            limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível cadastrar: {e}")

    def atualizar():
        cpf = entrada_cpf.get().strip()
        novo_status = entrada_status.get().strip()
        if not cpf or not novo_status:
            messagebox.showerror("Erro", "Informe CPF e novo status.")
            return
        try:
            linhas = update_aluno(cpf, {"status": novo_status})  
            if not linhas:
                messagebox.showwarning("Aviso", "Nenhum registro atualizado. Verifique o CPF.")
            else:
                messagebox.showinfo("Sucesso", "Status atualizado!")
            carregar_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível atualizar: {e}")

    def excluir():
        cpf = entrada_cpf.get().strip()
        if not cpf:
            messagebox.showerror("Erro", "Informe o CPF para excluir.")
            return
        try:
            linhas = delete_aluno(cpf)  
            if not linhas:
                messagebox.showwarning("Aviso", "Nenhum registro excluído. Verifique o CPF.")
            else:
                messagebox.showinfo("Sucesso", "Aluno excluído!")
            carregar_lista()
            limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível excluir: {e}")

    
    tk.Button(janela, text="Cadastrar", width=15, bg="#4CAF50", fg="white",
              command=cadastrar).pack(pady=5)
    tk.Button(janela, text="Atualizar", width=15, bg="#2196F3", fg="white",
              command=atualizar).pack(pady=5)
    tk.Button(janela, text="Excluir", width=15, bg="#f44336", fg="white",
              command=excluir).pack(pady=5)
    tk.Button(janela, text="Consultar", width=15, bg="#9C27B0", fg="white",
              command=carregar_lista).pack(pady=5)

    carregar_lista()

    janela.mainloop()


if __name__ == "__main__":
    criar_janela_principal()


#Tela do Relatorio

class TelaRelatorio(tk.Tk):
    """Janela principal de relatórios de alunos, com filtros e tabela Treeview."""
    def __init__(self):
        super().__init__()
        self.title("Relatórios de Alunos")
        self.geometry("750x450")
        self.configure(bg="#f0f0f0")

        
        self.var_somente_ativos = tk.BooleanVar()
        self.ent_busca_nome = None
        self.tree = None

       
        self._build()

    # --------------------------------------------------------------------------
    def _build(self):
        """Monta todos os elementos da interface."""
        ttk.Label(self, text="Relatórios de Alunos", font=("Arial", 16, "bold")).pack(pady=8)

        self._build_barra_filtros()
        self._build_tabela()
        self._carregar_relatorio()

    # --------------------------------------------------------------------------
    def _build_barra_filtros(self):
        """Cria a barra de filtros e botões de ação."""
        barra = tk.Frame(self, bg="#f0f0f0")
        barra.pack(fill="x", pady=5)

        tk.Label(barra, text="Buscar por nome:", bg="#f0f0f0").pack(side="left", padx=(10, 6))
        self.ent_busca_nome = tk.Entry(barra, width=30)
        self.ent_busca_nome.pack(side="left")

        tk.Checkbutton(barra, text="Somente Ativos",
                       bg="#f0f0f0",
                       variable=self.var_somente_ativos).pack(side="left", padx=10)

        ttk.Button(barra, text="Buscar", command=self._carregar_relatorio).pack(side="left", padx=5)
        ttk.Button(barra, text="Limpar Filtros", command=self._limpar_filtros).pack(side="left", padx=5)
        ttk.Button(barra, text="Atualizar", command=self._carregar_relatorio).pack(side="left", padx=5)

    # --------------------------------------------------------------------------
    def _build_tabela(self):
        """Cria e configura a tabela Treeview."""
        cols = ("id", "nome", "cpf", "data_nascimento", "status")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("data_nascimento", text="Nascimento")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("nome", width=200, anchor="w")
        self.tree.column("cpf", width=140, anchor="center")
        self.tree.column("data_nascimento", width=120, anchor="center")
        self.tree.column("status", width=100, anchor="center")

    # --------------------------------------------------------------------------
    def _aplicar_filtros(self, alunos):
        """Filtra os alunos pelo nome e status ativo."""
        nome_busca = self.ent_busca_nome.get().strip().lower()
        somente_ativos = self.var_somente_ativos.get()
        if nome_busca:
            alunos = [a for a in alunos if nome_busca in (a[1] or "").lower()]

        if somente_ativos:
            alunos = [a for a in alunos if (a[4] or "").strip().lower() == "ativo"]

        return alunos

    # --------------------------------------------------------------------------
    def _carregar_relatorio(self):
        """Limpa e carrega a tabela com base nos filtros aplicados."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            alunos = read_alunos() 
            alunos_filtrados = self._aplicar_filtros(alunos)

            if not alunos_filtrados:
                messagebox.showinfo("Relatório", "Nenhum registro encontrado com os filtros aplicados.")

            for a in alunos_filtrados:
                self.tree.insert("", "end", values=(a[0], a[1], a[2], a[3], a[4]))
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar relatório: {e}")

    # --------------------------------------------------------------------------
    def _limpar_filtros(self):
        """Limpa os campos de filtro e recarrega todos os registros."""
        self.ent_busca_nome.delete(0, tk.END)
        self.var_somente_ativos.set(False)
        self._carregar_relatorio()


# --------------------------------------------------------------------------
if __name__ == "__main__":
    app = TelaRelatorio()
    app.mainloop()
