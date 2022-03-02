
import pandas as pd

path = "../../UNSW-NB15 - CSV Files/UNSW-NB15_"

filenames = [path+"1.csv", path+"2.csv", path+"3.csv", path+"4.csv"]

print("reading data...")
dfs = []
for name in filenames:
    df = pd.read_csv(name, index_col=None)
    dfs.append(df)


honeypotDF = pd.concat(dfs, axis=0, ignore_index=True)

totalCount = len(honeypotDF.index)
honeypotDF = honeypotDF[honeypotDF["Label"] == 0]

benignCount = len(honeypotDF)
attacksCount = totalCount - benignCount

print("count: ",totalCount)
print("benign count: ", benignCount)
print("attacks count: ", attacksCount)
