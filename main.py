import tkinter, tkinter.font, tkinter.ttk
"""Предположил, что в БД хранятся Доска->Колонки, Колонка->Задачи, Задача->Инфа о задаче"""


class Settings:
    """Окно настроек, при вызове располагается поверх остальных и захватывает фокус"""
    def __init__(self):
        # Конфигурация окна
        self.window = tkinter.Toplevel()
        self.window.title("settings")
        self.window.minsize(640, 480)
        self.window.grab_set()
        # Выравнивание сетки
        self.window.columnconfigure(index=0, weight=1)
        self.window.columnconfigure(index=1, weight=1)
        # Кнопки
        tkinter.ttk.Label(self.window, text="App theme: ", font="text_font").grid(row=0, column=0)
        self.window.theme_combobox = tkinter.ttk.Combobox(self.window, values=themes, state="readonly",
                                                          font="text_font")
        self.window.theme_combobox.set(tkinter.ttk.Style().theme_use())
        self.window.theme_combobox.grid(row=0, column=1)
        self.window.theme_combobox.bind("<<ComboboxSelected>>", self.change_theme)
        # Закрытие
        self.window.protocol("WM_DELETE_WINDOW", self.close)

    def change_theme(self, event) -> None:
        """
        Меняет тему приложения
        :param event: ComboboxSelected event
        """
        theme = event.widget.get()
        if theme == "azure-dark":
            root_window.tk.call("set_theme", "dark")
        elif theme == "azure-light":
            root_window.tk.call("set_theme", "light")
        else:
            tkinter.ttk.Style().theme_use(theme)

    def close(self) -> None:
        """Удаляет окно, высвобаждая фокус"""
        self.window.grab_release()
        self.window.destroy()


class MainMenu:
    """Принимает меню и дополняет его элементами, создавая главное меню программы"""
    def __init__(self, main_menu):
        self.main_menu = main_menu
        # Файл
        self.menu = tkinter.Menu()
        self.menu.add_command(label="Настройки", command=Settings)  # Открывает новое меню с настройками
        self.main_menu.add_cascade(label="Файл", menu=self.menu)
        # Помощь
        self.main_menu.add_command(label="Помощь", command=self.menu_help)
        # О нас
        self.main_menu.add_command(label="Справка", command=self.menu_about)

    def menu_help(self) -> None:
        print("Clicked menu->help")

    def menu_about(self) -> None:
        print("Clicked menu->about")


class Card:
    """Карточка с заданием"""
    def __init__(self):
        pass


class Column:
    """Столбцы с задачами"""
    frame: tkinter.ttk.Frame

    def __init__(self, window, id):
        self.window = window
        self.frame = tkinter.ttk.Frame(window)
        # Кнопка
        tkinter.ttk.Button(self.frame, text="Добавить", command=self.add).grid(row=0)
        # Список
        self.listbox = tkinter.Listbox(self.frame, selectmode=tkinter.SINGLE)
        self.listbox.bind("<<ListboxSelect>>", self.select)
        for elem in ["a", "b", "c"]:  # TODO получение данных с БД
            self.listbox.insert(self.listbox.size(), elem)
        self.listbox.grid(row=1)
        # Выравнивание сетки
        self.frame.columnconfigure(index=0, weight=1)
        self.frame.rowconfigure(index=0, weight=2)
        self.frame.rowconfigure(index=1, weight=8)

    def select(self, event):
        index = event.widget.curselection()
        if len(index) != 0:
            print(f"Выбран {index[0]}")

    def add(self):
        print("Добавление задачи")


class Board:
    """Доска заданий, имеющая свои столбцы"""
    def __init__(self, notebook, board_id, add=False):
        self.notebook = notebook
        self.board_id = board_id
        if add:
            self.frame = tkinter.ttk.Frame(self.notebook, name="+")
            self.notebook.add(self.frame, text="+")
        else:
            self.frame = tkinter.ttk.Frame(self.notebook)
            # Добавление столбцов
            # TODO восстановление столбцов из БД
            self.columns = list()
            self.columns.append(Column(self.frame, 1))
            self.columns.append(Column(self.frame, 1))
            # TODO восстановление доски из БД
            self.text = "Доска"
            self.notebook.insert(self.notebook.index("end") - 1, self.frame, text=self.text)  # До должен быть frame "+"

            # Создание сетки
            self.number_of_rows = 3
            self.number_of_columns = len(self.columns)
            self.alignment()
            for i in range(len(self.columns)):
                self.columns[i].frame.grid(row=1, column=i)
            # Добавление кнопок управления
            self.frame_control = tkinter.ttk.Frame(self.frame)
            tkinter.ttk.Button(self.frame_control, text="Переименовать доску", command=self.rename).grid(row=0,
                                                                                                         column=0)
            tkinter.ttk.Button(self.frame_control, text="Удалить доску", command=self.delete).grid(row=0, column=1)
            tkinter.ttk.Button(self.frame_control, text="Добавить столбец", command=self.add_column).grid(row=0,
                                                                                                          column=2)
            self.frame_control.grid(row=0, column=0, columnspan=self.number_of_columns, sticky="nw")

    def alignment(self):
        """Выравнивание сетки для grid"""
        for c in range(self.number_of_columns):
            self.frame.columnconfigure(index=c, weight=1)
        for r in range(self.number_of_rows):
            self.frame.rowconfigure(index=r, weight=1)

    def add_column(self):
        print("Добавление столбца")
        self.alignment()

    def rename(self):
        print("Переименование доски")

    def delete(self):
        # TODO удаление из БД
        self.notebook.forget("current")


class MainScreen:
    def __init__(self, window):
        # Создание окна
        self.window = window
        self.main_frm = tkinter.ttk.Frame(self.window, padding=15)
        # Создание вкладок
        self.notebook = tkinter.ttk.Notebook(padding=5)
        # TODO проход по БД для восстановления досок
        Board(self.notebook, -1, add=tkinter.TRUE)
        Board(self.notebook, 1)
        Board(self.notebook, 1)
        self.notebook.select(0)
        self.notebook.bind("<<NotebookTabChanged>>", self.tab_changed)
        self.notebook.place(relx=0.5, rely=0.5, anchor="center", relheight=1.0, relwidth=1.0)

    def new_board(self):
        # TODO экран создания доски (или можно его встроить во вкладку "+")
        print("Создание новой доски")

    def tab_changed(self, event) -> None:
        if event.widget.select().endswith("+"):
            self.new_board()

    def show(self):
        """Отображает экран в окне"""
        self.main_frm.place(relx=0.5, rely=0.5, anchor="center", relheight=1.0, relwidth=1.0)


favicon_path = "favicon.png"

if __name__ == "__main__":
    # Главное окно
    root_window = tkinter.Tk()
    root_window.title("SuperApp")
    root_window.iconphoto(True, tkinter.PhotoImage(file=favicon_path))
    root_window.minsize(640, 480)
    # Темы
    root_window.tk.call("source", "themes/azure/azure.tcl")  # https://github.com/rdbende/Azure-ttk-theme
    root_window.tk.call("source", "themes/waldorf.tcl")  # https://wiki.tcl-lang.org/page/waldorf+ttk+theme
    root_window.tk.call("source", "themes/forest/forest-dark.tcl")  # https://github.com/rdbende/Forest-ttk-theme
    root_window.tk.call("source", "themes/forest/forest-light.tcl")  # https://github.com/rdbende/Forest-ttk-theme
    root_window.tk.call("source", "themes/breeze/breeze.tcl")  # https://github.com/MaxPerl/ttk-Breeze
    # Предустановки
    fonts = [tkinter.font.Font(root=root_window, name="text_font", family="Times", size=12, weight="normal"),
             tkinter.font.Font(root=root_window, name="header1_font", family="Times", size=18, weight="bold"),
             tkinter.font.Font(root=root_window, name="header2_font", family="Times", size=16, weight="normal"),
             tkinter.font.Font(root=root_window, name="header3_font", family="Times", size=14, weight="normal"),
             ]
    tkinter.ttk.Style().theme_use("clam")
    themes = [theme for theme in tkinter.ttk.Style().theme_names()]
    # Меню
    root_window.option_add("*tearOff", False)
    root_window.menu = tkinter.Menu()
    root_window["menu"] = root_window.menu
    root_window.menu = MainMenu(root_window.menu)
    # Главное окно
    root_window.main_frame = MainScreen(root_window)
    root_window.main_frame.show()
    # Запуск
    root_window.mainloop()
