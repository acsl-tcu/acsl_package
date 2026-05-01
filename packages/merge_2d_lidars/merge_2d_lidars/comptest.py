import numpy as np
import timeit

# データの準備
L = list(range(10000))
a = 5000

# リスト内包表記を使用する関数
def find_closest_index_list_comprehension(L, a):
    return min(range(len(L)), key=lambda i: abs(L[i] - a))

# NumPy を使用する関数
def find_closest_index_numpy(L, a):
    L = np.array(L)
    return np.argmin(np.abs(L - a))

# リスト内包表記の実行時間を計測
time_list_comprehension = timeit.timeit(
    'find_closest_index_list_comprehension(L, a)',
    globals=globals(),
    number=1000
)

# NumPy の実行時間を計測
time_numpy = timeit.timeit(
    'find_closest_index_numpy(L, a)',
    globals=globals(),
    number=1000
)

print(f"リスト内包表記の実行時間: {time_list_comprehension:.6f} 秒")
print(f"NumPy の実行時間: {time_numpy:.6f} 秒")
