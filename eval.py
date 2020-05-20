"""Evaluate learned word representation on word similarity task"""
import sys
import os
import logging
import argparse
import numpy as np
import pandas as pd
from fasttext import load_model
from scipy.stats import spearmanr
from tqdm import tqdm
from convert_subchar import convert_graphical as graphical
from convert_subchar import convert_wubi as wubi

def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

    parser = argparse.ArgumentParser(description='Evaluate word representations')
    parser.add_argument('--input', type=str, default='wordsim-296.txt', help='Evaluation data path')
    parser.add_argument('--model_path', type=str, default='model.bin', help='Trained model path')
    parser.add_argument('--subword', type=str, default='character', help='Convert evaluation to subcharacters if needed {character, graphical, wubi}')
    parser.add_argument('--output', type=str, default='result.txt',help='Path to save the words pairs and their predicted cosine similarity scores')
    args = parser.parse_args()

    logging.info('Start evaluation for {} data..'.format(args.subword))
    model = load_model(args.model_path)
    eval_data = open(args.input, 'r')
    human_score = []
    result_list = [] # Store (w1, w2, similarity) for error analysis

    for line in tqdm(eval_data):
        word1, word2, human = line.split()
        if args.subword == 'wubi':
            w1, w2 = wubi(word1), wubi(word2)
        elif args.subword == 'graphical':
            w1, w2 = graphical(word1), graphical(word2)
        elif args.subword == 'character':
            w1, w2 = word1, word2
        else:
            logging.error('Please enter the correct subword component {character, graphical, wubi}')
            break
        # Compute cosine similarity
        emb1, emb2 = model[w1], model[w2]
        pred = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        human_score.append(human)
        result_list.append((word1, word2, pred))
    # Save predicted scores
    result = pd.DataFrame(result_list, columns =['word_1', 'word_2', 'pred_score']) 
    result.to_csv(args.output, sep='\t')
    # Compute Spearman correlation coefficients for evaluation
    pred_score = [i[-1] for i in result_list]
    corr = spearmanr(human_score, pred_score)
    logging.info('Finish evaluation on dataset {}. Score = {}'.format(args.input,corr))
    eval_data.close()
    logging.info('Done')

if __name__ == '__main__':
    main()
