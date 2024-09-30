# LLM Annotation

## Summary
This repo is for the project on feature first annotation using LLMs.
In this repo there's a bash script that unzips the folder with data from this study ([link])(https://osf.io/6pnb2/) 
and saves 16 new csv-files in clean_data/. These are the files used in the LLM annotation project
and the analysis of performance. 

The cleaning script is in src/ and is called clean_data.py. There is utils.py script as well that contains helper functions. 

The bash script assumes that the .zip file from OSF is in the same layer as the script. 
It is run by:
1. opening the terminal
2. cloning this repo 
3. placing the .zip folder in the repo folder
4. navigating to this folder in the terminal
5. running ```bash run.sh``` in the terminal 

The bash script itself installs the unzip function, unzips the folder, install the dependencies for the python script, and then loads, cleans, and saves the data. 

## License ##
This software is [MIT licensed](./LICENSE.txt).
