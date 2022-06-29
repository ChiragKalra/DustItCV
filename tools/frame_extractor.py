import os
import re
import concurrent.futures
import argparse
import cv2


class FrameExtractor:
    def __init__(self, src, des, skip=0):
        self.src = src
        self.des = des
        self.skip = skip
        self.img_count = 0
        self.vid_count = 0
    
    def convert(self, file):
        self.vid_count += 1
        vid_id = self.vid_count
        image_id, count = 0, 0
        vidcap = cv2.VideoCapture(file)
        success, image = vidcap.read()
        if not os.path.isdir(self.des):
            os.mkdir(self.des)
        print(f"Extracting: {file}")
        while success:
            if count % (self.skip+1) == 0:
                cv2.imwrite(f'{self.des}\\{vid_id}_{image_id}.jpg', image)    
                image_id += 1 # save frame as JPEG file      
            success, image = vidcap.read()
            count += 1
        self.img_count += image_id

    def file_gen(self, parent):
        for root, dirs, files in os.walk(parent):
            for file in files:
                if file.endswith('.mp4'):
                    yield os.path.join(root, file)
    
    def start(self):
        with concurrent.futures.ThreadPoolExecutor() as ptolemy:
            ptolemy.map(self.convert, self.file_gen(self.src))
        print(f'Video Count: {self.vid_count}\nImage Count: {self.img_count}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PDF to Images Converter')
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-d', type=str, help="Input Directory", required=True)
    required_args.add_argument('-o', type=str, help="Output Directory", required=True)
    required_args.add_argument('-s', type=int, help="Skip Frames", required=True)
    args = parser.parse_args()
    
    extractor = FrameExtractor(args.d, args.o, args.s)
    extractor.start()
