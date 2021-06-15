import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import tkinter.messagebox as msb
import sqlite3

root = Tk()
root.title("Minhas Notas")
width = 900
height = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.iconbitmap("C:/Python/AvaliacaoAV2/img/icone-nota.ico")
root.config(background="#3E3E62")

aluno = StringVar()
disciplina = StringVar()
av1 = IntVar()
av2 = IntVar()
avd = IntVar()
situacao = (int(avd.get() + int(av2.get() + int(avd.get())))) / 3
id = None
updateWindow = None
newWindow = None
newWindowSearch = None


def database():
    conn = sqlite3.connect("C:/Python/AvaliacaoAV2/database.bd")
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS 'notas' (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            aluno TEXT, disciplina TEXT, av1 INTEGER, av2 INTEGER , avd INTEGER) """
    cursor.execute(query)
    cursor.execute("SELECT * FROM 'notas' ORDER BY aluno")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()


def submitData():
    if aluno.get() == "" or disciplina.get() == "" or av1.get() == '' or av2.get() == '' or avd.get() == '':
        resultado = tk.messagebox.showwarning("AVISO", "Não deixe os campos vazios.", icon="warning")

    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("C:/Python/AvaliacaoAV2/database.bd")
        cursor = conn.cursor()
        query = """INSERT INTO 'notas' (aluno, disciplina, av1, av2, avd) VALUES (?, ?, ?, ?, ?)"""
        cursor.execute(query,
                       (str(aluno.get()), str(disciplina.get()), int(av1.get()), int(av2.get()),
                        int(avd.get())))
        conn.commit()
        cursor.execute("SELECT * FROM 'notas' ORDER BY aluno")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        aluno.set("")
        disciplina.set("")
        av1.set("")
        av2.set("")
        avd.set("")
        newWindow.destroy()


def updateData():
    tree.delete(*tree.get_children())
    conn = sqlite3.connect("C:/Python/AvaliacaoAV2/database.bd")
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE 'notas' SET aluno = ?, disciplina = ?, av1 = ?, av2 = ?, avd = ? WHERE id = ?""",
        (str(aluno.get()), str(disciplina.get()), int(av1.get()), int(av2.get()), int(avd.get()),
         int(id)))
    conn.commit()
    cursor.execute("SELECT * FROM 'notas' ORDER BY aluno ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()
    aluno.set("")
    disciplina.set("")
    av1.set("")
    av2.set("")
    avd.set("")
    updateWindow.destroy()


def deleteData():
    if not tree.selection():
        resultado = msb.showwarning(
            "EXCLUSÃO", "Por favor, selecione o item a ser deletado.", icon="warning")
    else:
        resultado = msb.askquestion("CONFIRMAÇÃO DE EXCLUSÃO",
                                    "Tem certeza que deseja deletar a disciplina selecionada?")
        if resultado == 'yes':
            selectItem = tree.focus()
            conteudo = (tree.item(selectItem))
            selectedItem = conteudo['values']
            tree.delete(selectItem)
            conn = sqlite3.connect("C:/Python/AvaliacaoAV2/database.bd")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM 'notas' WHERE id = %d" % selectedItem[0])
            conn.commit()
            cursor.close()
            conn.close()


def searchData():
    global aluno, newWindowSearch
    selectItem = tree.focus()
    conteudo = (tree.item(selectItem))
    conn = sqlite3.connect("C:/Python/AvaliacaoAV2/database.bd")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 'notas' WHERE id = 'aluno'")
    conn.commit()
    conn.close()

    newWindowSearch = Toplevel()
    newWindowSearch.title("Busca de Aluno")
    formTitleS = Frame(newWindowSearch)
    formTitleS.pack(side=TOP)
    formContactS = Frame(newWindowSearch)
    formContactS.pack(side=TOP, pady=10)
    width = 400
    height = 160
    screen_width = newWindowSearch.winfo_screenwidth()
    screen_height = newWindowSearch.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    newWindowSearch.geometry("%dx%d+%d+%d" % (width, height, x, y))
    newWindowSearch.resizable(0, 0)

    lbl_title = Label(formTitleS, text="Procurando por Aluno", font=('system', 24), bg='#3E3E62', width=300)
    lbl_title.pack(fill=X)
    lbl_aluno = Label(formContactS, text='Aluno', font=('arial', 12))
    lbl_aluno.grid(row=0, sticky=W)

    alunoEntry = Entry(formContactS, textvariable=aluno, font=('arial', 12))
    alunoEntry.grid(row=0, column=1)

    btn_searchcom = Button(formContactS, text="Buscar",
                           width=50, command=updateData)
    btn_searchcom.grid(row=6, columnspan=2, pady=50)


def onSelect(event):
    global id, updateWindow
    selectItem = tree.focus()
    conteudo = (tree.item(selectItem))
    selectedItem = conteudo['values']
    id = selectedItem[0]
    aluno.set("")
    disciplina.set("")
    av1.set("")
    av2.set("")
    avd.set("")
    aluno.set(selectedItem[1])
    disciplina.set(selectedItem[2])
    av1.set(selectedItem[3])
    av2.set(selectedItem[4])
    avd.set(selectedItem[5])

    updateWindow = Toplevel()
    updateWindow.title("Atualizando notas")
    formTitle = Frame(updateWindow)
    formTitle.pack(side=TOP)
    formContact = Frame(updateWindow)
    formContact.pack(side=TOP, pady=10)
    width = 400
    height = 300
    screen_width = updateWindow.winfo_screenwidth()
    screen_height = updateWindow.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    updateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    updateWindow.resizable(0, 0)

    lbl_title = Label(formTitle, text="Atualização da nota", font=('system', 24), bg='#3E3E62', width=300)
    lbl_title.pack(fill=X)
    lbl_aluno = Label(formContact, text='Aluno', font=('arial', 12))
    lbl_aluno.grid(row=0, sticky=W)
    lbl_disciplina = Label(formContact, text='Nome da disciplina', font=('arial', 12))
    lbl_disciplina.grid(row=1, sticky=W)
    lbl_av1 = Label(formContact, text='Nota da AV1', font=('arial', 12))
    lbl_av1.grid(row=2, sticky=W)
    lbl_av2 = Label(formContact, text='Nota da AV2', font=('arial', 12))
    lbl_av2.grid(row=3, sticky=W)
    lbl_avd = Label(formContact, text='Nota da AVD', font=('arial', 12))
    lbl_avd.grid(row=4, sticky=W)

    alunoEntry = Entry(formContact, textvariable=aluno, font=('arial', 12))
    alunoEntry.grid(row=0, column=1)
    disciplinaEntry = Entry(formContact, textvariable=disciplina, font=('arial', 12))
    disciplinaEntry.grid(row=1, column=1)
    av1Entry = Entry(formContact, textvariable=av1, font=('arial', 12))
    av1Entry.grid(row=2, column=1)
    av2Entry = Entry(formContact, textvariable=av2, font=('arial', 12))
    av2Entry.grid(row=3, column=1)
    avdEntry = Entry(formContact, textvariable=avd, font=('arial', 12))
    avdEntry.grid(row=4, column=1)

    btn_updatecom = Button(formContact, text="Atualizar",
                           width=50, command=updateData)
    btn_updatecom.grid(row=6, columnspan=2, pady=50)


def addData():
    global newWindow
    aluno.set("")
    disciplina.set("")
    av1.set("")
    av2.set("")
    avd.set("")

    newWindow = Toplevel()
    newWindow.title("Inclusão de Disciplina")
    formTitle = Frame(newWindow)
    formTitle.pack(side=TOP)
    formContact = Frame(newWindow)
    formContact.pack(side=TOP, pady=10)
    width = 400
    height = 230
    screen_width = newWindow.winfo_screenwidth()
    screen_height = newWindow.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    newWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    newWindow.resizable(0, 0)

    lbl_title = Label(formTitle, text="Nova Disciplina",
                      font=('system', 18), bg='#3E3E62', fg='white', width=300)
    lbl_title.pack(fill=X)
    lbl_aluno = Label(formContact, text='Aluno', font=('arial', 12))
    lbl_aluno.grid(row=0, sticky=W)
    lbl_disciplina = Label(formContact, text='Nome da disciplina', font=('arial', 12))
    lbl_disciplina.grid(row=1, sticky=W)
    lbl_av1 = Label(formContact, text='Nota da AV1', font=('arial', 12))
    lbl_av1.grid(row=2, sticky=W)
    lbl_av2 = Label(formContact, text='Nota da AV2', font=('arial', 12))
    lbl_av2.grid(row=3, sticky=W)
    lbl_avd = Label(formContact, text='Nota da AVD', font=('arial', 12))
    lbl_avd.grid(row=4, sticky=W)

    alunoEntry = Entry(formContact, textvariable=aluno, font=('arial', 12))
    alunoEntry.grid(row=0, column=1)
    disciplinaEntry = Entry(
        formContact, textvariable=disciplina, font=('arial', 12))
    disciplinaEntry.grid(row=1, column=1)
    av1Entry = Entry(formContact, textvariable=av1, font=('arial', 12))
    av1Entry.grid(row=2, column=1)
    av2Entry = Entry(formContact, textvariable=av2, font=('arial', 12))
    av2Entry.grid(row=3, column=1)
    avdEntry = Entry(
        formContact, textvariable=avd, font=('arial', 12))
    avdEntry.grid(row=4, column=1)

    btn_includecom = Button(formContact, text="Incluir",
                            width=50, command=submitData)
    btn_includecom.grid(row=6, columnspan=2, pady=10)


top = Frame(root, width=500, bd=1, relief=SOLID)
top.pack(side=TOP)
mid = Frame(root, width=500, bg="#3E3E62")
mid.pack(side=TOP)
midleft = Frame(mid, width=100)
midleft.pack(side=LEFT, pady=10)
midleftPadding = Frame(mid, width=350, bg="#3E3E62")
midleftPadding.pack(side=LEFT)
midright = Frame(mid, width=100)
midright.pack(side=RIGHT, pady=10)
bottom = Frame(root, width=200)
bottom.pack(side=BOTTOM)
tableMargin = Frame(root, width=500)
tableMargin.pack(side=TOP)

lbl_title = Label(top, text="MINHAS DISCIPLINAS E NOTAS", bg="#3E3E62", fg='white', font=('system', 26), width=500)
lbl_title.pack(fill=X)

lbl_alterar = Label(bottom, text="Basta um duplo-click para alterar os campos", font=('system', 22), fg='white',
                    bg="#3E3E62", width=200)
lbl_alterar.pack(fill=X)

bttn_add = Button(midleft, text="INCLUIR DISCIPLINA",
                  bg="cornflower blue", command=addData)
bttn_add.pack()

bttn_exclude = Button(midright, text="EXCLUIR DISCIPLINA",
                      bg="orange red", command=deleteData)
bttn_exclude.pack(side=RIGHT)

bttn_search = Button(midleftPadding, text="BUSCAR ALUNO",
                     bg="yellow", command=searchData)
bttn_search.pack(side=RIGHT)

scrollbarX = Scrollbar(tableMargin, orient=HORIZONTAL)
scrollbarY = Scrollbar(tableMargin, orient=VERTICAL)

tree = ttk.Treeview(tableMargin, columns=("ID", "Aluno", "Disciplina", "AV1", "AV2", "AVD", "Situação"),
                    height=400, selectmode="extended", yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
scrollbarX.config(command=tree.xview)
scrollbarX.pack(side=BOTTOM, fill=X)
scrollbarY.config(command=tree.yview)
scrollbarY.pack(side=RIGHT, fill=Y)

tree.heading("ID", text="ID", anchor=W)
tree.heading("Aluno", text="Aluno", anchor=W)
tree.heading("Disciplina", text="Disciplina", anchor=W)
tree.heading("AV1", text="AV1", anchor=W)
tree.heading("AV2", text="AV2", anchor=W)
tree.heading("AVD", text="AVD", anchor=W)
tree.heading("Situação", text="Situação", anchor=W)

tree.column('#0', stretch=NO, minwidth=0, width=10)
tree.column('#1', stretch=NO, minwidth=0, width=32)
tree.column('#2', stretch=NO, minwidth=0, width=200)
tree.column('#3', stretch=NO, minwidth=0, width=200)
tree.column('#4', stretch=NO, minwidth=0, width=60)
tree.column('#5', stretch=NO, minwidth=0, width=60)
tree.column('#6', stretch=NO, minwidth=0, width=60)
tree.pack()
tree.bind('<Double-Button-1>', onSelect)

if __name__ == '__main__':
    database()
    root.mainloop()