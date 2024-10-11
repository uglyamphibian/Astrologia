#%%
from tabulate import tabulate
from functions import *
from pprint import pprint
import re




def decade_span(birth,gender):
    """
    大限
    """
    ying_yang = dict(zip(celestial ,[1,-1]*5))
    count ={'金':4,
            '木':3,
            '水':2,
            '火':6,
            '土':5}
    y = count[element_attr(birth)[2]]
    span1 = np.arange(0,120,step=10)+y
    span2 = np.arange(10,130,10)+y-1
    life_span = [str(ii)+'-'+str(jj) for ii,jj in zip(span1,span2)]

    # 起算位置, 先將dict轉為list 並轉為iterator
    start =  next(iter([ii for ii,jj in life_profile_loc(birth).items() if re.search('命',jj)]))
    start_map =  [ii for ii,jj in terr_map.items() if re.search(jj, start)][0]

    if re.search('m',gender,re.I):
        span_order = 1 * ying_yang[birth[0][0]]*np.arange(1,13) + start_map
    else:
        span_order= -1 * ying_yang[birth[0][0]]*np.arange(1,13) +start_map
    decade_fortune = {terr_map[i1%12]:j1  for i1,j1 in zip(span_order, life_span)}

    return decade_fortune




def annual_span(birth, gender):
    """
    小限
    """
    year_terrestrail = birth[0][1]
    annual_key = ['寅','午','戌'] + \
                 ['申','子','辰'] + \
                 ['巳','酉','丑'] + \
                 ['亥','卯','未']
    annual_value  = ['辰']*3 + ['戌']*3 + ['丑']*3+ ['未']*3 
    result = dict(zip(annual_key, annual_value))
    begin_loc = result[year_terrestrail]
    begin_index = terrestrial.index(begin_loc)
    if re.search('m',gender,re.I):
        span_order = 1 *np.arange(1,13) #+ start_map
    else:
        span_order= -1 *np.arange(1,13) #+start_map
    annual_flow = { (jj+begin_index)%13 : terr_map[(jj+begin_index)%12] for jj in span_order }


    return annual_flow


ex = life_dict2['李建佑']
#Z = combine_star(ex)
v = annual_span(ex,'m')
#pprint(v)
print(v)



# def flow_span(year):
#     """
#     流年
#     """
#     pass
#next( (start1[jj] for jj in start1.keys() if re.match(jj,'命')))
#test = flow_table()['壬戌']    
#result = pd.merge(left=Z, right=test, 
# how='left', left_index=True, right_index=True)

