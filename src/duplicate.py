import pandas as pd

def find_duplicates(df):
    duplicates = df[df.duplicated()]
    return duplicates