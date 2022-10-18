import math
from pygame import draw

G = 6.67e-11


class Planet:
    """Класс планет"""

    def __init__(self, x: float, y: float, v_x: float, v_y: float, m: float, color: str):
        self.x = x
        self.y = y
        self.Vx = v_x
        self.Vy = v_y
        self.m = m
        self.R = m / 9.42e17
        self.orbit = []
        self.color = color
        self.x_prev = None
        self.y_prev = None
        self.ax_prev = 0
        self.ay_prev = 0

    def __str__(self):
        return f"{self.x} {self.y} {self.Vx} {self.Vy} {self.m} {self.color}"

    def calculate_position(self, space_objects, dt, type):
        if type == 1:
            self.euler(space_objects, dt)
        elif type == 2:
            self.euler_kramer(space_objects, dt)
        elif type == 3:
            self.verle(space_objects, dt)
        elif type == 4:
            self.biman(space_objects, dt)
        else:
            self.runge(space_objects, dt)

    def euler(self, space_objects, dt):
        ax, ay = self.acceleration(space_objects)

        self.x += self.Vx * dt
        self.y += self.Vy * dt
        self.Vx += ax * dt
        self.Vy += ay * dt

    def euler_kramer(self, space_objects, dt):
        ax, ay = self.acceleration(space_objects)

        self.Vx += ax * dt
        self.Vy += ay * dt

        self.x += self.Vx * dt
        self.y += self.Vy * dt

    def start_verle_biman(self, space_objects, dt):
        ax, ay = self.acceleration(space_objects)
        self.x_prev = self.x
        self.y_prev = self.y
        self.ax_prev, self.ay_prev = ax, ay
        self.x += self.Vx * dt + 0.5 * ax * dt ** 2
        self.y += self.Vy * dt + 0.5 * ay * dt ** 2
        ax, ay = self.acceleration(space_objects)
        self.Vx += 0.5 * (self.ax_prev + ax) * dt
        self.Vy += 0.5 * (self.ay_prev + ay) * dt

    def verle(self, space_objects, dt):
        ax, ay = self.acceleration(space_objects)
        buff_x, buff_y = self.x, self.y
        self.x = 2 * self.x - self.x_prev + ax * dt ** 2
        self.y = 2 * self.y - self.y_prev + ay * dt ** 2
        self.Vx = (self.x - self.x_prev) / (2 * dt)
        self.Vy = (self.y - self.y_prev) / (2 * dt)
        self.x_prev = buff_x
        self.y_prev = buff_y

    def biman(self, space_objects, dt):
        ax, ay = self.acceleration(space_objects)
        self.x += self.Vx * dt + (1 / 6) * (4 * ax - self.ax_prev) * (dt ** 2)
        self.y += self.Vy * dt + (1 / 6) * (4 * ay - self.ay_prev) * (dt ** 2)
        ax_next, ay_next = self.acceleration(space_objects)
        self.Vx += (1 / 6) * (2 * ax_next + 5 * ax - self.ax_prev) * dt
        self.Vy += (1 / 6) * (2 * ay_next + 5 * ay - self.ay_prev) * dt
        self.ax_prev = ax
        self.ay_prev = ay

    def runge(self, space_objects, dt):
        k1 = dt * self.fx(space_objects, self.x)
        q1 = dt * self.Vx

        k2 = dt * self.fx(space_objects, self.x + q1 / 2)
        q2 = dt * (self.Vx + k1 / 2)

        k3 = dt * self.fx(space_objects, self.x + q2 / 2)
        q3 = dt * (self.Vx + k2 / 2)

        k4 = dt * self.fx(space_objects, self.x + q3)
        q4 = dt * (self.Vx + k3)

        self.Vx += (k1 + 2 * k2 + 2 * k3 + k4) / 6
        self.x += (q1 + 2 * q2 + 2 * q3 + q4) / 6

        k1 = dt * self.fy(space_objects, self.y)
        q1 = dt * self.Vy

        k2 = dt * self.fy(space_objects, self.y + q1 / 2)
        q2 = dt * (self.Vy + k1 / 2)

        k3 = dt * self.fy(space_objects, self.y + q2 / 2)
        q3 = dt * (self.Vy + k2 / 2)

        k4 = dt * self.fy(space_objects, self.y + q3)
        q4 = dt * (self.Vy + k3)
        self.Vy += (k1 + 2 * k2 + 2 * k3 + k4) / 6
        self.y += (q1 + 2 * q2 + 2 * q3 + q4) / 6

    def fx(self, space_objects, x):
        fx = 0
        for obj in space_objects:
            if self == obj:
                continue
            dx = obj.x - x
            dy = obj.y - self.y
            r = math.sqrt(dx ** 2 + dy ** 2)
            fx += G * dx * obj.m / (r ** 3)
        return fx

    def fy(self, space_objects, y):
        fy = 0
        for obj in space_objects:
            if self == obj:
                continue
            dx = obj.x - self.x
            dy = obj.y - y
            r = math.sqrt(dx ** 2 + dy ** 2)
            fy += G * dy * obj.m / (r ** 3)
        return fy

    def render(self, win, scale_factor):

        x = self.x * scale_factor + win.get_width() / 2
        y = self.y * scale_factor + win.get_height() / 2
        self.orbit.append((x, y))
        if len(self.orbit) > 2:
            draw.lines(win, self.color, False, self.orbit)
        draw.circle(win, self.color, (x, y), 6)

    def acceleration(self, space_objects):
        fx = fy = 0
        for obj in space_objects:
            if self == obj:
                continue
            dx = obj.x - self.x
            dy = obj.y - self.y
            r = math.sqrt(dx ** 2 + dy ** 2)
            f = (G * self.m * obj.m) / (r ** 2)
            theta = math.atan2(dy, dx)
            fx += math.cos(theta) * f
            fy += math.sin(theta) * f
        return fx / self.m, fy / self.m

    def crash(self, space_objects, scale_factor):
        for obj in space_objects:
            if self == obj:
                continue
            dx = (obj.x - self.x) * scale_factor
            dy = (obj.y - self.y) * scale_factor
            d = math.sqrt(dx ** 2 + dy ** 2)
            if d < 15:
                space_objects.remove(self)
                space_objects.remove(obj)
