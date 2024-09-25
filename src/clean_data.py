import pandas as pd
from pathlib import Path
import glob
import pathlib


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


def fix_discrete_emotions(data_dir, out_dir) -> None:
    """
    load, clean, and save the files for discrete emotions

    """
    emo_eng_3, emo_eng_4, emo_eng_4t, emo_ind_3, emo_ind_4 = load_discrete_emotion_dfs(
        data_dir
    )

    # clean datasets with dummy columns
    emo_eng_4 = fix_dummy_columns(emo_eng_4, ["anger", "joy", "sadness", "optimism"])
    emo_ind_4 = fix_dummy_columns(
        emo_ind_4, ["anger", "fear", "sadness", "love", "joy"]
    )

    # getting the full dfs and saving them
    full_emo_eng = create_full_discrete_emo_df(emo_eng_3, emo_eng_4, emo_eng_4t)
    full_emo_ind = create_full_discrete_emo_df(emo_ind_3, emo_ind_4)

    full_emo_eng.to_csv(out_dir / "emotion_twitter_english.csv", index=False)
    full_emo_ind.to_csv(out_dir / "emotion_twitter_indonesian.csv", index=False)

    return None


def fix_moral_foundations(data_dir, out_dir) -> None:
    # setting path and getting filenames
    files = data_dir.glob("**/MFRC*")

    for i, file in enumerate(files):
        # read file
        df = pd.read_csv(file)

        # get the name of the GPT annotation in this file
        annotation = file.name.split("-")[1].capitalize()

        # from the first file we get the text and the human annotations
        if i == 0:
            full_moral_df = df.loc[:, "text":"is_moral"]

        # if preview is in the file name, then it's GPT4-Turbo
        if "preview" in file.name:
            col_name = f"GPT4-Turbo_{annotation}"
        # else it's GPT4
        else:
            col_name = f"GPT4_{annotation}"

        # use col_name to save column that starts with 'question' -> that's the GPT annotation
        full_moral_df[col_name] = df.filter(regex="^question")

    # save the full df
    full_moral_df.to_csv(out_dir / "moral-foundations_reddit_english.csv", index=False)

    return None


def main():
    print("[INFO]: Setting up")
    # get the working directory
    cwd = Path.cwd()

    # create out folder
    out_folder = "clean_data/"
    out_dir = cwd / out_folder
    Path(out_dir).mkdir(exist_ok=True)

    # path to OSF data from Rathje et al
    data_dir = cwd / "Datasets_GPT_Output/"

    print("[INFO]: loading, cleaing, and saving discrete emotion annotations")
    fix_discrete_emotions(data_dir / "Discrete_Emotions", out_dir)

    print("[INFO]: loading, cleaning, and saving moral foundations")
    fix_moral_foundations(data_dir / "Moral Foundations", out_dir)

    print("[INFO]: loading, cleaning, and saving news headlines")
    news_data_dir = data_dir / "News_headlines"

    gpt3_news = pd.read_csv(news_data_dir / "GPT3.5" / "NewsHeadlinesOutput.csv")
    gpt4t_news = pd.read_csv(news_data_dir / "GPT4 Turbo" / "dataNHBTurboOutput.csv")

    news_full = gpt3_news.rename(
        {
            "headlines.headline": "text",
            "gptsentiment": "GPT3.5_Sentiment",
            "gptanger": "GPT3.5_Anger",
            "gptjoy": "GPT3.5_Joy",
            "gptsadness": "GPT3.5_Sadness",
            "gptfear": "GPT3.5_Fear",
        },
        axis=1,
    )

    gpt4t_news = gpt4t_news.rename(
        {
            "gptsentimentTurbo": "GPT4-Turbo_Sentiment",
            "gptangerTurbo": "GPT4-Turbo_Anger",
            "gptjoyTurbo": "GPT4-Turbo_Joy",
            "gptsadnessTurbo": "GPT4-Turbo_Sadness",
            "gptfearTurbo": "GPT4-Turbo_Fear",
        },
        axis=1,
    ).drop(["gptsentiment", "ggptjoyTurbo"], axis=1)

    for file in news_data_dir.glob("GPT4/*.csv"):
        df = pd.read_csv(file)
        if "sentiment" in file.name:
            news_full["GPT4_Sentiment"] = df["sentiment"]
        else:
            emotion = file.name.split("-")[3]
            col_name = f"GPT4_{emotion.capitalize()}"
            news_full[col_name] = df[emotion]

    news_full = pd.concat(
        [news_full, gpt4t_news.loc[:, "GPT4-Turbo_Sentiment":]], axis=1
    )
    news_full.to_csv(out_dir / "emotion-sentiment_news_english.csv", index=False)


if __name__ == "__main__":
    main()
