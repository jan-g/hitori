from hitori.union_find import UnionFind

def test_uf():
    uf = UnionFind([1, 2, 3, 4])

    # Join 1 and 2
    uf.union(1, 2)
    assert uf.connected(1, 2)
    assert uf.connected(2, 1)
    leader, n = uf.find(1)
    assert leader in [1, 2]
    assert n == 2

    assert not uf.connected(2, 3)
    assert not uf.connected(3, 4)

    # Join 3 and 4
    uf.union(3, 4)

    leader, n = uf.find(1)
    assert leader in [1, 2]
    assert n == 2

    leader, n = uf.find(3)
    assert leader in [3, 4]
    assert n == 2

    assert uf.connected(3, 4)
    assert uf.connected(4, 3)

    assert not uf.connected(1, 3)
    assert not uf.connected(1, 4)
    assert not uf.connected(2, 3)
    assert not uf.connected(2, 4)

    # Now join these two equivalence classes
    uf.union(1, 3)

    leader, n = uf.find(1)
    assert leader in [1, 2, 3, 4]
    assert n == 4
    assert uf.connected(1, 3)
    assert uf.connected(1, 4)
    assert uf.connected(2, 3)
    assert uf.connected(2, 4)
