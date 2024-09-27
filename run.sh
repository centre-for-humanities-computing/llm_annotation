sudo apt-get install unzip

unzip Datasets_GPT_Output.zip -d 'Datasets_GPT_Output'

pip3 install -r requirements.txt

python3 src/clean_data.py
