import pandas as pd

from pathlib import Path
import re
from numbers_parser import Document

def load_numbers_file(file_path):
    """
    takes a path to a numbers file and returns a pandas dataframe 
    """
    doc = Document(file_path)

    sheets = doc.sheets
    tables = sheets[0].tables
    data = tables[0].rows(values_only=True)
    df = pd.DataFrame(data[1:], columns=data[0])

    return df

def fix_dummy_columns(df: pd.DataFrame, dummy_cols: list, new_col_name: str) -> pd.DataFrame:
    """
    adds a column to the given dataframe which are the annotations based on the
    dummy columns specified.
    the function assumes that the list is ordered so the labels' indexes
    match the numerical labels (i.e., anger is first bc it is labelled using 1)
    """
    df[new_col_name] = pd.from_dummies(df[dummy_cols])

    # make dict used to make the annotations numerical
    label_dict = dict(zip(dummy_cols, range(1, len(dummy_cols) + 1)))

    df = df.replace({new_col_name: label_dict})

    return df


def make_clean_df(df1, df2, df3=None):
    """
    takes the dataframes and gives them consistent column names and formatting
    """

    # rename columns
    df1 = df1.rename({"gpt": "GPT3.5", "Tweet": "text", "tweet": "text"}, axis=1)
    # select only the relevant ones
    full_df = df1.loc[:, ["text", "human", "GPT3.5"]]

    # because the offensive GPT4 columns are called offensive
    if "offensive" in df2.columns:
        full_df["GPT4"] = df2["offensive"]

    # all others are gpt4
    else:
        full_df["GPT4"] = df2["gpt4"]

    # because indonesian only has two dataframes
    if df3 is not None:
        full_df["GPT4-Turbo"] = df3["gpt4"]

    return full_df


def change_news_colnames(df: pd.DataFrame, model: str):
    # find column names that contain annotations
    annotation_columns = [col for col in df.columns if col.startswith("gpt")]

    # create a list of new column names comprised of the model name and the annotated emotion
    # (the regex finds the emotion from the old column name)
    new_col_names = []
    for column in annotation_columns:
        emotion = re.match(pattern="gpt(.*?)(Turbo)?$", string=column).group(1)

        col_name = f"{model}_{emotion.capitalize()}"

        new_col_names.append(col_name)

    # create a dict for renaming the columns
    rename_dict = dict(zip(annotation_columns, new_col_names))

    # do the renaming
    df = df.rename(rename_dict, axis=1)

    return df


def load_lang_csv_from_list(lang, filelist):
    """
    find the csv file that matches the specified language from the filelist
    and return it as a pandas dataframe
    """
    # make df None per default, so if there is no file for that lang in the list, None is returned
    df = None

    # for each file in the list, make the file name lowercase and look for the languages
    for file in filelist:
        if lang in file.name.lower():
            # read the file path for the matched files
            try:
                df = pd.read_csv(file)
            # one file is a numbers file, so if pandas fails, use that function
            except UnicodeDecodeError: 
                df = load_numbers_file(file)
            # and then break out of the loop 
            break
            
    return df


def change_typo_filenames(data_dir):
    # specify file with the typo
    ibo_typo_file = (
        data_dir
        / "Sentiment"
        / "GPT 4 Turbo"
        / "sentiment-igbo-0-gpt-4-0125-preview-0-2.csv"
    )
    # specify the new file name
    try:
        ibo_typo_file.rename(
            data_dir
            / "Sentiment"
            / "GPT 4 Turbo"
            / "sentiment-ibo-0-gpt-4-0125-preview-0-2.csv"
        )
    except FileNotFoundError:
        pass

    # same here
    hau_typo_file = data_dir / "Sentiment" / "GPT4" / "sentiment-hau-0-gpt-4-0-1.csv"
    try:
        hau_typo_file.rename(
            data_dir / "Sentiment" / "GPT4" / "sentiment-hausa-0-gpt-4-0-1.csv"
        )
    except FileNotFoundError:
        pass

    # and for this one
    eng_typo_files = (
        data_dir / "Discrete_Emotions" / "GPT4" / "emotion-tweets-3-gpt-4-0-1.csv"
    )

    try:
        eng_typo_files.rename(
            data_dir / "Discrete_Emotions" / "GPT4" / "emotion-english-tweets.csv"
        )
    except FileNotFoundError:
        pass

    return None
