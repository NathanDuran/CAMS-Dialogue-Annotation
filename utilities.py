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
    with open(path + file_name + '.json', 'w+') as file:
        json.dump(data, file, sort_keys=False, indent=4, separators=(',', ': '))


def load_txt_data(path, file_name):
    with open(path + "/" + file_name + ".txt", "r") as file:
        # Read a line and strip newline char
        lines = [line.rstrip('\r\n') for line in file.readlines()]

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


# Creates a dialogue model from the specified dialogue file
def create_model(data_path, dialogue_file, user_id):

    # Load JSON file
    data = load_json_data(data_path, dialogue_file)

    # If file is not valid or invalid JSON
    if not data:
        print("Unable to load JSON data...")

    # Create dialogue object
    dialogues = dialogue_from_json(data)

    # If JSON is not valid or keys missing
    if not dialogues:
        print("Unable to load dialogue JSON data...")

    # Create the dialogue model
    model = DialogueModel(data['dataset'], dialogues, user_id)

    return model


# Creates a dialogue and its utterances object from json
def dialogue_from_json(data):
    try:
        # Loop over the dialogues and utterances in the data
        dialogues = []
        for dialogue in data['dialogues']:

            utterances = []
            for utterance in dialogue['utterances']:

                # Create a new utterance
                tmp_utterance = Utterance(utterance['text'], utterance['speaker'])

                # Set utterance labels if not blank
                if utterance['ap_label'] is not "":
                    tmp_utterance.set_ap_label(utterance['ap_label'])
                if utterance['da_label'] is not "":
                    tmp_utterance.set_da_label(utterance['da_label'])

                # Add to utterance list
                utterances.append(tmp_utterance)

            # Create a new dialogue with the utterances
            tmp_dialogue = Dialogue(dialogue['dialogue_id'], utterances)

            # Add to dialogue list
            dialogues.append(tmp_dialogue)

    except KeyError:
        traceback.print_exc()
        return False

    return dialogues


# Converts a dialogue object and its utterances to a dictionary
def dialogue_to_dict(dialogue):

    tmp_dialogue = dict()

    # Loop over utterances and add to dictionary
    utterances = []
    for utterance in dialogue.utterances:

        tmp_utterance = dict()

        # Add speaker, text and labels to utterance
        tmp_utterance['speaker'] = utterance.speaker
        tmp_utterance['text'] = utterance.text
        tmp_utterance['ap_label'] = utterance.ap_label
        tmp_utterance['da_label'] = utterance.da_label
        tmp_utterance['is_labeled'] = utterance.is_labeled

        # Add to utterance list
        utterances.append(tmp_utterance)

    # Add id, number of utterances, utterance and scenario to dialogue
    tmp_dialogue['dialogue_id'] = dialogue.dialogue_id
    tmp_dialogue['num_utterances'] = dialogue.num_utterances
    tmp_dialogue['utterances'] = utterances

    return tmp_dialogue
