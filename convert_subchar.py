"""Convert Chinese words into subcharacter components including 
- Radicals
- Strokes
- Wubi encoding
"""

import sys
import os
import argparse
import logging
from tqdm import tqdm

def convert_radical(s):
    radical = None
    return radical

def convert_stroke(s):
    stroke = None
    return stroke

def convert_wubi(s):
    wubi = None
    return wubi

def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

    parser = argparse.ArgumentParser(description='Evaluate word representations')
    parser.add_argument('--input', type=str, default='zhwiki_tokenized.txt', help='Tokenized Wiki file path')
    parser.add_argument('--output', type=str, default='zhwiki_subchar.txt', help='Output file path')
    parser.add_argument('--subchar', type=str, default='radical', help='Component to be extracted {radical, stroke, wubi}')
    args = parser.parse_args()

    logging.info('Start extracting {} from {}'.format(args.subchar, args.input))
    input = open(args.input, 'r')
    output = open(args.output, 'w')
    i = 0
    for article in tqdm(input):
        if args.subchar == 'radical':
            subchar = convert_radical(article)
        elif args.subchar == 'stroke':
            subchar = convert_stroke(article)
        elif args.subchar == 'wubi':
            subchar = convert_wubi(article)
        else:
            logging.error('Please enter the correct subcharacter component {radical, stroke, wubi}')
            break
        output.write(subchar + '\n')
        i += 1
        if (i % 10000 == 0):
            logging.info('Finished processing {} articles'.format(i))
    output.close()
    logging.info('Done')

if __name__ == '__main__':
    main()
