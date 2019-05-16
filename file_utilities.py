import traceback
import json


def load_json_data(path, file_name):
    try:
        with open(path + file_name + ".json") as file:
            data = json.load(file)

    except (IOError, ValueError):
        traceback.print_exc()
        return False

    return data


def save_json_data(path, file_name, data):
    with open(path + file_name + '.json', 'w+') as file:
        json.dump(data, file, sort_keys=False, indent=4, separators=(',', ': '))


def load_txt_data(path, file_name):
    with open(path + "/" + file_name + ".txt", "r") as file:

        # Read a line and strip newline char
        lines = [line.rstrip('\r\n') for line in file.readlines()]

    return lines


def split_label_groups(labels):

    labels_groups = []
    group = []

    for line in labels:

        # If line isn't empty add it to the group
        if line is not "":
            group.append(line)
        # Else we have reached the end of the group
        else:
            labels_groups.append(group)
            group = []
    # Don't miss the last group
    labels_groups.append(group)
    return labels_groups
