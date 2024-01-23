import pandas as pd

data = pd.DataFrame([['a', 2, 3], ['b', 5, 6], ['a', 8, 9]], columns=['A', 'B', 'C'])

data = data.drop(1).reset_index(drop=True)
print(data)
