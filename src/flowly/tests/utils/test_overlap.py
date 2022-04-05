from ...utils.overlap import overlay_combine_lists, overlay_paths


def test_overlay_combine_lists():
    assert overlay_combine_lists([1, 2, 3, 4, 5], [4, 5, 6, 7, 8]) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert overlay_combine_lists([1, 2, 3, 3, 3], [3, 4, 5, 6, 7, 8]) == [1, 2, 3, 3, 3, 4, 5, 6, 7, 8]
    # leading empty space in left list is a special case because absolute paths
    assert overlay_combine_lists(['', 2, 3, 4, 5], [4, 5, 6, 7, 8]) == ['', 2, 3, 4, 5, 6, 7, 8]

def test_overlay_paths():
    assert overlay_paths('/a/b/c', 'b/c/d') == '/a/b/c/d'
    assert overlay_paths('a/b/c/', 'b/c/d') == 'a/b/c/d'
    assert overlay_paths('a/b/c', '/b/c/d') == 'a/b/c/d'
    assert overlay_paths('a/b/c/', '/b/c/d') == 'a/b/c/d'
    assert overlay_paths('a/b/c/d/e', 'b/c/d/e/f') == 'a/b/c/d/e/f'
    assert overlay_paths('a/b/c', 'd/e/f') is None
    assert overlay_paths('a/b/cd', 'cd/e/f') == 'a/b/cd/e/f'
    assert overlay_paths('a/b/c', 'cd/e/f') is None
    assert overlay_paths('a/b/cd', 'd/e/f') is None

    assert overlay_paths('a.b.c', 'b/c/d', left_splitter='.') == 'a/b/c/d'
    assert overlay_paths('a/b/c', 'b.c.d', right_splitter='.') == 'a/b/c/d'
    assert overlay_paths('a.b.c', 'b.c.d', left_splitter='.', right_splitter='.') == 'a/b/c/d'
    assert overlay_paths('a/b/c', 'b/c/d', path_delimiter='.') == 'a.b.c.d'
