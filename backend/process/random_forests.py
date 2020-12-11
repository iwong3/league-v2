from math import log

import numpy as np


# TODO
# - predict champion based on in-game stats
# - for categorical attributes (items/runes/doublekills/firstblood/etc)
#   - can add an "attribute type" field and if its categorical, set all equal to left, otherwise right?
# - consider calculating deltas for more meaningful splits
class Utility(object):


    # calculate entropy in labels
    def entropy(self, y):

        # count all labels
        labels = {}
        for label in y:
            if label not in labels:
                labels[label] = {
                    "count": 0
                }
            labels[label]["count"] += 1

        # no labels / all labels are the same - no entropy
        if len(labels) <= 1:
            return 0

        # calculate probability for each label
        probabilities = []
        num_labels = len(y)
        for label in labels:
            probabilities.append(float(labels[label]["count"]) / num_labels)

        # calculate entropy
        entropy = 0
        for prob in probabilities:
            entropy += prob * log(prob, 2)
        entropy *= -1

        return entropy


    # split attributes/labels into two groups based on split attribute/value
    def partition_classes(self, X, y, split_attr, split_val):

        # set up split attributes/labels
        X_left, X_right, y_left, y_right = [], [], [], []

        # split on split_attribute and split_val
        for i in range(len(X)):
            if X[i][split_attr] < split_val:
                X_left.append(X[i])
                y_left.append(y[i])
            else:
                X_right.append(X[i])
                y_right.append(y[i])

        return (X_left, X_right, y_left, y_right)


    # calculate info gain from split
    def info_gain(self, prev_y, curr_y):

        # calculate pre split entropy
        initial_entropy = self.entropy(prev_y)

        # calculate post split entropy - weighted left + right
        left_entropy = self.entropy(curr_y[0])
        left_weight = len(curr_y[0]) / len(prev_y)
        right_entropy = self.entropy(curr_y[1])
        right_weight = len(curr_y[1]) / len(prev_y)
        new_entropy = (left_weight * left_entropy) + (right_weight * right_entropy)

        # calculate info gain - entropy removed
        info_gain = initial_entropy - new_entropy

        return info_gain


    # find best split that gives most info gain
    def best_split(self, X, y):

        # best split vars
        max_info_gain = -1.0
        best_split_attr = None
        best_split_val = None
        best_X_left, best_X_right, best_y_left, best_y_right = [], [], [], []

        # 1. get number of attributes to randomly select from - sqrt of number of attributes
        num_attr = int(len(X[0]) ** (0.5))

        # 2. randomly select columns to split on
        all_attrs = list(range(len(X[0])))
        selected_attrs = []
        while num_attr > 0:
            random_attribute_index = np.random.randint(len(all_attrs))
            selected_attrs.append(all_attrs[random_attribute_index])
            all_attrs.pop(random_attribute_index)
            num_attr -= 1

        # 3a. get the best split from all attribute/value combinations (from cmu slides)
        for split_attr in selected_attrs:
            for node in X:
                # 3b. split on column + value
                split_val = node[split_attr]
                (X_left, X_right, y_left, y_right) = self.partition_classes(X, y, split_attr, split_val)

                # 3c. update on max_information_gain
                info_gain = self.info_gain(y, [y_left, y_right])
                if info_gain > max_info_gain:
                    max_info_gain = info_gain
                    best_split_attr = split_attr
                    best_split_val = split_val
                    best_X_left, best_X_right, best_y_left, best_y_right = X_left, X_right, y_left, y_right

        return best_split_attr, best_split_val, best_X_left, best_X_right, best_y_left, best_y_right


    # get most common label
    def most_common_label(self, y):

        # count all labels
        labels = {}
        for label in y:
            if label not in labels:
                labels[label] = {
                    "label": label,
                    "count": 0
                }
            labels[label]["count"] += 1

        # get most common label
        most_common_label_count = -1
        most_common_label = None
        for label in labels:
            if labels[label]["count"] > most_common_label_count:
                most_common_label_count = labels[label]["count"]
                most_common_label = labels[label]["label"]

        return most_common_label


class DecisionTree(object):


    def __init__(self, max_depth):
        self.tree = {}
        self.max_depth = max_depth
        self.util = Utility()
        self.curr_key = 2
        self.entropy_threshold = 0.05


    # create a decision tree
    def learn(self, X, y, par_node = {}, depth=0):
        self.learn_helper(X, y, 1, depth)


    def learn_helper(self, X, y, key, depth):

        leaf = False

        # leaf - max depth or label entropy is below threshold
        if depth == self.max_depth or self.util.entropy(y) <= self.entropy_threshold:
            leaf = True

        # leaf - all data points are the same
        if not leaf:
            first_node = X[0]
            all_equal = True
            for node in X:
                if node != first_node:
                    all_equal = False
            if all_equal:
                leaf = True

        # create leaf if leaf
        if leaf:
            curr_node = {
                'label': self.util.most_common_label(y)
            }
            self.tree[key] = curr_node
            return

        # split
        split_attribute, split_value, X_left, X_right, y_left, y_right = self.util.best_split(X, y)

        # leaf - can't split anymore
        if len(X_left) == 0 or len(X_right) == 0:
            curr_node = {
                'label': self.util.most_common_label(y)
            }
            self.tree[key] = curr_node
            return

        # set up current node
        left_key = self.curr_key
        right_key = self.curr_key + 1
        self.curr_key += 2
        curr_node = {
            'left': left_key,
            'right': right_key,
            'split_attribute': split_attribute,
            'split_value': split_value
        }
        self.tree[key] = curr_node

        # recurse on left and right child nodes
        self.learn_helper(X_left, y_left, left_key, depth+1)
        self.learn_helper(X_right, y_right, right_key, depth+1)


    # classify record using decision tree
    def classify(self, record):

        curr_key = 1
        while True:
            curr_node = self.tree[curr_key]

            # leaf
            if 'label' in curr_node:
                return curr_node['label']

            # split
            if record[curr_node['split_attribute']] < curr_node['split_value']:
                curr_key = curr_node['left']
            else:
                curr_key = curr_node['right']


class RandomForest(object):

    num_trees = 0
    decision_trees = []
    bootstraps_datasets = []
    bootstraps_labels = []
    util = None


    def __init__(self, num_trees):
        # Initialization done here
        self.num_trees = num_trees
        self.decision_trees = [DecisionTree(max_depth=10) for i in range(num_trees)]
        self.bootstraps_datasets = []
        self.bootstraps_labels = []
        self.util = Utility()


    # prepare data for a decision tree
    def _bootstrapping(self, XX, n):

        # init selected data
        samples = [] # sampled dataset
        labels = []  # class labels for the sampled records

        # randomly select data with replacement
        while n > 0:
            index = np.random.randint(len(XX))
            samples.append(XX[index][:-1])
            labels.append(XX[index][-1])
            n -= 1

        return (samples, labels)


    # prepare data for all decision trees
    def bootstrapping(self, XX):

        # get bootstrapped data for each decision tree
        for i in range(self.num_trees):
            data_sample, data_label = self._bootstrapping(XX, len(XX))
            self.bootstraps_datasets.append(data_sample)
            self.bootstraps_labels.append(data_label)


    # train decision trees
    def fitting(self):

        for i in range(self.num_trees):
            dt = self.decision_trees[i]
            X = self.bootstraps_datasets[i]
            y = self.bootstraps_labels[i]
            dt.learn(X, y)
            self.decision_trees[i] = dt


    # classify data using all decision trees to vote
    def voting(self, X):

        y = []

        for record in X:
            # Following steps have been performed here:
            #   1. Find the set of trees that consider the record as an
            #      out-of-bag sample.
            #   2. Predict the label using each of the above found trees.
            #   3. Use majority vote to find the final label for this record.
            votes = []

            # classify with each decision tree
            for i in range(len(self.bootstraps_datasets)):
                # only if new data
                dataset = self.bootstraps_datasets[i]
                if record not in dataset:
                    OOB_tree = self.decision_trees[i]
                    effective_vote = OOB_tree.classify(record)
                    votes.append(effective_vote)

            # record was part of training data for all decision trees
            if len(votes) == 0:
                # take most popular from all trees
                for i in range(len(self.bootstraps_datasets)):
                    dataset = self.bootstraps_datasets[i]
                    index = dataset.index(record)
                    votes.append(self.bootstraps_labels[i][index])
                    y = np.append(y, self.util.most_common_label(votes))
            else:
                y = np.append(y, self.util.most_common_label(votes))

        return y
