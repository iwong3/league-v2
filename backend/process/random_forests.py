from math import log

import numpy as np


# TODO
# - categorical data is complicated (ie. champions)
#   - add "data type" array ["categorical", "continuous"]
#   - best_split
#     - try splitting on all champions
#     - keep set of champions that lead to most IG (threshold)
#     - all champs in that set go left/right, others go right/left
# - think of idea that doesn't use categorical data
class Utility(object):

    # calculate entropy given labels of 0s and 1s
    def entropy(self, y):

        # count zeros and ones
        zeros = y.count(0)
        ones = y.count(1)

        # all labels are the same - no entropy
        if zeros == 0 or ones == 0:
            return 0

        # calculate probabilities
        num_labels = len(y)
        p_zero = float(zeros) / num_labels
        p_one = float(ones) / num_labels

        # calculate entropy
        entropy = -((p_zero * log(p_zero, 2)) + (p_one * log(p_one, 2)))
        return entropy

    # split attributes/labels into two groups based on split attribute/value
    def partition_classes(self, X, y, split_attribute, split_val):

        # set up split attributes/labels
        X_left, X_right, y_left, y_right = [], [], [], []

        # split on split_attribute and split_val
        for i in range(len(X)):
            if X[i][split_attribute] < split_val:
                X_left.append(X[i])
                y_left.append(y[i])
            else:
                X_right.append(X[i])
                y_right.append(y[i])

        return (X_left, X_right, y_left, y_right)
