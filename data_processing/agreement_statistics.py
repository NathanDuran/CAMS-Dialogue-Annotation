import os
import pandas as pd
from itertools import combinations
from nltk.metrics.agreement import AnnotationTask


def test_agreement_statistics():
    """Tests agreement statistics functions against those found in NLTK:
        https://www.nltk.org/api/nltk.metrics.html#module-nltk.metrics.agreement

    Compares the values of agreement statistics with those found in:
        Artstein, R. and Poesio, M. (2005) Kappa 3 = Alpha (or Beta) University of Essex NLE Technote

    Data is in:
        artstein_poesio_example.txt
    """

    file_path = os.path.join("label_data", "artstein_poesio_example.txt")

    # Distance function for weighted agreement stats
    def test_distance_func(label_a, label_b):
        if label_a == label_b:
            return 0
        elif (label_a == 'ireq' and label_b == 'stat') or (label_b == 'ireq' and label_a == 'stat'):
            return 1
        else:
            return 0.5

    # Gets individual user labels
    def get_user_labels(path):
        with open(path, 'r') as file:
            a_stat = [0] * 100
            a_ireq = [0] * 100
            a_chck = [0] * 100

            b_stat = [0] * 100
            b_ireq = [0] * 100
            b_chck = [0] * 100

            for line in file:
                usr = line.split()[0]
                ind = int(line.split()[1])
                lbl = line.split()[2]
                if usr == 'a':
                    if lbl == 'chck':
                        a_chck[ind - 1] += 1
                    elif lbl == 'stat':
                        a_stat[ind - 1] += 1
                    elif lbl == 'ireq':
                        a_ireq[ind - 1] += 1

                elif usr == 'b':
                    if lbl == 'chck':
                        b_chck[ind - 1] += 1
                    elif lbl == 'stat':
                        b_stat[ind - 1] += 1
                    elif lbl == 'ireq':
                        b_ireq[ind - 1] += 1

            a_data = {'stat': a_stat, 'ireq': a_ireq, 'chck': a_chck}
            a_frame = pd.DataFrame(a_data)
            b_data = {'stat': b_stat, 'ireq': b_ireq, 'chck': b_chck}
            b_frame = pd.DataFrame(b_data)
            example_users_dict = {'a': a_frame, 'b': b_frame}
        return example_users_dict

    # NLTK stats
    nltk_stats = AnnotationTask(data=[x.split() for x in open(file_path)])
    print("nltk:")
    print("multi-Pi - " + str(nltk_stats.pi()))
    print("multi-kappa - " + str(nltk_stats.multi_kappa()))
    print("alpha - " + str(nltk_stats.alpha()))

    # Stats from my functions
    example_users = get_user_labels(file_path)
    print("Mine:")
    print("Multi-Pi - {0:.4f}".format(multi_pi(example_users)))
    print("multi-kappa - {0:.4f}".format(multi_kappa(example_users)))
    print("alpha - {0:.4f}".format(alpha(example_users, test_distance_func)))
    print("alpha prime - {0:.4f}".format(alpha_prime(example_users, test_distance_func)))
    print("beta - {0:.4f}".format(beta(example_users, test_distance_func)))

    # Expected values from Artstein and Poesio
    print("Expected:")
    print("mulit-Pi - " + str(0.7995))
    print("mulit-kappa - " + str(0.8013))
    print("alpha - " + str(0.8156))
    print("alpha prime - " + str(0.8146))
    print("beta - " + str(0.8163))


def create_coder_cumulative_matrix(data):
    """Gets the sums of labels for all coders in data.

    Example of returned matrix:
          FPP-base SPP-base FPP-pre SPP-pre Pre FPP-insert SPP-insert Insert FPP-post SPP-post Post
    0       11        1       0       1   0          0          0      0        2        0    0
    1        2        2       1       0   1          7          2      0        0        0    0
    2        0        4       1       2   0          2          5      1        0        0    0
    3        0        6       1       1   0          0          4      0        2        1    0
    4        0        0       0       0   0          0          0      0        7        1    7
    5        0        0       0       0   0          0          0      0        2       10    3

    Args:
        data (dict): Dictionary of Dataframes where keys user_id. Dataframe rows are utterances for the set or
                     dialogue and columns are label for coder (1 indicates assigned label).

    Returns:
        matrix (DataFrame): Dataframe rows are utterance index and columns are labels types, items are sum of labels
                            applied to that utterance by all coders.
    """
    # Create an empty dataframe with the same column names
    column_names = data[list(data.keys())[0]].columns
    matrix = pd.DataFrame(columns=column_names)

    # Add all dataframe values together
    for user_name, data in data.items():
        matrix = matrix.add(data, fill_value=0)

    return matrix


def create_reliability_matrix(data):
    """Creates a reliability matrix from data.

    Example of returned matrix:
               a     b
        0   stat  stat
        1   stat  stat
        2   stat  stat
        3   stat  stat

    Args:
        data (dict): Dictionary of Dataframes where keys user_id. Dataframe rows are utterances for the set or
                          dialogue and columns are label for coder (1 indicates assigned label).

    Returns:
        matrix (DataFrame): Dataframe rows are utterances for the set or dialogue and columns are coder id, items are
                            assigned labels as a string.
    """
    user_dict = dict()
    for user_name, data in data.items():

        # Get the label the user has assigned to each item
        user_dict[user_name] = list(data.idxmax(axis=1))

    # Create matrix/dataframe
    matrix = pd.DataFrame(user_dict)
    return matrix


def create_coder_sum_matrix(data):
    """Gets the sums of labels for all coders in data.

    Example of returned matrix:
           stat  ireq  chck
        a    46    44    10
        b    52    32    16

    Args:
        data (dict): Dictionary of Dataframes where keys user_id. Dataframe rows are utterances for the set or
                          dialogue and columns are label for coder (1 indicates assigned label).

    Returns:
        matrix (DataFrame): Dataframe rows are coder ids and columns are labels, items are sum of all labels applied
                            by that coder.
    """
    user_dict = dict()
    for user_name, data in data.items():
        # Get the label the user has assigned to each item
        user_dict[user_name] = data.sum(axis=0)

    # Create matrix/dataframe
    matrix = pd.DataFrame(user_dict).T

    return matrix


def pariwise_average(user_data, function):
    """Calculates an average of a given function over a set of coders pairs.

    Args:
        user_data (dict): Dictionary of users dataframes.
        function (func): The function to apply to all pairs, i.e. observed/expected agreement.

    Returns:
        average (float): The average of all the coder pairs.
    """
    # Get all the pariwise combinations of users
    user_combinations = list(combinations(user_data.keys(), 2))

    # Apply function and average
    total = 0
    n = 0
    for pair in user_combinations:
        total += function(user_data[pair[0]], user_data[pair[1]])
        n += 1

    return total / n


def observed_agreement_kappa(coder_a, coder_b):
    """Calculates the observed agreement between two coders."""
    num_items = len(coder_a)
    num_labels = len(coder_a.columns)
    total = 0
    for item in range(num_items):
        for label in range(num_labels):
            if coder_a.iloc[item, label] == 1 and coder_b.iloc[item, label] == 1:
                total += 1

    return total / num_items


def expected_agreement_kappa(coder_a, coder_b):
    """Calculates the expected agreement between two coders label distributions."""
    exp_agr = 0
    num_items = len(coder_a)

    # Get the frequency distribution of each coder
    a_lable_freq = coder_a.sum(axis=0)
    b_lable_freq = coder_b.sum(axis=0)

    # Calculate the expected agreement for each label
    for label in range(len(a_lable_freq)):
        exp_agr += (a_lable_freq.iloc[label] / num_items) * (b_lable_freq.iloc[label] / num_items)
    return exp_agr


def multi_kappa(data):
    """Davies and Fleiss (1982) Averages over observed and expected agreements for each coder pair.

        Generalisation of Cohens K for multiple coders. Expected agreement is directly computed from the observed
        distributions of the individual annotators.

        If input user_data is a dict of only two coders this if effectively just Cohen's Kappa - Cohen, J. (1960)
        A coefficient of agreement for nomial scales. Educational and Psychological Measurement.

    Args:
        data (dict): Dictionary of Dataframes where keys user_id. Dataframe rows are utterances for the set or
                          dialogue and columns are label for coder (1 indicates assigned label).

    Returns:
        multi_kappa (float): The Multi-kappa stat for the given set or dialogue and label type.
    """
    # Calculate the pairwise observed agreement
    obs_agr = pariwise_average(data, observed_agreement_kappa)

    # Calculate the pairwise expected agreement
    exp_agr = pariwise_average(data, expected_agreement_kappa)

    return (obs_agr - exp_agr) / (1.0 - exp_agr)


def multi_pi(data):
    """multi-pi = Fleiss, J.L. (1971) Measuring Nominal Scale Agreement Among Many Raters.

       Generalisation of Scots π for multiple coders. Expected agreement is estimated on the basis of the distribution
       of categories found in the observed data, but it is assumed that all coders assign categories on the basis of
       a single (but not necessarily uniform) distribution.

       If input data only has two coders (i.e. max sum of 2) this is effectively Scotts Pi -
       Scott, W.A.. (1955) Reliability of Content Analysis : The Case of Nominal Scale Coding.

    Args:
        data (DataFrame): Dictionary of Dataframes where keys user_id. Dataframe rows are utterances for the set or
                          dialogue and columns are label for coder (1 indicates assigned label).

    Returns:
        multi_pi (float): The Multi-pi stat for the given set or dialogue and label type.
    """
    # Need to get the cumulative labels for all coders in data
    data = create_coder_cumulative_matrix(data)

    # Get the number of annotators
    num_raters = data.sum(axis=1)[0]

    # Get the number of labeled items
    num_items = len(data)

    # Get the number of labels
    num_categories = len(data.columns)

    # Calculate the proportion of assignments
    pj = list(data.sum() / (num_raters * num_items))

    # Calculate expected agreement
    exp_agr = sum([i ** 2 for i in pj])

    # Calculate the extent that raters agree on each item
    pi = []
    for i in range(num_items):
        curr_item = []
        for j in range(num_categories):
            curr_item.append(data.iloc[i, j] ** 2)
        pi.append((1 / (num_raters * (num_raters - 1))) * (sum(curr_item) - num_raters))

    # Calculate observed agreements
    obs_agr = (1 / num_items) * sum(pi)

    return (obs_agr - exp_agr) / (1 - exp_agr)


def observed_disagreement(items, num_ratings, distance):
    """Observed disagreement for alpha/alpha prime and beta."""
    obs_dis_agr = 0.0
    for item in items:

        item_distances = sum(distance(i, j) for i in item for j in item)
        obs_dis_agr += item_distances / float(len(item) - 1)

    return obs_dis_agr / float(num_ratings)


def expected_disagreement_alpha(items, num_ratings, distance):
    """Coder sums / num_ratings * (num_ratings - 1)."""
    exp_dis_agr = 0.0
    for item_a in items:
        for item_b in items:
            exp_dis_agr += sum(distance(i, j) for i in item_a for j in item_b)

    exp_dis_agr /= float(num_ratings * (num_ratings - 1))
    return exp_dis_agr


def alpha(data, distance):
    """Krippendorff, K. (1980/2004) Content Analysis: An Introduction to its Methodology.

    Weighted agreement from category similarity for multiple coders.
    Assumes single probability distribution for all coders. Expected disagreement is the mean of the distances
    between all the judgment pairs in the data, without regard to items.

    Args:
        data (dict): Dictionary of Dataframes where keys user_id. Dataframe rows are utterances for the set or
                     dialogue and columns are label for coder (1 indicates assigned label).
        distance (func): Function which returns the distance between two labels (0=Min distance, 1=Max distance).

    Returns:
        alpha (float): The Alpha stat for the given set or dialogue and label type.
    """
    # Create a matrix of all of the labels the coders selected (utterances x coders)
    matrix = create_reliability_matrix(data)
    # Convert to 2d array
    items = matrix.values.tolist()

    # Number of pairable values (num utterances x num coders)
    num_ratings = sum(len(item) for item in items)

    # Calculate observed disagreement
    obs_dis_agr = observed_disagreement(items, num_ratings, distance)

    # Calculate expected disagreement
    exp_dis_agr = expected_disagreement_alpha(items, num_ratings, distance)

    return 1.0 - obs_dis_agr / exp_dis_agr if (obs_dis_agr and exp_dis_agr) else 1.0


def expected_disagreement_alpha_prime(items, num_ratings, distance):
    """Coder sums / num_ratings."""
    exp_dis_agr = 0.0
    for item_a in items:
        item_sum = 0.0
        for item_b in items:
            item_sum += sum(distance(i, j) for i in item_a for j in item_b)

        exp_dis_agr += item_sum / float(num_ratings)

    exp_dis_agr /= float(num_ratings)

    return exp_dis_agr


def alpha_prime(data, distance):
    """Artstein, R. and Poesio, M. (2008) Inter-Coder Agreement for Computational Linguistics.

    Weighted agreement from category similarity for multiple coders. A slight variation of Krippendorff's alpha.
    Assumes single probability distribution for all coders. Expected disagreement is the mean of the distances between
    categories, weighted by these probabilities for all (ordered) category pairs.

    Args:
        data (dict): Dictionary of Dataframes where keys user_id. Dataframe rows are utterances for the set or
                     dialogue and columns are label for coder (1 indicates assigned label).
        distance (func): Function which returns the distance between two labels (0=Min distance, 1=Max distance).

    Returns:
        alpha_prime (float): The Alpha stat for the given set or dialogue and label type.
    """
    # Create a matrix of all of the labels the coders selected (items x coders)
    matrix = create_reliability_matrix(data)
    # Convert to 2d array
    items = matrix.values.tolist()

    # Number of pairable values (coders x items)
    num_ratings = sum(len(item) for item in items)

    # Calculate observed disagreement
    obs_dis_agr = observed_disagreement(items, num_ratings, distance)

    # Calculate expected disagreement
    exp_dis_agr = expected_disagreement_alpha_prime(items, num_ratings, distance)

    return 1.0 - obs_dis_agr / exp_dis_agr if (obs_dis_agr and exp_dis_agr) else 1.0


def expected_disagreement_beta(items_matrix, num_items, distance):
    """Coder sums / num_items."""

    # Get a list of the labels so we can get the index
    labels = list(items_matrix.columns.values)

    # All values need to be divided by num_items, so easier to do it with the dataframe
    items_matrix = items_matrix.apply(lambda x: x / num_items)

    # Get the first row and then all other rows to lists
    items = items_matrix.values.tolist()
    first_row = items[0]
    other_rows = [items[i][:] for i in range(1, len(items))]

    # Iterate over first row and multiply by all other values (and distance between labels)
    exp_dis_agr = 0.0
    for curr in range(len(first_row)):
        current_val = first_row[curr]
        current_label = labels[curr]
        for row in range(len(other_rows)):
            for row_col in range(len(other_rows[row])):
                exp_dis_agr += current_val * other_rows[row][row_col] * distance(current_label, labels[row_col])

    return exp_dis_agr


def beta(data, distance):
    """Artstein, R. and Poesio, M. (2005) Kappa 3 = Alpha (or Beta).

    An agreement coefficient that is weighted, applies to multiple coders, and calculates expected agreement using a
    separate probability distribution for each coder.

    Args:
        data (dict): Dictionary of Dataframes where keys user_id. Dataframe rows are utterances for the set or
                     dialogue and columns are label for coder (1 indicates assigned label).
        distance (func): Function which returns the distance between two labels (0=Min distance, 1=Max distance).

    Returns:
        beta (float): The Alpha stat for the given set or dialogue and label type.
    """

    # Create a matrix of all of the labels the coders selected (items x coders)
    matrix = create_reliability_matrix(data)
    # Convert to 2d array
    items = matrix.values.tolist()

    # Number of pairable values (coders x items)
    num_ratings = sum(len(item) for item in items)

    # Calculate observed disagreement
    obs_dis_agr = observed_disagreement(items, num_ratings, distance)

    # Calculate expected disagreement
    sum_matrix = create_coder_sum_matrix(data)  # Easier to do with a summary matrix

    exp_dis_agr = expected_disagreement_beta(sum_matrix, len(matrix), distance)

    return 1.0 - obs_dis_agr / exp_dis_agr if (obs_dis_agr and exp_dis_agr) else 1.0
