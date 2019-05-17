
class DialogueModel:
    def __init__(self, dataset, dialogues):

        # Load data
        self.dataset = dataset

        # All dialogues
        self.dialogues = dialogues
        self.num_dialogues = len(self.dialogues)

        # Labeled and unlabeled
        self.labeled_dialogues = []
        self.unlabeled_dialogues = []
        self.num_labeled = len(self.labeled_dialogues)
        self.num_unlabeled = len(self.unlabeled_dialogues)

        # Current dialogue
        self.current_dialogue_index = 0
        self.current_dialogue = self.dialogues[self.current_dialogue_index]

        # Split into labeled and unlabeled
        self.get_dialogues_states()

    def get_current_dialogue(self):
        return self.current_dialogue

    def set_current_dialogue(self, index):

        self.current_dialogue_index = index
        self.current_dialogue = self.dialogues[self.current_dialogue_index]

        return True

    def update_dialogue(self, dialogue_data):

        # Find the matching dialogue
        for dialogue in self.dialogues:
            if dialogue.dialogue_id == dialogue_data['dialogue_id']:

                # Set the new utterance labels
                new_utterances = dialogue_data['utterances']
                for i, utterance in enumerate(dialogue.utterances):
                    utterance.set_ap_label(new_utterances[i]['ap_label'])
                    utterance.set_da_label(new_utterances[i]['da_label'])

                # Check if this dialogue is now fully labeled
                dialogue.check_labels()

        return True

    def get_dialogues_states(self):

        # Reset labeled and unlabeled lists
        self.labeled_dialogues = []
        self.unlabeled_dialogues = []

        # Split dialogues into lists
        for dialogue in self.dialogues:

            if dialogue.check_labels():
                self.labeled_dialogues.append(dialogue)
            else:
                self.unlabeled_dialogues.append(dialogue)

        # Set number of labeled, unlabeled and total
        self.num_labeled = len(self.labeled_dialogues)
        self.num_unlabeled = len(self.unlabeled_dialogues)

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

    def __init__(self, dialogue_id, utterances):
        self.dialogue_id = dialogue_id
        self.utterances = utterances
        self.num_utterances = len(self.utterances)
        # self.current_utterance_index = 0
        # self.current_utterance = self.utterances[0]
        self.is_labeled = False
        self.check_labels()

    # def set_current_utt(self, index):
    #     self.current_utterance_index = index
    #     self.current_utterance = self.utterances[self.current_utterance_index]

    # def set_utterances(self, utterances):
    #
    #     # Replace utterances
    #     self.utterances = utterances
    #     self.num_utterances = len(self.utterances)
    #
    #     # Reset current utterance to 0
    #     self.set_current_utt(0)
    #
    #     # Check labels
    #     self.check_labels()

    # def clear_labels(self):
    #
    #     # Set utterances to default labels
    #     for utt in self.utterances:
    #         utt.clear_ap_label()
    #         utt.clear_da_label()

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

    def clear_ap_label(self):
        self.set_ap_label('AP-Label')

    def clear_da_label(self):
        self.set_da_label('DA-Label')

    def check_labels(self):

        # Check if utterance still has default labels
        if self.ap_label == 'AP-Label' or self.da_label == 'DA-Label':
            self.is_labeled = False
            return self.is_labeled

        self.is_labeled = True
        return self.is_labeled
