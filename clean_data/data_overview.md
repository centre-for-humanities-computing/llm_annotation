# a brief description of the different csv-files


## Rathje et al
### emotion annotation of tweets
Two files: one with English tweets and one with Indonesian. 

No tweet IDs were part of the original csv-files from OSF. 

English columns: Tweet, human, GPT3.5, GPT4, GPT4_Turbo
- Raw(?) tweet text
- human annotation, 1: anger, 2: sadness, 3: sadness, 4: optimism
- GPT3.5:GPT4_Turbo -> gpt annotations, same labelling scheme as human

Indonesian columns: Tweet, human, GPT3.5, GPT4
- Preprocessed tweet text 
- human annottaion, 1: anger, 2: fear, 3: sadness, 4: love, 5: joy/happy

Note: Indonesian had different emotions than the English one. Also, inconsitency in whether "happy" or "joy" was used. 
NB: no file existed for GPT4_Turbo in Indonesian. 

