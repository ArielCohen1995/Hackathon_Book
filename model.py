import numpy as np
import pandas as pd
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import random


def cleaning():
    #df_books = pd.read_csv('Books2.zip', compression='zip')
    #df_ratings = pd.read_csv('Ratings.csv.zip', compression='zip')
    #df_users = pd.read_csv('Users2.csv')

    #books_data = df_books.merge(df_ratings, on="ISBN")
    #books_data_final = books_data.merge(df_users, on="User-ID")

    #df = books_data_final.copy()
    #df.dropna(inplace=True)
    #df.reset_index(drop=True, inplace=True)

    #df.drop(columns=["Image-URL-S", "Image-URL-L", 'Age'], axis=1, inplace=True)
    #df.drop(index=df[df["Book-Rating"] == 0].index, inplace=True)

    #df.to_csv("df_final.csv")
    df = pd.read_csv('df_final.zip', compression='zip')

    #df["Book-Title"] = df["Book-Title"].apply(lambda x: re.sub("[\W_]+", " ", x).strip())
    return df


def best_books(df, user_id):
    users_fav = df[df["User-ID"] == user_id].sort_values(["Book-Rating"], ascending=False)[0:10]
    return list(users_fav["ISBN"])


def books_return(df, user, user_id):
    x = df[df["User-ID"] == user_id]
    recommend_books = []
    #user = list(user)

    for i in user:
        y = df[(df["User-ID"] == i)]
        books = y.loc[~y["ISBN"].isin(x["ISBN"]), :]
        books = books.sort_values(["Book-Rating"], ascending=False)[0:10]
        recommend_books.extend(books["ISBN"].values)

    return recommend_books[0:10]


def user_basic_reco(df, user_id):
    new_df = df.loc[(df['User-ID'].map(df['User-ID'].value_counts()) > 10)]

    users_pivot = new_df.pivot_table(index=["User-ID"], columns=["ISBN"], values="Book-Rating")
    users_pivot.fillna(0, inplace=True)

    index = np.where(users_pivot.index == user_id)[0][0]
    similarity = cosine_similarity(users_pivot)
    similar_users = list(enumerate(similarity[index]))
    similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)[0:10]

    user_rec = []

    for i in similar_users:
        data = df[df["User-ID"] == users_pivot.index[i[0]]]
        user_rec.extend(list(data.drop_duplicates("User-ID")["User-ID"].values))

    return user_rec


def user_reco_culture(df, user_id):
    culture = df.loc[df["User-ID"] == user_id]['Location'].values[0]
    new_df = df.loc[(df['User-ID'].map(df['User-ID'].value_counts()) > 10)]
    new_df = new_df.loc[new_df['Location'] == culture]
    #if new_df.ISBN.nunique() < 10:
    #    return new_df

    users_pivot = new_df.pivot_table(index=["User-ID"], columns=["ISBN"], values="Book-Rating")
    users_pivot.fillna(0, inplace=True)

    index = np.where(users_pivot.index == user_id)[0][0]
    similarity = cosine_similarity(users_pivot)
    similar_users = list(enumerate(similarity[index]))
    similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)[0:10]

    user_rec = []

    for i in similar_users:
        data = df[df["User-ID"] == users_pivot.index[i[0]]]
        user_rec.extend(list(data.drop_duplicates("User-ID")["User-ID"].values))

    return user_rec


def user_reco_culture_other(df, user_id):
    culture_other = list(set(df.loc[df["User-ID"] != user_id]['Location'].values))
    new_df = df[df['User-ID'].map(df['User-ID'].value_counts()) > 10]
    new_df = new_df.loc[new_df['Location'].isin(culture_other)]

    users_pivot = new_df.pivot_table(index=["User-ID"], columns=["ISBN"], values="Book-Rating")
    users_pivot.fillna(0, inplace=True)

    index = np.where(users_pivot.index == user_id)[0][0]
    similarity = cosine_similarity(users_pivot)
    similar_users = list(enumerate(similarity[index]))
    similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)[0:10]

    user_rec = []

    for i in similar_users:
        data = df[df["User-ID"] == users_pivot.index[i[0]]]
        user_rec.extend(list(data.drop_duplicates("User-ID")["User-ID"].values))

    return user_rec

def main(user_id):
    df = pd.read_csv('df_final.zip', compression='zip')
    best_book = best_books(df, user_id)
    print(best_book)

    users_reco_culture = user_reco_culture(df, user_id)
    books_reco_culture = books_return(df, users_reco_culture, user_id)
    print(books_reco_culture)

    user_reco_culture_others = user_reco_culture_other(df, user_id)
    books_reco_culture_other = books_return(df, user_reco_culture_others, user_id)
    print(books_reco_culture_other)
    return best_book, books_reco_culture, books_reco_culture_other

#if __name__ == '__main__':
#    print(main(177458))

