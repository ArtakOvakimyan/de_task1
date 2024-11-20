import pandas as pd
import json
import msgpack
import os

df = pd.read_csv('./data/titanic.csv')
selected_columns = ['Survived', 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
df_selected = df[selected_columns]

numerical_stats = {
    'max': df_selected[['Age', 'SibSp', 'Parch', 'Fare']].max().to_dict(),
    'min': df_selected[['Age', 'SibSp', 'Parch', 'Fare']].min().to_dict(),
    'mean': df_selected[['Age', 'SibSp', 'Parch', 'Fare']].mean().to_dict(),
    'sum': df_selected[['Age', 'SibSp', 'Parch', 'Fare']].sum().to_dict(),
    'std': df_selected[['Age', 'SibSp', 'Parch', 'Fare']].std().to_dict()
}
categorical_freq = {
    'Survived': df_selected['Survived'].value_counts().to_dict(),
    'Pclass': df_selected['Pclass'].value_counts().to_dict(),
    'Sex': df_selected['Sex'].value_counts().to_dict(),
    'Embarked': df_selected['Embarked'].value_counts().to_dict()
}
results = {
    "numerical_stats": numerical_stats,
    "categorical_freq": categorical_freq
}

with open('fith_task_18.json', 'w') as json_file:
    json.dump(results, json_file, indent=4)
    
df_selected.to_csv('fith_task_18.csv', index=False)
df_selected.to_pickle('fith_task_18.pkl')

data_dict = df_selected.to_dict(orient='records')
with open('fith_task_18.msgpack', 'wb') as f:
    packed = msgpack.packb(data_dict)
    f.write(packed)

file_sizes = {
    "CSV": os.path.getsize('fith_task_18.csv'),
    "JSON": os.path.getsize('fith_task_18.json'),
    "MsgPack": os.path.getsize('fith_task_18.msgpack'),
    "Pickle": os.path.getsize('fith_task_18.pkl')
}

with open('fith_task_18.msgpack', 'rb') as f:
    packed = msgpack.load(f)

print("Размеры файлов:")
for format, size in file_sizes.items():
    print(f"{format}: {size} байт")

