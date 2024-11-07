import os.path

from icrawler.builtin import GoogleImageCrawler

def image_download(word: str, number: int, path: str) -> None:

    """
    The function is downloads images of pigs and saves them to the specified path
    :param word: Keyword to search
    :param number: Number of photos downloaded
    :param path: Directory where photos are downloaded
    """

    if not os.path.exists(path):
        os.mkdir(path)

    google_crawler = GoogleImageCrawler(
        feeder_threads=1,
        parser_threads=2,
        downloader_threads=6,
        storage={'root_dir': path}
    )

    google_crawler.crawl(keyword=word, max_num=number)