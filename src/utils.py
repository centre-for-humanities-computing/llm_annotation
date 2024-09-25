import pandas as pd

from pathlib import Path
import re


def load_discrete_emotion_dfs(data_dir):
    # english files
    emo_eng_3 = pd.read_csv(
        Path(data_dir / "GPT3.5" / "emotion-class-english-3.5_temp=0.csv")
    )
    emo_eng_4 = pd.read_csv(Path(data_dir / "GPT4" / "emotion-tweets-3-gpt-4-0-1.csv"))
    emo_eng_4t = pd.read_csv(
        Path(
            data_dir / "GPT4 Turbo" / "emotion-english-0-gpt-4-0125-preview-0-1 (4).csv"
        )
    )

    # indonesian
    emo_ind_3 = pd.read_csv(
        Path(data_dir / "GPT3.5" / "emotion-class-Indonesian-GPT-temp=0.csv")
    )

    emo_ind_4 = pd.read_csv(
        Path(data_dir / "GPT4" / "emotion-indonesian-0-gpt-4-0-1.csv")
    )

    return emo_eng_3, emo_eng_4, emo_eng_4t, emo_ind_3, emo_ind_4


def fix_dummy_columns(df: pd.DataFrame, dummy_cols: list):
    """
    adds a column to the given dataframe which are the annotations based on the
    one-hot columns specified.
    the function assumes that the list is ordered so the labels' indexes
    match the numerical labels (i.e., anger is first bc it is labelled using 1)
    """
    df["annotations"] = pd.from_dummies(df[dummy_cols])

    # make dict used to make the annotations numerical
    label_dict = dict(zip(dummy_cols, range(1, len(dummy_cols) + 1)))

    df = df.replace({"annotations": label_dict})

    return df


def create_full_discrete_emo_df(df1, df2, df3=None):
    """
    takes the discrete emotion dataframes and gives them consistent columns names and formatting
    """
    # rename columns and select only the relevant ones
    full_df = df1.rename({"gpt": "GPT3.5", "Tweet": "tweet"}, axis=1).loc[
        :, ["tweet", "human", "GPT3.5"]
    ]

    full_df["GPT4"] = df2["annotations"]

    # because indonesian only has two dataframes
    if df3 is not None:
        full_df["GPT4-Turbo"] = df3["gpt4"]

    return full_df


def change_news_colnames(df: pd.DataFrame, model: str):
    # find column names that contain annotations
    annotation_columns = [col for col in df.columns if col.startswith("gpt")]

    # create a list of new column names comprised of the model name and the annotated emotion
    # (the regex finds the emotion from the old column name and then it is capitalized)
    new_col_names = [
        f"{model}_{re.match(pattern='gpt(.*?)(Turbo)?$', string=col).group(1).capitalize()}"
        for col in annotation_columns
    ]

    # create a dict for renaming the columns
    rename_dict = dict(zip(annotation_columns, new_col_names))

    # do the renaming
    df = df.rename(rename_dict, axis=1)

    return df


def create_off_df(df1, df2, df3):
    ful_df = df1.loc[:, "tweet":]
    ful_df = ful_df.rename({"gpt": "GPT3.5"}, axis=1)

    ful_df["GPT4"] = df2["offensive"].astype(int)
    ful_df["GPT4-Turbo"] = df3["gpt4"].astype(int)

    return ful_df
