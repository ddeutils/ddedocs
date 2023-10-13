# Python: _Joblib Package_

## Installation

```shell
pip install joblib
```

## Parallel

### Functions

``` py hl_lines="6 20-23"
import os
import uuid
import requests
import pandas as pd
from colorthief import ColorThief
from joblib import Parallel, delayed

data = pd.read_csv("dress.csv")


def extract_img_colors(url: str):
    unique_id = uuid.uuid4()
    with open(f"{unique_id}.jpg", "wb") as f:
        f.write(requests.get(url).content)
    color_thief = ColorThief(f"{unique_id}.jpg")
    palette = color_thief.get_palette(color_count=2)
    os.remove(f"{unique_id}.jpg")
    return palette[0], palette[1]

colors = Parallel(n_jobs=-1)(
    delayed(extract_img_colors)(url)
    for url in data['image_url'].values[:100]
)
```

### Classes

``` py hl_lines="1 14-15"
from joblib import Parallel, delayed


class A:

    def __init__(self, x):
        self.x = x

    def square(self):
        return self.x ** 2


runs = [A(x) for x in range(20)]
with Parallel(n_jobs=6, verbose=5) as parallel:
    delayed_func = [delayed(lambda x: x.square())(run) for run in runs]
    output = parallel(delayed_func)
```

## References

- [Python Package: `joblib`](https://joblib.readthedocs.io/en/stable/)
