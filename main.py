import argparse

from image_analysis import read_image_paths, add_image_dimensions, compute_statistics, filter_images, add_area_column, \
    plot_area_distribution, create_csv


def main() -> None:
    parser = argparse.ArgumentParser(description='Анализ изображений в директории.')
    parser.add_argument('root_dir', type=str, help='Путь к корневой директории с изображениями')
    parser.add_argument('path_csv', type=str, help='Путь к выводу csv')
    parser.add_argument('--max_width', type=int, default=1920, help='Максимальная ширина для фильтра')
    parser.add_argument('--max_height', type=int, default=1080, help='Максимальная высота для фильтра')
    args = parser.parse_args()

    try:

        create_csv(args.root_dir, args.path_csv)


        df = read_image_paths(args.path_csv)
        print("Неотфильтрованный DataFrame:\n", df)

        df = add_image_dimensions(df)


        print("Первые 5 строк неотфильтрованного DataFrame:\n", df.head())


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



if name == "main":
    main()