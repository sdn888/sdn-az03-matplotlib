import matplotlib.pyplot as plt

x = [1, 4, 6, 7]
y = [3, 5, 8, 10]

plt.plot(x, y)

plt.title("Пример простого линейного графика")

plt.xlabel("x ось")
plt.ylabel("y ось")

plt.show()

data = [1, 2, 2, 3, 4, 4, 4, 5, 6, 6, 6, 6, 6]

plt.hist(data, bins=6) # bins - количество интервалов

plt.xlabel("x ось")
plt.ylabel("y ось")
plt.title("Тестовая гистограма")

plt.show()

x = [1, 4, 6, 7]
y = [3, 5, 8, 10]

plt.scatter(x, y)

plt.xlabel("ось Х")
plt.ylabel("ось Y")
plt.title("Тестовая диаграмма рассеяния")

plt.show()