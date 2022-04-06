def overlay_combine_lists(left, right):
    # Easier to show than describe:
    # > overlay_combine_lists([1, 2, 3, 4, 5], [4, 5, 6, 7, 8])
    # [1, 2, 3, 4, 5, 6, 7, 8]
    # > overlay_combine_lists([1, 2, 3, 3, 3], [3, 4, 5, 6, 7, 8])
    # [1, 2, 3, 3, 3, 4, 5, 6, 7, 8]
    left_starts_with_empty = left[0] == ''
    left = [item for item in left if item != '']
    if left_starts_with_empty:
        left = [''] + left
    right = [item for item in right if item != '']
    left_len, right_len = map(len, [left, right])
    if left_len >= right_len:
        starting_offset = right_len
    else:
        starting_offset = right_len - left_len
    for offset in range(starting_offset, 0, -1):
        if left[-offset:] == right[:offset]:
            return left[:-offset] + right[:offset] + right[offset:]


def overlay_paths(left, right, left_splitter='/', right_splitter='/', path_delimiter='/'):
    result = overlay_combine_lists(left.split(left_splitter), right.split(right_splitter))
    if result is not None:
        return path_delimiter.join(result)
