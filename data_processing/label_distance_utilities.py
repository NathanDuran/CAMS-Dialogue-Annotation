import os
import pandas as pd
from data_processing.data_utilities import save_dataframe, load_dataframe, load_json_data
from data_processing.plot_utilities import plot_table
from anytree import *
from anytree.importer import DictImporter
from anytree.exporter import DotExporter


def load_labels_tree(data_path):
    """Loads a tree from json format."""
    data = load_json_data(data_path)
    importer = DictImporter(nodecls=AnyNode)
    return importer.import_(data)


def show_labels_tree(tree):
    """Renders the tree in ascii format."""
    print(render.RenderTree(tree, style=render.DoubleStyle))


def plot_labels_tree(tree, path):
    """Generates Dot format image of tree."""
    DotExporter(tree).to_picture(path)


def get_tree_node(root_node, node_name):
    """Finds and converts node from AnyNode to Node format."""
    return find(root_node, lambda node: node.name == node_name)


def get_last_common_ancestor(tree, name_a, name_b):
    """Retuns the name of the last common ancestor of two nodes."""
    node_a = get_tree_node(tree, name_a)
    node_b = get_tree_node(tree, name_b)
    # Returns all common ancestors
    common_ancestor = util.commonancestors(node_a, node_b)
    # Return the name of the last one
    return common_ancestor[-1].name


def walk_tree(tree, name_a, name_b):
    """Generates a walk between two nodes.
        Returns a tuple of size 3:
        [0] = walk up from node_a
        [1] = root
        [2] = walk down from root to node_b
    """
    node_a = get_tree_node(tree, name_a)
    node_b = get_tree_node(tree, name_b)

    walk = Walker().walk(node_a, node_b)
    return walk


def get_walk_distance(tree, name_a, name_b):
    """Returns the distance between two nodes."""
    walk = walk_tree(tree, name_a, name_b)
    distance = len(walk[0]) + len(walk[2])
    return distance


def generate_da_distance_matrix(label_data_dir, labels, normalise=True):
    """Calculates distances between all DA label pairs and returns dataframe.
        Converts da_labels_tree.json to anytree object and calculate distance matrix.

    Args:
        label_data_dir (str): Directory to the 'da_labels_tree.json' file.
        labels (list): List of all DA labels.
        normalise (bool): Whether to normalise the returned matrix.

    Returns:
        matrix_frame (DataFrame): Matrix with distances between each label.
    """

    # Create the labels anytree from the json
    labels_tree = load_labels_tree(os.path.join(label_data_dir, 'da_labels_tree.json'))

    # Calculate the distance between each label pair
    matrix_arr = []
    for label_a in labels:
        row = [get_walk_distance(labels_tree, label_a, label_b) for label_b in labels]
        matrix_arr.append(row)

    # Create dataframe
    matrix_frame = pd.DataFrame(data=matrix_arr, index=labels, columns=labels)

    # Normalise if needed
    if normalise:
        matrix_frame = (matrix_frame - matrix_frame.min()) / (matrix_frame.max() - matrix_frame.min())
        matrix_frame = matrix_frame.round(3)
    return matrix_frame


def get_ap_distance(label_a, label_b):
    """Returns the distance between two AP labels."""

    distance = 0
    # If both labels are the same distance is 0, else need to compare
    if label_a == label_b:
        return distance

    else:
        # Get pieces for length and prefix (FPP/SPP) and postfix (base/pre/insert/post)
        a_pieces = label_a.split('-')
        b_pieces = label_b.split('-')

        # Both FPP/SPP labels
        if len(a_pieces) == 2 and len(b_pieces) == 2:

            # Check prefix and postfix for equality
            if a_pieces[0] != b_pieces[0]:
                distance += 0.5
            if a_pieces[1] != b_pieces[1]:
                distance += 0.5

        # Both minimal expansion labels
        elif len(a_pieces) == 1 and len(b_pieces) == 1:
            distance += 1

        # A is FPP/SPP and B is minimal expansion
        elif len(a_pieces) == 2 and len(b_pieces) == 1:
            # If A's postfix is same type as B
            if a_pieces[1] == b_pieces[0].lower():
                distance += 0.5
            else:
                distance = 1

        # B is FPP/SPP and A is minimal expansion
        elif len(b_pieces) == 2 and len(a_pieces) == 1:
            # If B's postfix is same type as A
            if b_pieces[1] == a_pieces[0].lower():
                distance += 0.5
            else:
                distance = 1
        else:
            raise ValueError("Error when calculating distance between  " + label_a + " and " + label_b + ".")

    return distance


def get_ap_distance_postfix_only(label_a, label_b):
    """Returns the distance between two AP labels."""

    distance = 0
    # If both labels are the same distance is 0, else need to compare
    if label_a == label_b:
        return distance

    else:
        # Get pieces for length and prefix (FPP/SPP) and postfix (base/pre/insert/post)
        a_pieces = label_a.split('-')
        b_pieces = label_b.split('-')

        # Both FPP/SPP labels
        if len(a_pieces) == 2 and len(b_pieces) == 2:

            # Check prefix and postfix for equality
            if a_pieces[1] != b_pieces[1]:
                distance += 1

        # Both minimal expansion labels
        elif len(a_pieces) == 1 and len(b_pieces) == 1:
            distance += 1

        # A is FPP/SPP and B is minimal expansion
        elif len(a_pieces) == 2 and len(b_pieces) == 1:
            # If A's postfix is same type as B
            if a_pieces[1] != b_pieces[0].lower():
                distance += 1

        # B is FPP/SPP and A is minimal expansion
        elif len(b_pieces) == 2 and len(a_pieces) == 1:
            # If B's postfix is same type as A
            if b_pieces[1] != a_pieces[0].lower():
                distance += 1
        else:
            raise ValueError("Error when calculating distance between  " + label_a + " and " + label_b + ".")

    return distance


def generate_ap_distance_matrix(labels, postfix_only=False):
    """Calculates distances between all AP label pairs and returns dataframe.

    Args:
        labels (list): List of all AP labels.
        postfix_only (bool): Whether to ignore AP FPP and SPP

    Returns:
        matrix_frame (DataFrame): Matrix with distances between each label.
    """
    # Calculate the distance between each label pair
    matrix_arr = []
    for label_a in labels:
        if postfix_only:
            row = [get_ap_distance_postfix_only(label_a, label_b) for label_b in labels]
        else:
            row = [get_ap_distance(label_a, label_b) for label_b in labels]
        matrix_arr.append(row)

    # Create dataframe
    matrix_frame = pd.DataFrame(data=matrix_arr, index=labels, columns=labels)

    return matrix_frame


def generate_ap_type_distance_matrix(label_data_dir, labels, postfix_only=False, normalise=True):
    """Calculates distances between all AP-type label pairs and returns dataframe.
        Must have generated da_distance_matrix.csv' and 'ap_distance_matrix.csv' files first.

    Args:
        label_data_dir (str): Directory to the 'da_distance_matrix.csv' and 'ap_distance_matrix.csv' files.
        labels (list): List of all AP-type labels.
        postfix_only (bool): Whether to ignore AP FPP and SPP
        normalise (bool): Whether to normalise the returned matrix.

    Returns:
        matrix_frame (DataFrame): Matrix with distances between each label.
    """
    # Load the pre-generated DA and AP distance matrices to dataframes
    da_matrix_path = os.path.join(label_data_dir, "da_distance_matrix.csv")
    if postfix_only:
        ap_matrix_path = os.path.join(label_data_dir, "ap_postfix_only_distance_matrix.csv")
    else:
        ap_matrix_path = os.path.join(label_data_dir, "ap_distance_matrix.csv")
    if os.path.exists(da_matrix_path):
        da_distance_matrix = load_dataframe(da_matrix_path)
    else:
        raise FileNotFoundError("Cannot find DA distance matrix in " + da_matrix_path)

    if os.path.exists(ap_matrix_path):
        ap_distance_matrix = load_dataframe(ap_matrix_path)
    else:
        raise FileNotFoundError("Cannot find AP distance matrix in " + ap_matrix_path)

    # Calculate the distance between each label pair
    matrix_arr = []
    for label_a in labels:
        row = []
        for label_b in labels:
            distance = 0

            # Get the da label distance
            label_a_da = label_a.split('-')[-1]
            label_b_da = label_b.split('-')[-1]
            distance += da_distance_matrix.loc[label_a_da, label_b_da]

            # Get the ap label distance
            label_a_ap = '-'.join(label_a.split('-')[:-1])
            label_b_ap = '-'.join(label_b.split('-')[:-1])
            distance += ap_distance_matrix.loc[label_a_ap, label_b_ap]

            row.append(distance)
        matrix_arr.append(row)

    # Create dataframe
    matrix_frame = pd.DataFrame(data=matrix_arr, index=labels, columns=labels)

    # Normalise if needed
    if normalise:
        matrix_frame = (matrix_frame - matrix_frame.min()) / (matrix_frame.max() - matrix_frame.min())
        matrix_frame = matrix_frame.round(3)

    return matrix_frame


def save_distance_matrix(save_dir, matrix, name):
    """Utility function saves dataframe as .csv and a .png.

    Args:
        save_dir (str): Directory to the save the files.
        matrix (DataFrame): Distance matrix to save.
        name (str): What to name the matrix.
    """
    # Save dataframe
    save_dataframe(os.path.join(save_dir, name + ".csv"), matrix, index_label='labels')

    # Create the dataframe as table image
    fig = plot_table(matrix, title='')
    fig.savefig(os.path.join(save_dir, name + ".png"))


def generate_label_distance_matrices(save_dir, labels):
    """Utility function generates DA, AP and AP-type distance matrices and saves them to .csv and .png.

    Args:
        save_dir (str): Directory to the save the files. Should be the same location as 'da_labels_tree.json'.
        labels (dict): Dictionary of all label types.
    """
    da_distance_matrix = generate_da_distance_matrix(save_dir, labels['da'])
    save_distance_matrix(save_dir, da_distance_matrix, 'da_distance_matrix')

    ap_distance_matrix = generate_ap_distance_matrix(labels['ap'])
    save_distance_matrix(save_dir, ap_distance_matrix, 'ap_distance_matrix')

    ap_type_distance_matrix = generate_ap_type_distance_matrix(save_dir, labels['ap_type'])
    save_distance_matrix(save_dir, ap_type_distance_matrix, 'ap_type_distance_matrix')

    ap_distance_matrix = generate_ap_distance_matrix(labels['ap'], postfix_only=True)
    save_distance_matrix(save_dir, ap_distance_matrix, 'ap_postfix_only_distance_matrix')

    ap_type_distance_matrix = generate_ap_type_distance_matrix(save_dir, labels['ap_type'], postfix_only=True)
    save_distance_matrix(save_dir, ap_type_distance_matrix, 'ap_type_postfix_only_distance_matrix')
