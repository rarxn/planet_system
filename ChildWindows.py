import Config
from tkinter import *
import tkinter.messagebox

class Window1:
    """Окно для ввода числа планет"""

    def __init__(self, parent, title):
        self.root = Toplevel(parent)
        self.root.title(title)
        self.root.resizable(False, False)
        self.root.attributes('-toolwindow', True)
        self.root.attributes('-topmost', True)

        self.text = StringVar(value="2")
        Label(self.root, text="Число планет: ").grid(row=0, column=0)
        Entry(self.root, width=15, textvariable=self.text).grid(row=0, column=1, pady=10)
        Button(self.root, width=10, text="Ввод", command=self.save).grid(row=1, column=0, columnspan=2)

        self.grab_focus()

    def grab_focus(self):
        """Забрать фокус на текущее окно"""
        self.root.grab_set()
        self.root.focus_set()
        # self.root.wait_window()

    def save(self):
        """Сохранение параметров"""
        text = self.text.get()
        if text.isdigit():
            n = int(text)
            if n >= 1:
                Config.default_values(n)
                self.root.destroy()
            else:
                tkinter.messagebox.showerror("Ошибка", "Значение должно быть больше 0")
        else:
            tkinter.messagebox.showerror("Ошибка", "Введенное значение не является числом")


class Window2:
    """Окно для ввода параметров планет"""

    def __init__(self, parent, title):
        self.root = Toplevel(parent)
        self.root.title(title)
        self.root.attributes('-topmost', True)
        self.root.resizable(False, False)
        self.temp = [[StringVar(value=str(Config.param_values[i][j])) for j in range(Config.COLUMNS)] for i
                     in
                     range(len(Config.param_values))]
        self.choice = IntVar(value=str(Config.scheme))
        self.dt = StringVar(value=str(Config.time_step))
        self.t = StringVar(value=str(Config.time))

    def draw(self):
        """Прорисовка объектов окна"""
        big_frame = Frame(self.root)
        big_frame.pack()
        Button(big_frame, width=10, text="Ввод", command=self.save).pack(side=LEFT, pady=5, padx=5)
        frame = Frame(big_frame)
        frame.pack(side=LEFT)
        Label(frame, text="Шаг по времени:").pack(side=LEFT)
        Entry(frame, width=10, textvariable=self.dt).pack(side=LEFT, padx=5)
        Label(frame, text="Время моделирования:").pack(side=LEFT)
        Entry(frame, width=20, textvariable=self.t).pack(side=LEFT, padx=5)

        big_frame = LabelFrame(self.root, text="Разностная схема")
        big_frame.pack()
        Radiobutton(big_frame, text="Эйлера", variable=self.choice, value=1).pack(side=LEFT, padx=8)
        Radiobutton(big_frame, text="Эйлера-Крамера", variable=self.choice, value=2).pack(side=LEFT, padx=8)
        Radiobutton(big_frame, text="Верле", variable=self.choice, value=3).pack(side=LEFT, padx=8)
        Radiobutton(big_frame, text="Бимана", variable=self.choice, value=4).pack(side=LEFT, padx=8)
        Radiobutton(big_frame, text="Рунге", variable=self.choice, value=5).pack(side=LEFT, padx=8)

        big_frame = Frame(self.root)
        big_frame.pack()
        frame = Frame(big_frame)
        frame.pack()
        Label(frame, width=5, text=str(Config.planets_count), relief=GROOVE).pack(side=LEFT)
        Label(frame, width=14, text="X", relief=GROOVE).pack(side=LEFT)
        Label(frame, width=14, text="Y", relief=GROOVE).pack(side=LEFT)
        Label(frame, width=14, text="V_x", relief=GROOVE).pack(side=LEFT)
        Label(frame, width=14, text="V_y", relief=GROOVE).pack(side=LEFT)
        Label(frame, width=14, text="Масса", relief=GROOVE).pack(side=LEFT)
        Label(frame, width=14, text="Цвет", relief=GROOVE).pack(side=LEFT)
        for i in range(Config.planets_count):
            frame = Frame(big_frame)
            frame.pack()
            Label(frame, width=5, text=str(i), relief=GROOVE).pack(side=LEFT)
            for j in range(Config.COLUMNS):
                Entry(frame, width=16, textvariable=self.temp[i][j]).pack(side=LEFT, padx=2)
        self.grab_focus()

    def grab_focus(self):
        """Забрать фокус на текущее окно"""
        self.root.grab_set()
        self.root.focus_set()
        # self.root.wait_window()

    def save(self):
        """Сохранение параметров"""
        t = self.t.get()
        dt = self.dt.get()
        if t.isdigit() and dt.isdigit():
            t = int(t)
            dt = int(dt)
            if t >= 1 and dt >= 1:
                buff = [[0.0] * Config.COLUMNS for i in range(Config.planets_count)]
                for i in range(len(self.temp)):
                    for j in range(Config.COLUMNS - 1):
                        if Config.is_float(self.temp[i][j].get()):
                            buff[i][j] = float(self.temp[i][j].get())
                        else:
                            tkinter.messagebox.showerror("Ошибка", "Введенное значение не является типом float")
                            return
                    buff[i][Config.COLUMNS - 1] = str(self.temp[i][Config.COLUMNS - 1].get())
            else:
                tkinter.messagebox.showerror("Ошибка", "Значение должно быть больше 0")
                return
        else:
            tkinter.messagebox.showerror("Ошибка", "Введенное значение не является числом")
            return
        Config.set_params(buff, t, dt, self.choice.get())
        self.root.destroy()
