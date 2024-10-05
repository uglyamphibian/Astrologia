from info import *
import numpy as np

"""
各函式說明
1.reorder_dict:
2.life_table:
3.life_profile_loc
4.element_attr
5.polar_loc
6.permute_star
7.add_level
8.combine_star
9.set_day_stars(birth)
10.choose_minor
11.add_prop_lv
12.swap_key_value
13.dct_to_df
14.permute_minor

"""


def reorder_dict(dct):
    """
    依據地支順序排列
    """
    new_dict={k:dct[k] for k in terrestrial}
    return new_dict

# life_ex and life_post  (決定命身宮位置)
def life_table():
    life_ex_table =[]
    life_post_table =[]
    for jj in range(12):
        life_ex =  [terrestrial[ii%12] for ii in range(2-jj,12+2-jj)]
        life_post =  [terrestrial[ii%12] for ii in range(2+jj,12+2+jj)]
        life_ex_table.append(life_ex)
        life_post_table.append(life_post)
    life_ex_table = pd.DataFrame(data = life_ex_table, 
                             columns=np.arange(1,13)).T
    life_post_table = pd.DataFrame(data = life_post_table, 
                               columns = np.arange(1,13)).T

    life_ex_table.columns = terrestrial
    life_post_table.columns = terrestrial
    return life_ex_table, life_post_table


ming, shen = life_table()


def life_profile_loc(birth):
    """
    決定命宮身宮位置
    """
    life_dict = dict()
    mon, hour = birth[1], birth[3]
    ming_loc, shen_loc = ming.loc[mon,hour], shen.loc[mon,hour]
    id1 = terrestrial.index(ming_loc)
    id2 = terrestrial.index(shen_loc)
    for ii in range(12):
        if (ii+id1)%12 == id2:
            life_dict[terr_map[(ii+id1)%12]] =life_profile[ii]+'/身宮'
        else:
            life_dict[terr_map[(ii+id1)%12]] =life_profile[ii]
    life_dict = reorder_dict(life_dict)
    return life_dict

def element_attr(birth):
    """
    決定納音屬性
    """
    Year, mon, hour = birth[0][0], birth[1], birth[3]
    ming_loc = ming.loc[mon,hour]
    celestial = tiger5.loc[ming_loc,Year]
    #print(celestial) 
    element_loc = celestial+ ming_loc 
    element =  sonus[sonus.index.str.contains(element_loc)].iloc[0]
    # print(element)
    return element

def polar_loc(birth):
    """
    尋找紫微位置, 
    並且根據生年列出祿權科忌
    """
    year = birth[0][0]
    day = birth[2]
    attrib = element_attr(birth)[2]
    loc = pole_star_map.loc[day,attrib]
    statement = '紫微在{a}'.format(a=loc)
    print(statement)
    life_prop = dict(zip(prop.loc[year,:], prop.columns))
    return loc, life_prop


def permute_star(birth):
    """
    紫微主星定盤
    """
    star_loc_all = {} # 輸出變數
    #紫微主星位置, 並列出祿權科忌
    a, life_prop = polar_loc(birth)
    loc_num = next((key for key,value in terr_map.items() if value==a)) 
    clock_star = ['紫微','天機','太陽','武曲','天同','廉貞']
    c1, c2 = [], []
    cclock_star =['天府','太陰','貪狼','巨門','天相','天梁','七殺','破軍']

    c1 = [jj+life_prop[jj] if jj in life_prop.keys() else jj for jj in clock_star]
    c2 = [jj+life_prop[jj] if jj in life_prop.keys() else jj for jj in cclock_star]
    # 給定排盤規則排序
    c_index  = [0,11,9,8,7,4]
    cc_index = [4,5,6,7,8,9,10,2]

    clock_index = [terr_map[(jj+loc_num)%12] for jj in c_index]
    cclock_index= [terr_map[(jj-loc_num)%12] for jj in cc_index]
    clock_dct = dict(zip(clock_index,c1))
    cclock_dct = dict(zip(cclock_index,c2))
    return clock_dct, cclock_dct

def add_level(dct): 
    """
    根據諸星位置定星等
    clockwise : 順行主星
    counter_clockwise: 逆行主星
    """
    star_dict ={key:value+star_level.loc[key,value[0:2]] for key,value in dct.items()}
    return star_dict 

 
def combine_star(birth):
    df0 = pd.DataFrame.from_dict(life_profile_loc(birth), orient='index').rename(columns={0:'宮位'})
    c_star, cc_star = permute_star(birth)
    c_star,cc_star  = add_level(c_star),add_level(cc_star)
    total=dict()
    for jj in set(c_star)|set(cc_star):
        if jj in c_star and jj in cc_star:
            total[jj] = [c_star[jj], cc_star[jj]]
        elif jj in c_star:
            total[jj] = c_star[jj]
        else:
            total[jj] = cc_star[jj]
    df1 = pd.Series(total); 
    df1.name  = '主星'
    df = pd.merge(left=df0, right=df1, how='left', left_index=True, right_index=True).fillna(' ')
    return df



#昌曲左右魁鉞
# 三台八座/恩光天貴
def set_day_stars(birth):
    """
    三台八座/恩光天貴
    """ 
    day =birth[2]
    dct_0 ={'月':['左輔','右弼'],'時':['文昌','文曲']}
    dct_1  ={'左輔':'三台', '右弼':'八座', 
             '文昌':'恩光', '文曲':'天貴'}
    ref_power = [0,1,0,0]  # 決定順行逆行
    ref_adj = [1,1,2,2]    # 退數步數
    loc = choose_minor(birth,dct_0)
    ref_loc = swap_key_value(terr_map)
    new_dict={} 
    for  num,key in enumerate(dct_1.keys()):
        new_x = (ref_loc[loc[key]]+ (day-ref_adj[num])*(-1)**(ref_power[num]) )%12
        x =  terr_map[new_x]
        new_dict[dct_1[key]] = x
    return new_dict


# 合併年干,年支,月, 時星系
def choose_minor(birth, dct):
    """
    根據生辰與各類星表篩選dct中的星等
    """
    export_dict = dict()
    year_c,year_t,month,hour= birth[0][0],birth[0][1], \
                              str(birth[1]), birth[3]
    for key,value in dct.items():
        # convert string to list
        if not isinstance(value, list):
            value=[value]
        #根據不同準則
        if key =='年干':
            v =minor_star.loc[value, year_c].to_dict()
        elif key =='年支':
            v =minor_star.loc[value, year_t].to_dict()
        elif key =='月':
            v =minor_star.loc[value, month].to_dict()
        else:
            v=minor_star.loc[value, hour].to_dict()
        export_dict ={**export_dict,**v}
    return export_dict

def add_prop_lv(birth,dct):
    """
    針對非主星dict補上星等及四化
    """
    new_dict ={}
    lv_set ={'祿存','文昌','文曲','火星','鈴星','擎羊','陀螺'}
    c_year = birth[0][0]
    prop_dct = swap_key_value(prop.loc[c_year,:].to_dict())
    for key,value in dct.items():
        #補上四化
        if key in prop_dct:
            new_key = key + prop_dct[key]
        else:
            new_key = key 

        #補上星等    
        if key in lv_set:
            new_key = new_key + star_level.loc[value,key]
        new_dict[new_key] = value
    return  new_dict

def swap_key_value(dct):
    result = dict()
    for key,value in dct.items():
        if value in result:
            if not isinstance(result[value], list):
                result[value] = [result[value]]
            result[value].append(key)
        else:
            result[value] = key
    return result

def dct_to_df(dct, name):
    """
    convert dct to pd.series  with name
    """
    df0 = pd.DataFrame(index=terrestrial)
    df1 = pd.Series(dct)
    df1.name= name
    df = pd.merge(left=df0, right=df1, how='left',
                  left_index=True,right_index=True).fillna(' ')
    return df


def permute_minor(birth,star_dct,name):
    """
    根據生日以及選擇的星名進行排盤
    """
    dct = choose_minor(birth, star_dct)
    new_dct = add_prop_lv(birth,dct)
    dct_swap = swap_key_value(new_dct)
    df = dct_to_df(dct_swap,name)
    return df

 
# 長生12用神煞
def life_cycle(birth, gender='M'):
    cycle=['長生','沐浴','冠帶','臨官','帝旺',
           '衰','病','死','墓','絕','胎','養']
    #尋找屬性
    attr = element_attr(birth)[2]

    #依據屬性及男女排盤
    set_initial ={'金':'巳','木':'亥',
                  '水':'申','火':'寅','土':'申'}
    initial = terrestrial.index(set_initial[attr])
    terr_new = terrestrial*2
    if gender =='M':
        life_map = terr_new[initial-1:initial+11]
    else:
        life_map = terr_new[initial+1:initial+13]
        life_map = [jj for jj in reversed(life_map)]
        
    life_dict = dict(zip(life_map,cycle))
    return life_dict


def empty_star(birth):
    sonus_list = list(sonus.keys())
    empty_dict={}
    year_full = birth[0]
    empty_loc = []
    for ii in sonus_list:
        list_tmp = [ii[0:2],ii[2:]]
        empty_loc.extend(list_tmp)
    np_empty = np.array(empty_loc).reshape(6,10)
    empty_value = ['戌亥','申酉','午未','辰巳','寅卯','子丑']
    v = np.where(np_empty==year_full)[0][0]
    loc = empty_value[v]
    empty_dict['旬中'], empty_dict['空亡'] = loc[0], loc[1]
    return empty_dict


#  流年組合
def flow_fortune(year):
    """
    year 為六十甲子
    """
    c_flow_star = dict(c_flow[year[0]])
    t_flow_star = dict(t_flow[year[1]])
    flow_stars= dict(**c_flow_star,**t_flow_star)
    flow_stars= pd.Series(swap_key_value(flow_stars))
    flow_stars.name = year
    return flow_stars

    

def flow_table():
    """
    流星組合
    """
    sonus_list = list(sonus.keys())
    df0 = pd.DataFrame(index=terrestrial)
    for ii in sonus_list:
        df_tmp = pd.concat([flow_fortune(ii[0:2]),flow_fortune(ii[2:])], 
                        axis=1,join='outer',ignore_index=False)
        df0= pd.concat([df0,df_tmp], axis=1, join='outer',ignore_index=False).fillna(' ') 
    return df0 
    
dff= flow_table()