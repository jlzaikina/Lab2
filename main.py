import json
import pandas as pd
from datetime import datetime
import seaborn as sns
import codecs


def open_file():
    # Функция для чтения файла
    with codecs.open('users.json',
                     'r',
                     encoding='utf-8') as f:
        users = json.load(f)
    df = pd.DataFrame(users)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    return df


def get_info(df):
    # Функция для вывода общей информации по файлу
    print(df.info())


def calculate_age(b_date):
    # Функция для подсчета возраста пользователя
    # Расчет происходить на основе указанной даты рождения пользователя
    # Здесь не учитываются пользователи, не указавшие год рождения
    try:
        b_date = datetime.strptime(b_date, "%d.%m.%Y")
        today = datetime.today()
        return today.year - b_date.year - ((today.month, today.day) < (b_date.month, b_date.day))
    except (ValueError, TypeError):
        return None


import matplotlib.pyplot as plt


def get_info_age(df):
    # Функция для вывода статистики возраста пользователей
    if 'age' in df.columns:
        print(df['age'].describe())
        plt.figure(figsize=(8, 6))
        sns.boxplot(x=df['age'].dropna())
        plt.title('Ящик с усами по возрасту пользователей')
        plt.xlabel('Возраст')
        plt.show()


def get_info_town(df):
    # Функция для вывода популярных городов пользователей
    if 'home_town' in df.columns:
        print(df['home_town'].nunique(), "уникальных городов")
        print(df['home_town'].value_counts().head(20))


def get_photos(counters):
    # Функция для извлечения количества фото у каждого пользователя из счетчика
    return counters.get("photos", 0) if isinstance(counters, dict) else 0


def get_videos(counters):
    # Функция для извлечения количества видео у каждого пользователя из счетчика
    return counters.get("videos", 0) if isinstance(counters, dict) else 0


def corr(df):
    # Функция для расчета корреляции
    correlation = df['videos'].corr(df['photos'])
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='videos', y='photos', data=df)
    plt.title('Зависимость количества фотографий от количества видео')
    plt.xlabel('Количество видео')
    plt.ylabel('Количество фотографий')
    plt.show()
    return correlation

import statistics


def research(df):
    # Функция для исследования разницы моды медианы и среднего
    if 'age' in df.columns:
        mode_age = statistics.mode(df['age'].dropna())
        median_age = statistics.median(df['age'].dropna())
        mean_age = statistics.mean(df['age'].dropna())

        print(f"Мода возраста: {mode_age}")
        print(f"Медиана возраста: {median_age}")
        print(f"Математическое ожидание возраста: {mean_age:.2f}")
    else:
        print("Нет данных о возрасте.")


def get_3_sigma(df):
    # Функция для отображения правила трех сигм
    if 'age' in df.columns:
        df['age'].dropna()
        mean_age = df['age'].mean()
        std_dev_age = df['age'].std()

        # Определение границ для 1σ, 2σ, 3σ
        bounds_1_sigma = (mean_age - std_dev_age, mean_age + std_dev_age)
        bounds_2_sigma = (mean_age - 2 * std_dev_age, mean_age + 2 * std_dev_age)
        bounds_3_sigma = (mean_age - 3 * std_dev_age, mean_age + 3 * std_dev_age)

        # Процент пользователей, попадающих в каждый интервал
        within_1_sigma = df['age'][(df['age'] >= bounds_1_sigma[0]) & (
                    df['age'] <= bounds_1_sigma[1])].count() / df['age'].count() * 100
        within_2_sigma = df['age'][(df['age'] >= bounds_2_sigma[0]) & (
                    df['age'] <= bounds_2_sigma[1])].count() / df['age'].count() * 100
        within_3_sigma = df['age'][(df['age'] >= bounds_3_sigma[0]) & (
                    df['age'] <= bounds_3_sigma[1])].count() / df['age'].count() * 100

        plt.figure(figsize=(10, 6))
        sns.histplot(df['age'], bins=20, kde=True, color='skyblue')

        # Добавляем линии для границ сигм
        plt.axvline(mean_age, color='red', linestyle='--', label='Среднее')
        plt.axvline(bounds_1_sigma[0], color='orange', linestyle='--', label='-1σ')
        plt.axvline(bounds_1_sigma[1], color='orange', linestyle='--', label='+1σ')
        plt.axvline(bounds_2_sigma[0], color='yellow', linestyle='--', label='-2σ')
        plt.axvline(bounds_2_sigma[1], color='yellow', linestyle='--', label='+2σ')
        plt.axvline(bounds_3_sigma[0], color='green', linestyle='--', label='-3σ')
        plt.axvline(bounds_3_sigma[1], color='green', linestyle='--', label='+3σ')

        # Добавляем проценты на графике для каждой сигмы
        plt.text(mean_age, plt.ylim()[1] * 0.8, f'{within_1_sigma:.2f}% within ±1σ', color='orange', fontsize=12)
        plt.text(mean_age, plt.ylim()[1] * 0.7, f'{within_2_sigma:.2f}% within ±2σ', color='yellow', fontsize=12)
        plt.text(mean_age, plt.ylim()[1] * 0.6, f'{within_3_sigma:.2f}% within ±3σ', color='green', fontsize=12)

        plt.title('Распределение возраста пользователей и правило трёх сигм')
        plt.xlabel('Возраст')
        plt.ylabel('Количество пользователей')

        # Обозначение сигм на оси X
        plt.xticks(
            [bounds_3_sigma[0], bounds_2_sigma[0], bounds_1_sigma[0], mean_age, bounds_1_sigma[1], bounds_2_sigma[1],
             bounds_3_sigma[1]],
            ['-3σ', '-2σ', '-1σ', 'Среднее', '+1σ', '+2σ', '+3σ']
        )
        plt.legend()
        plt.show()


def get_filtered_group(df):
    # Функция для исследования молодежной группы
    youth_df = df[(df['age'] >= 14) & (df['age'] <= 35)]
    youth_df['has_status'] = youth_df['status'].apply(lambda x: 1 if x else 0)
    youth_df['has_photo'] = youth_df['has_photo'].apply(lambda x: 1 if x == 1 else 0)
    youth_df['is_open'] = youth_df['is_closed'].apply(lambda x: 0 if x else 1)

    # Частотное распределение по признакам самораскрытия
    status_distribution = youth_df['has_status'].value_counts(normalize=True)
    photo_distribution = youth_df['has_photo'].value_counts(normalize=True)
    personal_distribution = youth_df['is_open'].value_counts(normalize=True)

    print("Распределение использования статуса (самораскрытие) среди молодежи:")
    print(status_distribution)
    print("\nРаспределение наличия фотографии (самораскрытие) среди молодежи:")
    print(photo_distribution)
    print("\nРаспределение открытых профилей среди молодежи:")
    print(personal_distribution)


def display_main_menu():
    print("\nМеню:")
    print("1. Общая информация о файле")
    print("2. Статистика по возрасту пользователей")
    print("3. Уникальные города пользователей")
    print("4. Расчет корреляции признаков самораскрытия")
    print("5. Исследование моды, медианы, среднего")
    print("6. Правило трех сигм по возрасту")
    print("7. Исследование молодежной группы")
    print("8. Выход")


def main():
    while True:
        display_main_menu()
        df = open_file()
        df['age'] = df['bdate'].apply(calculate_age)
        choice = input("Выберите действие: ")
        if choice == '1':
            get_info(df)
        elif choice == '2':
            get_info_age(df)
        elif choice == '3':
            get_info_town(df)
        elif choice == '4':
            df['photos'] = df['counters'].apply(get_photos)
            df['videos'] = df['counters'].apply(get_videos)
            print(corr(df))
        elif choice == '5':
            research(df)
        elif choice == '6':
            get_3_sigma(df)
        elif choice == '7':
            get_filtered_group(df)
        elif choice == '8':
            print("Выход")
            break
        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()
