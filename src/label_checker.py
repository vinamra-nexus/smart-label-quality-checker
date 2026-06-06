import pandas as pd

def check_label_consistency(df, label_column):
    df_copy = df.copy()

    # Standardized version of labels
    df_copy["standard_label"] = df_copy[label_column].str.strip().str.lower()

    # Rows where original label differs from standard form
    inconsistent = df_copy[
        df_copy[label_column] != df_copy["standard_label"]
    ]

    return inconsistent
    