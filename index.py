import tkinter
import random

# constants

WIDTH = 800 # размеры поля
HEIGHT = 600 # размеры поля
BACKGROUND = '#ccc' # цвет поля
ZERO = 0
Ball_COLOR = 'blue' # цвет шарика
INIT_DX = 5 # смещение шарика по x
INIT_DY = 5 # смещение шарика по y
BALL_RADIUS = 30 # радиус шарика
DELAY = 50 # задержка при выполнении цикла
BAD_COLORS = 'red' # цвет плохих шаров с которыми нельзя сталкиваться
BLACK = 'black' # это рамка для плохих шариков
COLORS = ['aqua', 'fuchsia', BAD_COLORS, 'pink', BAD_COLORS, 'yellow', 'gold', 'green', 'brown', BAD_COLORS]
COUNT_BALLS = 15 # количество шариков




class Balls:

    def __init__(self, x, y, radius, color, dx=0, dy=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dx = dx
        self.dy = dy

    # Функция создает кружок, задаются точнки квадрата в который будет вписан овал
    def draw(self):
        canvas.create_oval(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
            fill=self.color,
            outline=self.color if self.color != BAD_COLORS else BLACK
        )

    def is_collision(self, ball):
        a = abs(self.x + self.dx - ball.x)
        b = abs(self.y + self.dy - ball.y)
        return (a*a + b*b)**0.5 <= self.radius + ball.radius

    def hide(self):
        canvas.create_oval(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
            fill=BACKGROUND,
            outline=BACKGROUND
        )

    def move(self):
        if (self.x + self.radius + self.dx >= WIDTH) or (self.x - self.radius + self.dx <= ZERO):
            self.dx = - self.dx

        if (self.y + self.radius + self.dy >= HEIGHT) or (self.y - self.radius + self.dy <= ZERO):
            self.dy = - self.dy

        for ball in balls:
            if self.is_collision(ball):
                if ball.color == BAD_COLORS:
                    canvas.create_text(WIDTH / 2, HEIGHT / 2, text='Game Over !!!', fill=Ball_COLOR, font='Arial 20')
                    main_ball.dx = main_ball.dy = 0
                ball.hide()
                balls.remove(ball)
                self.dx = -self.dx
                self.dy = -self.dy

        self.hide()
        self.x += self.dx
        self.y += self.dy
        self.draw()


def count_of_bad_balls():
    res = 0
    for ball in balls:
        if ball.color == BAD_COLORS:
            res += 1
    return res


# mouse events, определили функции
def mouse_click(event):
    global main_ball
    print(event.num, event.x, event.y)
    if event.num == 1:

        if 'main_ball' not in globals():
            main_ball = Balls(event.x, event.y, BALL_RADIUS, Ball_COLOR, INIT_DX, INIT_DY)
            main_ball.draw()
        else:
            if main_ball.dx * main_ball.dy > 0:
                main_ball.dy = - main_ball.dy
            else:
                main_ball.dx = - main_ball.dx

    elif event.num == 3:
        if 'main_ball' not in globals():
            main_ball = Balls(event.x, event.y, BALL_RADIUS, Ball_COLOR, INIT_DX, INIT_DY)
            main_ball.draw()
        else:
            if main_ball.dx * main_ball.dy > 0:
                main_ball.dx = - main_ball.dx
            else:
                main_ball.dy = - main_ball.dy

    else:
        main_ball.hide()


def create_list_balls(number):
    lists = []
    while len(lists) < number:
        next_ball = Balls(
            random.choice(range(0, WIDTH)),
            random.choice(range(0, HEIGHT)),
            random.choice(range(10, 35)),
            random.choice(COLORS))
        lists.append(next_ball)
        next_ball.draw()
    return lists


def main():
    if 'main_ball' in globals():
        main_ball.move()
        if len(balls) == 0 or len(balls) == count_of_bad_balls():
            canvas.create_text(WIDTH / 2, HEIGHT / 2, text='ПОБЕДА!!!', font='Arial 20', fill=Ball_COLOR)
            main_ball.dx = main_ball.dy = 0

    root.after(DELAY, main)


root = tkinter.Tk()
root.title("Big balls")

# создадим конфас
canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT, bg=BACKGROUND)
canvas.pack()

canvas.bind('<Button-1>', mouse_click)
canvas.bind('<Button-2>', mouse_click, '+')
canvas.bind('<Button-3>', mouse_click, '+')

if 'main_ball' in globals():
    del main_ball


balls = create_list_balls(COUNT_BALLS)
main()
root.mainloop()
