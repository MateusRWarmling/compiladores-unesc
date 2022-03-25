from commands import *

menu = Menu(application)
menu.add_command(label='Abrir arquivo', command=open_file)
menu.add_command(label='Salvar', command=save)
menu.add_command(label='Começar', command=start)

application.config(menu=menu)
application.mainloop()
