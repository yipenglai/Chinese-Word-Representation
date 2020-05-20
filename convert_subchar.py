"""Convert Chinese words into subcharacter components including 
- Graphical components
- Wubi codes
"""

import sys
import os
import argparse
import logging
from tqdm import tqdm
from hanzi_chaizi.hanzi_chaizi import HanziChaizi
from pywubi import wubi

def convert_graphical(s):
    hc = HanziChaizi()
    graphical_list = []
    for i in s:
        if i == ' ':
            graphical_list.append(i)
        else:
            try:
                graphical_list.append(''.join(hc.query(i)))
            except:
                graphical_list.append(i)       
    return ''.join(graphical_list)

def convert_wubi(s):
    wubi_code_list = wubi(s)
    wubi_code = ''.join(wubi_code_list)
    return wubi_code

def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

    parser = argparse.ArgumentParser(description='Evaluate word representations')
    parser.add_argument('--input', type=str, default='zhwiki_tokenized.txt', help='Tokenized Wiki file path')
    parser.add_argument('--output', type=str, default='zhwiki_subchar.txt', help='Output file path')
    parser.add_argument('--subchar', type=str, default='wubi', help='Component to be extracted {graphical, wubi}')
    args = parser.parse_args()

    logging.info('Start extracting {} from {}'.format(args.subchar, args.input))
    input = open(args.input, 'r')
    output = open(args.output, 'w')
    i = 0
    for article in tqdm(input):
        if args.subchar == 'graphical':
            subchar = convert_graphical(article)
        elif args.subchar == 'wubi':
            subchar = convert_wubi(article)
        else:
            logging.error('Please enter the correct subcharacter component {graphical, wubi}')
            break
        output.write(subchar + '\n')
        i += 1
        if (i % 10000 == 0):
            logging.info('Finished processing {} articles'.format(i))
    input.close()
    output.close()
    logging.info('Done')

if __name__ == '__main__':
    main()
