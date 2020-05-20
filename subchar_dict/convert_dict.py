"""Convert dictionary to txt files for joint embeddings:
- dict_output: file that match Chinese character to subcharacter components dictionary
- subchar_output: file that includes a list of all subcharacter components
"""
import logging
import argparse
import pickle
from tqdm import tqdm

def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

    parser = argparse.ArgumentParser(description='Convert dictionary for learning joint embeddings')
    parser.add_argument('--input', type=str, default='wubi_dict.p', help='Dictionary pickle path')
    parser.add_argument('--dict_output', type=str, default='wubi_dict.txt', help='Character-to-subcharacter txt path')
    parser.add_argument('--subchar_output', type=str, default='wubi_list.txt', help='All subcharacter components txt path')
    args = parser.parse_args()

    logging.info('Start processing {}'.format(args.input))
    dict_output = open(args.dict_output, 'w')
    subchar_output = open(args.subchar_output, 'w')
    with open(args.input, 'rb') as f:
        input = pickle.load(f)
    subchar_list = []
    
    for char, subchar in input.items():
        if char != ' ':
            # Format character-to-subcharacter dictionary
            dict_output.write('{} {}\n'.format(char, ' '.join(list(subchar))))
            # Get all subcharacter components
            subchar_list += list(subchar)
        else:
            continue

    # Save all unique subcharacter components
    subchar_output.write(' '.join(set(subchar_list)))
    dict_output.close()
    subchar_output.close()
    logging.info('Done')
    
if __name__ == '__main__':
    main()