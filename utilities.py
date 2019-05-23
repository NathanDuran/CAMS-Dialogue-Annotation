import os
import traceback
import json
from dialogue_model import *


def load_json_data(path, file_name):
    try:
        with open(path + file_name + ".json") as file:
            data = json.load(file)

    except (IOError, ValueError):
        traceback.print_exc()
        return False

    return data


def save_json_data(path, file_name, data):
    try:
        with open(path + file_name + '.json', 'w+') as file:
            json.dump(data, file, sort_keys=False, indent=4, separators=(',', ': '))

    except (IOError, ValueError):
        traceback.print_exc()
        return False

    return True


def load_txt_data(path, file_name):
    try:
        with open(path + "/" + file_name + ".txt", "r") as file:
            # Read a line and strip newline char
            lines = [line.rstrip('\r\n') for line in file.readlines()]

    except (IOError, ValueError):
        traceback.print_exc()
        return False

    return lines


# Splits label groups on empty lines and returns 2d array of groups
def load_label_groups(labels):
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


# Creates a dialogue model from the specified dialogue dataset file
def create_model(data_path, datset_file, user_id):
    # Load JSON file
    data = load_json_data(data_path, datset_file)

    # If file is not valid or invalid JSON
    if not data:
        print("Unable to load JSON data...")

    # Create dialogue object
    dialogues = dialogues_from_dict(data)

    # If JSON is not valid or keys missing
    if not dialogues:
        print("Unable to load dialogue JSON data...")

    # Create the dialogue model
    model = DialogueModel(data['dataset'], dialogues, user_id)

    return model


def save_model(data_path, model, user_id):

    # Convert model to dictionary
    model_dict = dict()
    model_dict['dataset'] = model.dataset
    model_dict['user_id'] = model.user_id
    model_dict['num_dialogues'] = model.num_dialogues
    model_dict['num_labeled'] = model.num_labeled
    model_dict['num_unlabeled'] = model.num_unlabeled
    model_dict['dialogues'] = dialogues_to_dict(model.dialogues)

    # Save to JSON
    return save_json_data(data_path, user_id, model_dict)


# Creates dialogue objects from dataset dictionary/json
def dialogues_from_dict(data):
    try:
        # Loop over the dialogues in the data
        dialogues = []
        for dialogue in data['dialogues']:

            # Create the dialogue
            tmp_dialogue = dialogue_from_dict(dialogue)

            # Add to dialogue list
            dialogues.append(tmp_dialogue)

    except KeyError:
        traceback.print_exc()
        return False

    return dialogues


# Creates a dialogue object and its utterances from dictionary/json
def dialogue_from_dict(dialogue):
    tmp_dialogue = None
    try:
        # Loop over the utterances in the dialogue
        utterances = []
        for utterance in dialogue['utterances']:

            # Create a new utterance
            tmp_utterance = Utterance(utterance['text'], utterance['speaker'])

            # Set utterance labels if not blank
            if utterance['ap_label'] is not "":
                tmp_utterance.set_ap_label(utterance['ap_label'])
            if utterance['da_label'] is not "":
                tmp_utterance.set_da_label(utterance['da_label'])

            # Get labeled state if it exists
            if 'is_labeld' in utterance.keys():
                tmp_utterance.is_labeled = utterance['is_labeled']

            # Add to utterance list
            utterances.append(tmp_utterance)

        # Create a new dialogue with the utterances
        tmp_dialogue = Dialogue(dialogue['dialogue_id'], utterances, len(utterances))

        # Check if the labeled and time values are also set
        if 'is_labeled' in dialogue.keys():
            tmp_dialogue.is_labeled = dialogue['is_labeled']
        if 'time' in dialogue.keys():
            tmp_dialogue.time = dialogue['time']

    except KeyError:
        traceback.print_exc()

    return tmp_dialogue


# Converts dialogue objects to a dictionary/list
def dialogues_to_dict(dialogues):
    dialogues_list = []

    # Loop over the dialogues and utterances
    for dialogue in dialogues:

        # Create a new dialogue with the utterances
        tmp_dialogue = dialogue_to_dict(dialogue)

        # Add to dialogue list
        dialogues_list.append(tmp_dialogue)

    return dialogues_list


# Converts a dialogue object and its utterances to a dictionary
def dialogue_to_dict(dialogue):
    dialogue_dict = dict()

    # Loop over utterances and add to dictionary
    utterances = []
    for utterance in dialogue.utterances:
        utt_dict = dict()

        # Add speaker, text and labels to utterance
        utt_dict['speaker'] = utterance.speaker
        utt_dict['text'] = utterance.text
        utt_dict['ap_label'] = utterance.ap_label
        utt_dict['da_label'] = utterance.da_label
        utt_dict['is_labeled'] = utterance.is_labeled

        # Add to utterance list
        utterances.append(utt_dict)

    # Add id, number of utterances, utterances, is labeled and time to dialogue
    dialogue_dict['dialogue_id'] = dialogue.dialogue_id
    dialogue_dict['is_labeled'] = dialogue.is_labeled
    dialogue_dict['time'] = dialogue.time
    dialogue_dict['num_utterances'] = dialogue.num_utterances
    dialogue_dict['utterances'] = utterances

    return dialogue_dict
