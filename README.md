# Conversation Analysis Dialogue Tagger
The CA-Dialogue-Tagger facilitates annotation of dialogues with Dialogue Acts (DA) and Adjacency Pairs (AP) to create *AP-types* 
that are closely aligned with the concept of typed AP in Conversation Analysis (CA).
A full explanation of the intended use for the CA labelled corpus can be found in the paper 
[Conversation Analysis Structured Dialogue for Multi-Domain Dialogue Management](https://www.researchgate.net/publication/329809503_Conversation_Analysis_Structured_Dialogue_for_Multi-Domain_Dialogue_Management).
A definition of the DA and AP labels can be found in the [CA schema](https://nathanduran.github.io/CA-Schema/).

The server side implementation is written using Python 3.6 and [Flask](http://flask.pocoo.org/).

## TODO
- Add study/paper link.
- Add overview of study.

## Data
Users are presented with one of 5 sets of dialogue that contain a mixture of task-oriented and non-task oriented interactions
from 4 different corpora.
- [Saarbrücken Corpus of Spoken English (SCoSE)](https://github.com/NathanDuran/SCoSE-Copus)
- [CABNC](https://github.com/NathanDuran/CABNC-Corpus)
- [CA-KVRET](https://github.com/NathanDuran/CA-KVRET)
- [bAbI-Tasks](https://github.com/NathanDuran/bAbI-Tasks-Corpus)

### Example JSON Format
The following is an example of the JSON format created for each users annotations.
```json
{
    "dataset": "set_1",
    "user_id": "usr-1",
    "num_dialogues": 1,
    "num_labelled": 0,
    "num_unlabelled": 1,
    "num_complete": 0,
    "num_incomplete": 1,
    "dialogues": [
        {
            "dialogue_id": "Name of the dialogue",
            "is_labelled": false,
            "is_complete": false,
            "time": 0,
            "questions": [],
            "num_utterances": 2,
            "utterances": [
                {
                    "speaker": "A",
                    "text": "The utterance text.",
                    "ap_label": "AP-Label",
                    "da_label": "DA-Label",
                    "is_labelled": false,
                    "time": 0,
                    "ap_flag": false,
                    "da_flag": false
                },
                {
                    "speaker": "B",
                    "text": "The utterance text.",
                    "ap_label": "AP-Label",
                    "da_label": "DA-Label",
                    "is_labelled": false,
                    "time": 0,
                    "ap_flag": false,
                    "da_flag": false
                }
            ]
        }
    ]
}
```

## User Instructions
You will be given a set of five unlabelled dialogues that are a mixture of task-oriented and non-task-oriented conversations.
The first one you see will be short practice dialogue and the rest are selected from four different corpora,
[SCoSE](https://github.com/NathanDuran/SCoSE-Copus), 
[CABNC](https://github.com/NathanDuran/CABNC-Corpus), 
[CA-KVRET](https://github.com/NathanDuran/CA-KVRET) and
[bAbI-Tasks](https://github.com/NathanDuran/bAbI-Tasks-Corpus).
In total there are ~40 utterances across all dialogues in a set.
One dialogue in the set is longer than the rest, so dont worry if the first one you see is very long!

For each dialogue you will be asked to label each utterance with one AP and one DA label which combine into an AP-type label.
There is a lot of information in the Schema and you are not expected to remember all of the label types.
However, please make sure you follow the short Annotation Guidelines when selecting labels.
The label buttons on the annotation page have tooltips with short label descriptions, if you hover the mouse over them.
You can also return to the schema page for reference at any time during annotation and your progress will be saved.
        
Once a dialogue is fully labelled you will be asked to rate the different AP, DA and DA-type labels you have provided using a 7 point scale.
You will also be given the opportunity to highlight any labels, or combination of labels that you think do not adequately describe the dialogue.

### Annotation Screen
Once you have logged in using your unique user-id you can access the annotation screen by clicking on the Annotate tab above.
The first dialogue you see will be a short practice dialogue to give you an opportunity to get used to the tools controls
and the process of applying the labels.  

The currently selected utterance is highlighted in <span style="color: #0366d6; font-weight: bold">blue</span>.
You can select an utterance to label at any time just by clicking on it.
As you can see, the first utterance is automatically selected for you.  

To apply labels to this utterance simply click on one of the AP buttons and one of the DA buttons from the set at the bottom of the screen.
The labels to the right of the utterance will change to reflect your selection.
Once you have selected one of each label type (DA and AP) the utterance will turn <span style="color: green; font-weight: bold">green</span>,
indicating that it is now labelled with an AP-type and the next unlabelled utterance will be automatically selected for you.  

If you hover over one of the label buttons a tooltip will appear with an alternative name for that label and/or a short description and an example.  

You can remove the labels for any utterance by clicking on the ![clear button](/static/images/delete_square.png) button next to the labels.


<p align="center">
<img src="/static/images/annotation_screen.png" width="1100" height="650">
</p>

### Questionnaire Screen
Once every utterance in the dialogue is labelled you can click the 'Complete Dialogue' button or either of the navigation buttons
![prev button](/static/images/prev.png) ![next button](/static/images/next.png) to open the question popup for this dialogue.
Here you will be asked to rate the DA and AP labels you have selected for this dialogue as well as the combination of labels i.e. the AP-type labels.  

You also have the opportunity to select any labels or combination of labels that you think do not adequately describe the dialogue.
You can select as many you want, or none, but please try and highlight any labels that you found difficult to choose or did not quite fit the utterance(s).  

Once you have finished the questionnaire click submit to finish the current dialogue.
If you want to change your annotations or answers at any time just click the 'Revise Dialogue' button.  

You can now use the navigation buttons ![prev button](/static/images/prev.png) ![next button](/static/images/next.png) to move on to the next dialogue.

<p align="center">
<img src="/static/images/questionnaire_screen.png" width="1100" height="650">
</p>


