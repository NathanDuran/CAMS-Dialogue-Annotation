from data_processing.data_utilities import *
from data_processing.label_data_utilities import *
from data_processing.timing_data_utilities import *
from data_processing.rating_data_utilities import *

# Show full pandas Dataframes
pd.options.display.width = 0
pd.options.display.precision = 8

# Experiment data and labels directories
data_dir = os.path.join('..', 'static', 'data')
user_data_dir = os.path.join(data_dir, 'user_dialogues')
labels_dir = os.path.join(data_dir, 'labels')

# Processed data and label data directories
results_dir = 'results'
label_data_dir = 'label_data'
postfix_only = False
# Paths to label agreement, timing and confidence rating data
agreement_data_dir = os.path.join(results_dir, 'agreement_data')
if postfix_only:
    agreement_data_dir = os.path.join(agreement_data_dir, 'postfix_only')
timing_data_dir = os.path.join(results_dir, 'timing_data')
rating_data_dir = os.path.join(results_dir, 'rating_data')
distr_data_dir = os.path.join(results_dir, 'distribution_data')

# Load the user data and labels
user_data = load_user_data(user_data_dir)
labels = load_labels(labels_dir, user_data)

# List of sets
sets_list = ['set_1', 'set_2', 'set_3', 'set_4', 'set_5']

# Lists of dialogue corpora and groups
dialogue_groups = dict()
dialogue_groups['practice_dialogue'] = ['practice']
dialogue_groups['kvret_dialogues'] = ['test_28', 'test_52', 'test_96', 'test_129', 'test_102']
dialogue_groups['babl_dialogues'] = ['task1_test_290', 'task1_test_428', 'task1_test_555', 'task1_test_564', 'task1_test_894']
dialogue_groups['task-oriented_dialogues'] = dialogue_groups['kvret_dialogues'] + dialogue_groups['babl_dialogues']

dialogue_groups['scose_dialogues'] = ['jason-mammoth', 'jason-clone', 'jason-accident', 'lynne-hunter', 'lynne-tipsy']
dialogue_groups['cabnc_dialogues'] = ['KB7RE015', 'KBKRE03G', 'KDARE00G', 'KE2RE00Y', 'KBERE00G']
dialogue_groups['non-task-oriented_dialogues'] = dialogue_groups['scose_dialogues'] + dialogue_groups['cabnc_dialogues']

dialogue_type_groups = ['task-oriented_dialogues', 'non-task-oriented_dialogues']
dialogue_corpora_groups = ['kvret_dialogues', 'babl_dialogues', 'scose_dialogues', 'cabnc_dialogues']

print("========================= Agreement Values =========================")
# If user label data has already been generated then load, else create it
user_label_data = get_user_label_data(os.path.join(agreement_data_dir, 'user_label_data.pkl'), user_data, labels, sets_list, dialogue_groups)

print("========================= Set:")
generate_set_agreement_data(user_label_data['sets_labels'], labels, 'Dialogue Set Agreement', agreement_data_dir, postfix_only=postfix_only)

print("========================= Type:")
generate_group_agreement_data(user_label_data, dialogue_type_groups + ['practice_dialogue'], labels, 'Dialogue Type Agreement', agreement_data_dir, postfix_only=postfix_only)

print("========================= Corpus:")
generate_group_agreement_data(user_label_data, dialogue_corpora_groups, labels, 'Dialogue Corpora Agreement', agreement_data_dir, postfix_only=postfix_only)

print("========================= Full:")
generate_full_agreement_data(user_label_data, dialogue_type_groups, labels, 'Dialogue Agreement', agreement_data_dir, postfix_only=postfix_only)

print("========================= Dialogue Times =========================")
# If user timing data has already been generated then load, else create it
user_timing_data = get_user_timing_data(os.path.join(timing_data_dir, 'timing_data.pkl'), user_data, sets_list, dialogue_groups)

print("========================= Set:")
generate_set_time_data(user_timing_data['sets_times'], 'Dialogue Set Times', timing_data_dir)

print("========================= Ordered:")
generate_ordered_time_data(user_timing_data['ordered_times'], 'Ordered Dialogue Times', timing_data_dir)

print("========================= Type:")
generate_group_time_data(user_timing_data, dialogue_type_groups + ['practice_dialogue'], 'Dialogue Type Times', timing_data_dir)

print("========================= Corpus:")
generate_group_time_data(user_timing_data, dialogue_corpora_groups, 'Dialogue Corpora Times', timing_data_dir)

print("========================= Dialogue Ratings =========================")
# If user confidence data has already been generated then load, else create it
user_rating_data = get_user_rating_data(os.path.join(rating_data_dir, 'rating_data.pkl'), user_data, sets_list, dialogue_groups)

print("========================= Set:")
generate_set_rating_data(user_rating_data['sets_ratings'], 'Dialogue Set Confidence Scores', rating_data_dir)

print("========================= Ordered:")
generate_ordered_rating_data(user_rating_data['ordered_ratings'], 'Ordered Dialogue Confidence Scores', rating_data_dir)

print("========================= Set and Ordered:")
generate_combined_rating_data(user_rating_data['sets_ratings'], user_rating_data['ordered_ratings'], 'Dialogue Confidence Scores', rating_data_dir)

print("========================= Type:")
generate_group_rating_data(user_rating_data, dialogue_type_groups + ['practice_dialogue'], 'Dialogue Type Confidence Scores', rating_data_dir)

print("========================= Corpus:")
generate_group_rating_data(user_rating_data, dialogue_corpora_groups, 'Dialogue Corpora Confidence Scores', rating_data_dir)

print("========================= Statistics =========================")
print("========================= Agreement Stats:")
generate_dialogue_type_agreement_statistics('Dialogue Type Agreement Statistics', agreement_data_dir)
generate_corpora_agreement_statistics('Dialogue Corpora Agreement Statistics', agreement_data_dir)
generate_label_type_agreement_statistics('Label Type Agreement Statistics', agreement_data_dir)
generate_coefficient_agreement_statistics('Coefficient Agreement Statistics', agreement_data_dir)

print("========================= Dialogue Times:")
generate_dialogue_type_timing_statistics(user_timing_data, dialogue_type_groups, 'Dialogue Type Timing Statistics', timing_data_dir)
generate_corpora_timing_statistics(user_timing_data, dialogue_corpora_groups, 'Dialogue Corpora Timing Statistics', timing_data_dir)

print("========================= Dialogue Ratings:")
generate_dialogue_type_rating_statistics(user_rating_data, dialogue_type_groups, 'Dialogue Type Rating Statistics', rating_data_dir)
generate_corpora_rating_statistics(user_rating_data, dialogue_corpora_groups, 'Dialogue Corpora Rating Statistics', rating_data_dir)
generate_label_type_rating_statistics(user_rating_data, dialogue_type_groups, 'Label Type Rating Statistics', rating_data_dir)

print("========================= Label Distributions =========================")
print("========================= Type Distributions:")
generate_group_label_distributions(user_label_data, dialogue_type_groups, labels, 'Dialogue Type', distr_data_dir)

print("========================= Corpora Distributions:")
generate_group_label_distributions(user_label_data, dialogue_corpora_groups, labels, 'Dialogue Corpora', distr_data_dir)

print("========================= User Distributions:")
generate_user_label_distributions(user_label_data['sets_labels'], sets_list, labels, 'User', distr_data_dir)

print("========================= Postfix Only Plot =========================")
generate_postfix_only_plot(agreement_data_dir)


