import pandas as pd

df = pd.read_csv('/Users/rahmad/work/freelance-new/restbot/db/word_changes.csv')

text = "halo tolong rekomendasi restoran yang ada parkiran"

# run word by word inside text and replace with word_changes.csv
for word in text.split():
    try:
        text = text.replace(word, df.loc[df['word'] == word, 'changes_word'].iloc[0])
    except:
        pass

print(text)