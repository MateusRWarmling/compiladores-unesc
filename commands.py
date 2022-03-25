from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
from get_output import generate_output

application = Tk()
application.title('Compilador')
file_path = ''
editor = Text()
editor.pack()

def set_path(path):
    global file_path 
    file_path = path

def start ():
    if file_path == '':
        warning = Toplevel()
        text = Label(warning, text="Você deve salvar antes de começar")
        text.pack()
        return
    output = generate_output(file_path)
    code_output = Text(height=7)
    code_output.pack()
    for output_type in output:
        code_output.insert(END, output_type + '\n')

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
    set_path(path)

