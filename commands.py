from cmath import log
from faulthandler import disable
from tkinter import *
from tkinter.ttk import Treeview
from tkinter.filedialog import asksaveasfilename, askopenfilename
from lexicalStep import lexicalStep
from syntacticStep import syntacticStep

i = 1
idTabela = 0
scrollState = tuple()
application = Tk()

application.title('Compilador')
filePath = ''

superWrapper = Frame(application)

codeOutputFrame = Frame(superWrapper)
codeOutputFrame.pack(side=RIGHT)
codeOutput = Treeview(codeOutputFrame, height=40)
codeOutput['columns'] = ('value', 'key_name', 'key_id', 'line_id')
codeOutput.column("#0", width=0,  stretch=NO)
codeOutput.column("value",anchor=CENTER, width=130)
codeOutput.column("key_name",anchor=CENTER,width=130)
codeOutput.column("key_id",anchor=CENTER,width=130)
codeOutput.column("line_id",anchor=CENTER,width=130)

codeOutput.heading("#0",text="",anchor=CENTER)
codeOutput.heading("value",text="Valor digitado",anchor=CENTER)
codeOutput.heading("key_name",text="Token",anchor=CENTER)
codeOutput.heading("key_id",text="Código do token",anchor=CENTER)
codeOutput.heading("line_id",text="Linha",anchor=CENTER)

wrapper = Frame(superWrapper)

text_scroll = Scrollbar(wrapper)
text_scroll.pack(side=RIGHT, fill=Y)

editor = Text(wrapper, height=40, yscrollcommand=text_scroll.set)
console = Text(superWrapper, height=5, bg = 'black', fg="green") 
lineNumbers = Text(wrapper, height=40, width=3, yscrollcommand=text_scroll.set)
lineNumbers.pack(side=LEFT)

def multipleYview(*args):
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

def disable(*args):
    return 'break'

text_scroll.config(command=multipleYview)

editor.bind('<MouseWheel>', disable)
editor.bind('<Any-KeyPress>', createLineNumber)
lineNumbers.bind('<MouseWheel>', disable)

superWrapper.pack()
editor.pack(side=LEFT)
wrapper.pack()

def setPath(path):
    global filePath 
    filePath = path

def start ():
    createLineNumber()

    idOutput = 0
    y = 0
    if codeOutput.get_children():
        x = codeOutput.get_children()
        for item in x:
            codeOutput.delete(item)
    if filePath == '':
        warning = Toplevel()
        text = Label(warning, text="Você deve salvar antes de começar")
        text.pack()
        return
    
    output = lexicalStep(filePath)
    
    for outputType in output:
        splitedValues = outputType.split("%%%%")
        codeOutput.insert(parent='', index='end', iid=idOutput, text='',
        values=(splitedValues[0], splitedValues[1], splitedValues[2], splitedValues[3]))
        y = y + 1
        idOutput = idOutput + 1
    codeOutput.pack()

    console.delete('1.0', END)
    try:
        syntacticStep(output)
        console.insert('1.0', 'Sucesso!')
    except Exception as valueError:
        console.insert('1.0', valueError)
    console.pack(fill=X)


def save():
    if filePath == '':
        path = asksaveasfilename(filetypes=[('Text Document', '*.txt')])
        setPath(path)
    else: 
        path = filePath

    updated_file = open(path, 'w')
    updated_file.write(editor.get('1.0', END))

def openFile():
    path = askopenfilename(filetypes=[('Text Document', '*.txt')])
    openedFile = open(path, 'r')
    editor.delete('1.0', END)
    editor.insert('1.0', openedFile.read())
    createLineNumber()

    setPath(path)

