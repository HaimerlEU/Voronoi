# from https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html
import numpy as np
import pandas as pd

s = pd.Series([1, 3, 5, np.nan, 6, 8])
print(s)

dates = pd.date_range("20130101", periods=6)
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
print(df)

df2 = pd.DataFrame({
        "A": 1.0,
        "B": pd.Timestamp("20130102"),
        "C": pd.Series(1, index=list(range(4)), dtype="float32"),
        "D": np.array([3] * 4, dtype="int32"),
        "E": pd.Categorical(["test", "train", "test", "train"]),
        "F": "foo",
    })
print(df2)
print(df2.head(2))
# data as array - no index
print("---------------- to array")
print(df.to_numpy())

print("------------------  access  ")
# access data - same as df["A"]
print (df.A)
print("----------  subsection")
print (df[0:3])

print("------------------- to array")
print(df.to_numpy())

