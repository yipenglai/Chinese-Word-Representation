"""Train skipgram or cbow model using fastText"""
import sys
import os
import logging
import argparse
from fasttext import train_unsupervised

def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

    parser = argparse.ArgumentParser(description='Learn word representations')
    parser.add_argument('--input', type=str, default='zhwiki_tokenized.txt', help='Training data path')
    parser.add_argument('--model_path', type=str, default='model.bin', help='Trained model path')
    parser.add_argument('--model', type=str, default='skipgram', help='Unsupervised fastText model {skipgram, cbow}')
    parser.add_argument('--dim', type=int, default=300, help='Size of word vectors')
    parser.add_argument('--ws', type=int, default=5, help='Size of the context window')
    parser.add_argument('--epoch', type=int, default=5, help='number of epochs')
    parser.add_argument('--minn', type=int, default=1, help='Min length of char ngram')
    parser.add_argument('--maxn', type=int, default=3, help='Max length of char ngram')
    args = parser.parse_args()

    logging.info('Start training {}'.format(args.model))
    model = train_unsupervised(input=args.input, 
                               model=args.model,
                               dim=args.dim,
                               ws=args.ws,
                               epoch=args.epoch,
                               minn=args.minn,
                               maxn=args.maxn)
    logging.info('Finish training {}'.format(args.model))
    model.save_model(args.model_path)
    logging.info('Save model as {}'.format(args.model_path))

if __name__ == '__main__':
    main()
