
import pandas as pd
from app import app
from models import db, Translation, zimbabwe_now



# Read dataset
df = pd.read_excel('dataset.xlsx')  # use pd.read_csv() if CSV

# Make sure columns are: english_sentence, shona_subtitle, shona_translation, ndebele_subtitle, ndebele_translation
required_columns = [
    "English Sentence",
    "Shona Subtitle",
    "Shona Translation",
    "Ndebele Subtitle",
    "Ndebele Translation",
]

if not all(col in df.columns for col in required_columns):
    raise ValueError(f"Dataset must contain columns: {required_columns}")

# Populate the DB
with app.app_context():
    for _, row in df.iterrows():
        translation = Translation(
            english_sentence=row["English Sentence"],
            shona_subtitle=row["Shona Subtitle"],
            shona_translation=row["Shona Translation"],
            ndebele_subtitle=row["Ndebele Subtitle"],
            ndebele_translation=row["Ndebele Translation"],
            created_at=zimbabwe_now(),
        )
        db.session.add(translation)

    db.session.commit()
    print(f"Inserted {len(df)} rows into Translation table.")
