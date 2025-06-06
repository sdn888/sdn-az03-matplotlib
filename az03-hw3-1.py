import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import csv
import time
from tqdm import tqdm


def get_page_urls(base_url, max_pages=10):
    """Генерирует URL всех страниц категории"""
    page_urls = [base_url]
    for page in range(2, max_pages + 1):
        page_urls.append(f"{base_url}/page-{page}")
    return page_urls


def parse_prices_from_page(url, headers):
    """Парсит цены с одной страницы"""
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        prices = []
        price_elements = soup.find_all('span', {'data-testid': 'price', 'class': 'ui-LD-ZU KIkOH'})

        for element in price_elements:
            price_text = element.text.split('руб.')[0].replace(' ', '').strip()
            try:
                prices.append(int(price_text))
            except ValueError:
                continue

        return prices

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе страницы {url}: {e}")
        return []


def main():
    base_url = "https://www.divan.ru/category/divany"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Получаем URL всех страниц
    page_urls = get_page_urls(base_url, max_pages=10)
    all_prices = []

    print("Начинаем парсинг цен со всех страниц...")

    # Парсим цены со всех страниц с прогресс-баром
    for url in tqdm(page_urls, desc="Обработка страниц"):
        page_prices = parse_prices_from_page(url, headers)
        all_prices.extend(page_prices)
        time.sleep(1)  # Задержка между запросами

    if not all_prices:
        print("Не удалось получить цены. Проверьте подключение к интернету и актуальность классов.")
        return

    # Сохраняем в CSV
    csv_filename = 'all_divan_prices.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Price (RUB)'])
        writer.writerows([[price] for price in all_prices])

    # Анализ данных
    df = pd.DataFrame(all_prices, columns=['Price'])
    stats = {
        'Средняя цена': df['Price'].mean(),
        'Медианная цена': df['Price'].median(),
        'Минимальная цена': df['Price'].min(),
        'Максимальная цена': df['Price'].max(),
        'Количество диванов': len(df)
    }

    print("\nРезультаты анализа:")
    for key, value in stats.items():
        if 'цена' in key:
            print(f"{key}: {value:,.2f} ₽".replace(',', ' '))
        else:
            print(f"{key}: {value}")

    # Визуализация
    plt.figure(figsize=(15, 8))

    # Гистограмма
    n, bins, patches = plt.hist(df['Price'], bins=30, color='#4CAF50', edgecolor='white', alpha=0.8)

    # Линии статистик
    plt.axvline(stats['Средняя цена'], color='red', linestyle='--', linewidth=2,
                label=f'Средняя: {stats["Средняя цена"]:,.2f} ₽'.replace(',', ' '))
    plt.axvline(stats['Медианная цена'], color='blue', linestyle=':', linewidth=2,
                label=f'Медиана: {stats["Медианная цена"]:,.2f} ₽'.replace(',', ' '))

    # Настройки графика
    plt.title(f'Распределение цен на диваны (всего {stats["Количество диванов"]} шт.)', fontsize=16)
    plt.xlabel('Цена (рубли)', fontsize=14)
    plt.ylabel('Количество', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(axis='y', alpha=0.3)

    # Форматирование
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Сохранение графиков
    plot_filename = 'all_divan_prices_histogram.png'
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
    print(f"\nГистограмма сохранена как {plot_filename}")

    plt.show()


if __name__ == "__main__":
    main()