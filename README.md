# CA Dialogue Tagger
### TODO
- practice?

- generate valid user list

- Remove state flag from setButtonLabelled/Selected State?

- Label button tooltips
- Highlight DA/AP labels once labelled?

- Questionnaire popup
- Complete/finish dialogue labelling button? at bottom of popup

- on/before shutdown logout and save all users?
### Example JSON Format
The following is an example of the JSON format
```json
    {
        "dataset": "dataset_name",
        "num_dialogues": 1,
        "dialogues": [
            {
                "dialogue_id": "dataset_name_1",
                "num_utterances": 2,
                "utterances": [
                    {
                        "speaker": "A",
                        "text": "Utterance 1 text.",
                        "ap_label": "AP-Label",
                        "da_label": "DA-Label"
                    },
                    {
                        "speaker": "B",
                        "text": "Utterance 2 text.",
                        "ap_label": "AP-Label",
                        "da_label": "DA-Label",
                        "slots": { //Optional
                            "slot_name": "slot_value"
                        }
                    }
                ],
                "scenario": { //Optional
                    "db_id": "1",
                    "db_type": "i.e booking",
                    "task": "i.e book",
                    "items": []
                }
            }
        ]
    }
```
