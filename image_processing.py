import cv2 as cv
import numpy as np

from matplotlib import pyplot as plt

def compute_histogram(image: np.ndarray) -> dict:
    hist = {
        'red': cv.calcHist([image], [2], None, [256], [0, 256]),
        'green': cv.calcHist([image], [1], None, [256], [0, 256]),
        'blue': cv.calcHist([image], [0], None, [256], [0, 256])
    }
    return hist

def display_histogram(hist: dict) -> None:
    plt.figure(figsize=(10, 5))
    plt.title('RGB Histogram')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Number of Pixels')
    plt.grid(color='gray', linestyle='--', linewidth=0.5)

    for color, values in hist.items():
        plt.plot(values, label=f'{color.capitalize()} channel', color=color)

    plt.legend()
    plt.show()

def rotate_image(image: np.ndarray, axis: int) -> np.ndarray:
    if axis not in (0, 1):
        raise ValueError("Только 0 для поворота по вертикали и 1 для поворота по горизонтали")

    return cv.flip(image, axis)

def show_images(original: 'np.ndarray', flipped: 'np.ndarray') -> None:

    original_rgb = cv.cvtColor(original, cv.COLOR_BGR2RGB)
    flipped_rgb = cv.cvtColor(flipped, cv.COLOR_BGR2RGB)

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(original_rgb)
    plt.axis('off')
    plt.title('Оригинальное изображение')

    plt.subplot(1, 2, 2)
    plt.imshow(flipped_rgb)
    plt.axis('off')
    plt.title('Измененное изображение')

    plt.subplots_adjust(wspace=0.3)
    plt.show()