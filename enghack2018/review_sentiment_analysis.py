import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import nltk
from nltk.corpus import stopwords

#import yelp reviews
yelp = pd.read_csv('reviews_and_ids.csv')

#determine data set param
print(yelp.shape)