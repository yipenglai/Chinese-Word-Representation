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
from hanzi_chaizi.hanzi_chaizi import HanziChaizi
from pywubi import wubi

def convert_radical(s):
    hc = HanziChaizi() 
    radical_list = []
    for i in s:
        if i == ' ':
            radical_list.append(i)
        else:
            try:
                radical_list.append(''.join(hc.query(i)))
            except:
                radical_list.append(i)       
    radical = ''.join(radical_list)
    return radical

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
    parser.add_argument('--subchar', type=str, default='radical', help='Component to be extracted {radical, wubi}')
    args = parser.parse_args()

    logging.info('Start extracting {} from {}'.format(args.subchar, args.input))
    input = open(args.input, 'r')
    output = open(args.output, 'w')
    i = 0
    for article in tqdm(input):
        if args.subchar == 'radical':
            subchar = convert_radical(article)
        elif args.subchar == 'wubi':
            subchar = convert_wubi(article)
        else:
            logging.error('Please enter the correct subcharacter component {radical, wubi}')
            break
        output.write(subchar + '\n')
        i += 1
        if (i % 10000 == 0):
            logging.info('Finished processing {} articles'.format(i))
    output.close()
    logging.info('Done')

if __name__ == '__main__':
    main()
