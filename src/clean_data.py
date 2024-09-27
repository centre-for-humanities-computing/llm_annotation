import pandas as pd

from pathlib import Path

from utils import *


def fix_discrete_emotions(data_dir, out_dir) -> None:
    """
    load, clean, and save the files for discrete emotions

    """
    emo_eng_3, emo_eng_4, emo_eng_4t, emo_ind_3, emo_ind_4 = load_discrete_emotion_dfs(
        data_dir
    )
    # clean datasets with dummy columns
    emo_eng_4 = fix_dummy_columns(
        emo_eng_4, ["anger", "joy", "sadness", "optimism"], "gpt4"
    )
    emo_ind_4 = fix_dummy_columns(
        emo_ind_4, ["anger", "fear", "sadness", "love", "joy"], "gpt4"
    )

    # getting the full dfs and saving them
    full_emo_eng = make_clean_df(emo_eng_3, emo_eng_4, emo_eng_4t)
    full_emo_ind = make_clean_df(emo_ind_3, emo_ind_4)

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
        moral_name = file.name.split("-")[1].capitalize()

        # from the first file we get the text and the human annotations
        if i == 0:
            full_moral_df = df.loc[:, "text":"is_moral"]

        # if preview is in the file name, then it's GPT4-Turbo
        if "preview" in file.name:
            col_name = f"GPT4-Turbo_{moral_name}"
        # else it's GPT4
        else:
            col_name = f"GPT4_{moral_name}"

        # use col_name to save column that starts with 'question' -> that's the GPT annotation
        full_moral_df[col_name] = df.filter(regex="^question")

    # save the full df
    full_moral_df.to_csv(out_dir / "moral-foundations_reddit_english.csv", index=False)

    return None


def fix_news_headlines(data_dir, out_dir) -> None:
    # load gpt 3.5 and gpt 4 -> they only have 1 file
    gpt3_news = pd.read_csv(data_dir / "GPT3.5" / "NewsHeadlinesOutput.csv")
    gpt4t_news = pd.read_csv(data_dir / "GPT4 Turbo" / "dataNHBTurboOutput.csv")

    # drop redundant columns in gpt4-turbo data
    gpt4t_news = gpt4t_news.drop(["gptsentiment", "ggptjoyTurbo"], axis=1)

    # change the column names
    gpt3_news = change_news_colnames(gpt3_news, "GPT3.5")
    gpt4t_news = change_news_colnames(gpt4t_news, "GPT4-Turbo")

    # make the text column name make sense and create full df
    news_full = gpt3_news.rename({"headlines.headline": "text"}, axis=1)

    # fix gpt 4 files - read each file in GPT 4 folder, find the annotation column, add it to full df with proper name
    for file in data_dir.glob("GPT4/*.csv"):
        df = pd.read_csv(file)
        if "sentiment" in file.name:
            news_full["GPT4_Sentiment"] = df["sentiment"]
        else:
            # use file name to figure out which emotion is annotated
            emotion = file.name.split("-")[3]
            col_name = f"GPT4_{emotion.capitalize()}"
            # save the annotation column in full df
            news_full[col_name] = df[emotion]

    # add gpt4-turbo annotations to full data
    news_full = pd.concat(
        [news_full, gpt4t_news.loc[:, "GPT4-Turbo_Sentiment":]], axis=1
    )

    # save the data
    news_full.to_csv(out_dir / "emotion-sentiment_news_english.csv", index=False)

    return None


def fix_offensiveness(data_dir, out_dir) -> None:
    # read_files
    off_3_eng = pd.read_csv(data_dir / "GPT3.5" / "EnglishOffensiveOutput.csv")
    off_4_eng = pd.read_csv(data_dir / "GPT4" / "offensive-english-0-gpt-4-0-1.csv")
    off_4t_eng = pd.read_csv(
        data_dir / "GPT4 Turbo" / "offensive-english-0-gpt-4-0125-preview-0-1.csv"
    )
    off_3_tur = pd.read_csv(data_dir / "GPT3.5" / "offenseval-Turkish-GPT.csv")
    off_4_tur = pd.read_csv(data_dir / "GPT4" / "offensive-turkish-0-gpt-4-0-1.csv")
    off_4t_tur = pd.read_csv(
        data_dir / "GPT4 Turbo" / "offensive-turkish-0-gpt-4-0125-preview-0-1.csv",
        sep=";",
    )

    # concat the df's and fix column names
    full_off_eng = make_clean_df(off_3_eng, off_4_eng, off_4t_eng)
    full_off_tur = make_clean_df(off_3_tur, off_4_tur, off_4t_tur)

    # save the data
    full_off_eng.to_csv(out_dir / "offensive_twitter_english.csv", index=False)
    full_off_tur.to_csv(out_dir / "offensive_twitter_turkish.csv", index=False)

    return None


def fix_sentiment_multiling(data_dir, out_dir) -> None:
    change_typo_filenames(data_dir)

    gpt3_sentfiles = list(data_dir.joinpath("GPT3.5/").iterdir())
    gpt4_sentfiles = list(data_dir.joinpath("GPT4/").iterdir())
    gpt4t_sentfiles = list(data_dir.joinpath("GPT 4 Turbo/").iterdir())

    languages = {
        "amharic",
        "arabic",
        "english",
        "hausa",
        "ibo",
        "kinyarwanda",
        "swahili",
        "tsonga",
        "twi",
        "yoruba",
    }

    for lang in languages:
        # find the three files for each language
        gpt3_df = load_lang_csv_from_list(lang, gpt3_sentfiles)
        gpt4_df = load_lang_csv_from_list(lang, gpt4_sentfiles)
        gpt4t_df = load_lang_csv_from_list(lang, gpt4t_sentfiles)

        # some gpt4 files have dummy columns instead of a gpt4 one, fix that
        if "gpt4" not in gpt4_df.columns:
            gpt4_df = fix_dummy_columns(
                gpt4_df, ["positive", "neutral", "negative"], "gpt4"
            )

        full_df = make_clean_df(gpt3_df, gpt4_df, gpt4t_df)

        # save the file
        full_df.to_csv(out_dir / f"sentiment_twitter_{lang}.csv", index=False)

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
    fix_news_headlines(data_dir / "News_headlines", out_dir)

    print("[INFO]: loading, cleaning, and saving offensiveness data")
    fix_offensiveness(data_dir / "Offensiveness", out_dir)

    print("[INFO]: loading, cleaning, and saving multilingual sentiment annotations")
    fix_sentiment_multiling(data_dir / "Sentiment", out_dir)

    print("[INFO]: Done :)")


if __name__ == "__main__":
    main()
