import pandas as pd

def main():
    cleanJSON('franchises.json', 'games')
    cleanGames()

def cleanJSON(fileName, column):
    df = pd.read_json(fileName)
    df[column] = df[column].str.replace("{", "").str.replace("}", "").str.split(",")
    df[column] = df[column].apply(lambda x: [int(i) for i in x] if x is not None else None)

    df.to_json(f'cleaned_{fileName}', orient='records', indent=2)

def cleanGames():
    df = pd.read_json('games.json')
    df['genres'] = df['genres'].str.replace("{", "").str.replace("}", "").str.split(",")
    df['genres'] = df['genres'].apply(lambda x: [int(i) for i in x] if x is not None else None)

    df['franchises'] = df['franchises'].str.replace("{", "").str.replace("}", "").str.split(",")
    df['franchises'] = df['franchises'].apply(lambda x: [int(i) for i in x] if x is not None else None)

    df.to_json(f'cleaned_games.json', orient='records', indent=2)


if __name__ == "__main__":
    main()






