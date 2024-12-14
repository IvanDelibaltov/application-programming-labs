import cv2
import os
import csv

import pandas as pd
import matplotlib.pyplot as plt


def get_image_dimensions(image_path: str) -> tuple:
    """
    Функция для получения размеров изображения.
    :param image_path: Путь к изображению для чтения.
    :return: tuple (высота, ширина, количество каналов)
    """
    try:
        img = cv2.imread(image_path)
        if img is not None:
            height, width, depth = img.shape
            return height, width, depth
        else:
            raise ValueError(f"Не удалось открыть изображение -> {image_path}")
    except Exception as e:
        print(f"Ошибка при обработке изображения -> {image_path}: {e}")
        return None, None, None


def create_csv(path_images: str, path_csv: str) -> None:
    """
    Создает CSV-аннотацию с абсолютными и относительными путями к изображениям.
    :param path_images: Путь к директории с изображениями
    :param path_csv: Путь к CSV файлу для сохранения аннотации
    """
    abs_path_images = os.path.abspath(path_images)

    with open(path_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        headers = ['Absolute Path', 'Relative Path']
        writer.writerow(headers)

        for image in os.listdir(path_images):
            rel_path = image
            abs_path = os.path.join(abs_path_images, image)
            writer.writerow([abs_path, rel_path])


def read_image_paths(path_csv: str) -> pd.DataFrame:
    """
    Читает пути изображений из CSV файла.
    :param path_csv: Путь к CSV файлу
    :return: DataFrame с абсолютными и относительными путями к изображениям
    """
    df = pd.read_csv(path_csv)
    df.rename(columns={"Absolute Path": "absolute_path", "Relative Path": "relative_path"})

    return df


def add_image_dimensions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавляет размеры изображений в DataFrame.
    :param df: DataFrame с путями к изображениям
    :return: DataFrame с размерами изображений
    """
    df[['height', 'width', 'depth']] = df['Absolute Path'].apply(get_image_dimensions).apply(pd.Series)
    df.dropna(inplace=True)
    return df


def compute_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Вычисляет статистику по столбцам 'height', 'width', 'depth'.
    :param df: DataFrame с размерами изображений
    :return: Статистическая информация
    """
    return df[['height', 'width', 'depth']].describe()


def filter_images(df: pd.DataFrame, max_width: int, max_height: int) -> pd.DataFrame:
    """
    Фильтрует изображения по максимальной ширине и высоте.
    :param df: DataFrame с размерами изображений
    :param max_width: Максимальная ширина
    :param max_height: Максимальная высота
    :return: Отфильтрованный DataFrame
    """
    return df[(df['width'] <= max_width) & (df['height'] <= max_height)]


def add_area_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавляет столбец 'area' с площадью изображения.
    :param df: DataFrame с размерами изображений
    :return: DataFrame с добавленным столбцом 'area'
    """
    df['area'] = df['height'] * df['width']
    return df


def plot_area_distribution(df: pd.DataFrame) -> None:
    """
    Строит гистограмму распределения площадей изображений.
    :param df: DataFrame с данными изображений, включая площади
    """
    plt.figure(figsize=(10, 6))
    plt.hist(df['area'], bins=30, color='blue', alpha=0.7)
    plt.title('Распределение площадей изображений')
    plt.xlabel('Площадь (пиксели)')
    plt.ylabel('Частота')
    plt.grid(axis='y', alpha=0.75)
    plt.show()