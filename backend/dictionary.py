tsm_name = ['m', 't', 's']
m_dict = {f'{tsm_name[0]}{i}': i for i in range(1, 10)}
t_dict = {f'{tsm_name[1]}{i}': i for i in range(1, 10)}
s_dict = {f'{tsm_name[2]}{i}': i for i in range(1, 10)}
wind_dict = {'east', 'south', 'west', 'north'}
zfb_dict = {'zhong', 'fa', 'bai'}
flower_dict = {'f1' : 1, 'f2' : 2, 'f3' : 3, 'f4' : 4, 'ff1' : 1, 'ff2' : 2, 'ff3' : 3, 'ff4': 4}
seat_dict = {1: 'east', 2: 'south', 3: 'west', 4: 'north'}
joker = 'joker'

mst_dict = m_dict | t_dict | s_dict

eyes = 'eyes'
shang = 'shang'
pong = 'pong'