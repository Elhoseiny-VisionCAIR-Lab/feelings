import pandas as pd
import numpy as np
import re, string
import numpy as np



#https://stackoverflow.com/questions/54028199/are-for-loops-in-pandas-really-bad-when-should-i-care
#https://stackoverflow.com/questions/11350770/select-by-partial-string-from-a-pandas-dataframe
#https://stackoverflow.com/questions/3041320/regex-and-operator
#https://stackoverflow.com/questions/17972938/check-if-string-in-pandas-dataframe-column-is-in-list
#https://cmdlinetips.com/2018/02/how-to-subset-pandas-dataframe-based-on-values-of-a-column/








regex = re.compile('[%s]' % re.escape(string.punctuation))

prefix = 'https://s3-us-west-1.amazonaws.com/fairgames/resources/images/wiki-art/original/square-not-padded-600-pixels/'

def image_link(df):


    def f(df):
        return osp.join(prefix, df['genre'], df['painting']+".jpg")

    df['painting'] = df.apply(f, axis=1)


    # d =  {'links': pd.Series(df['painting'])}
    # return pd.DataFrame(d).to_json()

    for x in df['painting']:
        print(x)

    return pd.Series(df['painting']).to_json()

def data_pre_process(df):

    """
    :param df: Converts dataset into DF
    :return: string column in DF has all punctuation and uppercasses removed
    """

    df['utterance'] = df['utterance'].apply(lambda x: (regex.sub('', x).lower().split()))

    return df




def subset_search(words,df,feeling):

    """
    :param words: User Query
    :param df: pre - processed datafram
    :return: returns all proper subset of the user query against dataset strings
    """

    def try_search(words,x):
        return set(words) <= set(x)

    filter = df[[try_search(words, x) for x in df['utterance']]]

    if not feeling:
        return filter

    # means that feeling has been also included, filter based on that
    return  filter[filter['feeling']==feeling]




if __name__ == '__main__':

    df = pd.read_csv('demo.csv')

    df = data_pre_process(df)

    words = ['the','painting']
    feeling= 'fear'
    filter = subset_search(words,df,feeling)
    print(image_link(filter))


    # print(len(filter['utterance']))
    # print(filter['utterance'])



