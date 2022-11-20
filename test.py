from typing import Optional
import numpy as np
import numpy.typing as npt


class MyClass:
    arr: Optional[npt.NDArray[np.float64]] = None

    def __init__(self, arr: np.ndarray):
        self.arr = arr
        print(f'arr: {self.arr}')

#a = np.array([1, 2.0])
# MyClass(a)
