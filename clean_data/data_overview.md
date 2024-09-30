# a brief description of the different csv-files

All files (except the moral foundations and news headlines data) have the same columns: text,human,GPT3.5,GPT4,GPT4-Turbo

These are, respectively, the text (tweet, reddit comment, news headline), the human annotation, the GPT3.5 annotations, the GPT4 annotations, and the GPT4-Turbo annotations. 
All file naes are formated as such: {annotation task} _ {text medium} _ {language}.csv

Some files have some quirks, they are described in depth below. 

### emotion annotation of tweets

Two files: one with English tweets and one with Indonesian. 

Labelling of emotions was inconsistent. Indonesian was annotated with different emotions than the English one. Also, inconsitency in whether "happy" or "joy" was used. 

- English annotations -> 1: anger, 2: joy, 3: sadness, 4: optimism
- Indonesian annotations -> 1: anger, 2: fear, 3: sadness, 4: love, 5: joy/happy

- GPT3.5:GPT4_Turbo -> same labelling scheme as humans in respective languages

 NB: no file existed for GPT4_Turbo in Indonesian, meaning only a GPT3.5 and GPT4 column in that file. 


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

NB: the Turkish .csv file has +3k tweets for GPT3.5 but only 1k for GPT4 and GPT4-Turbo 

### Sentiment - polarity
 One csv per language 
 1: positive, 2: neutral, 3: negative

 Amharic:
 - GPT annotations are only for 1k of the tweets but there are human annotations for 2k tweets

Arabic:
- GPT4 and 4-Turbo annotations are only for first 1k tweets, there are 6.1k human and GPT3.5 annotations

English:
- GPT4 and 4-Turbo annotations are only for first 1k tweets, there are +12k human and GPT3.5 annotations