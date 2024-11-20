import numpy as np
import os

matrix = np.load('./data/second_task.npy')

x, y, z = [], [], []

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        if matrix[i][j] > 518:
            x.append(i)
            y.append(j)
            z.append(matrix[i][j])
            
np.savez('second_task_18.npz', x, y, z)
np.savez_compressed('second_task_compress_18.npz', x, y, z)

first_size = os.path.getsize('second_task_18.npz')
second_size = os.path.getsize('second_task_compress_18.npz')
print(f"Размер без сжатия: {first_size}")
print(f"Размер после сжатия: {second_size}")
print(f'Разница: {first_size-second_size}')