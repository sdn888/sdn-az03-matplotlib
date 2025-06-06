import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import csv

# Парсинг данных
url = "https://www.divan.ru/category/divany"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    print("Получаем данные с сайта...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все элементы с ценами по новым классам
    price_elements = soup.find_all('span', {'data-testid': 'price', 'class': 'ui-LD-ZU KIkOH'})

    prices = []
    for element in price_elements:
        price_text = element.text.split('руб.')[0].replace(' ', '').strip()
        try:
            price = int(price_text)
            prices.append(price)
        except ValueError:
            continue

    if not prices:
        print("Цены не найдены. Проверьте:")
        print("1. Актуальность классов в коде")
        print("2. Не блокирует ли сайт парсинг")
        exit()

    print(f"Найдено {len(prices)} цен на диваны")

    # Сохранение в CSV
    csv_filename = 'divan_prices.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Price (RUB)'])
        writer.writerows([[price] for price in prices])
    print(f"Данные сохранены в файл {csv_filename}")

    # Обработка данных
    df = pd.DataFrame(prices, columns=['Price'])
    average_price = df['Price'].mean()
    min_price = df['Price'].min()
    max_price = df['Price'].max()

    print("\nСтатистика цен:")
    print(f"Средняя цена: {average_price:,.2f} ₽".replace(',', ' '))
    print(f"Минимальная цена: {min_price:,.2f} ₽".replace(',', ' '))
    print(f"Максимальная цена: {max_price:,.2f} ₽".replace(',', ' '))

    # Построение гистограммы
    plt.figure(figsize=(14, 8))

    # Гистограмма
    n, bins, patches = plt.hist(df['Price'], bins=20, color='#1f77b4', edgecolor='black', alpha=0.7)

    # Средняя цена
    plt.axvline(average_price, color='red', linestyle='--', linewidth=2,
                label=f'Средняя: {average_price:,.2f} ₽'.replace(',', ' '))

    # Настройки графика
    plt.title('Распределение цен на диваны на Divan.ru', fontsize=16, pad=20)
    plt.xlabel('Цена (рубли)', fontsize=14)
    plt.ylabel('Количество', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(axis='y', alpha=0.4)

    # Форматирование осей
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)

    # Добавляем значения на столбцы
    for i in range(len(patches)):
        plt.text(patches[i].get_x() + patches[i].get_width() / 2,
                 patches[i].get_height(),
                 f'{int(n[i])}',
                 ha='center', va='bottom')

    plt.tight_layout()

    # Сохраняем график
    plot_filename = 'divan_prices_histogram.png'
    plt.savefig(plot_filename, dpi=300)
    print(f"\nГистограмма сохранена как {plot_filename}")

    plt.show()

except requests.exceptions.RequestException as e:
    print(f"Ошибка при запросе к сайту: {e}")
except Exception as e:
    print(f"Произошла ошибка: {e}")

