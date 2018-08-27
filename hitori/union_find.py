class UnionFind:
    """This is a simple implementation of a union-find data structure.

    The UF represents equivalence classes between members of a set.
    It's initialised by passing in the membership set.
    >>> uf = UnionFind([1, 2, 3])
    The members of the set must be usable as dictionary keys.

    Connections (equivalences) between any two members are registered by calling
    >>> uf.union(p, q)

    It's possible to see if two members are in the same equivalence set by calling
    >>> if uf.connected(p, q):
    >>>     pass

    The current equivalence set leader (an arbitrarily-chosen example) plus the
    size of the corresponding equivalence set can be retrieved thus:
    >>> leader, n = uf.find(p)
    """

    def __init__(self, members):
        self.leaders = {m: (m, 1) for m in members}

    def find(self, p):
        """For some member of the collection,
        return its equivalence class leader and the number of elements in that class"""
        if p not in self.leaders:
            return None, 0

        q, n = self.leaders[p]
        while True:
            if p == q:
                return p, n
            self.leaders[p] = self.leaders[q]
            p, (q, n) = q, self.leaders[q]

    def union(self, p, q):
        p_lead, p_num = self.find(p)
        q_lead, q_num = self.find(q)
        if p_lead is None or q_lead is None:
            return

        if p_lead != q_lead:
            self.leaders[p_lead] = self.leaders[q_lead] = q_lead, p_num + q_num

    def connected(self, p, q):
        return self.find(p) == self.find(q)
