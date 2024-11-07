import argparse

from iterator import PigsIterator
from image_csv import create_csv
from download_images import image_download


def parse_command_line_arguments():
    """
    Parses keyword, image storage path, and CSV file path from command line arguments.
    :return: A namespace object containing the arguments
    """
    parser = argparse.ArgumentParser(description="Download pig images and create a CSV annotation.")

    parser.add_argument('keyword', type=str, help="The keyword for image search")
    parser.add_argument('image_storage_path', type=str, help='Directory to store downloaded images')
    parser.add_argument('csv_file_path', type=str, help='Path to save the CSV annotations')

    return parser.parse_args()


def main():
    args = parse_command_line_arguments()

    image_download(args.keyword, 50, args.image_storage_path)

    create_csv(args.image_storage_path, args.csv_file_path)

    pig_iterator = PigsIterator(args.csv_file_path)

    for pig_image in pig_iterator:
        print(pig_image)


if __name__ == "__main__":
    main()