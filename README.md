
### How to read the data
- Download the zipped file: [`ratebeer.json.gz`](https://jmcauley.ucsd.edu/data/beer/ratebeer.json.gz)
- Unzip it in the folder to create `ratebeer.json`
- Load the data in memory in the `df_raw` dataframe using the snippet below (example to read only the first 100000 rows):

```python
import pandas as pd


def parse(path):
    with open(path, "r") as f:
        for line in f:
            yield eval(line)


filename = "ratebeer.json"
N_rows = 100000
df_raw = pd.DataFrame.from_records(parse(filename), nrows=N_rows)
```