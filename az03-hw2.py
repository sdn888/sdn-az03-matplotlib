import numpy as np
import matplotlib.pyplot as plt

# Генерация двух массивов случайных чисел
x = np.random.rand(5)
y = np.random.rand(5)
print(x)
print(y)

# Построение диаграммы рассеяния
plt.figure(figsize=(6, 6))
plt.scatter(x, y, color='blue', alpha=0.6, edgecolors='black')
plt.title("Диаграмма рассеяния случайных данных")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.show()
