from cmath import log
from faulthandler import disable
from tkinter import *
from tkinter.ttk import Treeview
from tkinter.filedialog import asksaveasfilename, askopenfilename
from get_output import generate_output

i = 1
idTabela = 0
scrollState = tuple()
application = Tk()

application.title('Compilador')
file_path = ''

code_output_frame = Frame(application)
code_output_frame.pack(side=RIGHT)
code_output = Treeview(code_output_frame, height=25)
code_output['columns'] = ('value', 'key_name', 'key_id', 'line_id')
code_output.column("#0", width=0,  stretch=NO)
code_output.column("value",anchor=CENTER, width=130)
code_output.column("key_name",anchor=CENTER,width=130)
code_output.column("key_id",anchor=CENTER,width=130)
code_output.column("line_id",anchor=CENTER,width=130)

code_output.heading("#0",text="",anchor=CENTER)
code_output.heading("value",text="Valor digitado",anchor=CENTER)
code_output.heading("key_name",text="Token",anchor=CENTER)
code_output.heading("key_id",text="Código do token",anchor=CENTER)
code_output.heading("line_id",text="Linha",anchor=CENTER)

wrapper = Frame(application)

text_scroll = Scrollbar(wrapper)
text_scroll.pack(side=RIGHT, fill=Y)

editor = Text(wrapper, height=25, yscrollcommand=text_scroll.set) 
lineNumbers = Text(wrapper, height=25, width=3, yscrollcommand=text_scroll.set)
lineNumbers.pack(side=LEFT)

def multiple_yview(*args):
    print('ARG PADRAO:')
    print(*args)

    global scrollState
    scrollState = args
    editor.yview(*args)
    lineNumbers.yview(*args)

def createLineNumber(*args):
    lineNumbers.delete('1.0', END)

    totalLines = int(editor.index('end-1c').split('.')[0])
    for line in range(totalLines):
        lineNumbers.insert("end", line + 1)
        if(line != totalLines - 1):
            lineNumbers.insert("end", "\n")
    print('MUDANDO PARA TUPLE:')

def disable(*args):
    return 'break'

text_scroll.config(command=multiple_yview)

editor.bind('<MouseWheel>', disable)
editor.bind('<Any-KeyPress>', createLineNumber)
lineNumbers.bind('<MouseWheel>', disable)

editor.pack(side=LEFT)
wrapper.pack()

def set_path(path):
    global file_path 
    file_path = path

def start ():
    createLineNumber()

    idOutput = 0
    y = 0
    if code_output.get_children():
        x = code_output.get_children()
        for item in x:
            code_output.delete(item)
    if file_path == '':
        warning = Toplevel()
        text = Label(warning, text="Você deve salvar antes de começar")
        text.pack()
        return
    
    output = generate_output(file_path)
    
    for output_type in output:
        splitedValues = output_type.split("%%%%")
        code_output.insert(parent='', index='end', iid=idOutput, text='',
        values=(splitedValues[0], splitedValues[1], splitedValues[2], splitedValues[3]))
        y = y + 1
        idOutput = idOutput + 1
    code_output.pack()

def save():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Text Document', '*.txt')])
        set_path(path)
    else: 
        path = file_path

    updated_file = open(path, 'w')
    updated_file.write(editor.get('1.0', END))

def open_file():
    path = askopenfilename(filetypes=[('Text Document', '*.txt')])
    opened_file = open(path, 'r')
    editor.delete('1.0', END)
    editor.insert('1.0', opened_file.read())
    createLineNumber()

    set_path(path)

