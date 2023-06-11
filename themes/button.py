import tkinter.ttk
def new_board():
    # TODO экран создания доски (или можно его встроить во вкладку "+")
#        DataBace.createNewDesk(name)
    window = tkinter.Toplevel()
    window.title("settings")
    window.minsize(640, 480)
    window.grab_set()
    window.columnconfigure(index=0, weight=1)
    window.columnconfigure(index=1, weight=1)
    entry = tkinter.ttk.Entry(window)
    entry.grid(row=0, column=0)
    btn = tkinter.ttk.Button(window, text="Enter", command=insert())
    btn.grid(row=0, column=1)

def insert(entry):
    name = entry.get()
    if name != None:
        print("Создание новой доски")
#         Board(self.notebook, 1, name)
if __name__ == "__main__":
    # Главное окно
    root_window = tkinter.Tk()
    new_board()
    root_window.mainloop()