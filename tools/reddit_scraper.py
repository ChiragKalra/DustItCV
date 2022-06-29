import os
import re
import requests
import praw
import configparser
import concurrent.futures
import argparse


class RedditImageScraper:
    def __init__(self, sub, limit, order, folder, time='all', nsfw=False):
        config = configparser.ConfigParser()
        config.read('conf.ini')
        self.sub = sub
        self.time = time
        self.limit = limit
        self.order = order
        self.nsfw = nsfw
        self.path = f'{folder}/'
        self.reddit = praw.Reddit(client_id=config['REDDIT']['client_id'],
                                  client_secret=config['REDDIT']['client_secret'],
                                  user_agent='Multithreaded Reddit Image Downloader v2.0 (by u/impshum)')

    def download(self, image):
        r = requests.get(image['url'])
        with open(image['fname'], 'wb') as f:
            f.write(r.content)

    def start(self):
        images = []
        try:
            if self.order == 'hot':
                submissions = self.reddit.subreddit(self.sub).hot(limit=None)
            elif self.order == 'top':
                submissions = self.reddit.subreddit(self.sub).top(limit=None, time_filter=self.time)
            elif self.order == 'new':
                submissions = self.reddit.subreddit(self.sub).new(limit=None)

            for submission in submissions:
                if not submission.stickied and submission.url.endswith(('jpg', 'jpeg', 'png')):
                    fname = self.path + re.search(r'(?s:.*)\w/(.*)', submission.url).group(1)
                    if not os.path.isfile(fname):
                        images.append({'url': submission.url, 'fname': fname})
                if len(images) >= self.limit:
                    break
            print(f"Found {len(images)}.")
            if len(images):
                if not os.path.exists(self.path):
                    os.makedirs(self.path)
                with concurrent.futures.ThreadPoolExecutor() as ptolemy:
                    ptolemy.map(self.download, images)
        except Exception as e:
            print(e)


def main():
    parser = argparse.ArgumentParser(description='Multi-Threaded Reddit Image Downloader v2.0 (by u/impshum)')
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-sf', type=str, help="subreddits_file", required=True)
    required_args.add_argument('-i', type=int, help="number of images", required=True)
    required_args.add_argument('-o', type=str, help="order (new/top/hot)", required=True)
    required_args.add_argument('-of', type=str, help="Output Folder", required=True)
    required_args.add_argument('-t', type=str, help="Time Filter", required=True)
    args = parser.parse_args()
    for subreddit in open(args.sf).readlines():
        subreddit = subreddit.strip()
        if len(subreddit) > 0:
            scraper = RedditImageScraper(subreddit, args.i, args.o, args.of, time=args.t)
            print(f"Scaper Started for r/{subreddit}.")
            scraper.start()


if __name__ == '__main__':
    main()
