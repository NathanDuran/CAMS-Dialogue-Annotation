# CA Dialogue Tagger
### TODO
- practice?

- generate valid user list

- stop auto redirect to annotate page if logged in from home.

- Getters and setters for dialogue model vars (is_labelled etc)
- Better checks for dialogue model vars
- checks for (labelled false and completed true) when saving/in dialogue model.py/utilities.py.

- Label button tooltips
- Highlight DA/AP labels once labelled?
- Colour code or otherwise highlight the AP and DA labele buttons differently?

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
