import numpy as np
import matplotlib.pyplot as plt
import time


def numerical_derivative(y2, y1, dx):
    return (y2 - y1) / dx


def second_numerical_derivative(y3, y2, y1, dx):
    return (y3 - 2*y2 + y1) / dx ** 2


def get_dist(x, y):
    return np.sqrt((x[1] - x[0]) ** 2 + (y[1] - y[0]) ** 2)


AB = 2
BC = CD = CM = 1.27 * AB
AD = 0.5 * AB
ANGLE = 123 / 180 * np.pi
N = 100 #  количество оборотов
delay_value = 0.002 # значение задержки
rotate_angle = 2 * np.pi #угол поворота
omega = (rotate_angle / N) / delay_value
print(omega)
x_m = []
y_m = []
phi = np.linspace(0, 2 * np.pi, N)
velocity = {'B': [], 'C': [], 'M': []}
acceleration = {'B': [], 'C': [], 'M': []}

plt.ion()
for i in range(len(phi) - 1):
    phi[i] %= 2 * np.pi
    plt.clf()
    x = lambda i: np.cos(phi[i]) * AB
    y = lambda i: np.sin(phi[i]) * AB
    dx = numerical_derivative(x(i+1), x(i), phi[i+1] - phi[i])
    dy = numerical_derivative(y(i+1), y(i), phi[i+1] - phi[i])
    dx_2 = second_numerical_derivative(x(i+1), x(i), x(i-1), phi[i+1] - phi[i])
    dy_2 = second_numerical_derivative(y(i + 1), y(i), y(i - 1), phi[i + 1] - phi[i])
    # print(dx, numerical_derivative(np.cos(phi[i+1]) * AB, x, phi[i+1] - phi[i]))
    velocity['B'].append(np.sqrt(dx ** 2 + dy ** 2) * omega)

    if i > 0 and i < len(phi) - 1:
        acceleration['B'].append(np.sqrt(dx_2 ** 2 + dy_2 ** 2) * omega ** 2 + (np.sqrt(dx ** 2 + dy ** 2) * 0))
    # endregion

    plt.scatter(x(i), y(i), color='#f50800')
    plt.annotate("B", (x(i), y(i)))
    plt.plot([0, x(i)], [0, y(i)], label=f"|AB| = {get_dist([0, x(i)], [0, y(i)]):.2f}")
    plt.scatter(0, 0, color='#0f0f0f')
    plt.annotate("A", (0, 0))
    plt.scatter(-AD, 0, color='b')
    plt.annotate("D", (-AD, 0))

    if phi[i] > np.pi:
        BD = np.sqrt(AD ** 2 + AB ** 2 - 2 * AB * AD * np.cos(phi[i] - np.pi))
        BDA_angle = np.arccos((BD ** 2 + AD ** 2 - AB ** 2) / (2 * BD * AD))
        CDB_angle = np.arccos((BD ** 2 + CD ** 2 - BC ** 2) / (2 * BD * CD))
        CDA_angle = 2 * np.pi - (BDA_angle - CDB_angle)

    else:
        BD = np.sqrt(AD ** 2 + AB ** 2 - 2 * AB * AD * np.cos(np.pi - phi[i]))
        BDA_angle = np.arccos((BD ** 2 + AD ** 2 - AB ** 2) / (2 * BD * AD))
        CDB_angle = np.arccos((BD ** 2 + CD ** 2 - BC ** 2) / (2 * BD * CD))
        CDA_angle = BDA_angle + CDB_angle

    x1 = CD * np.cos(CDA_angle) - AD
    y1 = CD * np.sin(CDA_angle)

    plt.scatter(x1, y1, color='#f500e9')
    plt.annotate("C", (x1, y1))

    plt.plot([-AD, x1], [0, y1],  label=f"|CD| = {get_dist([-AD, x1], [0, y1]):.2f}")
    # plt.plot([-AD, x1], [0, y1], label=f"CDA = {degrees(CDA_angle):.3f}")

    plt.plot([x(i), x1], [y(i), y1], label=f"|BC| = {get_dist([x(i), x1], [y(i), y1]):.2f}")
    # plt.plot([x, x1], [y, y1], label=f"CDB = {degrees(CDB_angle):.3f}")

    rotatedX = x1 + (x(i) - x1) * np.cos(ANGLE) - (y(i) - y1) * np.sin(ANGLE)
    rotatedY = y1 + (x(i) - x1) * np.sin(ANGLE) + (y(i) - y1) * np.cos(ANGLE)

    plt.plot([x1, rotatedX], [y1, rotatedY], label=f"|CM| = {get_dist([x1, rotatedX], [y1, rotatedY]):.2f}")
    # plt.plot([x1, rotatedX], [y1, rotatedY], label=f"BDA = {degrees(BDA_angle):.3f}")
    x_m.append(rotatedX)
    y_m.append(rotatedY)
    plt.plot(x_m, y_m, 'k--')

    plt.xlim(-3 * AB, 3 * AB)
    plt.ylim(-3 * AB, 3 * AB)

    plt.scatter(rotatedX, rotatedY)
    plt.plot(rotatedX, rotatedY)
    plt.annotate("M", (rotatedX, rotatedY))

    plt.legend()
    plt.draw()
    plt.gcf().canvas.flush_events()

    time.sleep(delay_value)
plt.ioff()
plt.show()

plt.plot(phi[:99], velocity['B'])
plt.show()