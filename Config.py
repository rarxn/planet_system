from Planet import Planet
import random

G = 6.67e-11
COLUMNS = 6

planets_count = 0
param_values = []
time = 31536000
time_step = 3600
planets = []
scheme = 2

run = False


def is_float(value):
    """Проверка является ли переменная типом данных float"""
    try:
        float(value)
        return True
    except:
        return False


def default_values(n):
    """Заполнение параметров стандартными значениями"""
    global planets_count, param_values, time, time_step, scheme
    planets_count = n
    param_values = [[0.0] * COLUMNS for i in range(planets_count)]
    param_values[0][4] = 1.2166e30
    param_values[0][COLUMNS - 1] = "#" + ''.join([random.choice('0123456789ABCDEF') for i in range(6)])
    for i in range(1, planets_count):
        param_values[i][0] = i * 1495e8
        param_values[i][4] = i * 6.083e24
        param_values[i][3] = (G * param_values[0][4] / param_values[i][0]) ** 0.5
        param_values[i][COLUMNS - 1] = "#" + ''.join([random.choice('0123456789ABCDEF') for i in range(6)])

    time = 315360000
    time_step = 36000
    scheme = 2
    planets_from_matrix(param_values)


def set_params(x, t, dt, choice):
    """Запись параметров"""
    global param_values, time, time_step, scheme
    param_values = x
    time = t
    time_step = dt
    scheme = choice
    planets_from_matrix(x)


def planets_from_matrix(matrix):
    """Заполнение массива планет по параметрам матрицы"""
    global planets
    planets = []
    for i in range(planets_count):
        planets.append(Planet(*matrix[i]))


def read_from_file(filename):
    """Чтение данных из файла"""
    with open(filename, 'r') as file:
        first_line = True
        for line in file:
            if first_line:
                n, t, dt = [int(x) for x in line.split()]
                buff = [[0.0] * COLUMNS for i in range(n)]
                first_line = False
                i = 0
            else:
                line = line.split()
                for j in range(COLUMNS - 1):
                    buff[i][j] = float(line[j])
                buff[i][COLUMNS - 1] = line[COLUMNS - 1]
                i += 1
    global planets_count
    planets_count = n
    set_params(buff, t, dt, 2)


def write_to_file(filename):
    """Запись данных в файл"""
    with open(filename, 'w') as file:
        print(planets_count, time, time_step, file=file)
        for planet in planets:
            print(planet, file=file)
