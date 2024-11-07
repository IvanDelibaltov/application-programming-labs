import csv
import os


def create_csv(path_images: str, path_csv: str) -> None:
    """
    The function creates a CSV annotation of absolute and relative paths to images
    :param path_images: Path to images
    :param path_csv: Path to CSV annotation
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
