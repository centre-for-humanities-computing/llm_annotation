import pandas as pd

from pathlib import Path

from utils import *


def fix_discrete_emotions(data_dir, out_dir) -> None:
    """
    load, clean, and save the files for discrete emotions

    """
    gpt3_files = list(data_dir.joinpath("GPT3.5/").iterdir())
    gpt4_files = list(data_dir.joinpath("GPT4/").iterdir())
    gpt4t_files = list(data_dir.joinpath("GPT4 Turbo/").iterdir())

    for lang in ["english", "indonesian"]:
        # find the three files for each language
        gpt3_df = load_lang_csv_from_list(lang, gpt3_files)
        gpt4_df = load_lang_csv_from_list(lang, gpt4_files)
        gpt4t_df = load_lang_csv_from_list(lang, gpt4t_files)

        # some gpt4 files have dummy columns instead of a gpt4 one, fix that
        if lang == "indonesian":
            gpt4_df = fix_dummy_columns(
                gpt4_df, ["anger", "fear", "sadness", "love", "joy"], "gpt4"
            )
        if lang == "english":
            gpt4_df = fix_dummy_columns(
                gpt4_df, ["anger", "joy", "sadness", "optimism"], "gpt4"
            )
        full_df = make_clean_df(gpt3_df, gpt4_df, gpt4t_df)

        # save the file
        full_df.to_csv(out_dir / f"emotion_twitter_{lang}.csv", index=False)

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
    # get file names

    gpt3_files = list(data_dir.joinpath("GPT3.5/").iterdir())
    gpt4_files = list(data_dir.joinpath("GPT4/").iterdir())
    gpt4t_files = list(data_dir.joinpath("GPT4 Turbo/").iterdir())
    
    for lang in ['english', 'turkish']:
        gpt3_df = load_lang_csv_from_list(lang, gpt3_files)
        gpt4_df = load_lang_csv_from_list(lang, gpt4_files)
        gpt4t_df = load_lang_csv_from_list(lang, gpt4t_files)

        # make the file consistent with others
        full_df = make_clean_df(gpt3_df, gpt4_df, gpt4t_df)

        # save
        full_df.to_csv(out_dir / f"offensive_twitter_{lang}.csv", index=False)

    return None

def fix_sentiment_multiling(data_dir, out_dir) -> None:
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
    out_folder = "new_clean_data/"
    out_dir = cwd / out_folder
    Path(out_dir).mkdir(exist_ok=True)

    # path to OSF data from Rathje et al
    data_dir = cwd / "Datasets_GPT_Output/"

    # fixing some file names
    change_typo_filenames(data_dir)

    # let's fix the files
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
