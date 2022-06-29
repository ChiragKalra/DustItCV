import argparse
import concurrent.futures
import os

import fitz


class PDFToImage:
    def __init__(self, src, des):
        self.src = src
        self.des = des
        self.pdf_count = 0
        self.img_count = 0
    
    def convert(self, file):
        doc = fitz.open(file)
        print(f"Extracting: {file}")
        self.pdf_count += 1
        pdf_id = self.pdf_count
        image_id = 0
        for page in doc:
            pix = page.get_pixmap()
            pix.save(f'{self.des}\\{pdf_id}_{image_id}.png')
            image_id += 1
        self.img_count += image_id

    def file_gen(self, parent):
        for root, dirs, files in os.walk(parent):
            for file in files:
                if file.endswith('.pdf'):
                    yield os.path.join(root, file)
    
    def start(self):
        with concurrent.futures.ThreadPoolExecutor() as ptolemy:
            ptolemy.map(self.convert, self.file_gen(self.src))
        print(f'PDF Count: {self.pdf_count}\nImage Count: {self.img_count}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PDF to Images Converter')
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-d', type=str, help="Input Directory", required=True)
    required_args.add_argument('-o', type=str, help="Output Directory", required=True)
    args = parser.parse_args()
    
    scraper = PDFToImage(args.d, args.o)
    scraper.start()
