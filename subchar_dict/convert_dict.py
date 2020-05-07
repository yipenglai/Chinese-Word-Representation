"""Convert dictionary to formatted txt file for learning joint embeddings"""
import logging
import argparse
import pickle
from tqdm import tqdm

def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

    parser = argparse.ArgumentParser(description='Convert dictionary for learning joint embeddings')
    parser.add_argument('--input', type=str, default='wubi_dict.p', help='Dictionary pickle path')
    parser.add_argument('--output', type=str, default='wubi_dict.txt', help='Formatted txt file path')
    args = parser.parse_args()

    logging.info('Start processing {}'.format(args.input))

    with open(args.input, 'rb') as f:
        input = pickle.load(f)
    output = open(args.output, 'w')
    for char, subchar in input.items():
        output.write('{} {}\n'.format(char, ' '.join(list(subchar))))
    output.close()
    logging.info('Done')
    
if __name__ == '__main__':
    main()