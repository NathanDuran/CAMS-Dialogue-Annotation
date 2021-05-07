import os
import pandas as pd
from itertools import combinations
from scipy.stats import levene, shapiro
from data_processing.agreement_statistics import multi_pi, multi_kappa, alpha, alpha_prime, beta
from data_processing.data_utilities import load_dataframe, save_dataframe, load_pickle, save_pickle, dataframe_wide_to_long
from data_processing.plot_utilities import plot_facetgrid, plot_dist_chart
from data_processing.stats_utilites import t_test, multi_t_test, anova_test, tukey_hsd, chi_squared, jensen_shannnon

# Load the distance matrices for weighted agreement stats
label_data_dir = 'label_data'
try:
    da_distance_matrix = load_dataframe(os.path.join(label_data_dir, "da_distance_matrix.csv"))
    ap_distance_matrix = load_dataframe(os.path.join(label_data_dir, "ap_distance_matrix.csv"))
    ap_type_distance_matrix = load_dataframe(os.path.join(label_data_dir, "ap_type_distance_matrix.csv"))
    # Postfix only distance matrices
    ap_postfix_only_distance_matrix = load_dataframe(os.path.join(label_data_dir, "ap_postfix_only_distance_matrix.csv"))
    ap_type_postfix_only_distance_matrix = load_dataframe(os.path.join(label_data_dir, "ap_type_postfix_only_distance_matrix.csv"))
except FileNotFoundError:
    print("Unable to load on of: "
          "\'da_distance_matrix.csv\', \'ap_distance_matrix.csv\' or \'ap_type_distance_matrix.csv\'. "
          "If the files are not present in " + label_data_dir + " directory please generate them using "
          "the generate_label_distance_matrices() function in label_distance_utilities.py.")


def get_user_label_data(path, user_data, labels, sets_list, dialogue_groups):
    """Utility function either loads user_label_data dictionary or generates and saves it.

    Args:
        path (str): Path to load or save label_data.pkl.
        user_data (list): List of user data dictionaries.
        labels (dict): Dictionary of all labels.
        sets_list (list): List of all dialogue sets.
        dialogue_groups (dict): Dictionary of all dialogue groups (task/non-task and corpora).

    Returns:
        label_data (dict): Dictionary of all dataframes created.
        keys:
        ['sets_labels', 'practice_dialogue', 'kvret_dialogues', 'babl_dialogues', 'task_oriented_dialogues',
        'scose_dialogues', 'cabnc_dialogues', 'non_task_oriented_dialogues']
        values:
        Dictionary with set or dialogue names as keys and Dictionary of users as values.
        (values dict has user_names as keys and Dataframe of individual labels for set/dialogue).
    """
    # If the file exists just load it, else generate the data and save
    if os.path.exists(path):
        user_label_data = load_pickle(path)
    else:
        user_label_data = dict()
        user_label_data['sets_labels'] = get_user_by_sets(user_data, labels, sets_list)
        for group_key in dialogue_groups.keys():
            user_label_data[group_key] = get_users_by_dialogues(user_data, labels, dialogue_groups[group_key])
        save_pickle(path, user_label_data)

    return user_label_data


def get_user_by_sets(user_data, labels, sets):
    """Returns dictionary of all user label dataframes for a list of sets."""
    sets_dict = dict()
    # Iterate over all dialogues and utterances and count all labels in each dialogue
    for set_name in sets:
        user_counts = dict()
        for user in user_data:

            if user['dataset'] == set_name:
                # Need to sort the user dialogues because they were shuffled during experiment
                for user_dialogue in sorted(user['dialogues'], key=lambda k: k['dialogue_id']):

                    # Create new user dictionary if this is the first time seeing it
                    if user['user_id'] not in user_counts.keys():
                        user_counts[user['user_id']] = dict()

                    # Count the current dialogue labels
                    current_user = user_counts[user['user_id']]
                    count_dialogue_utterance_labels(current_user, user_dialogue, labels)

        # Combine the users (per utterance) label counts into dataframes of label type
        sets_dict[set_name] = label_counts_to_dataframes(user_counts, labels)
    return sets_dict


def get_users_by_dialogues(user_data, labels, dialogues):
    """Returns dictionary of all user label dataframes for a list of dialogues."""
    dialogue_dict = dict()
    # Iterate over all dialogues and utterances and count all labels in each dialogue
    for dialogue in dialogues:
        user_counts = dict()
        for user in user_data:

            for user_dialogue in user['dialogues']:
                if user_dialogue['dialogue_id'] == dialogue:

                    # Create new user dictionary if this is the first time seeing it
                    if user['user_id'] not in user_counts.keys():
                        user_counts[user['user_id']] = dict()

                    # Count the current dialogue labels
                    current_user = user_counts[user['user_id']]
                    count_dialogue_utterance_labels(current_user, user_dialogue, labels)

        # Combine the users (per utterance) label counts into dataframes of label type
        dialogue_dict[dialogue] = label_counts_to_dataframes(user_counts, labels)
    return dialogue_dict


def count_dialogue_utterance_labels(current_item, dialogue, labels):
    """Count labels for each utterance of a dialogue. current_item could be a set, dialogue or user."""
    for i, utt in enumerate(dialogue['utterances']):
        # Concatenate the index so we don't count identical utterances the same
        curr_utt = str(i) + "_" + utt['text']
        # Create new lists if this is the first time seeing this utterance
        if curr_utt not in current_item.keys():
            current_item[curr_utt] = dict()
            current_item[curr_utt]['ap'] = [0] * len(labels['ap'])
            current_item[curr_utt]['da'] = [0] * len(labels['da'])
            current_item[curr_utt]['ap_type'] = [0] * len(labels['ap_type'])

        # Increase counts for each type of label
        current_item[curr_utt]['ap'][labels['ap'].index(utt['ap_label'])] += 1
        current_item[curr_utt]['da'][labels['da'].index(utt['da_label'])] += 1
        current_item[curr_utt]['ap_type'][labels['ap_type'].index(utt['ap_label'] + '-' + utt['da_label'])] += 1


def label_counts_to_dataframes(label_counts, labels):
    """Converts users dictionary of label counts (per utterance) into one dictionary of dataframes."""
    # Iterate over each set and create dataframe of label counts
    set_dict = dict()
    for item in label_counts.keys():
        current_item = label_counts[item]

        # Create a dataframe for AP
        ap_counts = [current_item[utt]['ap'] for utt in current_item]
        ap_frame = pd.DataFrame(ap_counts, columns=labels['ap'])

        # Create a dataframe for DA
        da_counts = [current_item[utt]['da'] for utt in current_item]
        da_frame = pd.DataFrame(da_counts, columns=labels['da'])

        # Create a dataframe for AP-Types
        ap_type_counts = [current_item[utt]['ap_type'] for utt in current_item]
        ap_type_frame = pd.DataFrame(ap_type_counts, columns=labels['ap_type'])

        # Concatenate
        set_frame = pd.concat([ap_frame, da_frame, ap_type_frame], axis=1)

        # Add the utterance text column
        set_frame.insert(0, 'text', current_item.keys())

        # Add to sets dictionary
        set_dict[item] = set_frame

    return set_dict


def get_label_type(data, label_type, labels):
    """Returns only the specific label columns for a given dictionary of dataframes."""
    result_dict = dict()
    for item in data.keys():
        if label_type == 'ap':
            result_dict[item] = data[item][labels['ap']]
        elif label_type == 'da':
            result_dict[item] = data[item][labels['da']]
        elif label_type == 'ap_type':
            result_dict[item] = data[item][labels['ap_type']]

    return result_dict


def da_distance(label_a, label_b):
    return da_distance_matrix.loc[label_a, label_b]


def ap_distance(label_a, label_b):
    return ap_distance_matrix.loc[label_a, label_b]


def ap_type_distance(label_a, label_b):
    return ap_type_distance_matrix.loc[label_a, label_b]


# Postfix only distance functions
def ap_postfix_only_distance(label_a, label_b):
    return ap_postfix_only_distance_matrix.loc[label_a, label_b]


def ap_type_postfix_only_distance(label_a, label_b):
    return ap_type_postfix_only_distance_matrix.loc[label_a, label_b]


def get_multi_pi(data, labels, add_mean=True):
    """Gets Multi-pi for each label type of a given set or dialogue set.

    Multi-pi is calculated using cumulative/sum of coder labels for a given utterance.

    Args:
        data (dict): Dictionary with set or dialogue names as keys and Dictionary as values
                    (values dict has user_names as keys and Dataframe of individual labels for set/dialogue).
        labels (dict): Dictionary of all labels.
        add_mean (bool): Whether to add a mean row to the resulting dataframe. Default=True.

    Returns:
        multi_pi_df (DataFrame): Rows are set or dialogue id, columns are label type and items are multi-kappa.
    """
    multi_pi_dict = dict()
    # For each set or dialogue in items list
    for item in data.keys():
        current = dict()
        users_dict = data[item]

        # Get each label type as a dataframe
        da = get_label_type(users_dict, 'da', labels)
        ap = get_label_type(users_dict, 'ap', labels)
        ap_type = get_label_type(users_dict, 'ap_type', labels)

        # Get the multi-pi stat for each label type
        current['da'] = multi_pi(da)
        current['ap'] = multi_pi(ap)
        current['ap type'] = multi_pi(ap_type)

        # Remove '_' from names
        multi_pi_dict[item.replace("_", " ")] = current

    # Create multi_pi_df dataframe and add mean for each row
    multi_pi_df = pd.DataFrame.from_dict(multi_pi_dict, orient='index')
    if add_mean:
        multi_pi_df.loc['mean'] = multi_pi_df.mean()
    multi_pi_df.columns = pd.MultiIndex.from_product([['Multi-Pi'], multi_pi_df.columns])
    return multi_pi_df


def get_multi_kappa(data, labels, add_mean=True):
    """Gets Multi-kappa for each label type of a given set or dialogue set.

    Multi-kappa is calculated using the pairwise average of each coder-pair.

    Args:
        data (dict): Dictionary with set or dialogue names as keys and Dictionary as values
                    (values dict has user_names as keys and Dataframe of individual labels for set/dialogue).
        labels (dict): Dictionary of all labels.
        add_mean (bool): Whether to add a mean row to the resulting dataframe. Default=True.

    Returns:
        multi_kappa_df (DataFrame): Rows are set or dialogue id, columns are label type and items are multi-kappa.
    """
    multi_kappa_dict = dict()
    # For each set or dialogue in items list
    for item in data.keys():
        current = dict()
        users_dict = data[item]

        # Get each label type as a dataframe
        da = get_label_type(users_dict, 'da', labels)
        ap = get_label_type(users_dict, 'ap', labels)
        ap_type = get_label_type(users_dict, 'ap_type', labels)

        # Get the multi-kappa stat for each label type
        current['da'] = multi_kappa(da)
        current['ap'] = multi_kappa(ap)
        current['ap type'] = multi_kappa(ap_type)

        # Remove '_' from names
        multi_kappa_dict[item.replace("_", " ")] = current

    # Create multi_kappa_df dataframe and add mean for each row
    multi_kappa_df = pd.DataFrame.from_dict(multi_kappa_dict, orient='index')
    if add_mean:
        multi_kappa_df.loc['mean'] = multi_kappa_df.mean()
    multi_kappa_df.columns = pd.MultiIndex.from_product([['Multi-Kappa'], multi_kappa_df.columns])
    return multi_kappa_df


def get_weighted_agreement(data, labels, stat_type, add_mean=True, postfix_only=False):
    """Gets Alpha, Alpha Prime or Beta for each label type of a given set or dialogue set.

    Weighted agreement is calculated using the pairwise average of each coder-pair.

    Args:
        data (dict): Dictionary with set or dialogue names as keys and Dictionary as values
                    (values dict has user_names as keys and Dataframe of individual labels for set/dialogue).
        labels (dict): Dictionary of all labels.
        stat_type (str): Which agreement statistic to use. Must be one of Alpha, Alpha Prime (Alpha') or Beta.
        add_mean (bool): Whether to add a mean row to the resulting dataframe. Default=True.
        postfix_only (bool): Whether to use the postfix only distance function. Default=False.

    Returns:
        weighted_df (DataFrame): Rows are set or dialogue id, columns are label type and items are alpha prime.
    """
    # Get the desired agreement function
    if stat_type.lower() == 'alpha':
        weighted_agreement_func = alpha
    elif stat_type.lower() == 'alpha\'' or stat_type.lower() == 'alpha prime':
        weighted_agreement_func = alpha_prime
    elif stat_type.lower() == 'beta':
        weighted_agreement_func = beta
    else:
        raise ValueError("Invalid weighted agreement type: \"" + stat_type + "\". "
                         "Must be one of \"Alpha\", \"Alpha Prime\", \"Alpha\'\" or \"Beta\".")

    weighted_dict = dict()
    # For each set or dialogue in items list
    for item in data.keys():
        current = dict()
        users_dict = data[item]

        # Get each label type as a dataframe
        da = get_label_type(users_dict, 'da', labels)
        ap = get_label_type(users_dict, 'ap', labels)
        ap_type = get_label_type(users_dict, 'ap_type', labels)

        # Get the weighted agreement stat for each label type
        current['da'] = weighted_agreement_func(da, da_distance)
        if not postfix_only:
            current['ap'] = weighted_agreement_func(ap, ap_distance)
            current['ap type'] = weighted_agreement_func(ap_type, ap_type_distance)
        else:
            current['ap'] = weighted_agreement_func(ap, ap_postfix_only_distance)
            current['ap type'] = weighted_agreement_func(ap_type, ap_type_postfix_only_distance)

        # Remove '_' from names
        weighted_dict[item.replace("_", " ")] = current

    # Create weighted_df dataframe and add mean for each row
    weighted_df = pd.DataFrame.from_dict(weighted_dict, orient='index')
    if add_mean:
        weighted_df.loc['mean'] = weighted_df.mean()
    weighted_df.columns = pd.MultiIndex.from_product([[stat_type], weighted_df.columns])
    return weighted_df


def generate_set_agreement_data(users_data, labels, group_name, save_dir, save=True, show=True, add_mean=True, postfix_only=False):
    """Utility function that generates all agreement statistics for dialogue sets.

    Creates a DataFrame of the results and saves to .csv and creates a multi-graph plot and saves to .png.

    Args:
        users_data (dict): Dictionary with set or dialogue names as keys and Dictionary of users as values.
        (values dict has user_names as keys and Dataframe of individual labels for set/dialogue).
        labels (dict): Dictionary of all labels.
        group_name (str): Name of set or dialogue group for file/graph titles.
        save_dir (str): Directory to save the resulting .csv and .png files to.
        save (bool): Whether to save the resulting .csv and .png files. Default=True.
        show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
        add_mean (bool): Whether to add a mean row to the data. Default=True.
        postfix_only (bool): Whether to use the postfix only distance function. Default=False.
    """
    # Create dataframe of agreement by set
    alpha_df = get_weighted_agreement(users_data, labels, 'Alpha', add_mean=add_mean, postfix_only=postfix_only)
    beta_df = get_weighted_agreement(users_data, labels, 'Beta', add_mean=add_mean, postfix_only=postfix_only)

    # Group stats into one dataframe
    group_frame = pd.concat([alpha_df, beta_df], axis=1)

    # Generate a group plot for all stats
    data = dataframe_wide_to_long(group_frame)
    g, plt = plot_facetgrid(data, title='', axis_titles=True, share_y=False, num_col=1, show_bar_value=True,
                            legend_loc='upper right', num_legend_col=1)
    g, plt = annotate_landis_koch(g, plt)  # Annotate with landis and koch range

    # Save and show results
    if show:
        print(group_frame)
        plt.show()
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), group_frame)
        g.savefig(os.path.join(save_dir, group_name + ".png"))

    return group_frame, plt


def generate_group_agreement_data(group_data, groups,  labels, group_name, save_dir, save=True, show=True, add_mean=True, postfix_only=False):
    """Utility function that generates all mean agreement statistics for a given group of data.

    Creates a DataFrame of the results and saves to .csv and creates a multi-graph plot and saves to .png.

    Args:
        group_data (dict): Dictionary with set or dialogue names as keys and Dictionary of users as values.
        (values dict has user_names as keys and Dataframe of individual labels for set/dialogue).
        groups (list): List of groups to process together. Should be keys in the group_data dict.
        labels (dict): Dictionary of all labels.
        group_name (str): Name of set or dialogue group for file/graph titles.
        save_dir (str): Directory to save the resulting .csv and .png files to.
        save (bool): Whether to save the resulting .csv and .png files. Default=True.
        show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
        add_mean (bool): Whether to add a mean row to the data. Default=True.
        postfix_only (bool): Whether to use the postfix only distance function. Default=False.
    """
    # Create dataframe of agreement by group
    groups_frame = pd.DataFrame()
    for group in groups:
        # Get alpha and beta
        alpha_df = get_weighted_agreement(group_data[group], labels, 'Alpha', add_mean=add_mean, postfix_only=postfix_only)
        beta_df = get_weighted_agreement(group_data[group], labels, 'Beta', add_mean=add_mean, postfix_only=postfix_only)

        # Create a frame for this group
        group_frame = pd.concat([alpha_df, beta_df], axis=1)
        group_frame.insert(loc=0, column='group', value=group.replace("_", " ").split()[0])
        # Add to groups frame
        groups_frame = pd.concat([groups_frame, group_frame], axis=0)

    # Generate a group plot for all stats
    data = groups_frame.reset_index().melt(id_vars=['index', 'group'])
    data = data.rename(columns={'variable_0': 'metric', 'variable_1': 'label_type'})
    data = data.dropna()
    g, plt = plot_facetgrid(data, x='group', y='value', hue='label_type', title='', axis_titles=True,
                            num_col=1, share_y=False, show_bar_value=True, ci=None,
                            legend_loc='upper right',num_legend_col=1)
    g, plt = annotate_landis_koch(g, plt)  # Annotate with landis and koch range

    # Save and show results
    if show:
        print(groups_frame)
        plt.show()
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), groups_frame)
        g.savefig(os.path.join(save_dir, group_name + ".png"))

    return groups_frame, plt


def generate_full_agreement_data(group_data, groups,  labels, group_name, save_dir, save=True, show=True, add_mean=True, postfix_only=False):
    """Utility function that generates all agreement statistics for a given group of data.

    Creates a DataFrame of the results and saves to .csv and creates a multi-graph plot and saves to .png.

    Args:
        group_data (dict): Dictionary with set or dialogue names as keys and Dictionary of users as values.
        (values dict has user_names as keys and Dataframe of individual labels for set/dialogue).
        groups (list): List of groups to process together. Should be keys in the group_data dict.
        labels (dict): Dictionary of all labels.
        group_name (str): Name of set or dialogue group for file/graph titles.
        save_dir (str): Directory to save the resulting .csv and .png files to.
        save (bool): Whether to save the resulting .csv and .png files. Default=True.
        show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
        add_mean (bool): Whether to add a mean row to the data. Default=True.
        postfix_only (bool): Whether to use the postfix only distance function. Default=False.
    """
    # Create dataframe of agreement by group
    groups_frame = pd.DataFrame()
    for group in groups:
        # Get alpha and Beta
        alpha_df = get_weighted_agreement(group_data[group], labels, 'Alpha', add_mean=add_mean, postfix_only=postfix_only)
        beta_df = get_weighted_agreement(group_data[group], labels, 'Beta', add_mean=add_mean, postfix_only=postfix_only)

        # Create a frame for this group
        group_frame = pd.concat([alpha_df, beta_df], axis=1)
        group_frame.insert(loc=0, column='group', value=group.replace("_", " ").split()[0])
        # Add to groups frame
        groups_frame = pd.concat([groups_frame, group_frame], axis=0)

    # Generate a group plot for all stats
    data = groups_frame.reset_index().melt(id_vars=['index', 'group'])
    data = data.rename(columns={'variable_0': 'metric', 'variable_1': 'label_type'})
    data = data.dropna()

    g, plt = plot_facetgrid(data, x='index', y='value', hue='label_type', row='metric', col='group', title='',
                            axis_titles=True, share_y=False, num_col=None, show_bar_value=True, ci=None,
                            legend_loc='upper right')
    g, plt = annotate_landis_koch(g, plt)  # Annotate with landis and koch range

    # Save and show results
    if show:
        print(groups_frame)
        plt.show()
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), groups_frame)
        g.savefig(os.path.join(save_dir, group_name + ".png"))

    return groups_frame, plt


def generate_dialogue_type_agreement_statistics(group_name, save_dir, save=True, show=True):
    """Utility function that generates all p-values and effect size for dialogue type groups of data.

      Creates a DataFrame of the results and saves to .csv.

       Args:
           group_name (str): Name of set for file/graph titles.
           save_dir (str): Directory to save the resulting .csv and .png files to.
           save (bool): Whether to save the resulting .csv and .png files. Default=True.
           show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
    """
    # Load the task and non-task dialogue agreement stats
    types_data = load_dataframe(os.path.join(save_dir, 'Dialogue Agreement.csv'), multi_index=True)
    types_data.drop('mean', inplace=True)
    types_data.columns = pd.MultiIndex.from_tuples([('group', '')] + types_data.columns.to_list()[1:])
    types_data = types_data.reset_index().melt(id_vars=['index', 'group'])
    types_data.rename(columns={'variable_0': 'agreement_stat', 'variable_1': 'label_type'}, inplace=True)

    # Generate the pairwise t-test data for label types per group and agreement statistic
    dialogue_type_frame = pd.DataFrame()
    basic_stat_frame = pd.DataFrame()
    for stat_type in ['Alpha', 'Beta']:
        # Select only this agreement stat data
        stat_type_data = types_data.loc[types_data['agreement_stat'] == stat_type]

        # Generate the pairwise t-test data for label types per group
        type_frame = multi_t_test(stat_type_data, 'group', 'label_type', 'value')

        # Reindex
        type_frame.reset_index(inplace=True)
        type_frame.rename(columns={'index': 'label_type'}, inplace=True)

        # Add t-test for all combined label types
        type_frame = type_frame.append(t_test(stat_type_data, 'group', 'value'), ignore_index=True, sort=False)
        type_frame.loc[3, 'label_type'] = 'all'

        # # Add the anova for the full group effect size
        # anova_groups = anova_test(stat_type_data, 'group', 'value')
        # type_frame.loc[3, 'eta_sq'] = anova_groups.loc['C(group)', 'eta_sq']
        # type_frame.loc[3, 'omega_sq'] = anova_groups.loc['C(group)', 'omega_sq']

        # Concatenate the type frame
        type_frame.columns = pd.MultiIndex.from_product([[stat_type], type_frame.columns])
        dialogue_type_frame = pd.concat([dialogue_type_frame, type_frame], axis=1, sort=False)

        # Get mean, sd and min/max for groups per agreement statistic
        group_tmp = pd.DataFrame()
        for group in stat_type_data.group.unique():
            group_data = stat_type_data.loc[stat_type_data['group'] == group]
            tmp = group_data.groupby(['label_type'], sort=False).agg({'value': ['min', 'max', 'mean', 'std']})
            tmp.columns = tmp.columns.droplevel()
            tmp = tmp.T
            tmp.columns = pd.MultiIndex.from_product([[stat_type + " " + group], tmp.columns])
            group_tmp = pd.concat([group_tmp, tmp], axis=1)

            # # Test for normality and heteroscedasticity
            # da_values = group_data.loc[group_data['label_type'] == 'da']['value'].to_list()
            # ap_values = group_data.loc[group_data['label_type'] == 'ap']['value'].to_list()
            # ap_type_values = group_data.loc[group_data['label_type'] == 'ap type']['value'].to_list()
            # print(stat_type + " " + group)
            # print("Test for normal distribution:")
            # da_w, da_p = shapiro(da_values)
            # print("DA w: " + str(round(da_w, 6)) + " p-value: " + str(round(da_p, 6)))
            # ap_w, ap_p = shapiro(ap_values)
            # print("AP w: " + str(round(ap_w, 6)) + " p-value: " + str(round(ap_p, 6)))
            # ap_type_w, ap_type_p = shapiro(ap_type_values)
            # print("AP-type w: " + str(round(ap_type_w, 6)) + " p-value: " + str(round(ap_type_p, 6)))
            #
            # print("Test for heteroscedasticity:")
            # levene_t, levene_p = levene(da_values, ap_values, ap_type_values)
            # print("t: " + str(round(levene_t, 6)) + " p-value: " + str(round(levene_p, 6)))

        # Add to basic stats frame
        basic_stat_frame = pd.concat([basic_stat_frame, group_tmp], axis=1)

    # Save and show results
    if show:
        print('Compare Task-oriented and Non-task-oriented dialogues:')
        print(dialogue_type_frame)
        print('General Task-oriented and Non-task-oriented stats:')
        print(basic_stat_frame)
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), dialogue_type_frame)
        save_dataframe(os.path.join(save_dir, group_name + " (basic).csv"), basic_stat_frame)
    return dialogue_type_frame, basic_stat_frame


def generate_corpora_agreement_statistics(group_name, save_dir, save=True, show=True):
    """Utility function that generates all p-values and effect size for corpora groups of data.

      Creates a DataFrame of the results and saves to .csv.

       Args:
           group_name (str): Name of set for file/graph titles.
           save_dir (str): Directory to save the resulting .csv and .png files to.
           save (bool): Whether to save the resulting .csv and .png files. Default=True.
           show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
    """
    # Load the corpora agreement stats
    corpora_data = load_dataframe(os.path.join(save_dir, 'Dialogue Corpora Agreement.csv'), multi_index=True)
    corpora_data.drop('mean', inplace=True)
    corpora_data.columns = pd.MultiIndex.from_tuples([('group', '')] + corpora_data.columns.to_list()[1:])
    corpora_data = corpora_data.reset_index().melt(id_vars=['index', 'group'])
    corpora_data.rename(columns={'variable_0': 'agreement_stat', 'variable_1': 'label_type'}, inplace=True)

    # Generate the pairwise t-test data for label types per group and agreement statistic
    corpora_type_frame = pd.DataFrame()
    basic_stat_frame = pd.DataFrame()
    for stat_type in ['Alpha', 'Beta']:
        # Select only this agreement stat data
        corpora_stat_data = corpora_data.loc[corpora_data['agreement_stat'] == stat_type]

        # Get pairwise comparisons for each label type and combined
        for label_type in ['DA', 'AP', 'AP type', 'All']:
            # Get the data for the current label type
            if label_type == 'All':
                corpora_label_data = corpora_stat_data
            else:
                corpora_label_data = corpora_stat_data.loc[corpora_stat_data['label_type'] == label_type.lower()]

            # Generate Tukey HSD, compare corpora dialogues
            label_type_frame = tukey_hsd(corpora_label_data, 'group', 'value')

            # Add the anova for the full corpora comparison and effect size
            anova_corpora = anova_test(corpora_label_data, 'group', 'value')
            label_type_frame.loc[6, 'p-value'] = anova_corpora.loc['C(group)', 'PR(>F)']
            label_type_frame.loc[6, 'eta_sq'] = anova_corpora.loc['C(group)', 'eta_sq']
            label_type_frame.loc[6, 'omega_sq'] = anova_corpora.loc['C(group)', 'omega_sq']
            label_type_frame.loc[6, 'cohen_f'] = anova_corpora.loc['C(group)', 'cohen_f']
            label_type_frame.loc[6, 'n'] = anova_corpora.loc['C(group)', 'n']
            label_type_frame.loc[6, 'exp_n'] = anova_corpora.loc['C(group)', 'exp_n']
            label_type_frame.loc[6, 'power'] = anova_corpora.loc['C(group)', 'power']
            label_type_frame.loc[6, 'exp_power'] = anova_corpora.loc['C(group)', 'exp_power']

            label_type_frame.columns = pd.MultiIndex.from_product([[stat_type + " " + label_type], label_type_frame.columns])
            corpora_type_frame = pd.concat([corpora_type_frame, label_type_frame], axis=1)

        # Get mean, sd and min/max for groups per agreement statistic
        group_tmp = pd.DataFrame()
        for group in corpora_stat_data.group.unique():
            group_data = corpora_stat_data.loc[corpora_stat_data['group'] == group]
            tmp = group_data.groupby(['label_type'], sort=False).agg({'value': ['min', 'max', 'mean', 'std']})
            tmp.columns = tmp.columns.droplevel()
            tmp = tmp.T
            tmp.columns = pd.MultiIndex.from_product([[stat_type + " " + group], tmp.columns])
            group_tmp = pd.concat([group_tmp, tmp], axis=1)

            # # Test for normality and heteroscedasticity
            # da_values = group_data.loc[group_data['label_type'] == 'da']['value'].to_list()
            # ap_values = group_data.loc[group_data['label_type'] == 'ap']['value'].to_list()
            # ap_type_values = group_data.loc[group_data['label_type'] == 'ap type']['value'].to_list()
            # print(stat_type + " " + group)
            # print("Test for normal distribution:")
            # da_w, da_p = shapiro(da_values)
            # print("DA w: " + str(round(da_w, 6)) + " p-value: " + str(round(da_p, 6)))
            # ap_w, ap_p = shapiro(ap_values)
            # print("AP w: " + str(round(ap_w, 6)) + " p-value: " + str(round(ap_p, 6)))
            # ap_type_w, ap_type_p = shapiro(ap_type_values)
            # print("AP-type w: " + str(round(ap_type_w, 6)) + " p-value: " + str(round(ap_type_p, 6)))
            #
            # print("Test for heteroscedasticity:")
            # levene_t, levene_p = levene(da_values, ap_values, ap_type_values)
            # print("t: " + str(round(levene_t, 6)) + " p-value: " + str(round(levene_p, 6)))

        # Add to basic stats frame
        basic_stat_frame = pd.concat([basic_stat_frame, group_tmp], axis=1)

    # Save and show results
    if show:
        print('Compare Corpora:')
        print(corpora_type_frame)
        print('General Corpora stats:')
        print(basic_stat_frame)
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), corpora_type_frame)
        save_dataframe(os.path.join(save_dir, group_name + " (basic).csv"), basic_stat_frame)
    return corpora_type_frame, basic_stat_frame


def generate_label_type_agreement_statistics(group_name, save_dir, save=True, show=True):
    """Utility function that generates p-values and effect size for pairwise comparisons of label type agreement data.

      Creates a DataFrame of the results and saves to .csv.

       Args:
           group_name (str): Name of set for file/graph titles.
           save_dir (str): Directory to save the resulting .csv and .png files to.
           save (bool): Whether to save the resulting .csv and .png files. Default=True.
           show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
    """
    # Load the task and non-task dialogue agreement stats
    agreement_data = load_dataframe(os.path.join(save_dir, 'Dialogue Agreement.csv'), multi_index=True)
    agreement_data.drop('mean', inplace=True)
    agreement_data.columns = pd.MultiIndex.from_tuples([('group', '')] + agreement_data.columns.to_list()[1:])
    agreement_data = agreement_data.reset_index().melt(id_vars=['index', 'group'])
    agreement_data.rename(columns={'variable_0': 'agreement_stat', 'variable_1': 'label_type'}, inplace=True)

    # Generate the pairwise t-test data for pairwise label types and agreement statistic
    label_type_frame = pd.DataFrame()
    basic_stat_frame = pd.DataFrame()
    for stat_type in ['Alpha', 'Beta']:
        # Select only this agreement stat data
        stat_type_data = agreement_data.loc[agreement_data['agreement_stat'] == stat_type]

        # Generate Tukey HSD, compare label types across task/non-task oriented dialogues
        label_frame = tukey_hsd(stat_type_data, 'label_type', 'value')

        # Add the anova for the full label_type comparison and effect size
        anova_labels = anova_test(stat_type_data, 'label_type', 'value')
        label_frame.loc[3, 'p-value'] = anova_labels.loc['C(label_type)', 'PR(>F)']
        label_frame.loc[3, 'eta_sq'] = anova_labels.loc['C(label_type)', 'eta_sq']
        label_frame.loc[3, 'omega_sq'] = anova_labels.loc['C(label_type)', 'omega_sq']
        label_frame.loc[3, 'cohen_f'] = anova_labels.loc['C(label_type)', 'cohen_f']
        label_frame.loc[3, 'n'] = anova_labels.loc['C(label_type)', 'n']
        label_frame.loc[3, 'exp_n'] = anova_labels.loc['C(label_type)', 'exp_n']
        label_frame.loc[3, 'power'] = anova_labels.loc['C(label_type)', 'power']
        label_frame.loc[3, 'exp_power'] = anova_labels.loc['C(label_type)', 'exp_power']

        # Concatenate the label frame
        label_frame.columns = pd.MultiIndex.from_product([[stat_type], label_frame.columns])
        label_type_frame = pd.concat([label_type_frame, label_frame], axis=1, sort=False)

        # Get mean, sd and min/max for groups per agreement statistic
        tmp = stat_type_data.groupby(['label_type'], sort=False).agg({'value': ['min', 'max', 'mean', 'std']})
        tmp.columns = tmp.columns.droplevel()
        tmp = tmp.T
        tmp.columns = pd.MultiIndex.from_product([[stat_type], tmp.columns])

        # Add to basic stats frame
        basic_stat_frame = pd.concat([basic_stat_frame, tmp], axis=1)

        # # Test for normality and heteroscedasticity
        # da_values = stat_type_data.loc[stat_type_data['label_type'] == 'da']['value'].to_list()
        # ap_values = stat_type_data.loc[stat_type_data['label_type'] == 'ap']['value'].to_list()
        # ap_type_values = stat_type_data.loc[stat_type_data['label_type'] == 'ap type']['value'].to_list()
        # print(stat_type)
        # print("Test for normal distribution:")
        # da_w, da_p = shapiro(da_values)
        # print("DA w: " + str(round(da_w, 6)) + " p-value: " + str(round(da_p, 6)))
        # ap_w, ap_p = shapiro(ap_values)
        # print("AP w: " + str(round(ap_w, 6)) + " p-value: " + str(round(ap_p, 6)))
        # ap_type_w, ap_type_p = shapiro(ap_type_values)
        # print("AP-type w: " + str(round(ap_type_w, 6)) + " p-value: " + str(round(ap_type_p, 6)))
        #
        # print("Test for heteroscedasticity:")
        # levene_t, levene_p = levene(da_values, ap_values, ap_type_values)
        # print("t: " + str(round(levene_t, 6)) + " p-value: " + str(round(levene_p, 6)))

    # Save and show results
    if show:
        print('Compare Label Types:')
        print(label_type_frame)
        print('General Label stats:')
        print(basic_stat_frame)
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), label_type_frame)
        save_dataframe(os.path.join(save_dir, group_name + " (basic).csv"), basic_stat_frame)
    return label_type_frame


def generate_coefficient_agreement_statistics(group_name, save_dir, save=True, show=True):
    """Utility function that generates p-values and effect size for comparisons of agreement coefficient data.

      Creates a DataFrame of the results and saves to .csv.

       Args:
           group_name (str): Name of set for file/graph titles.
           save_dir (str): Directory to save the resulting .csv and .png files to.
           save (bool): Whether to save the resulting .csv and .png files. Default=True.
           show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
    """
    # Load the task and non-task dialogue agreement stats
    agreement_data = load_dataframe(os.path.join(save_dir, 'Dialogue Agreement.csv'), multi_index=True)
    agreement_data.drop('mean', inplace=True)
    agreement_data.columns = pd.MultiIndex.from_tuples([('group', '')] + agreement_data.columns.to_list()[1:])
    agreement_data = agreement_data.reset_index().melt(id_vars=['index', 'group'])
    agreement_data.rename(columns={'variable_0': 'agreement_stat', 'variable_1': 'label_type'}, inplace=True)

    # Generate the pairwise t-test data for label types per group
    stat_type_frame = multi_t_test(agreement_data, 'agreement_stat', 'label_type', 'value')

    # Reindex
    stat_type_frame.reset_index(inplace=True)
    stat_type_frame.rename(columns={'index': 'label_type'}, inplace=True)

    # Add t-test for all combined label types
    stat_type_frame = stat_type_frame.append(t_test(agreement_data, 'agreement_stat', 'value'), ignore_index=True, sort=False)
    stat_type_frame.loc[3, 'label_type'] = 'all'

    # Save and show results
    if show:
        print('Compare Coefficient Types:')
        print(stat_type_frame)
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), stat_type_frame)
    return stat_type_frame


def generate_group_label_distributions(group_data, groups, labels, group_name, save_dir, save=True, show=True):
    """Utility function that generates label distributions for given groups of data.

      Creates a DataFrame of the results and saves to .csv.

       Args:
           group_data (dict): Dictionary with set or dialogue names as keys and Dictionary of users as values.
           groups (list): List of groups to process together. Should be keys in the group_data dict.
           labels (dict): Dictionary of all labels.
           group_name (str): Name of set for file/graph titles.
           save_dir (str): Directory to save the resulting .csv and .png files to.
           save (bool): Whether to save the resulting .csv and .png files. Default=True.
           show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
    """
    # Get all label assignments by group to a dataframe
    group_frame = pd.DataFrame()
    for group in groups:
        for dialogue in group_data[group].values():
            for user_frame in dialogue.values():
                tmp = pd.DataFrame()
                for label_type in ['da', 'ap']:
                    label_tmp = user_frame[labels[label_type]]
                    label_tmp.columns = pd.MultiIndex.from_product([[label_type.upper()], label_tmp.columns])
                    tmp = pd.concat([tmp, label_tmp], axis=1)
                tmp.insert(loc=0, column='group', value=group.replace("_", " ").split()[0])
                group_frame = pd.concat([group_frame, tmp], axis=0)

    # Get totals of all assignments for each label
    count_frame = group_frame.groupby('group', sort=False).sum()
    count_frame.reset_index(col_level=0, inplace=True)

    # Get percentages of all assignments for each label
    dist_frame = count_frame
    for group in groups:
        group_pcnt = group_frame.loc[group_frame['group'] == group.replace("_", " ").split()[0]]
        group_pcnt = 100 / len(group_pcnt) * group_pcnt.sum(axis=0, numeric_only=True)
        group_pcnt = group_pcnt.append(pd.Series([group.replace("_", " ").split()[0] + '-%'], index=[('group', '')]))
        dist_frame = dist_frame.append([group_pcnt], ignore_index=True).round(3)
    pcnt_frame = dist_frame[dist_frame['group'].str.contains('%')]

    # Get all the pariwise combinations of groups
    group_combinations = list(combinations(groups, 2))

    # Compare pairwise distributions of each group
    chi_frame = pd.DataFrame()
    for pair in group_combinations:

        # Get only group name
        group_1 = pair[0].replace("_", " ").split()[0]
        group_2 = pair[1].replace("_", " ").split()[0]

        # Get the lists of labels from each group
        group_1_list = count_frame.loc[(count_frame['group'] == (group_1))].values.flatten().tolist()[1:]
        group_1_da_list = group_1_list[:27]
        group_1_ap_list = group_1_list[-11:]

        group_2_list = count_frame.loc[(count_frame['group'] == (group_2))].values.flatten().tolist()[1:]
        group_2_da_list = group_2_list[:27]
        group_2_ap_list = group_2_list[-11:]

        # Generate Chi squared stats
        stat_da = chi_squared(group_1_da_list, group_2_da_list)
        stat_ap = chi_squared(group_1_ap_list, group_2_ap_list)

        # Create chi stat dataframe
        da_frame = pd.DataFrame.from_dict({'dof': [stat_da[0]], 'critical': [stat_da[1]], 'stat': [stat_da[2]],
                                               'p-value': [stat_da[3]], 'reject': stat_da[4]})
        da_frame.columns = pd.MultiIndex.from_product([['DA'], da_frame.columns])
        ap_frame = pd.DataFrame.from_dict({'dof': [stat_ap[0]], 'critical': [stat_ap[1]], 'stat': [stat_ap[2]],
                                               'p-value': [stat_ap[3]], 'reject': stat_ap[4]})
        ap_frame.columns = pd.MultiIndex.from_product([['AP'], ap_frame.columns])

        tmp_frame = pd.concat([da_frame, ap_frame], axis=1, levels=0)
        tmp_frame.insert(0, 'Group 1', group_1)
        tmp_frame.insert(1, 'Group 2', group_2)
        chi_frame = pd.concat([chi_frame, tmp_frame])

    chi_frame.reset_index(drop=True, inplace=True)

    # Create a bar chart of all assignments
    data = group_frame.melt(id_vars=['group'])
    data = data.rename(columns={'variable_0': 'label_type', 'variable_1': 'label'})
    bar_g, bar_plt = plot_facetgrid(data, x='label', y='value', hue='group', col='label_type',
                                    title='', colour='default', axis_titles=True,
                                    num_col=1, num_legend_col=1, x_tick_rotation=45, ci=None)

    # Create distribution plot of all assignments
    data = count_frame.melt(id_vars=['group'])
    data = data.rename(columns={'index': 'group', 'variable_0': 'label_type', 'variable_1': 'label'})
    # Don't plot histogram if >2 groups
    plt_hist = False if data['group'].nunique() > 2 else True
    dist_g, dist_fig = plot_dist_chart(data, hue='group', col='label_type',
                                       title='', colour='default', axis_titles=True, share_x=True, share_y=True,
                                       plt_hist=plt_hist, num_col=1, all_legend=False, legend_loc='best', num_legend_col=1)

    # Save and show results
    if show:
        print(dist_frame)
        print('Chi-squared:')
        print(chi_frame)
        bar_plt.show()
        dist_fig.show()
    if save:
        save_dataframe(os.path.join(save_dir, group_name + " Label Distributions.csv"), dist_frame)
        save_dataframe(os.path.join(save_dir, group_name + " Chi-Squared.csv"), chi_frame)
        bar_g.savefig(os.path.join(save_dir, group_name + " Label Assignments.png"))
        dist_g.savefig(os.path.join(save_dir, group_name + " Label Distributions.png"))

    return count_frame, bar_plt, dist_fig


def generate_user_label_distributions(user_data, groups, labels, group_name, save_dir, save=True, show=True):
    """Utility function that generates label distributions for user data.

      Creates a DataFrame of the results and saves to .csv.

       Args:
           user_data (dict): Dictionary with set or dialogue names as keys and Dictionary of users as values.
           groups (list): List of groups to process together. Should be keys in the group_data dict.
           labels (dict): Dictionary of all labels.
           group_name (str): Name of set for file/graph titles.
           save_dir (str): Directory to save the resulting .csv and .png files to.
           save (bool): Whether to save the resulting .csv and .png files. Default=True.
           show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
    """
    # Get all label assignments by group to a dataframe
    group_frame = pd.DataFrame()
    for group in groups:
        for user_name, user in user_data[group].items():
            tmp = pd.DataFrame()
            for label_type in ['da', 'ap']:
                label_tmp = user[labels[label_type]]
                label_tmp.columns = pd.MultiIndex.from_product([[label_type.upper()], label_tmp.columns])
                tmp = pd.concat([tmp, label_tmp], axis=1)
            tmp.insert(loc=0, column='group', value=group.replace("_", " "))
            tmp.insert(loc=1, column='user', value=user_name)
            group_frame = pd.concat([group_frame, tmp], axis=0)

    # Get totals of all assignments for each label
    count_frame = group_frame.groupby(['group', 'user'], as_index=True).sum()
    count_frame.reset_index(col_level=0, inplace=True)

    # Get percentages of all assignments for each label
    dist_frame = count_frame
    for user_name in group_frame.user.unique():
        user = group_frame.loc[group_frame['user'] == user_name]
        group = group_frame.loc[group_frame['user'] == user_name]['group'].unique()
        user_pcnt = 100 / len(user) * user.sum(axis=0, numeric_only=True)
        user_pcnt = user_pcnt.append(pd.Series([user_name + '-%'], index=[('user', '')]))
        user_pcnt = user_pcnt.append(pd.Series(group, index=[('group', '')]))
        dist_frame = dist_frame.append([user_pcnt], ignore_index=True).round(3)
    pcnt_frame = dist_frame[dist_frame['user'].str.contains('%')]

    # Compare pairwise distributions of each group
    chi_frame = pd.DataFrame()
    for group in groups:
        # Get all the pariwise combinations of users
        group_data = count_frame.loc[count_frame['group'] == group.replace("_", " ")]
        user_combinations = list(combinations(group_data['user'].unique(), 2))

        for pair in user_combinations:

            # Get the lists of labels from each user
            user_1_list = count_frame.loc[(count_frame['user'] == pair[0])].values.flatten().tolist()[2:]
            user_1_da_list = user_1_list[:27]
            user_1_ap_list = user_1_list[-11:]

            user_2_list = count_frame.loc[(count_frame['user'] == pair[1])].values.flatten().tolist()[2:]
            user_2_da_list = user_2_list[:27]
            user_2_ap_list = user_2_list[-11:]

            # Generate Chi squared stats
            stat_da = chi_squared(user_1_da_list, user_2_da_list)
            stat_ap = chi_squared(user_1_ap_list, user_2_ap_list)

            # Create chi stat dataframe
            da_frame = pd.DataFrame.from_dict({'dof': [stat_da[0]], 'critical': [stat_da[1]], 'chi': [stat_da[2]],
                                               'p-value': [stat_da[3]], 'reject': stat_da[4]})
            da_frame.columns = pd.MultiIndex.from_product([['DA'], da_frame.columns])
            ap_frame = pd.DataFrame.from_dict({'dof': [stat_ap[0]], 'critical': [stat_ap[1]], 'chi': [stat_ap[2]],
                                               'p-value': [stat_ap[3]], 'reject': stat_ap[4]})
            ap_frame.columns = pd.MultiIndex.from_product([['AP'], ap_frame.columns])

            # Compare DA and AP distributions with spearman
            # stat_da = spearmanr(user_1_da_list, user_2_da_list)
            # stat_ap = spearmanr(user_1_ap_list, user_2_ap_list)
            #
            # # Create stat dataframe
            # da_frame = pd.DataFrame.from_dict({'Rho': [stat_da[0]], 'p-value': [stat_da[1]]})
            # da_frame.columns = pd.MultiIndex.from_product([['DA'], da_frame.columns])
            # ap_frame = pd.DataFrame.from_dict({'Rho': [stat_ap[0]], 'p-value': [stat_ap[1]]})
            # ap_frame.columns = pd.MultiIndex.from_product([['AP'], ap_frame.columns])

            # Add user and group
            tmp_frame = pd.concat([da_frame, ap_frame], axis=1, levels=0)
            tmp_frame.insert(0, 'Group', group.replace("_", " "))
            tmp_frame.insert(1, 'User 1', pair[0])
            tmp_frame.insert(2, 'User 2', pair[1])
            chi_frame = pd.concat([chi_frame, tmp_frame])
    chi_frame.reset_index(drop=True, inplace=True)

    # # Compare DA and AP probability distribution with jensen-shannon
    # stats_frame = pd.DataFrame()
    # for group in groups:
    #     # Get all the pariwise combinations of users
    #     group_data = count_frame.loc[count_frame['group'] == group.replace("_", " ")]
    #     user_combinations = list(combinations(group_data['user'].unique(), 2))
    #
    #     group_stat_frame = pd.DataFrame()
    #     for pair in user_combinations:
    #         # Get the lists of labels from each user
    #         user_1_list = pcnt_frame.loc[(pcnt_frame['user'] == pair[0]+'-%')].values.flatten().tolist()[2:]
    #         user_1_da_list = user_1_list[:27]
    #         user_1_ap_list = user_1_list[-11:]
    #
    #         user_2_list = pcnt_frame.loc[(pcnt_frame['user'] == pair[1]+'-%')].values.flatten().tolist()[2:]
    #         user_2_da_list = user_2_list[:27]
    #         user_2_ap_list = user_2_list[-11:]
    #
    #         from scipy.spatial import distance
    #         stat_da = distance.jensenshannon(user_1_da_list, user_2_da_list)
    #         stat_ap = distance.jensenshannon(user_1_ap_list, user_2_ap_list)
    #
    #         # Create stat dataframe
    #         da_frame = pd.DataFrame.from_dict({'DA JS': [stat_da]})
    #         ap_frame = pd.DataFrame.from_dict({'AP JS': [stat_ap]})
    #
    #         tmp_frame = pd.concat([da_frame, ap_frame], axis=1, levels=0)
    #         tmp_frame.insert(0, 'Group', group.replace("_", " "))
    #         tmp_frame.insert(1, 'User 1', pair[0])
    #         tmp_frame.insert(2, 'User 2', pair[1])
    #         group_stat_frame = pd.concat([group_stat_frame, tmp_frame])
    #
    #     # Add mean for group and concat with main stats frame
    #     group_stat_frame.loc['mean'] = group_stat_frame.mean(numeric_only=True)
    #     group_stat_frame.loc['std'] = group_stat_frame.std(numeric_only=True)
    #     stats_frame = pd.concat([stats_frame, group_stat_frame])
    #
    # stats_frame.reset_index(drop=True, inplace=True)
    # # stats_frame.loc['mean'] = stats_frame.mean(numeric_only=True)
    # # stats_frame.loc['std'] = stats_frame.std(numeric_only=True)

    # Compare DA and AP probability distribution with generalised jensen-shannon
    js_frame = pd.DataFrame()
    for group in groups:
        # Get this groups data
        group_data = count_frame.loc[count_frame['group'] == group.replace("_", " ")]

        users_da = []
        users_ap = []
        for user in group_data['user'].unique():
            # Get the lists of labels from each user
            user_labels = pcnt_frame.loc[(pcnt_frame['user'] == user+'-%')].values.flatten().tolist()[2:]
            users_da.append(user_labels[:27])
            users_ap.append(user_labels[-11:])

        stat_da = jensen_shannnon(users_da)
        stat_ap = jensen_shannnon(users_ap)

        # Create stat dataframe
        group_stat_frame = pd.DataFrame.from_dict({'Group': group.replace("_", " "), 'DA JS': [stat_da], 'AP JS': [stat_ap]})

        # Concat with main stats frame
        js_frame = pd.concat([js_frame, group_stat_frame])

    js_frame.reset_index(drop=True, inplace=True)
    js_frame.loc['mean'] = js_frame.mean(numeric_only=True)
    js_frame.loc['std'] = js_frame.std(numeric_only=True)

    # Create a bar chart of all assignments
    data = group_frame.melt(id_vars=['group', 'user'])
    data = data.rename(columns={'variable_0': 'label_type', 'variable_1': 'label'})
    bar_g, bar_plt = plot_facetgrid(data, x='label', y='value', hue='user', col='label_type', row='group',
                                    title='', colour='triples', axis_titles=True,
                                    num_col=None, all_legend=True, num_legend_col=5, x_tick_rotation=45, ci=None)

    # Create distribution plot of all assignments
    data = count_frame.melt(id_vars=['group', 'user'])
    data = data.rename(columns={'index': 'group', 'variable_0': 'label_type', 'variable_1': 'label'})
    # Don't plot histogram if >2 groups
    plt_hist = False if data['group'].nunique() > 2 else True
    dist_g, dist_fig = plot_dist_chart(data, hue='user', col='label_type',  # Separate plots row='group', num_col=None
                                       title='', colour='triples', axis_titles=True, share_x=True, share_y=True,
                                       plt_hist=plt_hist, num_col=1, all_legend=False, legend_loc='best', num_legend_col=5)

    # Save and show results
    if show:
        print(dist_frame)
        print('Chi-squared:')
        print(chi_frame)
        print('Jensen-shannon:')
        print(js_frame)
        bar_plt.show()
        dist_fig.show()
    if save:
        save_dataframe(os.path.join(save_dir, group_name + " Label Distributions.csv"), dist_frame)
        save_dataframe(os.path.join(save_dir, group_name + " Chi-squared.csv"), chi_frame)
        save_dataframe(os.path.join(save_dir, group_name + " Jensen-Shannon.csv"), js_frame)
        bar_g.savefig(os.path.join(save_dir, group_name + " Label Assignments.png"))
        dist_g.savefig(os.path.join(save_dir, group_name + " Label Distributions.png"))

    return count_frame, chi_frame, js_frame, bar_plt, dist_fig


def generate_postfix_only_plot(agreement_data_dir, save=True, show=True):
    """Utility function generates Postfix only agreement comparison plot."""

    # Load dialogue set agreement data
    corpora_data = load_dataframe(os.path.join(agreement_data_dir, 'Dialogue Corpora Agreement.csv'), multi_index=True)
    # Drop DA and mean
    corpora_data.drop('mean', inplace=True)
    corpora_data.drop('da', axis=1, level=1, inplace=True)
    # Rename labels
    corpora_data.columns.set_levels(['', 'ap (full)', 'ap type (full)', 'da (full)'], level=1, inplace=True)
    # Wide to long
    corpora_data = corpora_data.reset_index().melt(id_vars=['index', 'group'])
    corpora_data = corpora_data.rename(columns={'variable_0': 'metric', 'variable_1': 'label_type'})
    corpora_data = corpora_data.dropna()

    # Load postfix-only agreement data
    corpora_pf_data = load_dataframe(os.path.join(agreement_data_dir, 'postfix_only', 'Dialogue Corpora Agreement.csv'), multi_index=True)
    # Drop DA and mean
    corpora_pf_data.drop('mean', inplace=True)
    corpora_pf_data.drop('da', axis=1, level=1, inplace=True)
    # Rename labels
    corpora_pf_data.columns.set_levels(['', 'ap (postfix)', 'ap type (postfix)', 'da (postfix)'], level=1, inplace=True)
    # Rename labels
    corpora_pf_data = corpora_pf_data.reset_index().melt(id_vars=['index', 'group'])
    corpora_pf_data = corpora_pf_data.rename(columns={'variable_0': 'metric', 'variable_1': 'label_type'})
    corpora_pf_data = corpora_pf_data.dropna()

    # Concatenate both
    data = pd.concat([corpora_data, corpora_pf_data])

    # Generate a group plot
    g, plt = plot_facetgrid(data, x='group', y='value', hue='label_type', title='', axis_titles=True,
                            num_col=1, share_y=False, show_bar_value=True, ci=None,
                            legend_loc='upper right', num_legend_col=1)
    g, plt = annotate_landis_koch(g, plt)

    # Save and show results
    if show:
        plt.show()
    if save:
        g.savefig(os.path.join(agreement_data_dir, "Dialogue Corpora Agreement Postfix-only.png"))

    return g


def annotate_landis_koch(g, plt):
    """Utility function that annotates a plot with the Landis and Koch (1977) agreement scale."""
    for ax in g.axes.flatten():
        # Turn off grid lines
        ax.grid(False)

        # Get the maximum x/y values
        max_y = ax.get_ylim()[1]
        max_x = ax.get_xlim()[1]
        # Annotate up to largest y value
        if max_y > 0.1:
            ax.axhline(.2, ls='-', color='#cccccc', zorder=-1)
            ax.text(max_x, 0.1, "Slight", verticalalignment='center', rotation=90)
        if max_y > 0.3:
            ax.axhline(.4, ls='-', color='#cccccc', zorder=-1)
            ax.text(max_x, 0.3, "Fair", verticalalignment='center', rotation=90)
        if max_y > 0.5:
            ax.axhline(.6, ls='-', color='#cccccc', zorder=-1)
            ax.text(max_x, 0.5, "Moderate", verticalalignment='center', rotation=90)
        if max_y > 0.7:
            ax.axhline(.8, ls='-', color='#cccccc', zorder=-1)
            ax.text(max_x, 0.7, "Substantial", verticalalignment='center', rotation=90)
        if max_y > 0.9:
            ax.axhline(1.0, ls='-', color='#cccccc', zorder=-1)
            ax.text(max_x, 0.9, "Perfect", verticalalignment='center', rotation=90)
    return g, plt
