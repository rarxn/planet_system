import tkinter.filedialog

from ChildWindows import *
import pygame


class Window:
    """Главное окно приложения"""

    def __init__(self, width, height, title):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+100+75")
        self.root.resizable(False, False)
        self.displayed_time = StringVar(value="0")
        self.energy = StringVar(value="0.0")
        self.m_vx = StringVar(value="0.0")
        self.m_vy = StringVar(value="0.0")
        self.button = None

    def run(self):
        self.draw()
        self.root.mainloop()

    def draw(self):
        """Прорисовка объектов окна"""
        self.draw_menu()
        frame = Frame(self.root)
        frame.pack(side=LEFT, anchor=N, padx=10)
        Label(frame, text="Текущее время (с)").pack(pady=(10, 0))
        Entry(frame, width=25, textvariable=self.displayed_time, state=DISABLED).pack()
        Label(frame, text="Общая энергия (Дж)").pack(pady=(10, 0))
        Entry(frame, width=25, textvariable=self.energy, state=DISABLED).pack()
        frame = Frame(self.root)
        frame.pack(side=LEFT, padx=12)
        self.button = Button(frame, width=20, height=10, text="Запуск модели", command=self.start_exec)
        self.button.pack()

    def draw_menu(self):
        """Добавление объектов меню"""
        main_menu = Menu(self.root)

        file_menu = Menu(main_menu, tearoff=0)
        file_menu.add_command(label="Новая система", command=self.create_system)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_command(label="Открыть", command=self.open_file)
        main_menu.add_cascade(label="Файл", menu=file_menu)

        main_menu.add_command(label="Параметры", command=self.change_params)
        self.root.configure(menu=main_menu)

    def create_system(self):
        """Открытие окна для создания новой системы"""
        Window1(self.root, "Новая система")

    def change_params(self):
        """Открытие окна для изменения параметров"""
        a = Window2(self.root, "Параметры")
        a.draw()

    def open_file(self):
        """Открытие файла"""
        filename = tkinter.filedialog.askopenfilename(filetypes=(("Text file", ".txt"),))
        if filename:
            Config.read_from_file(filename)

    def save_file(self):
        """Сохранение в файл"""
        filename = tkinter.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text file", "*.txt"),))
        if filename:
            Config.write_to_file(filename)

    def start_exec(self):
        """Запуск циклического выполнения симуляции"""
        print('\nStarted execution...')
        print(Config.planets_count)
        for planet in Config.planets:
            print(planet)
        if len(Config.planets) == 0:
            tkinter.messagebox.showerror("Ошибка!", "Сначала необходимо создать систему")
            return

        Config.run = True
        self.button["state"] = DISABLED
        clock = pygame.time.Clock()
        FPS = 144
        pygame.init()
        width, height = 800, 800
        t = 0
        if Config.scheme == 3 or Config.scheme == 4:
            for planet in Config.planets:
                planet.start_verle_biman(Config.planets, Config.time_step)
        win = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Planet Simulation")
        max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in Config.planets])
        scale_factor = 0.4 * min(width, height) / max_distance
        while Config.run:
            clock.tick(FPS)
            win.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Config.run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause()
                    if event.key == pygame.K_BACKSPACE:
                        clear()
                    if event.key == pygame.K_UP:
                        scale_factor *= 1.5
                        clear()
                    if event.key == pygame.K_DOWN:
                        scale_factor /= 1.5
                        clear()
            t += Config.time_step
            self.displayed_time.set(str(t))
            for planet in Config.planets:
                planet.calculate_position(Config.planets, Config.time_step, Config.scheme)
                planet.render(win, scale_factor)
                # planet.crash(Config.planets, scale_factor)
            self.energy.set(str(calc_energy(Config.planets)))
            pygame.display.update()
            self.root.update()
            if t >= Config.time:
                Config.run = False
                pause()

        pygame.quit()
        Config.planets_from_matrix(Config.param_values)
        self.button["state"] = NORMAL


def clear():
    for planet in Config.planets:
        planet.orbit = []


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Config.run = False
                paused = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False


def calc_energy(objects):
    e = 0.
    for obj in objects:
        for obj2 in objects:
            if obj == obj2:
                continue
            dx = obj.x - obj2.x
            dy = obj.y - obj2.y
            r = (dx ** 2 + dy ** 2) ** 0.5
            e += obj.m * obj2.m / r
    return - Config.G * e / 4

