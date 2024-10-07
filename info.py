import pandas as pd

# 古命例
life_example = pd.read_excel('basic/example.xlsx', sheet_name='全書',
                             nrows=113, usecols='A:F', index_col='姓名')
life_dict = dict()
for jj in life_example.index:
     life_dict[jj] = life_example.loc[jj].to_list()

life_example2 = pd.read_excel('basic/example.xlsx',sheet_name='其他', index_col='姓名')
life_dct2 = {ii: life_example2.loc[ii,:].to_list() for ii in life_example2.index}

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

minor_star = pd.concat([c_year_star, t_year_star,m_star,t_hour_star], axis=0,
                       join='outer', ignore_index=False)
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

c_flow = pd.read_csv('basic/c_flow_star.csv', index_col='星名')
t_flow = pd.read_csv('basic/t_flow_star.csv', index_col='星名')

#def flow_stars():

 

