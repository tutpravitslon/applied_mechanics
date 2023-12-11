import numpy as np
import matplotlib.pyplot as plt
import time

AB = 3.5
BC = 1.27 * AB
CD = 1.27 * AB
CM = 1.27 * AB
AD = 0.5 * AB
ANGLE = 123 / 180 * np.pi
N = 100  # количество точек
delay_value = 0.001  # значение задержки
rotate_angle = 2 * np.pi  # угол поворота
omega = (rotate_angle / N) / delay_value / 100
phi = np.linspace(0, rotate_angle, N)
velocity = {'B': [], 'C': [], 'M': []}
acceleration = {'B': [], 'C': [], 'M': []}


def numerical_derivative(y2, y1, dx):
    return (y2 - y1) / dx


def second_numerical_derivative(y3, y2, y1, dx):
    return (y3 - 2 * y2 + y1) / dx ** 2


def get_dist(x, y):
    return np.sqrt((x[1] - x[0]) ** 2 + (y[1] - y[0]) ** 2)


def point_velocity(phi, i, x, y):
    if i == 50:
        dx = numerical_derivative(x(i + 1), x(i), phi[i + 1] - phi[i])
        dy = numerical_derivative(y(i + 1), y(i), phi[i + 1] - phi[i])
    else:
        dx = numerical_derivative(x(i), x(i - 1), phi[i] - phi[i - 1])
        dy = numerical_derivative(y(i), y(i - 1), phi[i] - phi[i - 1])
    return dx, dy


def point_acceleration(phi, i, x, y):
    dx_2 = second_numerical_derivative(x(i + 1), x(i), x(i - 1), phi[i + 1] - phi[i])
    dy_2 = second_numerical_derivative(y(i + 1), y(i), y(i - 1), phi[i + 1] - phi[i])
    return dx_2, dy_2


def point_calcs(phi, i, x, y, link):
    if i > 0:
        dx, dy = point_velocity(phi, i, x, y)
        velocity_point = np.sqrt(dx ** 2 + dy ** 2) * omega
        if link in velocity.keys():
            velocity[link].append([velocity_point, x(i), y(i)])
        else:
            velocity[link] = [[velocity_point, x(i), y(i)]]
        if i < len(phi) - 1:
            dx_2, dy_2 = point_acceleration(phi, i, x, y)
            if i == 50:
                print(x(i + 1), x(i), x(i - 1))
                print(y(i + 1), y(i), y(i - 1))
                print(dx_2, dy_2, np.sqrt(dx_2 ** 2 + dy_2 ** 2) * omega ** 2 + (np.sqrt(dx ** 2 + dy ** 2) * 0))
            acceleration_point = np.sqrt(dx_2 ** 2 + dy_2 ** 2) * omega ** 2 + (np.sqrt(dx ** 2 + dy ** 2) * 0)
            if link in velocity.keys():
                acceleration[link].append([acceleration_point, x(i), y(i)])
            else:
                acceleration[link] = [[acceleration_point, x(i), y(i)]]


def main():
    max_length = max(AB, BC, CD, CM, AD)
    x_m = []
    y_m = []

    plt.ion()
    for i in range(len(phi)):
        plt.clf()
        # B point
        B_point_x = lambda i: np.cos(phi[i]) * AB
        B_point_y = lambda i: np.sin(phi[i]) * AB

        plt.annotate(f'time: {delay_value * i:.4g}', (0, -5))
        plt.scatter(B_point_x(i), B_point_y(i), color='#f50800')
        plt.annotate("B", (B_point_x(i), B_point_y(i)))
        plt.plot([0, B_point_x(i)], [0, B_point_y(i)],
                 label=f"|AB| = {get_dist([0, B_point_x(i)], [0, B_point_y(i)]):.2f}")
        plt.scatter(0, 0, color='#0f0f0f')
        plt.annotate("A", (0, 0))
        plt.scatter(-AD, 0, color='b')
        plt.annotate("D", (-AD, 0))

        if phi[i] >= np.pi:
            BD = lambda i: np.sqrt(AD ** 2 + AB ** 2 - 2 * AB * AD * np.cos(phi[i] - np.pi))
            BDA_angle = lambda i: np.arccos((BD(i) ** 2 + AD ** 2 - AB ** 2) / (2 * BD(i) * AD))
            CDB_angle = lambda i: np.arccos((BD(i) ** 2 + CD ** 2 - BC ** 2) / (2 * BD(i) * CD))
            CDA_angle = lambda i: 2 * np.pi - (BDA_angle(i) - CDB_angle(i))

        else:
            BD = lambda i: np.sqrt(AD ** 2 + AB ** 2 - 2 * AB * AD * np.cos(np.pi - phi[i]))
            BDA_angle = lambda i: np.arccos((BD(i) ** 2 + AD ** 2 - AB ** 2) / (2 * BD(i) * AD))
            CDB_angle = lambda i: np.arccos((BD(i) ** 2 + CD ** 2 - BC ** 2) / (2 * BD(i) * CD))
            CDA_angle = lambda i: BDA_angle(i) + CDB_angle(i)

        # C point
        C_point_x = lambda i: CD * np.cos(CDA_angle(i)) - AD
        C_point_y = lambda i: CD * np.sin(CDA_angle(i))

        plt.scatter(C_point_x(i), C_point_y(i), color='#f500e9')
        plt.annotate("C", (C_point_x(i), C_point_y(i)))

        plt.plot([-AD, C_point_x(i)], [0, C_point_y(i)],
                 label=f"|CD| = {get_dist([-AD, C_point_x(i)], [0, C_point_y(i)]):.2f}")
        # plt.plot([-AD, C_point_x(i)], [0, C_point_y(i)], label=f"CDA = {degrees(CDA_angle):.3f}")

        plt.plot([B_point_x(i), C_point_x(i)], [B_point_y(i), C_point_y(i)],
                 label=f"|BC| = {get_dist([B_point_x(i), C_point_x(i)], [B_point_y(i), C_point_y(i)]):.2f}")
        # plt.plot([x, C_point_x(i)], [y, C_point_y(i)], label=f"CDB = {degrees(CDB_angle(i)):.3f}")

        # M point
        M_point_x = lambda i: C_point_x(i) + (B_point_x(i) - C_point_x(i)) * np.cos(ANGLE) - (
                    B_point_y(i) - C_point_y(i)) * np.sin(ANGLE)
        M_point_y = lambda i: C_point_y(i) + (B_point_x(i) - C_point_x(i)) * np.sin(ANGLE) + (
                    B_point_y(i) - C_point_y(i)) * np.cos(ANGLE)

        plt.plot([C_point_x(i), M_point_x(i)], [C_point_y(i), M_point_y(i)],
                 label=f"|CM| = {get_dist([C_point_x(i), M_point_x(i)], [C_point_y(i), M_point_y(i)]):.2f}")

        # plt.plot([C_point_x(i), M_point_x(i)], [C_point_y(i), M_point_y(i)], label=f"BDA = {degrees(BDA_angle(i)):.3f}")
        x_m.append(M_point_x(i))
        y_m.append(M_point_y(i))
        plt.plot(x_m, y_m, 'k--')

        plt.xlim(-3 * max_length, 3 * max_length)
        plt.ylim(-3 * max_length, 3 * max_length)

        plt.scatter(M_point_x(i), M_point_y(i))
        plt.plot(M_point_x(i), M_point_y(i))
        plt.annotate("M", (M_point_x(i), M_point_y(i)))

        plt.legend()
        plt.draw()
        plt.gcf().canvas.flush_events()

        # calculating velocities and accelerations
        point_calcs(phi, i, B_point_x, B_point_y, 'B')
        point_calcs(phi, i, C_point_x, C_point_y, 'C')
        point_calcs(phi, i, M_point_x, M_point_y, 'M')

        time.sleep(delay_value)
    plt.ioff()
    plt.show()
    for key, value in velocity.items():
        plt.plot([i * delay_value for i in range(1, len(phi))], [item[0] for item in value])
        plt.title(f'Скорость точки {key}')
        plt.show()

    for key, value in acceleration.items():
        plt.plot([i * delay_value for i in range(1, len(phi) - 1)], [item[0] for item in value])
        plt.title(f'Ускорение точки {key}')
        plt.show()


if __name__ == '__main__':
    main()
