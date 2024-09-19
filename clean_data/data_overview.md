# a brief description of the different csv-files


## Rathje et al
### emotion annotation of tweets
Two files: one with English tweets and one with Indonesian. 

No tweet IDs were part of the original csv-files from OSF. 

English columns: Tweet, human, GPT3.5, GPT4, GPT4_Turbo
- Raw(?) tweet text
- human annotation, 1: anger, 2: joy, 3: sadness, 4: optimism
- GPT3.5:GPT4_Turbo -> gpt annotations, same labelling scheme as human

Indonesian columns: Tweet, human, GPT3.5, GPT4 (NB: no file existed for GPT4_Turbo in Indonesian.)
- Preprocessed tweet text 
- human annottaion, 1: anger, 2: fear, 3: sadness, 4: love, 5: joy/happy

Note: Indonesian had different emotions than the English one. Also, inconsitency in whether "happy" or "joy" was used. 


### moral foundations in reddit comments
One file with reddit comments in English

Columns: 
- text: the reddit comment
- Care,Equality,Proportionality,Loyalty,Authority,Purity,Thin Morality,Non-Moral,is_moral: human annotations, 0's and 1's, one text can have multiple 1's 
- GPT4_Authority,GPT4_Care,GPT4_Equality,GPT4_Loyalty,GPT4_MoralSentiment,GPT4_Purity,GPT4_Proportionality: GPT4 annotations 
- GPT4-Turbo_Authority,GPT4-Turbo_Equality,GPT4-Turbo_Loyalty,GPT4-Turbo_MoralSentiment,GPT4-Turbo_Proportionality,GPT4-Turbo_Purity: GPT4-Turbo annotations

NB: Care not annotated with GPT4-Turbo

### Sentiment and emotion in news headlines - Likert scales (1-7)
One file with news headlines in English

Columns: 
- text: the headline 
- sentiment,anger,fear,joy,sadness: human annotations, mean(?) of multiple annotators
- GPT3.5_Sentiment,GPT3.5_Anger,GPT3.5_Joy,GPT3.5_Sadness,GPT3.5_Fear: GPT3.5 annotations
- GPT4_Sentiment,GPT4_Anger,GPT4_Joy,GPT4_Sadness,GPT4_Fear: GPT4 annotations
- GPT4-Turbo_Sentiment,GPT4-Turbo_Anger,GPT4-Turbo_Joy,GPT4-Turbo_Sadness,GPT4-Turbo_Fear: GPT4-Turbo annotations

### Offensiveness 
Two files: one with English tweets and one with Turkish tweets.
Annotated for offensiveness - 1's and 0's. 

No official tweet IDs were included in the data. 

Columns: 
- tweet: the tweet text
- human: the human annotation
- GPT3.5:GPT4-Turbo: the gpt annotations

NB: the Turkish .csv file has +3k tweets for GPT3.5 but only 1k for GPT4 and GPT4-Turbo 

### Sentiment - polarity
 One csv per language 
 1: positive, 2: neutral, 3: negative

 Amharic:
 - tweet, label names, human annotation, GPT3.5, GPT4, GPT4-Turbo annotations
 - GPT annotations are only for 1k of the tweets but there are human annotations for 2k tweets
 - NB: no tweets IDs part of the data

Arabic:
- ID, tweet, human annotation, GPT3.5, GPT4, GPT4-Turbo annotations
- GPT4 and 4-Turbo annotations are only for first 1k tweets, there are 6.1k human and GPT3.5 annotations
- NB: unsure whether IDs are official tweet IDs. 

English:
- ID, tweet, human annotation, GPT3.5, GPT4, GPT4-Turbo annotations
- GPT4 and 4-Turbo annotations are only for first 1k tweets, there are +12k human and GPT3.5 annotations
- NB: unsure whether IDs are official tweet IDs. 

Hausa:
- tweet,label names, human annotations, GPT3.5, GPT4, GPT4-Turbo
- NB: no tweet IDs part of the data 

Igbo:
- tweet,label,human,GPT3.5,GPT4,GPT4-Turbo
- NB: no tweet IDs part of the data 

 Kinyarwanda:
- tweet,human,GPT3.5,GPT4,GPT4-Turbo
- NB: no tweet IDs 

Swahili:
- tweet,human,GPT3.5,GPT4,GPT4-Turbo
- NB: no tweet IDs 

Tsonga:
- tweet,label,human,GPT3.5,GPT4,GPT4-Turbo
- NB: no tweet IDs

Twi:
- id,tweet,human,GPT3.5,GPT4,GPT4-Turbo
- NB: ID is not tweet IDs, it's doc IDs 


Yoruba:
- id,tweet,human,GPT3.5,GPT4,GPT4-Turbo
- NB: ID is not tweet IDs, it's doc IDs 




## Gilardi et al

There are six different annotation tasks: 
- relevance-content: binary, is the tweet relevant for the content moderation issue
- relevance-poli: binary, is the tweet relevant for political issues 
- stance: 3 classes, stance regarding Section 230 (keep/repeal/neutral)
- topic: 6 classes 
- frames1: 3 classes, content moderation frames (problem/solution/neutral)
- frames2: 14 classes, policy frames 

There are four datasets:
- tweets-old: random tweets posted in 2020-2021
    - dataset A in the paper
- tweets-new: random tweets posted in Jan 2023
    - dataset C 
- tweet-poli: tweets posted by members of US congress in 2017-2022
    - dataset D 
- news: news articles on content mdoeration 
    - dataset B

There are 11 different files - 1 per task per dataset
- no dataset has done all tasks 


NB: status_id columns was kept across datasets because it might be tweet IDs, but I'm not sure. 

