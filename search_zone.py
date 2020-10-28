# Проверяется входимость указанных координат в выбранную зону
def zone(data, point):
    data = data.split(';')
    x, y = [float(i) for i in point.split(',')]
    xp, yp = [], []
    for i in range(len(data)):
        data[i] = [float(j) for j in data[i].split(',')]
        xp += [data[i][0]]
        yp += [data[i][1]]

    c = 0
    for i in range(len(xp)):
        if (((yp[i] <= y and y < yp[i - 1]) or (yp[i - 1] <= y and y < yp[i])) and
                (x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i])):
            c = 1 - c
    return c
