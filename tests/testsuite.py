#! /usr/bin/env python3

import argparse
import os
import random
import subprocess
import sys


def compare(word, query1, query2, dist):
    ans1 = subprocess.check_output(query1, shell=True, stderr=subprocess.PIPE)
    ans2 = subprocess.check_output(query2, shell=True, stderr=subprocess.PIPE)

    if ans1 != ans2:
        return False
    else:
        return True

def get_random_word(path, dist):
    total_bytes = os.stat(path).st_size
    word = ""

    dist = dist + 1 if dist == 0 else dist

    with open(path, 'r') as f:
        while(len(word) < dist):
            random_point = random.randint(0, total_bytes)
            f.seek(random_point)
            line = f.readline()
            word = line.split()

    return word[0].strip()


def create_query(word, path, dist):
    app = os.path.join(path, 'TextMiningApp')
    trie = os.path.join(path, 'dict.bin')

    return 'echo "approx {} {}" | {} {}'.format(str(dist), word, app, trie)


def main(argv):
    parser = argparse.ArgumentParser(description='Test suite.')
    parser.add_argument('--ref', action='store', dest='ref', required=True)
    parser.add_argument('--own', action='store', dest='own', required=True)
    parser.add_argument('--run', action='store', type=int, default=100, dest='run')
    parser.add_argument('--words', action='store', dest='words', required=True)
    parser.add_argument('--dist', action='store', dest='dist', type=int,
                        nargs='+', required=True)

    args = parser.parse_args(argv)
    word = ""
    for dist in args.dist:
        for i in range(args.run):
            word = get_random_word(args.words, dist)
            query1 = create_query(word, args.ref, dist)
            query2 = create_query(word, args.own, dist)
            ans = compare(word, query1, query2, dist)
            if not ans:
                print("FAIL:\t{} distance: {}".format(word, dist))


if __name__ == '__main__':
    main(sys.argv[1:])