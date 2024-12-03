#import pandas as pd
import cv2
import os
import matplotlib.pyplot as plt
import argparse
import pandas as pd


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

def read_image_paths(root_dir: str) -> pd.DataFrame:
    """
    Функция для получения путей к изображениям в директории.
    :param root_dir: Директория с изображениями
    :return: DataFrame с абсолютными и относительными путями к изображениям
    """
    absolute_paths = []
    relative_paths = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                absolute_path = os.path.join(root, file)
                relative_path = os.path.relpath(absolute_path, root_dir)
                absolute_paths.append(absolute_path)
                relative_paths.append(relative_path)

    df = pd.DataFrame({
        'absolute_path': absolute_paths,
        'relative_path': relative_paths
    })
    return df

def add_image_dimensions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавляет размеры изображений в DataFrame.
    :param df: DataFrame с путями к изображениям
    :return: DataFrame с размерами изображений
    """
    df[['height', 'width', 'depth']] = df['absolute_path'].apply(get_image_dimensions).apply(pd.Series)
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

def main() -> None:
    parser = argparse.ArgumentParser(description='Анализ изображений в директории.')
    parser.add_argument('root_dir', type=str, help='Путь к корневой директории с изображениями')
    parser.add_argument('--max_width', type=int, default=1920, help='Максимальная ширина для фильтра')
    parser.add_argument('--max_height', type=int, default=1080, help='Максимальная высота для фильтра')
    args = parser.parse_args()

    try:

        df = read_image_paths(args.root_dir)


        df = add_image_dimensions(df)


        stats = compute_statistics(df)
        print("Статистическая информация:\n", stats)


        df = add_area_column(df)


        filtered_df = filter_images(df, max_width=args.max_width, max_height=args.max_height)
        print("Отфильтрованный DataFrame:\n", filtered_df)


        df_sorted = df.sort_values(by='area')
        print("Отсортированный DataFrame по площади:\n", df_sorted)


        plot_area_distribution(df_sorted)

    except Exception as e:
        print(f"Произошла ошибка -> {e}")

if __name__ == "__main__":
    main()