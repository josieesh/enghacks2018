import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import nltk
from nltk.corpus import stopwords

#import yelp reviews
yelp = pd.read_csv('reviews_and_ids.csv')

#add text length column
yelp['text length'] = yelp['review'].apply(len)
yelp.head()

#visualize to explore correlation between length of review and rating
g = sns.FacetGrid(data=yelp, col='rating')
g.map(plt.hist, 'text length', bins=50)
