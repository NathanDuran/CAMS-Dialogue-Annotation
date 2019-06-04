from random import shuffle


class DialogueModel:
    def __init__(self, dataset, dialogues, user_id):

        # Load data
        self.dataset = dataset

        # Set the user
        self.user_id = user_id

        # All dialogues
        self.dialogues = dialogues
        # shuffle(self.dialogues)  # TODO Uncomment when deployed
        self.num_dialogues = len(self.dialogues)

        # Current dialogue
        self.current_dialogue_index = 0
        self.current_dialogue = self.dialogues[self.current_dialogue_index]

        # Labelled and unlabelled counts
        self.num_labelled = 0
        self.num_unlabelled = 0

        # Count labelled and unlabelled dialogues
        self.update_labelled_dialogue_counts()

    def get_current_dialogue(self):
        return self.current_dialogue

    def set_current_dialogue(self, index):

        self.current_dialogue_index = index
        self.current_dialogue = self.dialogues[self.current_dialogue_index]

        return True

    def get_dialogue(self, dialogue_id):
        # Find the matching dialogue
        for dialogue in self.dialogues:
            if dialogue.dialogue_id == dialogue_id:
                return dialogue
            else:
                return False

    def set_dialogue(self, dialogue_data, target_id):
        # Find the matching dialogue
        for i, dialogue in enumerate(self.dialogues):
            if dialogue.dialogue_id == target_id:
                # Set the new dialogue data
                self.dialogues[i] = dialogue_data
                # Update dialogue states
                self.update_labelled_dialogue_counts()
                return True
            else:
                return False

    def update_labelled_dialogue_counts(self):

        # Reset labeled and unlabeled counts
        self.num_labelled = 0
        self.num_unlabelled = 0

        # Update counts
        for dialogue in self.dialogues:

            if dialogue.check_labels():
                self.num_labelled += 1
            else:
                self.num_unlabelled += 1

    def inc_current_dialogue(self):

        # Increment dialogue index or wrap to beginning
        if self.current_dialogue_index + 1 < self.num_dialogues:
            self.current_dialogue_index += 1
        else:
            self.current_dialogue_index = 0

        # Set new current dialogue with index
        self.set_current_dialogue(self.current_dialogue_index)

        return True

    def dec_current_dialogue(self):

        # Decrement dialogue index or wrap to end
        if self.current_dialogue_index - 1 < 0:
            self.current_dialogue_index = self.num_dialogues - 1
        else:
            self.current_dialogue_index -= 1

        # Set new current dialogue with index
        self.set_current_dialogue(self.current_dialogue_index)

        return True


class Dialogue:

    def __init__(self, dialogue_id, utterances, num_utterances):
        self.dialogue_id = dialogue_id
        self.utterances = utterances
        self.num_utterances = num_utterances
        self.is_labeled = False
        self.time = 0.0
        self.check_labels()

    def check_labels(self):
        # Check if any utterances still have default labels
        for utt in self.utterances:
            if not utt.check_labels():
                self.is_labeled = False
                return self.is_labeled

        self.is_labeled = True
        return self.is_labeled


class Utterance:
    def __init__(self, text, speaker='', ap_label='AP-Label', da_label='DA-Label'):
        self.text = text
        self.speaker = speaker
        self.ap_label = ap_label
        self.da_label = da_label
        self.is_labeled = False

    def set_ap_label(self, label):
        self.ap_label = label
        self.check_labels()

    def set_da_label(self, label):
        self.da_label = label
        self.check_labels()

    def check_labels(self):
        # Check if utterance still has default labels
        if self.ap_label == 'AP-Label' or self.da_label == 'DA-Label':
            self.is_labeled = False
            return self.is_labeled

        self.is_labeled = True
        return self.is_labeled
