import os
import pandas as pd
from scipy.stats import levene, shapiro
from data_processing.data_utilities import load_pickle, save_pickle, save_dataframe, dataframe_wide_to_long
from data_processing.plot_utilities import plot_bar_chart, plot_violin_chart, plot_facetgrid
from data_processing.stats_utilites import t_test, anova_test, tukey_hsd


def get_user_timing_data(path, user_data, sets_list, dialogue_groups, mean_utt=False):
    """Utility function either loads timing_data dictionary or generates and saves it.

    Args:
        path (str): Path to load or save timing_data .pkl.
        user_data (list): List of user data dictionaries.
        sets_list (list): List of all dialogue sets.
        dialogue_groups (dict): Dictionary of all dialogue groups (task/non-task and corpora).
        mean_utt (bool): Determines if times are the average utterance time, or sum of utterance times.

    Returns:
        timing_data (dict): Dictionary of all dataframes created.
        keys: ['sets_times', 'practice_dialogue', 'kvret_dialogues', 'babl_dialogues', 'task_oriented_dialogues',
              'scose_dialogues', 'cabnc_dialogues', 'non_task_oriented_dialogues']
        values: Dictionary with set or dialogue names as keys and Dataframe of user times by dialogue.
    """
    # If the file exists just load it, else generate the data and save
    if os.path.exists(path):
        timing_data = load_pickle(path)
    else:
        timing_data = dict()
        timing_data['sets_times'] = get_user_timings_by_sets(user_data, sets_list, mean_utt=mean_utt)
        timing_data['ordered_times'] = get_ordered_user_timings_by_sets(user_data, sets_list, mean_utt=True)
        for group_key in dialogue_groups.keys():
            group_dict = get_user_timings_by_dialogues(user_data, dialogue_groups[group_key], mean_utt=True)
            group_frame = pd.concat(group_dict.values(), axis=0, sort=False)
            group_frame.index = group_dict.keys()
            timing_data[group_key] = group_frame
        save_pickle(path, timing_data)

    return timing_data


def get_user_timings_by_sets(user_data, sets, mean_utt=False):
    """Returns dictionary of all user dialogue timing dataframes for a list of sets."""

    sets_dict = dict()
    # Iterate over all sets and users and get the times for each dialogue
    for set_name in sets:
        dialogue_times = dict()
        for user in user_data:

            # If the user labeled this set
            if user['dataset'] == set_name:

                # Get the dialogue times
                for dialogue in user['dialogues']:
                    # Create new dialogue dictionary if this is the first time seeing it
                    if dialogue['dialogue_id'] not in dialogue_times.keys():
                        dialogue_times[dialogue['dialogue_id']] = dict()

                    # Set the current dialogue
                    current_dialogue = dialogue_times[dialogue['dialogue_id']]

                    # TODO Don't use dialogue total as usr6-1 "KB7RE015" is very wrong
                    # current_dialogue[user['user_id']] = dialogue['time']

                    # Get the sum of all the utterance times
                    utt_time_sum = 0
                    for utterance in dialogue['utterances']:
                        utt_time_sum += utterance['time']

                    # Divide by the number of utterances if we want the mean utterance time
                    if mean_utt:
                        utt_time_sum /= len(dialogue['utterances'])

                    # Divide by 1k to convert milliseconds to seconds
                    current_dialogue[user['user_id']] = utt_time_sum / 1000

        # Create a dataframe for this set
        set_frame = pd.DataFrame.from_dict(dialogue_times, orient='index')

        # Set practice as first dialogue
        practice = pd.Series(set_frame.loc['practice']).to_frame().T
        set_frame = set_frame.drop('practice')
        set_frame = pd.concat([practice, set_frame], axis=0)

        # Add to dict
        sets_dict[set_name.replace("_", " ")] = set_frame

    return sets_dict


def get_ordered_user_timings_by_sets(user_data, sets, mean_utt=False):
    """Returns dictionary of all user dialogue timing dataframes in the order they were annotated for a list of sets."""

    sets_dict = dict()
    # Iterate over all sets and users and get the times for each dialogue
    for set_name in sets:
        users_dict = dict()
        for user in user_data:

            # If the user labeled this set
            if user['dataset'] == set_name:

                user_times = []
                # Get the dialogue times
                for i, dialogue in enumerate(user['dialogues']):

                    # Get the sum of all the utterance times
                    utt_time_sum = 0
                    for utterance in dialogue['utterances']:
                        utt_time_sum += utterance['time']

                    # Divide by the number of utterances if we want the mean utterance time
                    if mean_utt:
                        utt_time_sum /= len(dialogue['utterances'])

                    # Add to users times (Divide by 1k to convert milliseconds to seconds)
                    user_times.append(utt_time_sum / 1000)

                # Add user to set
                users_dict[user['user_id']] = user_times

        # Create a dataframe for this set
        set_frame = pd.DataFrame(users_dict, index=['Practice', 'Dialogue 1', 'Dialogue 2', 'Dialogue 3', 'Dialogue 4'])

        # Add to dict
        sets_dict[set_name.replace("_", " ")] = set_frame

    return sets_dict


def get_user_timings_by_dialogues(user_data, dialogues, mean_utt=False):
    """Returns dictionary of all user dialogue timing dataframes for a list of dialogues."""

    dialogues_dict = dict()
    # Iterate over all dialogues and users and get the times for each dialogue
    for dialogue_id in dialogues:
        dialogue_times = dict()
        for user in user_data:

            for dialogue in user['dialogues']:

                # If the user labeled this dialogue
                if dialogue['dialogue_id'] == dialogue_id:
                    # Create new dialogue dictionary if this is the first time seeing it
                    if dialogue['dialogue_id'] not in dialogue_times.keys():
                        dialogue_times[dialogue['dialogue_id']] = dict()

                    # Set the current dialogue
                    current_dialogue = dialogue_times[dialogue['dialogue_id']]

                    # TODO Don't use dialogue total as usr6-1 "KB7RE015" is very wrong
                    # current_dialogue[user['user_id']] = dialogue['time']

                    # Get the sum of all the utterance times
                    utt_time_sum = 0
                    for utterance in dialogue['utterances']:
                        utt_time_sum += utterance['time']

                    # Divide by the number of utterances if we want the mean utterance time
                    if mean_utt:
                        utt_time_sum /= len(dialogue['utterances'])

                    # Divide by 1k to convert milliseconds to seconds
                    current_dialogue[user['user_id']] = utt_time_sum / 1000

        # Create a dataframe for this set
        dialogue_frame = pd.DataFrame.from_dict(dialogue_times, orient='index')

        # Add to dict
        dialogues_dict[dialogue_id.replace("_", " ")] = dialogue_frame

    return dialogues_dict


def generate_set_time_data(set_data, group_name, save_dir, save=True, show=True):
    """Utility function that generates all timing statistics for a given set data.

       Creates a DataFrame of the results and saves to .csv and creates a multi-graph plot and saves to .png.

       Args:
           set_data (dict): Dictionary with set names as keys and Dataframe of user times by dialogues as values.
           group_name (str): Name of set for file/graph titles.
           save_dir (str): Directory to save the resulting .csv and .png files to.
           save (bool): Whether to save the resulting .csv and .png files. Default=True.
           show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
    """
    # Crate dataframe of timings by set
    sets_frame = pd.DataFrame()
    for set_name, set_frame in set_data.items():
        set_frame.columns = pd.MultiIndex.from_product([[set_name], set_frame.columns])
        sets_frame = pd.concat([sets_frame, set_frame], axis=1, sort=False)

    # Create mean and sum of set times dataframe
    mean_times = pd.Series(sets_frame.mean(), name='Mean time').to_frame().T
    mean_times.columns = mean_times.columns.droplevel()
    sum_times = pd.Series(sets_frame.sum(), name='Total time').to_frame().T
    sum_times.columns = sum_times.columns.droplevel()
    mean_and_sum = pd.concat([mean_times, sum_times])
    mean_and_sum.columns = pd.MultiIndex.from_product([['Total'], mean_and_sum.columns])
    # Add to sets frame
    sets_frame_columns = sets_frame.columns.tolist()
    sets_frame_totals = pd.concat([sets_frame, mean_and_sum], axis=0, sort=False)
    # Set order of concatenated mean_and_sum frame columns (because concat reorders them)
    sets_frame_totals = sets_frame_totals[sets_frame_columns + mean_and_sum.columns.tolist()]

    # Creat plots of timings by set
    data = dataframe_wide_to_long(sets_frame_totals)
    g, fig = plot_facetgrid(data, title='', y_label='Total Time (Seconds)', kind='bar',
                            share_y=True, colour='triples', num_legend_col=5, all_legend=True,
                            show_bar_value=True, bar_value_rotation=90)

    # Save and show results
    if show:
        print(sets_frame)
        fig.show()
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), sets_frame)
        g.savefig(os.path.join(save_dir, group_name + ".png"))

    return sets_frame, fig


def generate_ordered_time_data(set_data, group_name, save_dir, save=True, show=True):
    """Utility function that generates all ordered timing statistics for a all set data.

       Creates a DataFrame of the results and saves to .csv and creates a multi-graph plot and saves to .png.

       Args:
           set_data (dict): Dictionary with set names as keys and Dataframe of ordered user times by dialogues as values.
           group_name (str): Name of set for file/graph titles.
           save_dir (str): Directory to save the resulting .csv and .png files to.
           save (bool): Whether to save the resulting .csv and .png files. Default=True.
           show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
    """
    # Crate dataframe of timings by set
    sets_frame = pd.DataFrame()
    for set_name, set_frame in set_data.items():
        sets_frame = pd.concat([sets_frame, set_frame], axis=1, sort=False)

    # Creat plots of timings by set
    data = dataframe_wide_to_long(sets_frame)
    g, fig = plot_violin_chart(data, title='', y_label='Average Utterance Time (Seconds)', colour='five_colour')

    # Add mean and SD for each dialogue
    sets_frame['min'] = sets_frame.min(axis=1)
    sets_frame['max'] = sets_frame.max(axis=1)
    sets_frame['mean'] = sets_frame.mean(axis=1)
    sets_frame['std'] = sets_frame.std(axis=1)

    # Save and show results
    if show:
        print(sets_frame)
        fig.show()
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), sets_frame)
        fig.savefig(os.path.join(save_dir, group_name + ".png"))

    return sets_frame, fig


def generate_group_time_data(group_data, groups, group_name, save_dir, save=True, show=True):
    """Utility function that generates all timing statistics for a given list of group data.

       Creates a DataFrame of the results and saves to .csv and creates a multi-graph plot and saves to .png.
       Calculates mean, standard deviation, min and max of each group of data.

       Args:
           group_data (dict): Dictionary with set names as keys and Dataframe of user times by dialogues as values.
           groups (list): List of groups to process together. Should be keys in the group_data dict.
           group_name (str): Name of set for file/graph titles.
           save_dir (str): Directory to save the resulting .csv and .png files to.
           save (bool): Whether to save the resulting .csv and .png files. Default=True.
           show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
    """
    # For each group
    group_frame_list = []
    group_stats_frame = pd.DataFrame(columns=['mean', 'sd', 'min', 'max'])
    for group in groups:
        # Get the data from group_data dict
        group_frame = group_data[group]

        # Calculate the statistics
        tmp_frame = pd.DataFrame()
        tmp_frame['mean'] = group_frame.mean(numeric_only=True, axis=1)
        tmp_frame['sd'] = group_frame.std(numeric_only=True, axis=1)
        tmp_frame['min'] = group_frame.min(numeric_only=True, axis=1)
        tmp_frame['max'] = group_frame.max(numeric_only=True, axis=1)

        # Add dataframe to list
        group_frame = tmp_frame.loc[:, ['mean', 'sd', 'min', 'max']]
        group_frame.columns = pd.MultiIndex.from_product([[group.replace("_", " ").split()[0]], group_frame.columns])
        group_frame_list.append(group_frame)

        # Get stats for the whole group
        group_stats_frame.loc[group.replace("_", " ").split()[0], 'mean'] = tmp_frame['mean'].mean(axis=0)
        group_stats_frame.loc[group.replace("_", " ").split()[0], 'sd'] = tmp_frame['sd'].mean(axis=0)
        group_stats_frame.loc[group.replace("_", " ").split()[0], 'min'] = tmp_frame['min'].min(axis=0)
        group_stats_frame.loc[group.replace("_", " ").split()[0], 'max'] = tmp_frame['max'].max(axis=0)

    # Create frame for all groups
    groups_frame = pd.concat(group_frame_list, axis=1, sort=True)

    # Create plot of timing stats by group
    data = dataframe_wide_to_long(group_stats_frame)
    g = fig = plot_bar_chart(data, title='', y_label='Average Utterance Time (Seconds)', dodge=True, num_legend_col=2)

    # Save and show results
    if show:
        print(groups_frame)
        fig.show()
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), groups_frame)
        g.savefig(os.path.join(save_dir, group_name + ".png"))

    return groups_frame, fig


def generate_dialogue_type_timing_statistics(group_data, groups, group_name, save_dir, save=True, show=True):
    """Utility function that generates all p-values and effect size for given dialogue type groups of data.

      Creates a DataFrame of the results and saves to .csv.

       Args:
           group_data (dict): Dictionary with set names as keys and Dataframe of user ratings by dialogues as values.
           groups (list): List of groups to process together. Should be keys in the group_data dict.
           group_name (str): Name of set for file/graph titles.
           save_dir (str): Directory to save the resulting .csv and .png files to.
           save (bool): Whether to save the resulting .csv and .png files. Default=True.
           show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
    """
    # Crate dataframe of timings by group
    groups_frame = pd.DataFrame()
    for group in groups:
        group_frame = pd.concat([group_data[group]], keys=[group.replace("_", " ").split()[0]], names=['group'], axis=1)
        groups_frame = pd.concat([groups_frame, group_frame], axis=1, sort=False)

    data = dataframe_wide_to_long(groups_frame)
    data.rename(columns={None: 'users'}, inplace=True)
    data.drop('users', axis=1, inplace=True)

    # Generate the t-test data
    stats_frame = t_test(data, 'group', 'value')

    # Generate the anova data for effect size
    anova_frame = anova_test(data, 'group', 'value')

    # Add effect size to data
    stats_frame['eta_sq'] = anova_frame.loc['C(group)', 'eta_sq']
    stats_frame['omega_sq'] = anova_frame.loc['C(group)', 'omega_sq']

    # Get mean, sd and min/max for groups per agreement statistic
    basic_stat_frame = data.groupby(['group'], sort=False).agg({'value': ['min', 'max', 'mean', 'std']})
    basic_stat_frame.columns = basic_stat_frame.columns.droplevel()
    basic_stat_frame = basic_stat_frame.T

    # Test for normality and heteroscedasticity
    task_values = data.loc[data['group'] == 'task-oriented']['value'].to_list()
    non_task_values = data.loc[data['group'] == 'task-oriented']['value'].to_list()
    print("Test for normal distribution:")
    task_w, task_p = shapiro(task_values)
    print("task w: " + str(round(task_w, 6)) + " p-value: " + str(round(task_p, 6)))
    non_task_w, non_task_p = shapiro(non_task_values)
    print("non-task w: " + str(round(non_task_w, 6)) + " p-value: " + str(round(non_task_p, 6)))

    print("Test for heteroscedasticity:")
    levene_t, levene_p = levene(task_values, non_task_values)
    print("t: " + str(round(levene_t, 6)) + " p-value: " + str(round(levene_p, 6)))

    # Save and show results
    if show:
        print('Compare Task-oriented and Non-task-oriented dialogues:')
        print(stats_frame)
        print('General Task-oriented and Non-task-oriented stats:')
        print(basic_stat_frame)
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), stats_frame)
        save_dataframe(os.path.join(save_dir, group_name + " (basic).csv"), basic_stat_frame)
    return stats_frame, basic_stat_frame


def generate_corpora_timing_statistics(group_data, groups, group_name, save_dir, save=True, show=True):
    """Utility function that generates all p-values and effect size for given corpora of data.

      Creates a DataFrame of the results and saves to .csv.

       Args:
           group_data (dict): Dictionary with set names as keys and Dataframe of user ratings by dialogues as values.
           groups (list): List of groups to process together. Should be keys in the group_data dict.
           group_name (str): Name of set for file/graph titles.
           save_dir (str): Directory to save the resulting .csv and .png files to.
           save (bool): Whether to save the resulting .csv and .png files. Default=True.
           show (bool): Whether to print/show the resulting graphs and dataframes. Default=True.
    """
    # Crate dataframe of timings by group
    groups_frame = pd.DataFrame()
    for group in groups:
        group_frame = pd.concat([group_data[group]], keys=[group.replace("_", " ").split()[0]], names=['group'], axis=1)
        groups_frame = pd.concat([groups_frame, group_frame], axis=1, sort=False)

    data = dataframe_wide_to_long(groups_frame)
    data.rename(columns={None: 'users'}, inplace=True)
    data.drop('users', axis=1, inplace=True)

    # Generate Tukey HSD, compare label types across task/non-task oriented dialogues
    stats_frame = tukey_hsd(data, 'group', 'value')

    # Add the anova for the full label_type comparison and effect size
    anova_labels = anova_test(data, 'group', 'value')
    stats_frame.loc[6, 'p-value'] = anova_labels.loc['C(group)', 'PR(>F)']
    stats_frame.loc[6, 'eta_sq'] = anova_labels.loc['C(group)', 'eta_sq']
    stats_frame.loc[6, 'omega_sq'] = anova_labels.loc['C(group)', 'omega_sq']

    # Get mean, sd and min/max for groups per agreement statistic
    basic_stat_frame = data.groupby(['group'], sort=False).agg({'value': ['min', 'max', 'mean', 'std']})
    basic_stat_frame.columns = basic_stat_frame.columns.droplevel()
    basic_stat_frame = basic_stat_frame.T

    # Test for normality and heteroscedasticity
    groups_values = []
    for group in data.group.unique():
        print(group)
        group_values = data.loc[data['group'] == group]['value'].to_list()
        print("Test for normal distribution:")
        w, p = shapiro(group_values)
        print("w: " + str(round(w, 6)) + " p-value: " + str(round(p, 6)))
        groups_values.append(group_values)
    print("Test for heteroscedasticity:")
    levene_t, levene_p = levene(*groups_values)
    print("t: " + str(round(levene_t, 6)) + " p-value: " + str(round(levene_p, 6)))

    # Save and show results
    if show:
        print('Compare Corpora:')
        print(stats_frame)
        print('General Corpora stats:')
        print(basic_stat_frame)
    if save:
        save_dataframe(os.path.join(save_dir, group_name + ".csv"), stats_frame)
        save_dataframe(os.path.join(save_dir, group_name + " (basic).csv"), basic_stat_frame)
    return stats_frame, basic_stat_frame
