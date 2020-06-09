# Unit testing for modeling
import logging
import sys

sys.path.append('../')
from src import recommend_dogs

def test_modeling():
    for i in [5,10,20,30]:
        recommendations = recommend_dogs.recommend_dogs(i)
        assert abs(len(recommendations) - i) <= (i/5) + 3
        logging.info('Tests passed!')

if __name__=="__main__":
    test_modeling()