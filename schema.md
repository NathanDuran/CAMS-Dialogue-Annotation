# Conversation Analysis Schema

Overview
========

The Conversation Analysis (CA) schema defines a domain agnostic annotation scheme for dialogue that is aligned
with the relevant theories from within the CA literature and is also appropriate for computational modelling.
The schema defines both Adjacency Pairs (AP) and Dialogue Acts (DA) which combine to form AP-types.

AP are the base units of sequence-construction in talk,
and in their basic unexpanded form comprise of two turns by different speakers that take place one after the other.
The initial turn is called the *First Pair Part* (FPP) and initiates an exchange,
the second turn is a *Second Pair Part* (SPP) which are responsive to the prior FPP.
To account for more complex dialogue structures,
AP also include the concept of *expansion* which allows the construction of sequences of talk that are made up of more
than one AP, while still contributing to the same basic action,
i.e. a question (FPP-base) could be followed by a question (FPP-insert),
to elicit information required to better answer the initial question, see below:


A: Do you know the directions? &emsp;**FPP-base**

&emsp;B: You driving or walking? &emsp;&emsp;&emsp;&emsp; **FPP-insert**

&emsp;A: Walking.&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;**SPP-insert**

B: Get on the subway. &emsp;&emsp;&emsp;&emsp;&emsp;**SPP-base**


AP can also be ‘type related’, for example, a question and an answer.
This pair-type relation has the useful property of limiting the range of possible SPP responses to a given FPP,
i.e. a question could be followed by an answer (positive or negative).
Within the CA Schema the AP-types are defined by the addition of a DA label.
DA are a method of labelling the *semantic content* and *communicative function* of an utterance,
such as, a question, request or greeting etc.
The semantic content specifies objects, propositions and events that the DA is about;
the communicative function specifies of the way an addressee should use the semantic content to update the
information state (Bunt *et al*., 2012).
Both the AP and DA labels are combined to create an AP-type label for each utterance of a dialogue, see below:


A: Do you know the directions? &emsp;**FPP-base - setQuestion**

&emsp;B: You driving or walking? &emsp;&emsp;&emsp;&emsp;**FPP-insert - choiceQuestion**

&emsp;A: Walking.&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;**SPP-insert - answer**

B: Get on the subway. &emsp;&emsp;&emsp;&emsp;&emsp;**SPP-base - answer**


There are 11 AP in the schema and the set includes;
FPP and SPP for *base*, *pre*, *post* and *insert-expansions* as described by Liddicoat, (2007) and Sidnell, (2010).
Because dialogue does not always contain even numbers of utterances,
there are also single-labels (*pre*, *post* and *insert*)
for utterances that do not belong to conventional AP.
These are closely related to the idea of *minimal-expansions* (Schegloff, 2007),
in that they are not designed to project any further sequences of talk,
but rather open, close or add to sequences respectively.
The set of 35 DA are derived from the Dialogue Act Mark-up Language (DiAML)
as defined in ISO 24617 (British Standards Institution, 2012).
DiAML was developed as an empirically and theoretically well founded, application independent,
DA annotation scheme and is also intended to be used by both human annotators and automatic annotation methods.


Contents
========

[Adjacency Pairs](#adjacency-pairs)
------------
[Base](#base)


[Expansions](#expansions)

&emsp; [Pre-expansions](#pre-expansions)

&emsp; [Insert-expansions](#insert-expansions)

&emsp; [Post-expansions](#post-expansions)


[Minimal-expansions](#minimal-expansions)


[Dialogue Acts](#dialogue-acts)
------------

[Information-seeking Functions](#information-seeking-functions)

&emsp; [propoitionalQuestion (Yes/No)](#propositionalquestion-yesno)

&emsp; [setQuestion (Who/What/Where/How)](#setquestion-whowhatwherehow)

&emsp; [choiceQuestion](#choicequestion)

&emsp; [checkQuestion](#checkquestion)


[Information-providing Functions](#information-providing-functions)

&emsp; [inform (Statement)](#inform-statement)

&emsp; [answer](#answer)

&emsp; [agreement](#agreement)

&emsp; [disagreement](#disagreement)

&emsp; [correction](#correction)

&emsp; [confirm](#confirm)

&emsp; [disconfirm](#disconfirm)


[Commissive Functions](#commissive-functions)

&emsp; [offer](#offer)

&emsp; [addressRequest (Consider/On Condition)](#addressrequest-consideron-condition)

&emsp; [acceptRequest](#acceptrequest)

&emsp; [declineRequest](#declinerequest)

&emsp; [addressSuggest (Consider/On Condition)](#addresssuggest-consideron-condition)

&emsp; [acceptSuggest](#acceptsuggest)

&emsp; [declineSuggest](#declinesuggest)


[Directive Functions](#directive-functions)

&emsp; [request](#request)

&emsp; [suggest](#suggest)

&emsp; [addressOffer (Consider/On Condition)](#addressoffer-consideron-condition)

&emsp; [acceptOffer](#acceptoffer)

&emsp; [declineOffer](#declineoffer)


[Feedback Functions](#feedback-functions)

&emsp; [autoPositive (Positive Understanding/Feedback)](#autopositive-positive-understandingfeedback)

&emsp; [autoNegative (Negative Understanding/Feedback)](#autonegative-negative-understandingfeedback)


[Time Management Functions](#time-management-functions)

&emsp; [stalling (Pausing)](#stalling-pausing)


[Own and Partner Communication Management Functions](#own-and-partner-communication-management-functions)

&emsp; [retraction (Abandon)](#retraction-abandon)


[Social Obligations Management Functions](#social-obligations-management-functions)

&emsp; [initialGreeting](#initialgreeting)

&emsp; [returnGreeting](#returngreeting)

&emsp; [initialGoodbye](#initialgoodbye)

&emsp; [returnGoodbye](#returngoodbye)

&emsp; [thanking](#thanking)

&emsp; [acceptThanking](#acceptthanking)

&emsp; [apology](#apology)

&emsp; [acceptApology](#acceptapology)


[Reference List](#references)
------------

Adjacency Pairs
===============

Adjacency pairs are the basic units on which sequences in conversation are
built. Their core features are:

1.  Consist of two turns (utterances) by different speakers.

2.  Placed next to each other in basic (unexpanded) form, i.e. without an *expansion*.

3.  Are ordered, so that one always occurs after another. Initiation of a
    sequence is a *First Pair Part* (FPP) and the response *Second Pair Part* (SPP).

4.  Differentiated into AP-types. The relationship between FPP and SPP is
    constrained by the type of FPP produced i.e. a *question* followed by an *answer*.

Base
----

The basic sequence is composed of two ordered turns at talk, the FPP and SPP.
Participants in conversation orient to this basic sequence structure in
developing their talk and AP have a normative force in organizing conversation
,in that, AP set up expectations about how talk will proceed.

**Labels:** *FPP-base, SPP-base*

**Example:**

A: What time is it? &emsp;**FPP-base - setQuestion**

B: Three o’ clock. &emsp; **SPP-base - answer**

Expansions
----------

Expansion allow talk which is made up of more than a single AP to be constructed
and understood as performing the same basic action and the various additional
elements are seen as doing interactional work related to the basic action under
way. Sequence expansion is constructed in relation to a base sequence of a FPP
and SPP in which the core action under way is achieved.
There are three types of expansion pairs:

### Pre-expansions

Pre-expansions are designed to be preliminary to some projected base sequence
and are hearable by participants as preludes to some other action.

**Labels:** *FPP-pre, SPP-pre*

**Example:**

A: What you doing? &emsp; **FPP-pre - setQuestion**

B: Not much. &emsp;&emsp;&emsp;&emsp; **SPP-pre - answer**

&emsp; A: Wanna drink? &emsp;&emsp; **FPP-base - propositionalQuestion**

&emsp; B: Sure. &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;**SPP-base - confirm**

### Insert-expansions

Insert-expansions occur between base adjacency pairs and separates the FPP and
SPP. Insert-expansions interrupt the activity previously underway but are still
relevant to that action and allows the second speaker (who must produce the base
SPP), to do interactional work relevant to the base SPP. Insert expansion is
realised through a sequence of its own and is launched by a FPP from the second
speaker which requires a SPP for completion. Once the sequence is completed the
base SPP once again becomes relevant as the next action.

**Labels:** *FPP-insert, SPP-insert*

**Example:**

A: Do you know the directions? &emsp;**FPP-base - setQuestion**

&emsp;B: You driving or walking? &emsp;&emsp;&emsp;&emsp;**FPP-insert - choiceQuestion**

&emsp;A: Walking.&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;**SPP-insert - answer**

B: Get on the subway. &emsp;&emsp;&emsp;&emsp;&emsp;**SPP-base - answer**

### Post-expansions

Sequences are also potentially expandable after the completion of the base SPP.
Once an SPP has been completed, the sequence is potentially complete: the action
launched by the FPP has run its course and a new action could appropriately be
begun. However, it is also possible for talk to occur after the SPP which is
recognizably associated with the preceding sequence. That is, it is possible for
sequences to be expanded after their SPP.

**Labels:** *FPP-post, SPP-post*

**Example:**

A: What is the weather like today in tomorrow? &emsp; **FPP-base - setQuestion**

B: Forecast for cloudy skies today. &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **SPP-base - answer**

&emsp; A: Okay. &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;**FPP-post - autoPositive**

&emsp; B: No problem. &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;**SPP-post - acceptThanking**

Minimal-expansions
------------------

Minimal-expansion involves the addition of one additional turn to a sequence.
The turn which is added is designed not to project any further within-sequence
talk beyond itself; that is, it is designed to constitute a minimal expansion
before, during or after the pair part. The primary role is to allow for
additional turns that behave as expansions but consist only of one turn.

**Labels:** *Pre, Insert, Post*

**Example:**

A: When is my dentist appointment? &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;**FPP-base - setQuestion**

&emsp; A: Who am I going with? &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **Insert - setQuestion**

B: The appointment is at 11 am with your Aunt. &emsp;**SPP-base - answer**

A: Thanks. &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **Post - thanking**

Dialogue Acts
=============

An utterances DA describes not just its meaning, but the speakers intentions in
the wider context of the conversation, and therefore, facilitate the
computational modelling of communicative behaviour in dialogue (Bunt *et al.*,
2012). The following DA are aligned with DiAML (ISO 24617-2) (British Standards
Institution, 2012) and are arranged into eight categories according to their
function.

Information-seeking Functions
-----------------------------

### propositionalQuestion (Yes/No)

Communicative function of a dialogue act performed by the sender, S, in order to
know whether the proposition, which forms the semantic content, is true. S
assumes that A knows whether the proposition is true or not and puts pressure on
A to provide this information.

A propositional question corresponds to what is commonly termed a YN-question in
the linguistic literature. This standard prefers the term ‘propositional
question’ because the term ‘YN-Question’ carries the suggestion that this kind
of question can only be answered by ‘yes’ or ‘no’, which is not the case.

**Example:** “Does the meeting start at ten?”

### setQuestion (Who/What/Where/How)

Communicative function of a dialogue act performed by the sender, S, in order to
know which elements of a given set have a certain property specified by the
semantic content; S puts pressure on the addressee, A, to provide this
information, which S assumes that A possesses. S believes that at least one
element of the set has that property.

A set question corresponds to what is commonly termed a WH- question in the
linguistic literature. The term ‘set question’ is preferred because: (a) it
clearly separates form from function by removing any oblique reference to
syntactic criteria for the identification of such acts; and (b) it is not a
language specific term (it may be further noted that even in English, not all
questioning words begin with ’wh’, e.g. “How?”).

**Example:** “What time does the meeting start?”; “How far is it to the
station?”

### choiceQuestion

Communicative function of a dialogue act performed by the sender, S, in order to
know which one from a list of alternative propositions, specified by the
semantic content, is true; S believes that exactly one element of that list is
true; S assumes that the addressee, A, knows which of the alternative
propositions is true, and S puts pressure on A to provide this information.

It is not very common in annotation schemes to specifically distinguish the
concept of choice questions from that of set questions. However, whereas it is
common for the concept set question to carry the expectation that all members of
the set with a given property should be returned by the addressee, for a choice-
question the expectation is that there will be exactly one. The different
preconditions and effects indicate that these are semantically different
concepts, and they have been treated here as such.

**Example:** “Should the telephone cable go in telephone line or in external
line?”

### checkQuestion

Communicative function of a dialogue act performed by the sender, S, in order to
know whether a proposition, which forms the semantic content, is true, S holds
the uncertain belief that it is true S. S assumes that A knows whether the
proposition is true or not and puts pressure on A to provide this information.

**Example:** “The meeting starts at ten, right?”

Information-providing Functions
-------------------------------

### inform (Statement)

Communicative function of a dialogue act performed by the sender, S, in order to
make the information contained in the semantic content known to the addressee,
A; S assumes that the information is correct.

The inform function may also have more specific rhetorical functions such as:
explain, elaborate, exemplify and justify; this is treated in this standard by
means of rhetorical relations.

**Example:** “The 6.34 to Breda leaves from platform 2.”

### answer

Communicative function of a dialogue act performed by the sender, S, in order to
make certain information available to the addressee, A, which S believes A wants
to know; S assumes that this information is correct.

**Example:**

S: “what does the display say?”

A: “Send error document ready”

### agreement

Communicative function of a dialogue act performed by the sender, S, in order to
inform the addressee, A that S assumes a given proposition to be true, which S
believes that A also assumes to be true.

DAMSL and SWBD-DAMSL use “Agreement” to refer to various degrees in which some
previous proposal, plan, opinion or statement is accepted; “accept” is one of
these degrees; “reject” is another.

**Example:** “Exactly”

### disagreement

Communicative function of a dialogue act performed by the sender, S, in order to
inform the addressee, A that S assumes a given proposition to be false, which S
believes that A assumes to be true.

DAMSL and SWBD-DAMSL use “Agreement” to refer to various degrees in which a
speaker accepts some previous proposal, plan, opinion or statement; “accept” is
one of these degrees; “reject” is another.

**Example:**

S: “Do you know where to find ink saving?”

A: “ehm... oh I think to the left of the ink cartridge”

S: “ehm... no”

### correction

Communicative function of a dialogue act performed by the sender, S, in order to
inform the addressee, A, that certain information which S has reason to believe
that A assumes to be correct, is in fact incorrect and that instead the
information that S provides is correct.

**Example:** “To Montreal, not to Ottawa.”

### confirm

Communicative function of a dialogue act performed by the sender, S, in order to
inform the addressee, A, that certain information that A wants to know, and
concerning which A holds an uncertain belief, is indeed correct.

**Example:** “Indeed”

### disconfirm

Communicative function of a dialogue act performed by the sender, S, in order to
let the addressee, A, know that certain information that A wants to know, and
concerning which A holds an uncertain belief, is incorrect.

**Example:** “Nope”

Commissive Functions
--------------------

### offer

Communicative function of a dialogue act by which the sender, S, indicates his
willingness and ability to perform the action, specified by the semantic
content, conditional on the consent of addressee A that S do so.

**Example:** “I will look that up for you”

### addressRequest (Consider/On Condition)

Communicative function of a dialogue act by which the sender, S, indicates that
he considers the performance of an action that he was requested to perform.

The addressRequest function covers a range of possible responses to a request.
If the response does not express a condition, then the sender commits himself
unconditionally to perform the requested action; this is the special case of
acceptRequest. If the condition is specified that the action be performed zero
times, then the sender in fact declines to perform the requested action (as he
commits him- self to not perform the action). See also the data categories for
the qualifiers /conditional/ and /partial/

**Example:**

A: “Please give me the gun.”

S: “If you push the bag to me.”

### acceptRequest

Communicative function of a dialogue act by which the sender, S, commits himself
to perform an action that he has been requested to perform, possibly depending
on certain conditions that he makes explicit.

**Example:** “Sure”

### declineRequest

Communicative function of a dialogue act by which the sender, S, indicates that
he refuses to perform an action that he has been re- quested to perform,
possibly depending on certain conditions that he makes explicit.

**Example:** “Not now”

### addressSuggest (Consider/On Condition)

Communicative function of a dialogue act by which the sender, S, indicates that
he considers performing an action that was suggested to him, possibly depending
on certain conditions that he makes explicit.

**Example:**

A: “Let’s go there together.”

S: “Only if we’re in full agreement about the way to proceed when we get there.”

### acceptSuggest

Communicative function of a dialogue act by which the sender, S, commits himself
to perform an action that was suggested to him, possibly with certain
restrictions or conditions concerning manner or frequency of performance.

**Example:** “Let’s do that”

### declineSuggest

Communicative function of a dialogue act by which the sender, S, indicates that
he will not perform an action that was suggested to him, possibly depending on
certain conditions that he makes explicit.

**Example:** “I don’t think so”

Directive Functions
-------------------

### request

Communicative function of a dialogue act performed by the sender, S, in order to
create a commitment for the addressee, A, to perform a certain action in the
manner or with the frequency described by the semantic content, conditional on
A’s consent to perform the action. S assumes that A is able to perform this
action.

**Example:** “Please turn to page five”; “Please don’t do this ever again”;
“Please drive very carefully”.

### suggest

Communicative function of a dialogue act performed by the sender, S, in order to
make the addressee, A, consider the performance of a certain action, specified
by the semantic content, S believes that this action is in A’s interest, and
assumes that A is able to perform the action.

**Example:** “Let’s wait for the speaker to finish.”

### addressOffer (Consider/On Condition)

Communicative function of a dialogue act performed by the sender, S, in order to
indicate that he is considering the possibility that A performs the action.

**Example:** “That would be good!”

### acceptOffer

Communicative function of a dialogue act performed by the sender, S, in order to
inform the addressee, A, that S would like A to perform the action that A has
offered to perform, possibly with certain conditions that he makes explicit.

**Example:** “Yes please”

### declineOffer

Communicative function of a dialogue act performed by the sender, S, in order to
inform the addressee, A, that S does not want A to perform the action that A has
offered to perform, possibly depending on certain conditions that he makes
explicit.

**Example:** “No thank you”

Feedback Functions
------------------

### autoPositive (Positive Understanding/Feedback)

Communicative function of a dialogue act performed by the sender, S, in order to
inform the addressee, A that S believes that S’s processing of the previous
utterance(s) was successful.

Feedback mostly concerns the processing of the last utterance from the
addressee, but sometimes, especially in the case of positive feed- back, it
concerns a longer stretch of dialogue.

**Example:** “Uh-huh”; “Okay”; “Yes”

### autoNegative (Negative Understanding/Feedback)

Communicative function of a dialogue act performed by the sender, S, in order to
inform the addressee, A that S’s processing of the previous utterance(s)
encountered a problem.

**Example:** “Sorry?”; “What?”

Time Management Functions
-------------------------

### stalling (Pausing)

Communicative function of a dialogue act performed by the sender, S, in order to
have a little extra time to construct his contribution or to suspend the
dialogue for a short while.

Pausing occurs either in preparation of continuing the dialogue, or because
something else came up which is more urgent for the sender to attend to.

**Example: “**Let me see...”; “Ehm...”; “Just a moment”

Own and Partner Communication Management Functions
--------------------------------------------------

### retraction (Abandon)

Communicative function of a dialogue act performed by the sender, S, in order to
withdraw something that he just said within the same turn.

**Example:** “then we’re going to g– ”

Social Obligations Management Functions
---------------------------------------

### initialGreeting

Communicative function of a dialogue act performed by the sender, S, in order to
inform the addressee, A that S is present and aware of A’s presence; S puts
pressure on A to acknowledge this.

Greetings usually come in initiative-response pairs within a dialogue; this data
category corresponds to the first element of such a pair.

**Example:** “Hello!”; “Good morning”

### returnGreeting

Communicative function of a dialogue act performed by the sender, S, in order to
acknowledge that S is aware of the presence of the addressee, A, and of A having
signalled his presence to S.

### initialGoodbye

Communicative function of a dialogue act performed by the sender, S, in order to
inform the addressee, A, that S intends the current utterance to be his final
contribution to the dialogue; S puts pressure on A to acknowledge this.

Goodbyes usually come in initiative-response pairs within a dialogue; this data
category corresponds to the second element of such a pair. Initial and return
goodbyes are commonly used to close a dialogue

**Example:** “Bye bye, see you later”

### returnGoodbye

Communicative function of a dialogue act performed by the sender, S, in order to
acknowledge his awareness that the addressee, A, has signalled his final
contribution to the dialogue and S signals in return his agreement to end the
dialogue; S has been pressured to respond to an initialGoodbye by A.

**Example: “**Bye bye, see you.”

### thanking

Communicative function of a dialogue act performed by the sender, S, in order to
inform the addressee, A, that S is grateful for some action performed by A; S
puts pressure on A to acknowledge this.

Utterances used for thanking often also indicate that the sender wants to end
the dialogue.

**Example:** “Thanks a lot.”

### acceptThanking

Communicative function of a dialogue act performed by the sender, S, in order to
mitigate to the feelings of gratitude which the addressee, A’, has expressed.

**Example:** “Don’t mention it”

### apology

Communicative function of a dialogue act performed by the sender, S, in order to
signal that he wants the addressee, A, to know that S regrets something; S puts
pressure on A to acknowledge this.

**Example:** “Sorry about that.”

### acceptApology

Communicative function of a dialogue act performed by the sender, S, in order to
mitigate, the feelings of regret that the addressee, A, has expressed.

**Example: “**No problem.”

References
==========

British Standards Institution (2012) ‘ISO 24617-2: Language Resource Management
*-* Semantic Annotation Framework (SemAF) Part 2: Dialogue acts’. British
Standards Institution.

Bunt, H. *et al.* (2012) ‘ISO 24617-2 : A Semantically-based Standard for
Dialogue Annotation’, in *Proceedings of LREC 2012*, pp. 430–437.

Liddicoat, A. J. (2007) *An Introduction to Conversation Analysis*. London:
Continuum.

Schegloff, E. A. (2007) *Sequence Oranization in Interaction: A Primer in
Conversation Analysis I*. Cambridge: Cambridge University Press. doi:
10.1017/CBO9780511791208.

Sidnell, J. (2010) *Conversation Analysis - An Introduction*. Whiley-Blackwell.
doi: 10.1093/acrefore/9780199384655.013.40.
