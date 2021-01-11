def get_grid_cell(row, column):
    '''
    Return the grid and cell indices for a given [row] and [column] location
    '''
    grid = 3 * int(row / 3) + int(column / 3)
    base_r = 3 * int(grid / 3)
    base_c = 3 * (grid % 3)
    off_r = row - base_r
    off_c = column - base_c
    cell = 3 * int(off_r) + int(off_c)
    return grid, cell



def get_row_column(grid, cell):
    '''
    Return the row and column indices for a given [grid] and [cell] location
    '''
    base_r = 3*int(grid / 3)
    base_c = 3*(grid % 3)
    off_r = int(cell / 3)
    off_c = cell % 3
    return base_r + off_r, base_c + off_c

def heuristic(x):
    return x%10

some_list = [2343, 323, 34254, 49, 595]

s = sorted(some_list, key=lambda x: heuristic(x))


print(s)
