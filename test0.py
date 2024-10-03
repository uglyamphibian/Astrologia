#%%
from functions import *
from pprint import pprint
a = {'年干':['天魁','天鉞']}
b = {'時':['文昌','文曲']}
c ={'月':['左輔','右弼']}
d = {'年支':'火星'}

ex1 = life_dict['娼婦']
print(ex1)
aa = life_cycle(ex1, gender='F')
#pprint(sonus)




# set_empty
#%%
sonus_list = list(sonus.keys())

empty_loc = []
for ii in sonus_list:
    list_tmp = [ii[0:2],ii[2:]]
    empty_loc.extend(list_tmp)

np_empty = np.array(empty_loc).reshape(6,10)
empty_value = ['戌亥','申酉','午未','辰巳','寅卯','子丑']
#VV = dict(zip(empty_value,np_empty))


#def set_empty(birth):
#    empty_dct = {}

