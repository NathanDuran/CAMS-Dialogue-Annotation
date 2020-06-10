import os
import json
import pandas as pd
import pickle


def load_json_data(path):
    with open(path) as file:
        data = json.load(file)
    return data


def save_json_data(path, data):
    with open(path, 'w+') as file:
        json.dump(data, file, sort_keys=False, indent=4, separators=(',', ': '))


def load_dataframe(path, multi_index=False, num_header_rows=1):
    # Create list for the number of rows with headers
    header_rows = [0 + i for i in range(num_header_rows + 1)]
    if multi_index:
        return pd.read_csv(path, header=header_rows, index_col=[0], skipinitialspace=True)
    else:
        return pd.read_csv(path, index_col=0)


def save_dataframe(path, data, index_label=None):
    data.to_csv(path, index_label=index_label)


def load_pickle(path):
    with open(path, 'rb') as file:
        return pickle.load(file)


def save_pickle(path, data):
    with open(path, 'wb') as file:
        pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)


def load_user_data(path):
    """Loads each of the user .json files as a dictionary and saves to a list."""
    # Get all the user data file names
    user_files = os.listdir(path)

    # Load the user json as dictionary and save to a list
    user_data = []
    for file in user_files:
        file_name = file.split('.')[0]
        file_name += ".json"
        user_data.append(load_json_data(os.path.join(path, file_name)))

    return user_data


def load_labels(labels_dir, user_data):
    """Loads all of the DA, AP and AP-Types assigned by users and returns a dictionary."""
    ap_labels, da_labels = [], []
    ap_type_labels = set()

    # Load the AP and DA labels
    label_data = load_json_data(os.path.join(labels_dir, 'labels.json'))

    # Get the AP labels from the json
    for group in label_data['ap-labels']:
        for label in range(len(group['group'])):
            ap_labels.append(group['group'][label]['name'])

    # Get the DA labels from the json
    for group in label_data['da-labels']:
        for label in range(len(group['group'])):
            da_labels.append(group['group'][label]['name'])

    # Get the user assigned AP-type labels
    for user in user_data:
        for dialogue in user['dialogues']:
            for utt in dialogue['utterances']:
                ap_type_labels.add(utt['ap_label'] + '-' + utt['da_label'])

    # Save to dictionary
    labels = dict()
    labels['ap'] = ap_labels
    labels['da'] = da_labels
    labels['ap_type'] = sorted(list(ap_type_labels))
    return labels


def dataframe_wide_to_long(data):
    """Utility function for reshaping dataframes for plotting.
    Converts from 'wide' to 'long' format, where each observation is on a separate row.

    Example input:
              Multi-Pi
                 ap        da   ap type
    set 1  0.127465  0.404772  0.110144
    set 2  0.053677  0.252012  0.051167
    set 3  0.071018  0.367728  0.073543
    set 4  0.127416  0.465957  0.137216
    set 5  0.145793  0.441656  0.157172
    mean   0.105074  0.386425  0.105849

    Example output:
        index    metric group     value
    0   set 1  Multi-Pi    ap  0.127465
    1   set 2  Multi-Pi    ap  0.053677
    2   set 3  Multi-Pi    ap  0.071018
    3   set 4  Multi-Pi    ap  0.127416
    4   set 5  Multi-Pi    ap  0.145793
    5    mean  Multi-Pi    ap  0.105074
    ...etc
    """
    data = data.copy()
    data = data.reset_index().melt(id_vars=["index"])
    data = data.rename(columns={'variable_0': 'metric', 'variable_1': 'group'})
    data = data.dropna()
    return data
