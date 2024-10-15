#%%
from tabulate import tabulate
from functions import *
from pprint import pprint
from flow_compute import *
import re



 

ex = life_dict2['俞欣榮']
Z = combine_star(ex,'m')
Z2 = combine_flow(ex,'m', 38)
print('\n========================\n')
print(tabulate(Z2,tablefmt='psql'))
#u = combine_flow(ex, 'm', 67)



 