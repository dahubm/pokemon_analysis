#### 포켓몬의 강함을 측정하여 실험한다

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


#### against damage 속성을 제외한 기본 정보만 가지고 point1 를 구함
def calc_base_power(defense_total, attack, sp_attack ) :
    result = defense_total - attack - sp_attack
    if result < 0 : return 0
    return result

#### against damage 속성을 고려하여 point(point2, point3) 구함
def calc_against_power(defense_total, attack, sp_attack, against) :
    result = defense_total - ((attack + sp_attack) * against)
    #result = defense_total - attack - sp_attack - against  #point2
    if result < 0 : return 0
    return result

#### 포켓몬 데이터 읽어옴
df = pd.read_csv("./data/pokemon.csv")

#### against damage 속성을 정의
features = ['against_bug', 'against_dark', 'against_dragon', 'against_electric', 'against_fairy', 'against_fight', 'against_fire', 'against_flying',
            'against_ghost','against_grass', 'against_ground', 'against_ice', 'against_normal', 'against_poison', 'against_psychic', 'against_rock', 'against_steel', 'against_water']
### against damage 속성을 읽어옴
against_df = df[features]

### 포켓몬의 강함이 기준이 되는 속성을 읽어옴
base_power_features = ["name", "hp", 'attack', 'sp_attack', 'defense', 'sp_defense', 'speed', 'type1']
base_df = df[base_power_features]

base_values = base_df.values

counter = Counter()


### 각각의 포멧몬에 대해서 win, draw, lose 빈도수 구함
for i, value in enumerate(base_values) :
    ### 강함의 긍정속성 합(방어)
    defense_total = value[1] + value[4] + value[5] + value[6]
    for j, t_value in enumerate(base_values) :
        if value[0] == t_value[0] : continue
        #base_power = calc_base_power(defense_total, t_value[2], t_value[3])
        keyname = t_value[7].lower()
        if keyname == 'fighting' :
            keyname = "fight"
        base_power = calc_against_power(defense_total, t_value[2], t_value[3], against_df["against_" + keyname ][i] )

        ### 상대 강함의 긍정속성 합(방어)
        t_defense_total = t_value[1] + t_value[4] + t_value[5] +t_value[6]
        keyname = value[7].lower()
        if keyname == 'fighting' :
            keyname = "fight"
        base_power_t = calc_against_power(t_defense_total, value[2], value[3], against_df["against_" + keyname ][j])

        #base_power_t = calc_base_power(t_defense_total, value[2], value[3])

        if base_power < base_power_t :
            name = value[0] + "_l"
            counter[name] += 1
        elif base_power > base_power_t :
            name = value[0] + "_w"
            counter[name] += 1
        else:
            name = value[0] + "_d"
            counter[name] += 1
        #print(value[0], t_value[0], base_power, base_power_t)

### win - lose 빈도수 기준으로 ranking을 구함
rank_counter = Counter()
for i, value in enumerate(base_values) :
    rank_counter[value[0]] = counter[value[0] + "_w"] - counter[value[0] + "_l"]


#### ranking 을 그래프로 출력
values = []
names = []
for name, cnt in rank_counter.most_common(10) :
    values.append(cnt)
    names.append(name)
x = np.arange(10)
plt.bar(x, height=values)
plt.xticks(x + .5, names);
plt.show()
