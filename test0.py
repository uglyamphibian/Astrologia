#%%
from tabulate import tabulate
from functions import *
from pprint import pprint
import re




def decade_span(birth,gender):
    """
    大限
    """
    count ={'金':4,
            '木':3,
            '水':2,
            '火':6,
            '土':5}
    y = count[element_attr(birth)[2]]
    span1 = np.arange(0,120,step=10)+y
    span2 = np.arange(10,130,10)+y-1
    life_loc =[key for key,value in life_profile_loc(birth).items() if re.search(value,'命宮')]
    #, None)
    #next(
    #swap_key_value(life_profile_loc(birth))['*命宮*']
    if gender == re.match('m', re.IGNORECASE):
        a=1
    else:
        a=-1

    print(life_loc)


def annual_span(birth):
    """
    小限
    """
    pass

def flow_span(birth):
    """
    流年
    """
    pass

ex = life_dict['寶壇僧']
Z = combine_star(ex)
decade_span(ex,'m')
#test = flow_table()['壬戌']    
#result = pd.merge(left=Z, right=test, 
# how='left', left_index=True, right_index=True)

