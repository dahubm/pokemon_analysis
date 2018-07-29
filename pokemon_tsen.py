#### TSNE을 이용한 against damage 시각화 코드
#### 해당 소스는

#  를 참고

from sklearn.manifold import TSNE
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

### against damage 속성을 읽어옴
df = pd.read_csv("./data/pokemon.csv").drop('type2', axis=1)
df['type1id'] = df['type1'].rank(method='dense').astype(int)
features = ['against_bug', 'against_dark', 'against_dragon', 'against_electric', 'against_fairy', 'against_fight', 'against_fire', 'against_flying', 'against_ghost','against_grass', 'against_ground', 'against_ice', 'against_normal', 'against_poison', 'against_psychic', 'against_rock', 'against_steel', 'against_water']
df_norm = df.copy()
#### against damage 값에 특별히 scaled 를 하지 않고 적용해봄
### TSNE 학습
X_tsne = TSNE(learning_rate=1000, n_components=2).fit_transform(df_norm[features])
types1 = df['type1'].unique()
type1_ids = df['type1id'].unique()  ### 타입에 대한 수치화

##### 화면에 모두 출력 할수 없기 때문에 rows_types, row_type_ids, column_type_ids, column_types 를 적절히 변경해 가면서 확인
###  ex) row_types[5:], column_types[10:]
row_types = types1
row_type_ids = type1_ids
num_types1 = len(types1)
column_type_ids = type1_ids
column_types = types1

fig = plt.figure(figsize=(11,11))
cmap = plt.get_cmap('nipy_spectral')
rows, cols = 5, 5
num = 1
### 타입 vs 타입 별로 TSEN 으로 학습한 against damage 2차원 속성의 분포를 표시한다.
### color 값을 type을 구분한다.
for row, t1_id, t1 in zip(range(rows), row_type_ids, row_types):
    for col, t2_id, t2 in zip(range(cols), column_type_ids, column_types):
        plt.subplot(rows, cols, num)
        X_i = X_tsne[np.where(df['type1id'] == t1_id)[0]]
        X_j = X_tsne[np.where(df['type1id'] == t2_id)[0]]
        plt.scatter(X_i[:, 0], X_i[:, 1], c=cmap(t1_id / num_types1))
        plt.scatter(X_j[:, 0], X_j[:, 1], c=cmap(t2_id / num_types1))
        plt.title(str(t1) + ' vs ' + str(t2))
        num += 1
fig.tight_layout()
plt.show()
