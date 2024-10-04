#%%
from functions import *
from pprint import pprint
a = {'年干':['天魁','天鉞']}
b = {'時':['文昌','文曲']}
c ={'月':['左輔','右弼']}
d = {'年支':'火星'}


#pprint(sonus)




# set_empty
#%%
sonus_list = list(sonus.keys())


def empty_star(birth):
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
    
    

ex1 = life_dict['楊貴妃']
print(ex1)
aa = empty_star(ex1)
print(aa)
#life_cycle(ex1, gender='F')



