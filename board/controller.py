from typing import List, Callable, Tuple
import numpy as np

AutoController = Callable[[np.ndarray, List[int], List[int]], List[List[int]]]

Controller = Callable[[List[Tuple[int, int]]], List[Tuple[int, int]]]
