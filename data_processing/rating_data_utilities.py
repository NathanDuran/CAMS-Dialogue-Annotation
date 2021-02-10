import os
import pandas as pd
from scipy.stats import levene, shapiro
from data_processing.data_utilities import load_pickle, save_pickle, save_dataframe, dataframe_wide_to_long
from data_processing.plot_utilities import plot_facetgrid, plot_violin_chart
from data_processing.stats_utilites import t_test, multi_t_test, anova_test, tukey_hsd


def get_user_rating_data(path, user_data, sets_list, dialogue_groups):
    """Utility function either loads rating_data dictionary or generates and saves it.

    Args:
        path (str): Path to load or save timing_data .pkl.
        user_data (list): List of user data dictionaries.
        sets_list (list): List of all dialogue sets.
        dialogue_groups (dict): Dictionary of all dialogue groups (task/non-task and corpora).

    Returns:
        rating_data (dict): Dictionary of all dataframes created.
        keys: ['sets_ratings', 'practice_dialogue', 'kvret_dialogues', 'babl_dialogues', 'task_oriented_dialogues',
              'scose_dialogues', 'cabnc_dialogues', 'non_task_oriented_dialogues']
        values: Dictionary with set or dialogue names as keys and Dataframe of user rating by dialogue.
    """
    # If the file exists just load it, else generate the data and save
    if os.path.exists(path):
        rating_data = pd.read_pickle(path)
    else:
        rating_data = dict()
        rating_data['sets_ratings'] = get_user_ratings_by_sets(user_data, sets_list)
        rating_data['ordered_ratings'] = get_ordered_user_ratings_by_sets(user_data, sets_list)
        for group_key in dialogue_groups.keys():
            group_dict = get_user_ratings_by_dialogues(user_data, dialogue_groups[group_key])
            group_frame = pd.concat(group_dict.values(), axis=0, sort=False)
            group_frame.index = group_dict.keys()
            rating_data[group_key] = group_frame
        save_pickle(path, rating_data)

    return rating_data


def get_user_ratings_by_sets(user_data, sets):
    """Returns dictionary of all user dialogue rating dataframes for a list of sets."""

    sets_dict = dict()
    # Iterate over all sets and users and get the ratings for each dialogue
    for set_name in sets:
        users_dict = dict()
        for user in user_data:
            user_ratings = dict()

            # If the user labeled this set
            if user['dataset'] == set_name:

                # Get the dialogue ratings
                for dialogue in user['dialogues']:
                    # Create new dialogue dictionary if this is the first time seeing it
                    if dialogue['dialogue_id'] not in user_ratings.keys():
                        user_ratings[dialogue['dialogue_id']] = dict()

                    # Get the current dialogue ratings
                    current_dialogue = user_ratings[dialogue['dialogue_id']]

                    # Get the relevant value from the dialogues questions
                    current_dialogue['da'] = int(dialogue['questions'][0])
                    current_dialogue['ap'] = int(dialogue['questions'][1])
                    current_dialogue['ap type'] = int(dialogue['questions'][2])

                # Create dataframe for this user
                user_frame = pd.DataFrame.from_dict(user_ratings, orient='index')
                # Set practice as first dialogue
                practice = pd.Series(user_frame.loc['practice']).to_frame().T
                user_frame = user_frame.drop('practice')
                user_frame = pd.concat([practice, user_frame], axis=0)
                user_frame.columns = pd.MultiIndex.from_product([[user['user_id']], user_frame.columns])
                # Add to users dict
                users_dict[user['user_id']] = user_frame

        # Create a dataframe for this set
        set_frame = pd.concat(users_dict.values(), axis=1)

        # Add to set dict
        sets_dict[set_name.replace("_", " ")] = set_frame

    return sets_dict


def get_ordered_user_ratings_by_sets(user_data, sets):
    """Returns dictionary of all user dialogue rating dataframes in the order they were annotated for a list of sets."""

    sets_dict = dict()
    # Iterate over all sets and users and get the ratings for each dialogue
    for set_name in sets:
        users_dict = dict()
        for user in user_data:

            # If the user labeled this set
            if user['dataset'] == set_name:

                user_ratings = []
                # Get the dialogue times
                for i, dialogue in enumerate(user['dialogues']):

                    # Get the relevant value from the dialogues questions
                    user_ratings.append([int(i) for i in dialogue['questions']])

                # Create dataframe for this user
                user_frame = pd.DataFrame(user_ratings,
                                          index=['Practice', 'Dialogue 1', 'Dialogue 2', 'Dialogue 3', 'Dialogue 4'],
                                          columns=['da', 'ap', 'ap type'])
                user_frame.columns = pd.MultiIndex.from_product([[user['user_id']], user_frame.columns])

                # Add to users dict
                users_dict[user['user_id']] = user_frame

        # Create a dataframe for this set
        set_frame = pd.concat(users_dict.values(), axis=1)

        # Add to set dict
        sets_dict[set_name.replace("_", " ")] = set_frame

    return sets_dict


def get_user_ratings_by_dialogues(user_data, dialogues):
    """Returns dictionary of all user dialogue rating dataframes for a list of dialogues."""

    dialogues_dict = dict()
    # Iterate over all dialogues and users and get the ratings for each dialogue
    for dialogue_id in dialogues:
        users_dict = dict()
        for user in user_data:
            user_ratings = dict()

            # For each of the users dialogues
            for dialogue in user['dialogues']:
                # If the user labeled this dialogue
                if dialogue_id == dialogue['dialogue_id']:

                    # Create new dialogue dictionary if this is the first time seeing it
                    if dialogue['dialogue_id'] not in user_ratings.keys():
                        user_ratings[dialogue['dialogue_id']] = dict()

                    # Get the current dialogue ratings
                    current_dialogue = user_ratings[dialogue['dialogue_id']]

                    # Get the relevant value from the dialogues questions
                    current_dialogue['da'] = int(dialogue['questions'][0])
                    current_dialogue['ap'] = int(dialogue['questions'][1])
                    current_dialogue['ap type'] = int(dialogue['questions'][2])

                # Create dataframe for this user
                user_frame = pd.DataFrame.from_dict(user_ratings, orient='index')
                user_frame.columns = pd.MultiIndex.from_product([[user['user_id']], user_frame.columns])
                # Add to users dict
                users_dict[user['user_id']] = user_frame

        # Create a dataframe for this dialogue
        dialogue_frame = pd.concat(users_dict.values(), axis=1)

        # Add to set dict
        dialogues_dict[dialogue_id.replace("_", " ")] = dialogue_frame

    return dialogues_dict


def generate_set_rating_data(set_data, group_name, save_dir, save=True, show=True):
    """Utility function that generates all rating statistics for a all sets of data.

   Creates a DataFrame of the results and saves to .csv and creates a multi-graph plot and saves to .png.

   Args:
       set_data (dict): Dictionary with set names as keys and Dataframe of user ratings by dialogues as values.
       group_name (str): Name of set for file/graph titles.
       save_dir (str): Directory to save the resulting .csv and .png files to.
       save (bool): Whether to save the resulting .csv and .png files. Default=True.
       show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
   """
    # Crate dataframe of ratings by set
    sets_frame = pd.DataFrame()
    for set_name, set_frame in set_data.items():
        set_frame = pd.concat([set_frame], keys=[set_name], names=['Set'], axis=1)
        sets_frame = pd.concat([sets_frame, set_frame], axis=1, sort=False)

    # Creat plots of ratings by set
    data = dataframe_wide_to_long(sets_frame)
    g, fig = plot_facetgrid(data, hue='variable_2', title='', y_label='Confidence', kind='violin',
                            share_y=True, colour='five_colour', num_legend_col=5, inner='box', cut=0)

    # Save and show results
    if show:
        print(sets_frame)
        fig.show()
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), sets_frame)
        g.savefig(os.path.join(save_dir, group_name + ".png"))

    return sets_frame, fig


def generate_ordered_rating_data(set_data, group_name, save_dir, save=True, show=True):
    """Utility function that generates all ordered rating statistics for a all sets data.

       Creates a DataFrame of the results and saves to .csv and creates a multi-graph plot and saves to .png.

       Args:
           set_data (dict): Dictionary with set names as keys and Dataframe of ordered user ratings by dialogues as values.
           group_name (str): Name of set for file/graph titles.
           save_dir (str): Directory to save the resulting .csv and .png files to.
           save (bool): Whether to save the resulting .csv and .png files. Default=True.
           show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
    """
    # Crate dataframe of ratings by set
    sets_frame = pd.DataFrame()
    for set_name, set_frame in set_data.items():
        sets_frame = pd.concat([sets_frame, set_frame], axis=1, sort=False)

    # Creat plots of ratings by set
    data = dataframe_wide_to_long(sets_frame)
    g, fig = plot_violin_chart(data, hue='group', title='', y_label='Confidence', colour='five_colour',
                               inner='box', legend=True)

    # Save and show results
    if show:
        print(sets_frame)
        fig.show()
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), sets_frame)
        fig.savefig(os.path.join(save_dir, group_name + ".png"))

    return sets_frame, fig


def generate_combined_rating_data(set_data, ordered_data, group_name, save_dir, save=True, show=True):
    """Utility function that generates all set and ordered rating statistics for a all set data, i.e. it combines
     results from generate_set_rating_stats() and generate_ordered_rating_stats().

       Creates a DataFrame of the results and saves to .csv and creates a multi-graph plot and saves to .png.

       Args:
           set_data (dict): Dictionary with set names as keys and Dataframe of user ratings by dialogues as values.
           ordered_data (dict): Dictionary with set names as keys and Dataframe of ordered user ratings by dialogues as values.
           group_name (str): Name of set for file/graph titles.
           save_dir (str): Directory to save the resulting .csv and .png files to.
           save (bool): Whether to save the resulting .csv and .png files. Default=True.
           show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
    """
    # Generate both dataframes
    # Crate dataframe of ratings by set
    sets_frame = pd.DataFrame()
    for set_name, set_frame in set_data.items():
        set_frame = pd.concat([set_frame], keys=[set_name], names=['Set'], axis=1)
        sets_frame = pd.concat([sets_frame, set_frame], axis=1, sort=False)

    ordered_sets_frame = pd.DataFrame()
    for set_name, set_frame in ordered_data.items():
        ordered_sets_frame = pd.concat([ordered_sets_frame, set_frame], axis=1, sort=False)

    # Concatenate into one frame, treating ordered like a set
    ratings_frame = pd.concat([ordered_sets_frame], keys=['Ordered Dialogues'], names=['Set'], axis=1)
    ratings_frame = pd.concat([sets_frame, ratings_frame], axis=1, sort=False)

    # Creat plots of ratings by set
    data = dataframe_wide_to_long(ratings_frame)
    g, fig = plot_facetgrid(data, hue='variable_2', title='', y_label='Confidence', kind='violin',
                            share_y=True, colour='five_colour', num_legend_col=5, inner='box', cut=0)

    # Save and show results
    if show:
        print(ratings_frame)
        fig.show()
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), ratings_frame)
        fig.savefig(os.path.join(save_dir, group_name + ".png"))

    return ratings_frame, fig


def generate_group_rating_data(groups_data, groups, group_name, save_dir, save=True, show=True):
    """Utility function that generates all rating statistics for a given group of data.

    Creates a DataFrame of the results and saves to .csv and creates a multi-graph plot and saves to .png.

       Args:
           groups_data (dict): Dictionary with set names as keys and Dataframe of user ratings by dialogues as values.
           groups (list): List of groups to process together. Should be keys in the group_data dict.
           group_name (str): Name of set for file/graph titles.
           save_dir (str): Directory to save the resulting .csv and .png files to.
           save (bool): Whether to save the resulting .csv and .png files. Default=True.
           show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
   """
    # Crate dataframe of ratings by group
    groups_frame = pd.DataFrame()
    for group in groups:
        group_data = groups_data[group].copy()
        # Need to reorder label columns (not for practice because they are already correct and pandas will reverse it!!)
        if not group == 'practice_dialogue':
            group_data.columns.set_levels(['da', 'ap', 'ap type'], level=1, inplace=True)
        group_data.insert(loc=0, column='group', value=group.replace("_", " ").split()[0])
        groups_frame = pd.concat([groups_frame, group_data], axis=0)

    # Creat plots of ratings by group
    data = groups_frame.reset_index().melt(id_vars=['index', 'group'])
    data = data.rename(columns={'variable_0': 'user', 'variable_1': 'label_type'})
    data = data.dropna()
    g, fig = plot_violin_chart(data, x='group', y='value', hue='label_type', title='', y_label='Confidence',
                               colour='five_colour', inner='box', legend=True)
    # Save and show results
    if show:
        print(groups_frame)
        fig.show()
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), groups_frame)
        fig.savefig(os.path.join(save_dir, group_name + ".png"))

    return groups_frame, fig


def generate_dialogue_type_rating_statistics(group_data, groups, group_name, save_dir, save=True, show=True):
    """Utility function that generates all p-values and effect size for given dialogue type groups of data.
        Also compares label types as groups.

      Creates a DataFrame of the results and saves to .csv.

       Args:
           group_data (dict): Dictionary with set names as keys and Dataframe of user ratings by dialogues as values.
           groups (list): List of groups to process together. Should be keys in the group_data dict.
           group_name (str): Name of set for file/graph titles.
           save_dir (str): Directory to save the resulting .csv and .png files to.
           save (bool): Whether to save the resulting .csv and .png files. Default=True.
           show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
    """
    # Crate dataframe of ratings by group
    groups_frame = pd.DataFrame()
    for group in groups:
        group_frame = pd.concat([group_data[group]], keys=[group.replace("_", " ")], names=['Group'], axis=1)
        groups_frame = pd.concat([groups_frame, group_frame], axis=1, sort=False)

    data = dataframe_wide_to_long(groups_frame)
    data.drop('group', axis=1, inplace=True)
    data.rename(columns={'metric': 'group', 'variable_2': 'label_type'}, inplace=True)

    # Generate the pairwise t-test data for label types per group
    dialogue_type_frame = multi_t_test(data, 'group', 'label_type', 'value')

    # Set da to first row and rename label type column
    dialogue_type_frame.reset_index(inplace=True)
    dialogue_type_frame["new"] = range(1, len(dialogue_type_frame)+1)
    dialogue_type_frame.loc[2, 'new'] = 0
    dialogue_type_frame = dialogue_type_frame.sort_values("new").reset_index(drop='True').drop('new', axis=1)
    dialogue_type_frame.rename(columns={'index': 'label_type'}, inplace=True)

    # Add t-test for all combined label types
    dialogue_type_frame = dialogue_type_frame.append(t_test(data, 'group', 'value'), ignore_index=True, sort=False)
    dialogue_type_frame.loc[3, 'label_type'] = 'all'

    # Add the anova for the full group effect size
    # anova_groups = anova_test(data, 'group', 'value')
    # dialogue_type_frame.loc[3, 'eta_sq'] = anova_groups.loc['C(group)', 'eta_sq']
    # dialogue_type_frame.loc[3, 'omega_sq'] = anova_groups.loc['C(group)', 'omega_sq']

    # Get mean, sd and min/max for groups per agreement statistic
    basic_stat_frame = pd.DataFrame()
    for group in data.group.unique():
        # Get each label type for the group
        group_data = data.loc[data['group'] == group]
        tmp = group_data.groupby(['label_type'], sort=False).agg({'value': ['min', 'max', 'mean', 'std']})
        tmp.columns = tmp.columns.droplevel()
        tmp = tmp.T
        tmp = tmp.reindex(columns=['da', 'ap', 'ap type'])

        # Add overall stats
        tmp['all'] = pd.Series({'min': group_data['value'].min(), 'max': group_data['value'].max(),
                         'mean': group_data['value'].mean(), 'std': group_data['value'].std()})

        # Add to basic stats frame
        tmp.columns = pd.MultiIndex.from_product([[group.split()[0]], tmp.columns])
        basic_stat_frame = pd.concat([basic_stat_frame, tmp], axis=1)

        # Test for normality and heteroscedasticity
        # da_values = group_data.loc[group_data['label_type'] == 'da']['value'].to_list()
        # ap_values = group_data.loc[group_data['label_type'] == 'ap']['value'].to_list()
        # ap_type_values = group_data.loc[group_data['label_type'] == 'ap type']['value'].to_list()
        # print(group)
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
        print('Compare Task-oriented and Non-task-oriented dialogues:')
        print(dialogue_type_frame)
        print('General Task-oriented and Non-task-oriented stats:')
        print(basic_stat_frame)
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), dialogue_type_frame)
        save_dataframe(os.path.join(save_dir, group_name + " (basic).csv"), basic_stat_frame)
    return dialogue_type_frame, basic_stat_frame


def generate_corpora_rating_statistics(group_data, groups, group_name, save_dir, save=True, show=True):
    """Utility function that generates all p-values and effect size for given corpora groups of data.
        Also compares label types as groups.

      Creates a DataFrame of the results and saves to .csv.

       Args:
           group_data (dict): Dictionary with set names as keys and Dataframe of user ratings by dialogues as values.
           groups (list): List of groups to process together. Should be keys in the group_data dict.
           group_name (str): Name of set for file/graph titles.
           save_dir (str): Directory to save the resulting .csv and .png files to.
           save (bool): Whether to save the resulting .csv and .png files. Default=True.
           show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
    """
    # Crate dataframe of ratings by group
    groups_frame = pd.DataFrame()
    for group in groups:
        group_frame = pd.concat([group_data[group]], keys=[group.replace("_", " ").split()[0]], names=['Group'], axis=1)
        groups_frame = pd.concat([groups_frame, group_frame], axis=1, sort=False)

    data = dataframe_wide_to_long(groups_frame)
    data.drop('group', axis=1, inplace=True)
    data.rename(columns={'metric': 'group', 'variable_2': 'label_type'}, inplace=True)

    # Get pairwise comparisons for each label type and combined
    corpora_type_frame = pd.DataFrame()
    for label_type in ['DA', 'AP', 'AP type', 'All']:
        # Get the data for the current label type
        if label_type == 'All':
            corpora_label_data = data
        else:
            corpora_label_data = data.loc[data['label_type'] == label_type.lower()]

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

        label_type_frame.columns = pd.MultiIndex.from_product([[label_type], label_type_frame.columns])
        corpora_type_frame = pd.concat([corpora_type_frame, label_type_frame], axis=1)

    # Get mean, sd and min/max for groups per agreement statistic
    basic_stat_frame = pd.DataFrame()
    for group in data.group.unique():
        # Get each label type for the group
        group_data = data.loc[data['group'] == group]
        tmp = group_data.groupby(['label_type'], sort=False).agg({'value': ['min', 'max', 'mean', 'std']})
        tmp.columns = tmp.columns.droplevel()
        tmp = tmp.T
        tmp = tmp.reindex(columns=['da', 'ap', 'ap type'])

        # Add overall stats
        tmp['all'] = pd.Series({'min': group_data['value'].min(), 'max': group_data['value'].max(),
                                'mean': group_data['value'].mean(), 'std': group_data['value'].std()})

        # Add to basic stats frame
        tmp.columns = pd.MultiIndex.from_product([[group.split()[0]], tmp.columns])
        basic_stat_frame = pd.concat([basic_stat_frame, tmp], axis=1)

        # # Test for normality and heteroscedasticity
        # da_values = group_data.loc[group_data['label_type'] == 'da']['value'].to_list()
        # ap_values = group_data.loc[group_data['label_type'] == 'ap']['value'].to_list()
        # ap_type_values = group_data.loc[group_data['label_type'] == 'ap type']['value'].to_list()
        # print(group)
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
        print('Compare Corpora:')
        print(corpora_type_frame)
        print('General Corpora stats:')
        print(basic_stat_frame)
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), corpora_type_frame)
        save_dataframe(os.path.join(save_dir, group_name + " (basic).csv"), basic_stat_frame)
    return corpora_type_frame, basic_stat_frame


def generate_label_type_rating_statistics(group_data, groups, group_name, save_dir, save=True, show=True):
    """Utility function that generates all p-values and effect size for pairwise comparisons of label type rating data.
        Also compares label types as groups.

      Creates a DataFrame of the results and saves to .csv.

       Args:
           group_data (dict): Dictionary with set names as keys and Dataframe of user ratings by dialogues as values.
           groups (list): List of groups to process together. Should be keys in the group_data dict.
           group_name (str): Name of set for file/graph titles.
           save_dir (str): Directory to save the resulting .csv and .png files to.
           save (bool): Whether to save the resulting .csv and .png files. Default=True.
           show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
    """
    # Crate dataframe of ratings by group
    groups_frame = pd.DataFrame()
    for group in groups:
        group_frame = pd.concat([group_data[group]], keys=[group.replace("_", " ")], names=['Group'], axis=1)
        groups_frame = pd.concat([groups_frame, group_frame], axis=1, sort=False)

    data = dataframe_wide_to_long(groups_frame)
    data.drop('group', axis=1, inplace=True)
    data.rename(columns={'metric': 'group', 'variable_2': 'label_type'}, inplace=True)

    # Generate Tukey HSD, compare label types across task/non-task oriented dialogues
    label_type_frame = tukey_hsd(data, 'label_type', 'value')

    # Add the anova for the full label_type comparison and effect size
    anova_labels = anova_test(data, 'label_type', 'value')
    label_type_frame.loc[3, 'p-value'] = anova_labels.loc['C(label_type)', 'PR(>F)']
    label_type_frame.loc[3, 'eta_sq'] = anova_labels.loc['C(label_type)', 'eta_sq']
    label_type_frame.loc[3, 'omega_sq'] = anova_labels.loc['C(label_type)', 'omega_sq']
    label_type_frame.loc[3, 'cohen_f'] = anova_labels.loc['C(label_type)', 'cohen_f']
    label_type_frame.loc[3, 'n'] = anova_labels.loc['C(label_type)', 'n']
    label_type_frame.loc[3, 'exp_n'] = anova_labels.loc['C(label_type)', 'exp_n']
    label_type_frame.loc[3, 'power'] = anova_labels.loc['C(label_type)', 'power']
    label_type_frame.loc[3, 'exp_power'] = anova_labels.loc['C(label_type)', 'exp_power']

    # Test for normality and heteroscedasticity
    # da_values = data.loc[data['label_type'] == 'da']['value'].to_list()
    # ap_values = data.loc[data['label_type'] == 'ap']['value'].to_list()
    # ap_type_values = data.loc[data['label_type'] == 'ap type']['value'].to_list()
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
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), label_type_frame)

    return label_type_frame
