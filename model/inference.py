import pandas as pd
import numpy as np
import re, string
import numpy as np
import pandas as pd
import os.path as osp



class MyModel:

    def __init__(self):
        self.df = pd.read_csv('model/demo.csv')
        self.regex = re.compile('[%s]' % re.escape(string.punctuation))
        self.prefix = 'https://s3-us-west-1.amazonaws.com/fairgames/resources/images/wiki-art/original/square-not-padded-600-pixels/'
        self._initialize()

    def _initialize(self):
        #pre-process data
        self.df['utterance'] = self.df['utterance'].apply(lambda x: (self.regex.sub('', x).lower().split()))
        # self.df =  self.df['utterance'].apply(lambda x: (self.regex.sub('', x).lower().split()))
        # return self.df

    def update_df(self,df):
        self.df = df


    def subset_search(self,words,feeling):

        """

        :param words: list format
        :param feeling: (OPTIONAL) as a STRING
        :return: JSON Format links
        """

        def try_search(words, x):
            return set(words) <= set(x)

        filter = self.df[[try_search(words, x) for x in self.df['utterance']]]

        #if no feeling is supplied with request
        if not feeling:
            return self.filter_df(filter), filter['utterance']

        #filtering dataframe by the feeling
        filter = filter[filter['feeling']==feeling]

        if len(filter) == 0:
            return None,None


        return self.filter_df(filter), filter['utterance']


    def filter_df(self,df):

        """
        :param df: filtered Datafram
        :return: All filtered links in JSON format
        """

        def f(df):
            return osp.join(self.prefix, df['genre'], df['painting'] + ".jpg")

        df['painting'] = df.apply(f, axis=1)

        return df

