import numpy as np
import matplotlib.pyplot as plt
import time


def get_dist(x, y):
    return np.sqrt((x[1] - x[0]) ** 2 + (y[1] - y[0]) ** 2)


AB = 1
BC = CD = CM = 1.27 * AB
AD = 0.5 * AB
ANGLE = 123 / 180 * np.pi

x_m = []
y_m = []
phi = np.linspace(0, 4 * np.pi, 200)
plt.ion()
for delay in phi:
    delay %= 2 * np.pi
    plt.clf()
    x = np.cos(delay) * AB
    y = np.sin(delay) * AB

    plt.scatter(x, y, color='#f50800')
    plt.annotate("B", (x, y))
    plt.plot([0, x], [0, y], label=f"|AB| = {get_dist([0, x], [0, y]):.2f}")
    plt.scatter(0, 0, color='#0f0f0f')
    plt.annotate("A", (0, 0))
    plt.scatter(-AD, 0, color='b')
    plt.annotate("D", (-AD, 0))

    if delay > np.pi:
        BD = np.sqrt(AD ** 2 + AB ** 2 - 2 * AB * AD * np.cos(delay - np.pi))
        BDA_angle = np.arccos((BD ** 2 + AD ** 2 - AB ** 2) / (2 * BD * AD))
        CDB_angle = np.arccos((BD ** 2 + CD ** 2 - BC ** 2) / (2 * BD * CD))
        CDA_angle = 2 * np.pi - (BDA_angle - CDB_angle)

    else:
        BD = np.sqrt(AD ** 2 + AB ** 2 - 2 * AB * AD * np.cos(np.pi - delay))
        BDA_angle = np.arccos((BD ** 2 + AD ** 2 - AB ** 2) / (2 * BD * AD))
        CDB_angle = np.arccos((BD ** 2 + CD ** 2 - BC ** 2) / (2 * BD * CD))
        CDA_angle = BDA_angle + CDB_angle

    x1 = CD * np.cos(CDA_angle) - AD
    y1 = CD * np.sin(CDA_angle)

    plt.scatter(x1, y1, color='#f500e9')
    plt.annotate("C", (x1, y1))

    plt.plot([-AD, x1], [0, y1],  label=f"|CD| = {get_dist([-AD, x1], [0, y1]):.2f}")
    # plt.plot([-AD, x1], [0, y1], label=f"CDA = {degrees(CDA_angle):.3f}")

    plt.plot([x, x1], [y, y1], label=f"|BC| = {get_dist([x, x1], [y, y1]):.2f}")
    # plt.plot([x, x1], [y, y1], label=f"CDB = {degrees(CDB_angle):.3f}")

    rotatedX = x1 + (x - x1) * np.cos(ANGLE) - (y - y1) * np.sin(ANGLE)
    rotatedY = y1 + (x - x1) * np.sin(ANGLE) + (y - y1) * np.cos(ANGLE)

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

    time.sleep(0.002)
plt.ioff()
plt.show()
