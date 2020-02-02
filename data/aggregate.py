import pandas as pd

df = pd.read_json('data.json')

output = pd.DataFrame()

for i in range(0, len(df)):
    decade = pd.DataFrame(df.iloc[i]['songs'])
    size = len(decade)

    neg = [None] * size
    neu = [None] * size
    pos = [None] * size
    compound = [None] * size

    for j in range(0, size):
        neg[j] = decade.iloc[j].sentiment['neg']
        neu[j] = decade.iloc[j].sentiment['neu']
        pos[j] = decade.iloc[j].sentiment['pos']
        compound[j] = decade.iloc[j].sentiment['compound']

    decade['sentiment_neg'] = neg
    decade['sentiment_neu'] = neu
    decade['sentiment_pos'] = pos
    decade['sentiment_compound'] = compound

    path = r'year/' + str(df.iloc[i]['year']) + r'.csv'
    decade.to_csv(path)

    output = output.append(decade, ignore_index = True)

output.to_csv('data.csv')


