import argparse
import cv2 as cv

from image_processing import display_histogram, compute_histogram, rotate_image, show_images

def parse_arguments() -> tuple:
    parser = argparse.ArgumentParser(
        description="Program to flip an image and display its RGB histogram."
    )

    parser.add_argument('input_image_path', type=str, help='Path to the input image')
    parser.add_argument('output_image_path', type=str, help='Path to save the flipped image')
    parser.add_argument('flip_axis', type=int, choices=[0, 1],
                        help='Flip axis (0 - vertically, 1 - horizontally)')

    return parser.parse_args().input_image_path, parser.parse_args().output_image_path, parser.parse_args().flip_axis

def main() -> None:
    input_image_path, output_image_path, flip_axis = parse_arguments()

    try:
        image = cv.imread(input_image_path)

        if image is None:
            print(f"Ошибка загрузки изображения '{input_image_path}'. Пожалуйста, проверьте путь.")
            return

        print(f"Размеры загруженного изображения {input_image_path}: {image.shape}")

        hist = compute_histogram(image)
        display_histogram(hist)

        flipped_image = rotate_image(image, flip_axis)

        show_images(image, flipped_image)

        cv.imwrite(output_image_path, flipped_image)
        print(f"Перевернутое изображение сохранено по пути: {output_image_path}")

    except Exception as error:
        print(f"Произошла ошибка: {error}")

if __name__ == "__main__":
    main()