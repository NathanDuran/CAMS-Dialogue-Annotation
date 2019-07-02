# Generates labels json from plain text labels
import utilities as utils


# Splits label groups on empty lines and returns 2d array of groups
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


# Load text data
label_data_path = "static/labels/"
ap_labels_data = utils.load_txt_data(label_data_path, 'ap_labels')
da_labels_data = utils.load_txt_data(label_data_path, 'da_labels')

# Split into groups
ap_labels = split_label_groups(ap_labels_data)
da_labels = split_label_groups(da_labels_data)

labels_dict = dict()

# Generate ap labels
tmp_groups = []
for group in ap_labels:

    tmp_group_dict = dict()
    tmp_group = []
    for label in group:
        tmp_label = dict()
        tmp_label['name'] = label
        tmp_label['alt_name'] = ""
        tmp_label['description'] = ""
        tmp_label['example'] = ""
        tmp_group.append(tmp_label)
    tmp_group_dict['group'] = tmp_group
    tmp_groups.append(tmp_group_dict)

labels_dict['ap-labels'] = tmp_groups

# Generate da labels
tmp_groups = []
for group in da_labels:

    tmp_group_dict = dict()
    tmp_group = []
    for label in group:
        tmp_label = dict()
        tmp_label['name'] = label
        tmp_label['alt_name'] = ""
        tmp_label['description'] = ""
        tmp_label['example'] = ""
        tmp_group.append(tmp_label)
    tmp_group_dict['group'] = tmp_group
    tmp_groups.append(tmp_group_dict)

labels_dict['da-labels'] = tmp_groups

utils.save_json_data(label_data_path, "labels", labels_dict)