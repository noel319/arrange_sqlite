import pandas as pd

# Sample DataFrame
df = pd.DataFrame({'col1': ['A', 'B', 'C'], 'col2': ['X', 'Y', 'Z']})

# Combine col1 and col2 with a space in between and remove the original columns
df['combined'] = df['col1'] + ' ' + df['col2']
df = df.drop(['col1', 'col2'], axis=1)

print(df)
