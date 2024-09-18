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


