import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Simulação de banco de dados de usuários
usuarios = {
    "admin": {"senha": "admin123", "cargo": "Admin"},
    "user1": {"senha": "password1", "cargo": "User"},
}

# Dados de exemplo de funcionários
funcionarios = {
    "001": {"nome": "Alice", "cargo": "Engenheira"},
    "002": {"nome": "Bob", "cargo": "Técnico"},
    "003": {"nome": "Carlos", "cargo": "Operador"}
}

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Treinamentos")
        self.root.geometry("600x400")
        self.current_user = None
        self.trainings = {}

        self.show_login_screen()

    def show_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Usuário:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Senha:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)

    def show_main_screen(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Bem-vindo, {self.current_user}").pack(pady=10)

        tk.Button(self.root, text="Gerenciar Funcionários", command=self.show_employee_management).pack(pady=5)
        tk.Button(self.root, text="Gerenciar Treinamentos", command=self.show_training_management).pack(pady=5)
        
        if usuarios[self.current_user]["cargo"] == "Admin":
            tk.Button(self.root, text="Cadastrar Usuário", command=self.show_register_user_screen).pack(pady=5)
        tk.Button(self.root, text="Sair", command=self.show_login_screen).pack(pady=5)


    def show_register_user_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Novo Usuário:").pack(pady=5)
        self.new_username_entry = tk.Entry(self.root)
        self.new_username_entry.pack(pady=5)

        tk.Label(self.root, text="Senha:").pack(pady=5)
        self.new_password_entry = tk.Entry(self.root, show="*")
        self.new_password_entry.pack(pady=5)

        tk.Label(self.root, text="Cargo:").pack(pady=5)
        self.new_cargo_entry = tk.Entry(self.root)
        self.new_cargo_entry.pack(pady=5)

        tk.Button(self.root, text="Cadastrar", command=self.register_user).pack(pady=10)
        tk.Button(self.root, text="Voltar", command=self.show_main_screen).pack(pady=5)

        
    def show_employee_management(self):
        self.clear_screen()

        tk.Label(self.root, text="Gerenciamento de Funcionários").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.root, text="Nome:").grid(row=1, column=0, padx=10, pady=10)
        self.nome_entry = tk.Entry(self.root)
        self.nome_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Cargo:").grid(row=2, column=0, padx=10, pady=10)
        self.cargo_entry = tk.Entry(self.root)
        self.cargo_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.root, text="ID do Funcionário:").grid(row=3, column=0, padx=10, pady=10)
        self.id_entry = tk.Entry(self.root)
        self.id_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Adicionar Funcionário", command=self.add_employee).grid(row=4, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Nome", "Cargo", "ID"), show='headings')
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Cargo", text="Cargo")
        self.tree.heading("ID", text="ID do Funcionário")
        self.tree.grid(row=5, column=0, columnspan=2, pady=10)
        self.load_employees()

        tk.Button(self.root, text="Voltar", command=self.show_main_screen).grid(row=6, column=0, columnspan=2, pady=10)

    def show_training_management(self):
        self.clear_screen()

        tk.Label(self.root, text="Selecionar Funcionário:").grid(row=0, column=0, padx=10, pady=10)
        self.funcionario_combobox = ttk.Combobox(self.root)
        self.funcionario_combobox['values'] = list(funcionarios.keys())
        self.funcionario_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.funcionario_combobox.bind("<<ComboboxSelected>>", self.update_employee_info)

        self.funcionario_info_label = tk.Label(self.root, text="")
        self.funcionario_info_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(self.root, text="Treinamento:").grid(row=2, column=0, padx=10, pady=10)
        self.treinamento_entry = tk.Entry(self.root)
        self.treinamento_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Validade (dd/mm/yyyy):").grid(row=3, column=0, padx=10, pady=10)
        self.validade_entry = tk.Entry(self.root)
        self.validade_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Adicionar/Atualizar Treinamento", command=self.add_update_training).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Deletar Treinamento", command=self.delete_training).grid(row=5, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Treinamento", "Validade"), show='headings')
        self.tree.heading("Treinamento", text="Treinamento")
        self.tree.heading("Validade", text="Validade")
        self.tree.grid(row=6, column=0, columnspan=2, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        tk.Button(self.root, text="Voltar", command=self.show_main_screen).grid(row=7, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in usuarios and usuarios[username]["senha"] == password:
            self.current_user = username
            self.show_main_screen()
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha incorretos")

    def register_user(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        new_cargo = self.new_cargo_entry.get()

        if new_username in usuarios:
            messagebox.showerror("Erro", "Usuário já existe")
        elif not new_username or not new_password or not new_cargo:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios")
        else:
            usuarios[new_username] = {"senha": new_password, "cargo": new_cargo}
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso")
            self.show_main_screen()

    def add_employee(self):
        nome = self.nome_entry.get()
        cargo = self.cargo_entry.get()
        emp_id = self.id_entry.get()

        if not nome or not cargo or not emp_id:
            messagebox.showwarning("Entrada Inválida", "Todos os campos são obrigatórios.")
            return

        if emp_id in funcionarios:
            messagebox.showerror("Erro", "ID de funcionário já existe.")
            return

        funcionarios[emp_id] = {"nome": nome, "cargo": cargo}
        self.load_employees()
        self.clear_employee_entries()

    def load_employees(self):
        self.tree.delete(*self.tree.get_children())
        for emp_id, info in funcionarios.items():
            self.tree.insert("", "end", values=(info["nome"], info["cargo"], emp_id))

    def clear_employee_entries(self):
        self.nome_entry.delete(0, tk.END)
        self.cargo_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)

    def update_employee_info(self, event):
        emp_id = self.funcionario_combobox.get()
        if emp_id in funcionarios:
            info = funcionarios[emp_id]
            self.funcionario_info_label.config(text=f"Nome: {info['nome']}, Cargo: {info['cargo']}")
            self.load_trainings(emp_id)
        else:
            self.funcionario_info_label.config(text="")
            self.tree.delete(*self.tree.get_children())

    def load_trainings(self, emp_id):
        self.tree.delete(*self.tree.get_children())
        for training in self.trainings.get(emp_id, []):
            self.tree.insert("", "end", values=training)

    def add_update_training(self):
        emp_id = self.funcionario_combobox.get()
        treinamento = self.treinamento_entry.get()
        validade = self.validade_entry.get()

        if not emp_id or not treinamento or not validade:
            messagebox.showwarning("Entrada Inválida", "Todos os campos são obrigatórios.")
            return

        try:
            validade_date = datetime.strptime(validade, "%d/%m/%Y")
        except ValueError:
            messagebox.showwarning("Entrada Inválida", "A validade deve estar no formato dd/mm/yyyy.")
            return

        if emp_id not in self.trainings:
            self.trainings[emp_id] = []

        for i, (t, v) in enumerate(self.trainings[emp_id]):
            if t == treinamento:
                self.trainings[emp_id][i] = (treinamento, validade)
                break
        else:
            self.trainings[emp_id].append((treinamento, validade))

        self.load_trainings(emp_id)
        self.clear_training_entries()

    def delete_training(self):
        emp_id = self.funcionario_combobox.get()
        selected_item = self.tree.selection()

        if not emp_id or not selected_item:
            messagebox.showwarning("Seleção Inválida", "Selecione um treinamento para deletar.")
            return

        training_values = self.tree.item(selected_item[0], "values")
        self.trainings[emp_id] = [t for t in self.trainings[emp_id] if t != training_values]

        self.load_trainings(emp_id)

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            training_values = self.tree.item(selected_item[0], "values")
            self.treinamento_entry.delete(0, tk.END)
            self.treinamento_entry.insert(0, training_values[0])
            self.validade_entry.delete(0, tk.END)
            self.validade_entry.insert(0, training_values[1])

    def clear_training_entries(self):
        self.treinamento_entry.delete(0, tk.END)
        self.validade_entry.delete(0, tk.END)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
