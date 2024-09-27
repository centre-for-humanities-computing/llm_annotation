# LLM Annotation

## Summary
This repo is for the project on feature first annotation using LLMs.
In this repo there's a bash script that unzips the folder with data from this study (link)
and saves 16 new csv-files in clean_data/ which are the files used for the LLM annotation
and following analysis of performance. 

The cleaning script is in src/ and is called clean_data.py. There is utils.py script as well that contains helper functions. 

The bash script assumes that the .zip file from OSF is in the same layer as the script. 
It is run by:
1. opening the terminal
2. cloning this repo 
3. placing the .zip folder in the repo folder
4. navigating to this folder in the terminal
5. running ```bash run.sh``` in the termianl 


## License ##
This software is [MIT licensed](./LICENSE.txt).
