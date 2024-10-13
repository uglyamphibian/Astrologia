
from info import *
from functions import *
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
    
    # 先確認屬性(五行)
    y = count[element_attr(birth)[2]]
    span1 = np.arange(0,120,step=10)+y

    #span2 = np.arange(10,130,10)+y-1
    #life_span = [str(ii)+'-'+str(jj) for ii,jj in zip(span1,span2)]
    life_span = span1

    # 起算位置, 先將dict轉為list 並轉為iterator, 找命宮
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
    大小限
    """
    year_terrestrail = birth[0][1]
    #print(year_terrestrail)
    annual_key = ['寅','午','戌'] + \
                 ['申','子','辰'] + \
                 ['巳','酉','丑'] + \
                 ['亥','卯','未']
    annual_value  = ['辰']*3 + ['戌']*3 + ['未']*3+ ['丑']*3 
    result = dict(zip(annual_key, annual_value))
    begin_loc = result[year_terrestrail]
    #print('小限起運在{a}'.format(a = begin_loc))

    begin_index = terrestrial.index(begin_loc)
    if re.search('m',gender,re.I):
         span_order = 1 *np.arange(1,13) #+ start_map
    else:
         span_order= -1 *np.arange(1,13) #+start_map
    annual_flow = { ((jj)%12+1) : terr_map[(jj+begin_index)%12] for jj in span_order }  
    return annual_flow

def convert_age_year(birth,age):
    """
    根據生辰與年紀推算流年
    """
    birth_year = birth[0]
    chinese_year = list(flow_table().columns)
    start_year  = chinese_year.index(birth_year)
    flow_year = (start_year+age-1)%60
    output = chinese_year[flow_year]
    return output



def flow_fortune(t_year):
    lee = ['太歲','太陽','喪門','太陰','官符','死符','歲破',
           '龍德','白虎','福德','弔客','病符']
    start = terrestrial.index(t_year)

    result = {terrestrial[(start+ii)%12]: lee[ii] for ii in range(12)}
    result = pd.Series(result); 
    result.name = '四利八凶'
    return result



def combine_flow(birth, gender,age):
    # 合併流星, 大小限, 
    df0 = pd.Series(life_profile_loc(birth))
    df0.name ='宮位'

    #大限
    df1 = pd.Series(decade_span(birth, gender))
    bool_decade = df1 < age
    decade_loc = df1[bool_decade].sort_values(ascending=True).index[-1]

    # 小限
    annual_dct = annual_span(birth, gender)
    if age%12==0:
         age_loc = 12
    else:
         age_loc = age%12
    annual_flow_loc = annual_dct[age_loc]

    #合併大小限位置
    anf = pd.Series(dict(zip(terrestrial, [' ']*12)))
    anf.name = '大小限'
    #print(annual_flow_loc)
    flow_year = convert_age_year(birth,age)
    print('流年在{ans}'.format(ans=flow_year[1]))
    flow_stars = flow_table()[flow_year]
    anf.loc[decade_loc] = '大'
    anf.loc[annual_flow_loc] = '小'
    anf.loc[flow_year[1]] = '流'


    # 災星
    jinx = {'年干':['擎羊','陀羅','截空'], '年支':['火星','鈴星'], '時':['天空','地劫']}
    star_jinx = permute_minor(birth, jinx, name='災星')


    flow_fortune2 = flow_fortune(flow_year[1])


    df = pd.concat([df0, anf, flow_fortune2 ,flow_stars,star_jinx], join='inner', 
                   axis=1, ignore_index=False)
    return df

