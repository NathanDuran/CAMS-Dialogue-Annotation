# Conversation Analysis Modelling Schema Dialogue Annotation
This tool facilitates annotation of dialogues with the Conversation Analysis Modelling Schema (CAMS).
CAMS combines the Conversation Analysis concept of Adjacency Pairs (AP), with Dialogue Acts (DA),
to create *AP-types*, descriptive labels that capture the semantic and syntactic structure of dialogue.
A full definition of the schema labels and annotation instructions can be found in the
[Conversation Analysis Modelling Schema](https://nathanduran.github.io/Conversation-Analysis-Modelling-Schema/).
The tool was created as part of a study to measure inter-annotator agreement when applying CAMS to a range of dialogues.
This repository contains all data and results/analysis for the paper
[Inter-annotator Agreement Using the Conversation Analysis Modelling Schema, for Dialogue.](https://www.tandfonline.com/doi/full/10.1080/19312458.2021.2020229)

This repository also contains all necessary code to run the tool, the annotated datasets,
and the Python scripts used to calculate inter-annotator agreement and analyse the results.
The server side implementation is written using Python 3.6 and [Flask](http://flask.pocoo.org/),
and client side written in JavaScript.

## Contents
- [Overview](#overview-link)
- [Dialogue Data](#dialogue-data-link)
- [User Instructions](#user-instructions-link)
- [Data Processing/Analysis](/data_processing/README.md)

## Overview<a name="overview-link">
The study participants were asked to label 5 dialogues, containing both task and non-task-oriented conversations.
In total, 15 participants took part in the study, and each was assigned one of 5 different sets of dialogue for
annotation. The dialogue sets were evenly distributed among the participants, resulting in 3 annotators per set.
The first dialogue in each set is a practice dialogue,
followed by the 4 dialogues in their respective set (2 task-oriented and 2 non-task-oriented).
The latter 4 dialogues were shown to participants in a random order to encourage independent annotation,
and mitigate any learning effect of the software, or schema, on annotation results.
The participants were given one hour to annotate all dialogues,
and had no previous training using the annotation tool or knowledge of CAMS.
Upon completion of each dialogue, participants were asked to rate, by means of a Likert Scale,
how well their annotations fit the data. Timing data was also collected during the annotation process,
which recorded how long participants spent annotating each utterance of dialogue.
The timing and rating data were used, in addition to the calculated inter-annotator agreement,
for further analysis of the manner in which annotators apply the schema,
and comparison of task and non-task-oriented dialogues.

## Dialogue Data<a name="dialogue-data-link">
Users are presented with one of 5 sets of dialogue that contain a mixture of task-oriented and non-task oriented dialogues
from 4 different corpora:

- [Saarbrücken Corpus of Spoken English (SCoSE)](https://github.com/NathanDuran/SCoSE-Copus)
- [Conversation Analytic of the British National CorpusCABNC](https://github.com/NathanDuran/CABNC-Corpus)
- [CAMS-KVRET](https://github.com/NathanDuran/CAMS-KVRET)
- [bAbI-Tasks](https://github.com/NathanDuran/bAbI-Tasks-Corpus)


|     Set     |     KVRET       |     # Utts    |     bAbl              |     # Utts    |     CABNC       |     # Utts    |     SCoSE             |     # Utts    |     Total    |
|-------------|-----------------|---------------|-----------------------|---------------|-----------------|---------------|-----------------------|---------------|--------------|
|     1       |     test_28     |     7         |     task1_test_290    |     7         |     KB7RE015    |     9         |     jason-mammoth     |     19        |     48       |
|     2       |     test_52     |     8         |     task1_test_428    |     7         |     KBKRE03G    |     6         |     jason-clone       |     19        |     46       |
|     3       |     test_96     |     4         |     task1_test_555    |     5         |     KDARE00G    |     4         |     jason-accident    |     29        |     48       |
|     4       |     test_129    |     6         |     task1_test_564    |     5         |     KE2RE00Y    |     4         |     lynne-hunter      |     25        |     46       |
|     5       |     test_102    |     4         |     task1_test_894    |     5         |     KBERE00G    |     5         |     lynne-tipsy       |     26        |     46       |
|     Mean    |                 |     5.8       |                       |     5.8       |                 |     5.6       |                       |     23.6      |     46.8     |

### Example Dialogues
#### KVRET
A1:	Where can I find a parking garage?

B1:	Palo Alto Garage is at 481 Amaranta Ave.

A2:	Is that the quickest route?

B2:	I will send on your screen the quickest route, sure, there is heavy traffic now and we will have to make the route slightly longer

A3:	Ok thanks for the notification.

#### bAbI
A1:	good morning

B1:	hello what can i help you with today

A2:	i’d like to book a table in london in a moderate price range for six with French cuisine

B2:	i’m on it

B3:	ok let me look into some options for you

#### CABNC
A1:	That’s filled you up has it.

B1:	That’s very nice yes yes.

A2:	Do you want a bit of ice cream or.

B2:	Yeah have ice cream have that lovely one we had the other day.

#### SCoSE
A1:	didn’t they, didn’t you ever hear that they, they found an entire woolly mammoth, frozen.

B1:	yeah, and they ate it.

A2:	an entire one though.

B2:	yeah

A3:	almost practically whole

A3:	yeah, like almost perfectly, preserved.

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

## User Instructions<a name="user-instructions-link">
You will be given a set of **five unlabelled dialogues** that are a mixture of task-oriented and non-task-oriented conversations.
For each dialogue you will be asked to label each utterance with one AP and one DA label which combine into an AP-type label.
Once a dialogue is fully labelled you will be asked to rate the different AP,
DA and DA-type labels you have provided using a 7 point scale.
You will also be given the opportunity to highlight any labels,
or combination of labels that you do not think adequately describe the dialogue.

### Annotation Screen
Once you have logged in using your unique user-id you can access the annotation screen by clicking on the Annotate tab.
The first dialogue you see will be a short practice dialogue to give you an opportunity to get used to the tools controls
and the process of applying the labels.  

The currently selected utterance is highlighted in <span style="color: #0366d6; font-weight: bold">blue</span>.
You can select an utterance to label at any time just by clicking on it.
As you can see, the first utterance is automatically selected for you.  

To apply labels to this utterance simply click on one of the AP buttons and one of the DA buttons from the set at the bottom of the screen.
The labels to the right of the utterance will change to reflect your selection.
Once you have selected one of each label type (DA and AP) the utterance will turn
<span style="color: green; font-weight: bold">green</span> and the next unlabelled utterance will be automatically selected for you.  

If you hover over one of the label buttons a popup will appear an alternative name for that label and/or a short description and an example.  

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

---------------
# Citation

If you are using any code or data from this project in your work please cite: [Nathan Duran, Steve Battle & Jim Smith (2022) Inter-annotator Agreement Using the Conversation Analysis Modelling Schema, for Dialogue, Communication Methods and Measures, DOI: 10.1080/19312458.2021.2020229](https://www.tandfonline.com/doi/full/10.1080/19312458.2021.2020229)