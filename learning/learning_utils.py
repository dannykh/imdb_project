__author__ = 'Danny'

import csv

file_index = 3

empty_cell = 6.95


def _load_lines(fname, dst):
    max_len = 0
    with open(fname, 'r') as fptr:
        for line in fptr.readlines():
            try:
                line_digest = []
                for val in line[:-1].split(','):
                    if val == '':
                        line_digest.append(empty_cell)
                    else:
                        line_digest.append(float(val))
                max_len = max(max_len, len(line_digest))
                dst.append(line_digest)
            except:
                {}
    for item in dst:
        item += [empty_cell] * (max_len - len(item))


def load_data(data_fname="../data/data_{}.csv".format(file_index),
              realTags_fname="../data/real_tags_{}.csv".format(file_index),
              binTags_fname="../data/bin_tags_{}.csv".format(file_index)):
    data = []
    real_tags = []
    bin_tags = []

    _load_lines(data_fname, data)
    # _load_lines(realTags_fname, real_tags)

    with open(realTags_fname, 'r') as fptr:
        for line in fptr.readlines():
            line_digest = float(line)
            real_tags.append(line_digest)

    with open(binTags_fname, 'r') as fptr:
        for line in fptr.readlines():
            line_digest = int(line[0][0])
            bin_tags.append(line_digest)

    return data, real_tags, bin_tags
