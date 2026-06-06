from sklearn.ensemble import IsolationForest
from sentence_transformers import SentenceTransformer
import numpy as np

model_embed = SentenceTransformer('all-MiniLM-L6-v2')

def detect_outliers(df, text_column):
    texts = df[text_column].astype(str).tolist()

    # Convert text → numbers (VERY IMPORTANT STEP)
    embeddings = model_embed.encode(texts)

    # ML model works on numbers now
    model = IsolationForest(contamination=0.1, random_state=42)
    preds = model.fit_predict(embeddings)

    df['outlier'] = preds

    return df[df['outlier'] == -1]