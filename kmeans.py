##### against damage 속성에 따른 KMEANS 클러스터링
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(11,11))


#### 포켓몬 데이터 읽어옴
df = pd.read_csv("./data/pokemon.csv")

#### against damage 속성을 정의
features = ['against_bug', 'against_dark', 'against_dragon', 'against_electric', 'against_fairy', 'against_fight', 'against_fire', 'against_flying',
            'against_ghost','against_grass', 'against_ground', 'against_ice', 'against_normal', 'against_poison', 'against_psychic', 'against_rock', 'against_steel', 'against_water']
### against damage 속성을 읽어옴
against_df = df[features]

### type1 값을 수치값으로 만듬
df['type1id'] = df['type1'].rank(method='dense').astype(int)
type_ids = df['type1id'].values

#### data scale 을 column 단위가 아니라 전체 against 단위로 적용하기 위해 별도로 작성
def min_max_scale(x):
    ### min =0, max =4 로 고정
    ### X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
    ### X_scaled = X_std * (max - min) + min
    x_std = x / 4
    x_scaled = x_std * 1
    return x_scaled

### data scaled
x_scaled = np.apply_along_axis(min_max_scale, 0, against_df.values)
## 실험할 k 값
ks = [2, 4, 6, 8, 10, 15, 20, 25, 30, 40, 50, 60 , 70, 100]
inertias = []   ## 오차값
### k 값을 바꾸어 가며 오차 저장
for k in ks :
#k= 35 최적의 k값
    kmeans = KMeans(n_clusters=k, random_state=0, max_iter=10000).fit(x_scaled)
    inertias.append(kmeans.inertia_)
    ###pred_labels = kmeans.predict(x_scaled)   ### 포켓몬 분포도 표시때 사용

#####
##### 클러스터링 된 포켓몬들을 type 별로 분포도 표시  type 은 아래에 정의된 colors 의 색으로 구분하여 표시한다.
##### 사용시 해당 부분 주석해제
#x = list(range(801))
#colors = ['palevioletred', 'deeppink', 'violet', 'k', 'r', 'cyan', 'b', 'brown', 'cadetblue', 'skyblue', 'gold',
#          'tomato', 'peru', 'c', 'pink', 'y', 'crimson', 'tan']
#for i, v in enumerate(x) :
#    plt.scatter(v, pred_labels[i], c=colors[type_ids[i] - 1])

### k값에 따른 오류값 출력
plt.plot(ks, inertias)
plt.show()




