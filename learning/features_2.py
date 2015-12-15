import pandas as pd

data = pd.DataFrame(pd.read_pickle('../data/movies.pkl'))


def get_person_filmography(pid):
    return [x['title'] for x in data.iterrows() if pid in x['stars']]


if __name__ == "__main__":
    # print get_person_filmography(1682705)
    print pd.rolling_mean(data['rating'])
