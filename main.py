import tkinter
import tkinter.font
import tkinter.ttk
import webbrowser

import database as db

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

    @staticmethod
    def change_theme(event) -> None:
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


class Help_Info(tkinter.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Справка")

        # Текст с описанием использования
        help_text = """
                Добро пожаловать в наше приложение!

                Как пользоваться:
                1. Создайте новую доску заданий, нажав кнопку "Добавить доску".
                2. Введите имя для новой доски и нажмите "ОК".
                3. Для переименования доски нажмите кнопку "Переименовать доску".
                4. Добавьте столбцы на доску, нажав кнопку "Добавить столбец".
                5. Введите заголовок и текст для нового столбца и нажмите "ОК".
                6. Для переименования столбца нажмите кнопку "Переименовать столбец".
                7. Для удаления столбца нажмите кнопку "Удалить столбец".
                8. Для удаления доски нажмите кнопку "Удалить доску".

                Приятного использования!
                """

        # Создаем метку с текстом справки
        help_label = tkinter.Label(self, text=help_text, justify=tkinter.LEFT)
        help_label.pack(padx=10, pady=10)

        # Кнопка "Закрыть" для закрытия окна
        close_button = tkinter.Button(self, text="Начать пользоваться!", command=self.destroy)
        close_button.pack(pady=10)


class About_Us(tkinter.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("О нас")

        hello_text = """Привет! Это наша команда. Приятно познакомиться!"""
        help_label = tkinter.Label(self, text=hello_text, justify=tkinter.LEFT)
        help_label.pack(padx=10, pady=10)

        link_label = tkinter.Label(self, text="Никита", fg="blue", cursor="hand2")
        link_label.pack()
        link_label.bind("<Button-1>", lambda e: self.open_link("https://github.com/hoohep5"))

        link_label = tkinter.Label(self, text="Олег", fg="blue", cursor="hand2")
        link_label.pack()
        link_label.bind("<Button-1>", lambda e: self.open_link("https://github.com/aethersoljuh"))

        link_label = tkinter.Label(self, text="Витя", fg="blue", cursor="hand2")
        link_label.pack()
        link_label.bind("<Button-1>", lambda e: self.open_link("https://github.com/Vorin2473"))

        link_label = tkinter.Label(self, text="Илья", fg="blue", cursor="hand2")
        link_label.pack()
        link_label.bind("<Button-1>", lambda e: self.open_link("https://github.com/Lorane-I"))

        link_label = tkinter.Label(self, text="И конечно же сказочный персонаж: Макар", fg="blue", cursor="hand2")
        link_label.pack()
        link_label.bind("<Button-1>", lambda e: self.open_link("https://github.com/CH4NG35"))

        # Кнопка "Закрыть" для закрытия окна
        close_button = tkinter.Button(self, text="Profit?!?!?!??!?!??!??", command=self.destroy)
        close_button.pack(pady=10)

    @staticmethod
    def open_link(url):
        webbrowser.open(url)


class MainMenu:
    """Принимает меню и дополняет его элементами, создавая главное меню программы"""

    def __init__(self, main_menu):
        self.main_menu = main_menu
        # Файл
        self.menu = tkinter.Menu()
        self.menu.add_command(label="Настройки", command=Settings)  # Открывает новое меню с настройками
        self.main_menu.add_cascade(label="Файл", menu=self.menu)
        # Помощь
        self.main_menu.add_command(label="Помощь", command=Help_Info)  # Открывает меню помощи
        # О нас
        self.main_menu.add_command(label="Справка", command=About_Us)


class Column:
    """Столбцы с задачами"""
    frame: tkinter.ttk.Frame

    def __init__(self, window, name, title, text, column_id):
        self.window = window
        self.frame = tkinter.ttk.Frame(window)
        self.id = column_id
        self.name = name
        self.title = title
        self.text = text
        # Кнопка

        # Список
        self.listbox = tkinter.Listbox(self.frame, selectmode=tkinter.SINGLE)
        #        self.listbox.bind("<<ListboxSelect>>", self.select)
        self.btn1 = tkinter.ttk.Button(self.frame, text=title, command=self.rename)
        self.btn1.grid(row=0)
        for elem in [text]:  # TODO получение данных с БД
            self.listbox.insert(self.listbox.size(), elem)
        self.listbox.grid(row=1)
        # Выравнивание сетки
        self.frame.columnconfigure(index=0, weight=1)
        self.frame.rowconfigure(index=0, weight=2)
        self.frame.rowconfigure(index=1, weight=8)

    #    def select(self, event):
    #       index = event.widget.curselection()
    #        if len(index) != 0:
    #            print(f"Выбран {index[0]}")

    def rename(self):
        print("Input title and text:\n")
        title = input()
        text = input()
        self.listbox.delete(0)
        for elem in [text]:  # получение данных с БД
            self.listbox.insert(self.listbox.size(), elem)
        DataBace.update(self.name, "title", self.title, title)
        DataBace.update(self.name, "about", self.text, text)
        DataBace.deleteAboutLast(self.name, "title", self.title)
        self.btn1.config(text=title)


class Board:
    """Доска заданий, имеющая свои столбцы"""

    def __init__(self, notebook, board_id, name, add=False):
        self.notebook = notebook
        self.board_id = board_id
        if add:
            self.frame = tkinter.ttk.Frame(self.notebook, name="+")
            self.notebook.add(self.frame, text="+")
        else:
            self.name1 = name
            self.id = 0
            self.titles = []
            self.texts = []
            self.frame = tkinter.ttk.Frame(self.notebook)
            # Добавление столбцов
            # Восстановление столбцов из БД
            DataBace.createNewDesk(self.name1)
            if not DataBace.check(self.name1, "new"):
                DataBace.addText(self.name1, "new", "-")
            self.columns = []
            DataBace.returnAll(self.name1)

            for i in DataBace.returnAll(name):
                data = str(i).split(",")
                title = data[0][2:-1]
                self.titles.append(title)
                text = data[1][2:-2]
                self.texts.append(text)
                self.columns.append(Column(self.frame, self.name1, title, text, self.id))
            #            self.columns.append(Column(self.frame, 1))
            # Восстановление доски из БД
            self.notebook.insert(self.notebook.index("end") - 1, self.frame,
                                 text=self.name1)  # До должен быть frame "+"
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
            tkinter.ttk.Button(self.frame_control, text="Удалить столбец", command=self.delete_column).grid(row=0,
                                                                                                            column=3)
            self.frame_control.grid(row=0, column=0, columnspan=self.number_of_columns, sticky="nw")

    def rename_board(self, new_name):
        self.name1 = new_name
        self.notebook.tab(self.frame, text=new_name)

    def rename(self):
        text_input_window = TextInputWindow(self.frame)
        self.frame.wait_window(text_input_window)  # Ждем закрытия окна

        new_name = text_input_window.name
        if new_name:
            self.name1 = new_name
            self.notebook.tab(self.frame, text=new_name)

    def alignment(self):
        """Выравнивание сетки для grid"""
        for c in range(self.number_of_columns):
            self.frame.columnconfigure(index=c, weight=1)
        for r in range(self.number_of_rows):
            self.frame.rowconfigure(index=r, weight=1)

    def add_column(self):
        self.id += 1
        title_input_window = TitleInputWindow(self.frame)
        self.frame.wait_window(title_input_window)
        title = title_input_window.new_title
        text = title_input_window.new_text
        while DataBace.check(self.name1, title):
            title_input_window = TitleInputWindow(self.frame)
            self.frame.wait_window(title_input_window)
            title = title_input_window.new_title
            text = title_input_window.new_text
        self.titles.append(title)
        self.texts.append(text)
        DataBace.addText(self.name1, title, text)
        self.columns.append(Column(self.frame, self.name1, title, text, self.id))
        self.number_of_columns = len(self.columns)
        self.alignment()
        for i in range(len(self.columns)):
            self.columns[i].frame.grid(row=1, column=i)
        self.frame_control.grid(row=0, column=0, columnspan=self.number_of_columns, sticky="nw")

    def delete_column(self):
        self.columns[-1].listbox.destroy()
        self.columns[-1].btn1.destroy()
        self.columns.pop()
        print(self.titles)
        DataBace.deleteAboutLast(self.name1, "title", self.titles[-1])
        self.titles.pop()

    def delete(self):
        # Удаление из БД
        self.notebook.forget("current")
        DataBace.deleteDesk(self.name1)
        if self.notebook.index("end") == 1:
            self.notebook.select(self.notebook.index("end") - 1)
        else:
            self.notebook.select(self.notebook.index("end") - 2)


class TitleInputWindow(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.new_title = ""
        self.new_text = ""

        self.input_label = tkinter.Label(self, text="Введите название и текст:")
        self.input_label.pack()

        self.input_title = tkinter.Entry(self)
        self.input_title.pack()

        self.input_text = tkinter.Entry(self)
        self.input_text.pack()

        self.confirm_button = tkinter.Button(self, text="Подтвердить", command=self.confirm)
        self.confirm_button.pack()

    def confirm(self):
        # Получаем введенное имя из поля ввода
        self.new_title = self.input_title.get()
        self.new_text = self.input_text.get()
        # Вызываем метод rename_board у родительского экземпляра Board
        # if isinstance(self.parent, Board):
        #     self.parent.rename_board(self.name)

        # Закрываем окно ввода
        self.destroy()


class TextInputWindow(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.name = ""

        self.input_label = tkinter.Label(self, text="Введите имя:")
        self.input_label.pack()

        self.input_entry = tkinter.Entry(self)
        self.input_entry.pack()

        self.confirm_button = tkinter.Button(self, text="Подтвердить", command=self.confirm)
        self.confirm_button.pack()

    def confirm(self):
        # Получаем введенное имя из поля ввода
        self.name = self.input_entry.get()

        # Вызываем метод rename_board у родительского экземпляра Board
        if isinstance(self.parent, Board):
            self.parent.rename_board(self.name)

        # Закрываем окно ввода
        self.destroy()


class MainScreen:
    def __init__(self, window):
        # Создание окна
        self.window = window
        self.main_frm = tkinter.ttk.Frame(self.window, padding=15)
        # Создание вкладок
        self.notebook = tkinter.ttk.Notebook(padding=5)
        # Проход по БД для восстановления досок
        Board(self.notebook, -1, "+", add=tkinter.TRUE)
        for i in DataBace.returnNameTables():
            Board(self.notebook, 1, str(i).split("'")[1])
        self.notebook.select(0)
        self.notebook.bind("<<NotebookTabChanged>>", self.tab_changed)
        self.notebook.place(relx=0.5, rely=0.5, anchor="center", relheight=1.0, relwidth=1.0)

    # def rename_Board(self):
    #     text_input_window = TextInputWindow(self.window)
    #     self.window.wait_window(text_input_window)  # Ждем закрытия окна
    #
    #     self.name = text_input_window.name
    #     self.name_input.delete(0, tkinter.END)
    #     self.name_input.insert(0, self.name)

    def new_board(self):
        # Создание доски
        #        NewTab()
        name = "New"
        count = 0
        names = []
        try:
            for i in DataBace.returnNameTables():
                names.append(str(i).split("'")[1])
            while name in names:
                name = name.split("_")[0]
                count += 1
                name += f"_{count}"
            DataBace.createNewDesk(name)
        except:
            DataBace.createNewDesk(name)
        Board(self.notebook, 1, name)
        self.notebook.select(self.notebook.index("end") - 2)

    def tab_changed(self, event) -> None:
        if event.widget.select().endswith("+"):
            self.new_board()

    def show(self):
        """Отображает экран в окне"""
        self.main_frm.place(relx=0.5, rely=0.5, anchor="center", relheight=1.0, relwidth=1.0)


favicon_path = "favicon.png"

DataBace = db.Desk("desk2")
DataBace.createNewDesk("Desk1")

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
