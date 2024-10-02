#%%
import datetime as dt
import numpy as np
import pandas as pd
import re
from pprint import pprint

# 古命例
life_example = pd.read_excel('basic/example.xlsx', sheet_name='全書',
                             nrows=113, usecols='A:F', index_col='姓名')
life_dict = dict()
for jj in life_example.index:
     life_dict[jj] = life_example.loc[jj].to_list()



#% Basic Information
celestial = ['甲','乙','丙','丁','戊',
             '己','庚','辛','壬','癸']
terrestrial =['子','丑','寅','卯',
              '辰','巳','午','未',
              '申','酉','戌','亥']

terr_map = dict(zip(range(12), terrestrial))



prop =  pd.read_csv('basic/property.csv', index_col='天干')
# 年干星系
c_year_star = pd.read_csv('basic/celestial_yr_star.csv', index_col='星名') 
c_year_star['type'] = '年干'
# 年支星系
t_year_star = pd.read_csv('basic/terrestial_yr_star.csv', index_col='星名')
t_year_star['type'] ='年支'
#月星系
m_star = pd.read_csv('basic/month_star.csv', index_col='星名')
t_year_star['type'] ='月'
# 時星系
t_hour_star = pd.read_csv('basic/t_hour_star.csv', index_col='星名')
t_hour_star['type'] = '時'
# 紫微定盤
pole_star_map  = pd.read_csv('basic/north_star_loc.csv', 
                              index_col='Date')

# # 星等表/化祿
star_level =pd.read_csv('basic/star_level.csv', index_col ='宮位').astype(str)

#五虎遁(納音會用)
tiger5 = pd.read_csv('basic/five_tiger.csv',index_col='地支')

#%%
# 納音
sonus= pd.Series({
'甲子乙丑':'海中金', '丙寅丁卯':'爐中火',
'戊辰己巳':'大林木', '庚午辛未':'路旁土',
'壬申癸酉':'劍鋒金', '甲戌乙亥':'山頭火',
'丙子丁丑':'澗下水', '戊寅己卯':'城頭土',
'庚辰辛巳':'白臘金', '壬午癸未':'楊柳木',
'甲申乙酉':'井泉水', '丙戌丁亥':'屋上土',
'戊子己丑':'霹靂火', '庚寅辛卯':'松柏木',
'壬辰癸巳':'長流水', '甲午乙未':'砂中金',
'丙申丁酉':'山下火', '戊戌己亥':'平地木',
'庚子辛丑':'壁上土', '壬寅癸卯':'金箔金',
'甲辰乙巳':'覆燈火', '丙午丁未':'天河水',
'戊申己酉':'大驛土', '庚戌辛亥':'釵釧金',
'壬子癸丑':'桑柘木', '甲寅乙卯':'大溪水',
'丙辰丁巳':'砂中土', '戊午己未':'天上火',
'庚申辛酉':'石榴木', '壬戌癸亥':'大海水'})


life_profile =['*命宮*','父母','福德','田宅','*官祿*','奴僕',
               '*遷移*','疾厄','*財帛*','子女','夫妻','兄弟']


def reorder_dict(dct):
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
minor_star = pd.concat([c_year_star, t_year_star,m_star,t_hour_star], axis=0,
                       join='outer', ignore_index=False)



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


def arrange_star(birth,star_dct,name):
    """
    根據生日決定
    """
    dct = choose_minor(birth, star_dct)
    dct_swap = swap_key_value(dct)
    df = dct_to_df(dct_swap,name)
    return df





a = {'年干':['天魁','天鉞']}
b = {'時':['文昌','文曲']}
c ={'月':['左輔','右弼']}
d = {'年支':'龍池'}

ex1 = life_dict['嚴介溪']
test1 = arrange_star(ex1, {**a,**b,**c},'吉星組合')
 




            

# def blessing(birth):
#     """
#     魁鉞/昌曲/左右
#     """     
#     stars_c = ['天魁','天鉞','左輔','右弼','文昌','文曲']
#     c_star =minor_star.loc[stars_c[0:2], year_c]
#     m_star =minor_star.loc[stars_c[2:4],month]
#     t_star =minor_star.loc[stars_c[4:6], hour]
#     return t_star


def jinx(birth):
    """
    羊陀火鈴空截
    """
    pass


# %%
