import pandas as pd
from pathlib import Path
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


def fix_dummie_columns(df: pd.DataFrame, dummy_cols: list):
    """
    adds a column to the given dataframe which are the annotations based on the
    one-hot columns specified. the function assumes that the list is ordered so the
    labels match the numerical labels (i.e., anger is first bc it is labelled using 1)
    """
    df["annotations"] = pd.from_dummies(df[dummy_cols])

    # make dict used to make the annotations numerical
    label_dict = dict(zip(dummy_cols, range(1, len(dummy_cols) + 1)))

    df = df.replace({"annotations": label_dict})

    return df


def main():
    print("[INFO]: Setting up")
    # get the working directory
    cwd = Path.cwd()

    # create out folder
    out_folder = "clean_data"
    out_dir = cwd / out_folder
    Path(out_dir).mkdir(exist_ok=True)

    # path to OSF data from Rathje et al
    data_dir = cwd / "Datasets_GPT_Output/"

    print("[INFO]: loading and cleaing discrete emotion annotations")
    emo_eng_3, emo_eng_4, emo_eng_4t, emo_ind_3, emo_ind_4 = load_discrete_emotion_dfs(
        data_dir.joinpath("Discrete_Emotions")
    )

    # prep full dfs - rename columns and select only the relevant ones
    full_emo_eng = emo_eng_3.rename({"gpt": "GPT3.5", "Tweet": "tweet"}, axis=1).loc[
        :, ["tweet", "human", "GPT3.5"]
    ]
    full_ind_eng = emo_ind_3.rename({"gpt": "GPT3.5"}, axis=1).loc[
        :, ["tweet", "human", "GPT3.5"]
    ]


if __name__ == "__main__":
    main()
