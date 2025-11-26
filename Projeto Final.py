import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter


def conectar():
    return sqlite3.connect('banco.db')


def criar_tabela():
    co = conectar()
    c = co.cursor()
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS usuarios(
            cpf TEXT,
            nome TEXT,
            email TEXT,
            telefone TEXT
        )   
    ''')
    co.commit()
    co.close()


def inserir_usuario():
    cpf = CPF_entry.get()
    nome = nome_entry.get()
    email = email_entry.get()
    telefone = telefone_entry.get()

    if cpf and nome and email and telefone:
        co = conectar()
        c = co.cursor()
        c.execute("INSERT INTO usuarios VALUES(?,?,?,?)", 
                  (cpf, nome, email, telefone))
        co.commit()
        co.close()
        messagebox.showinfo('', 'DADOS INSERIDOS COM SUCESSO!')
        mostrar_usuario()
    else:
        messagebox.showwarning('', 'INSIRA OS DADOS SOLICITADOS')


def mostrar_usuario():
    for row in tree.get_children():
        tree.delete(row)

    co = conectar()
    c = co.cursor()
    c.execute('SELECT * FROM usuarios')
    usuarios = c.fetchall()

    for us in usuarios:
        tree.insert("", "end", values=(us[0], us[1], us[2], us[3]))

    co.close()


def atualizar():
    selecao = tree.selection()
    if selecao:
        cpf_original = tree.item(selecao)['values'][0]

        novo_cpf = CPF_entry.get()
        novo_nome = nome_entry.get()
        novo_email = email_entry.get()
        novo_telefone = telefone_entry.get()

        if novo_cpf and novo_nome and novo_email and novo_telefone:
            co = conectar()
            c = co.cursor()
            c.execute("""
                UPDATE usuarios 
                SET cpf=?, nome=?, email=?, telefone=? 
                WHERE cpf=?
            """, (novo_cpf, novo_nome, novo_email, novo_telefone, cpf_original))
            co.commit()
            co.close()

            messagebox.showinfo('', 'DADOS ATUALIZADOS COM SUCESSO!')
            mostrar_usuario()
        else:
            messagebox.showwarning('', 'TODOS OS DADOS PRECISAM SER PREENCHIDOS')
    else:
        messagebox.showwarning('', 'SELECIONE UM ITEM PARA ATUALIZAR')


def delete_usuario():
    selecao = tree.selection()
    if selecao:
        cpf_del = tree.item(selecao)['values'][0]
        co = conectar()
        c = co.cursor()
        c.execute("DELETE FROM usuarios WHERE cpf = ?", (cpf_del,))
        co.commit()
        co.close()
        messagebox.showinfo('', 'DADO DELETADO COM SUCESSO')
        mostrar_usuario()
    else:
        messagebox.showerror('', 'SELECIONE UM ITEM PARA DELETAR')

def consultar():
    termo = consulta_entry.get()

    if not termo:
        messagebox.showwarning("", "DIGITE ALGO PARA CONSULTAR")
        return

    for row in tree.get_children():
        tree.delete(row)

    co = conectar()
    c = co.cursor()

    c.execute("""
        SELECT * FROM usuarios 
        WHERE cpf LIKE ? OR nome LIKE ?
    """, (f"%{termo}%", f"%{termo}%"))

    resultados = c.fetchall()
    co.close()

    for r in resultados:
        tree.insert("", "end", values=(r[0], r[1], r[2], r[3]))

    if len(resultados) == 0:
        messagebox.showinfo("", "Nenhum registro encontrado")


janela = tk.Tk()
janela.title('Cadastro de Novos Clientes')
janela.geometry('900x930')
janela.configure(bg='gray')

caminho = 'ico.ico'
janela.iconbitmap(caminho)

tk.Label(janela, text='Cadastro', font=('arial', 15),
         bg='gray', fg='white').grid(row=0, column=0, pady=10, padx=10)

fr0 = tk.Frame(janela,bg='gray')
fr0.grid(columnspan=3)

CPF_label = tk.Label(fr0, text='CPF', font=('arial', 15), bg='gray', fg='white')
CPF_label.grid(row=1, column=4, pady=10, padx=10)

CPF_entry = tk.Entry(fr0, font=('arial', 15), bg='gray')
CPF_entry.grid(row=1, column=5, pady=10, padx=10)

nome_label = tk.Label(fr0, text='Nome', font=('arial', 15), bg='gray', fg='white')
nome_label.grid(row=2, column=4, pady=10, padx=10)

nome_entry = tk.Entry(fr0, font=('arial', 15), bg='gray')
nome_entry.grid(row=2, column=5, pady=10, padx=10)

email_label = tk.Label(fr0, text='E-mail', font=('arial', 15), bg='gray', fg='white')
email_label.grid(row=3, column=4, pady=10, padx=10)

email_entry = tk.Entry(fr0, font=('arial', 15), bg='gray')
email_entry.grid(row=3, column=5, pady=10, padx=10)

telefone_label = tk.Label(fr0, text='Telefone', font=('arial', 15), bg='gray', fg='white')
telefone_label.grid(row=4, column=4, pady=10, padx=10)

telefone_entry = tk.Entry(fr0, font=('arial', 15), bg='gray')
telefone_entry.grid(row=4, column=5, pady=10, padx=10)

fr = tk.Frame(janela,bg='gray')
fr.grid(padx=10, columnspan=3)

btn_salvar = tk.Button(fr, text='SALVAR', font=('arial', 15),
                       bg='blue', fg='white',
                         command=inserir_usuario)
btn_salvar.grid(row=5, column=0, padx=10, pady=10)

btn_atualizar = tk.Button(fr, text='ATUALIZAR', font=('arial', 15),
                          bg='blue', fg='white',
                            command=atualizar)
btn_atualizar.grid(row=5, column=2, padx=10, pady=10)

btn_delete = tk.Button(fr, text='DELETAR', font=('arial', 15),
                       bg='blue', fg='white',
                         command=delete_usuario)
btn_delete.grid(row=5, column=3, padx=10, pady=10)

fr_consulta = tk.Frame(janela, bg='gray')
fr_consulta.grid(row=0, column=1, padx=10)


tk.Label(fr_consulta, text="Consultar:", font=('arial', 12),
         bg='gray', fg='white').grid(row=0, column=0)


consulta_entry = tk.Entry(fr_consulta, font=('arial', 12),bg='gray')
consulta_entry.grid(row=0, column=1, padx=10)

btn_consultar = tk.Button(fr_consulta, text="BUSCAR", font=('arial', 12),
                          bg='blue', fg='white',
                            command=consultar)
btn_consultar.grid(row=0, column=2, padx=0)

fr2 = tk.Frame(janela, bg='gray')
fr2.grid(columnspan=3)

colunas = ('CPF', 'NOME', 'E-MAIL', 'TELEFONE')
tree = ttk.Treeview(fr2, columns=colunas, show='headings', height=15)
tree.grid(row=0, column=1, padx=40, pady= 10, sticky='nsew')

for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER)

criar_tabela()
mostrar_usuario()

janela.mainloop()