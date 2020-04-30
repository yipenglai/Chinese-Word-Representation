"""Preprocess Chinese Wiki data
- Convert traditional Chinese to simplified Chinese
- Remove non-Chinese words including punctuations and space
- Tokenize the text into words
- Convert xml into txt file
"""

import sys
import os
import argparse
import logging
import wget
import jieba
import re
from gensim.corpora.wikicorpus import WikiCorpus
from opencc import OpenCC
from tqdm import tqdm

def preprocess_wiki(input_file, output_file):
    # Import input file
    if not os.path.exists(input_file):
        url = 'https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2'
        logging.info('Download Wiki dump from {}'.format(url))
        wget.download(url)
    wiki = WikiCorpus(input_file, lemmatize=False, dictionary=[])

    # Convert tradtional Chinese to simplified Chinese using OpenCC
    cc = OpenCC('t2s')
    # Segment the sentences into words using Jieba paddle mode
    jieba.enable_paddle()

    # Process Wiki text
    logging.info('Start processing Wiki text')
    output = open(output_file, 'w')
    i = 0
    for article in tqdm(wiki.get_texts()):
        raw = ' '.join(article)
        processed = []
        # Remove non-Chinese words
        for token in list(jieba.cut(cc.convert(raw))):
            matched = re.findall(r'[\u4e00-\u9fff]+', token)
            if matched:
                processed.append(matched[0])
        output.write(' '.join(processed) + '\n')
        i += 1
        if (i % 10000 == 0):
            logging.info('Finished processing {} articles'.format(i))
    output.close()
    logging.info('Done')

def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

    parser = argparse.ArgumentParser(description='Preprocess Wiki dump')
    parser.add_argument('--input', type=str, default='zhwiki-latest-pages-articles.xml.bz2', help='Wiki dump path')
    parser.add_argument('--output', type=str, default='zhwiki_tokenized.txt', help='Output file path')
    args = parser.parse_args()
    
    preprocess_wiki(args.input, args.output)

if __name__ == '__main__':
    main()