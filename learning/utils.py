import numpy as np


def load_data(data_path, tag_transform=lambda x: x, delimiter=','):
    loaded = np.genfromtxt(data_path, dtype=float, delimiter=delimiter)
    return {"data": loaded[:, 1:],
            "tags": [tag_transform(x) for x in loaded[:, 0]]}


def select_rows(mat, rows):
    return [mat[row_i, :] for row_i in rows]


def select_cols(mat, cols):
    return np.transpose([mat[:, col_i] for col_i in cols])
