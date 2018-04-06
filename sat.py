
"""
Classes for representing 2SAT problems
"""

class CNF:
    """
    Conjunctive Normal Form
    """

    def __init__(self, *clauses):
        self.clauses = clauses

    def __str__(self):
        return ' ^ '.join(map(str, self.clauses))

    def isSat(self, ta):
        """
        :param ta: a TruthAssignment
        :return: boolean saying whether this CNF is satisfied by
                 the given assignment
        """
        v = True
        for c in self.clauses:
            v &= c.isSat(ta)
        return v


class DNF:
    """
    Disjunctive Normal Form
    """

    def __init__(self, *terms):
        self.terms = terms

    def __str__(self):
        return ' v '.join(map(str, self.terms))


class Term:
    """
    A two-literal term.
    """

    def __init__(self, litA, litB):
        self.litA = litA
        self.litB = litB

    def __str__(self):
        return '(%s ^ %s)' % (self.litA, self.litB)


class Clause:
    """
    In 2SAT every clause has exactly two literals.
    Pass two literals to the constructor of this class.
    """

    def __init__(self, litA, litB):
        self.litA = litA
        self.litB = litB

    def __str__(self):
        return '(%s v %s)' % (self.litA, self.litB)

    def isSat(self, ta):
        """
        :param ta: a TruthAssignment
        :return: boolean saying whether this CNF is satisfied by
                 the given assignment
        """
        return (self.litA.isSat(ta) or self.litB.isSat(ta))


class Lit:
    """
    Represents a literal.

    var: a Variable object

    valence: integer in {1, -1} representing whether the variable
             is expressed positively or negated, in this literal

    Examples:
            x1:  Lit(Variable(1), 1)
           ~x2:  Lit(Variable(2), -1)
    """

    def __init__(self, var, valence):
        self.var = var
        self.valence = valence

    def __str__(self):
        return '%s%s' % (
            {1: '', -1:'~'}[self.valence],
            self.var
        )

    def isSat(self, ta):
        """
        :param ta: a TruthAssignment
        :return: boolean saying whether this CNF is satisfied by
                 the given assignment
        """
        v = self.var.isSat(ta)
        return v if self.valence == 1 else (not v)

class Var:
    """
    Represents a variable with an index.

    Index must be an integer.

    For example to define the variable x1, use Var(1).
    """

    def __init__(self, index):
        self.index = index

    def __str__(self):
        return 'x_%s' % self.index

    def __lt__(self, other):
        return self.index < other.index

    def isSat(self, ta):
        """
        :param ta: a TruthAssignment
        :return: boolean saying whether this CNF is satisfied by
                 the given assignment
        """
        return ta[self]


class TruthAssignment:
    """
    This is mostly just a glorified dictionary.
    """

    def __init__(self):
        self.assignment = {}

    def __str__(self):
        A = self.assignment
        return '\n'.join(
            '%s: %s' % (k, A[k])
            for k in sorted(A.keys())
        )

    def __setitem__(self, key, value):
        """
        Set the truth value for a variable.
        :param key: a Var object
        :param value: a boolean
        :return: nothing
        """
        if not isinstance(key, Var):
            raise Exception('Keys must be Var objects!')
        self.assignment[key] = value

    def __getitem__(self, item):
        return self.assignment[item]

x1 = Var(1)
x2 = Var(2)
x3 = Var(3)
x4 = Var(4)

p1 = Lit(x1, 1)
p2 = Lit(x2, 1)
p3 = Lit(x3, 1)
p4 = Lit(x4, 1)

n1 = Lit(x1, -1)
n2 = Lit(x2, -1)
n3 = Lit(x3, -1)
n4 = Lit(x4, -1)

cnf1 = CNF(
    Clause(p1, p2),
    Clause(p1, n3),
    Clause(p3, n4)
)

print
print 'Here is an example of an expression in CNF:'
print cnf1

ta1 = TruthAssignment()
ta1[x1] = True
ta1[x2] = True
ta1[x3] = False
ta1[x4] = True

print
print "Here is a truth assignment:"
print ta1

print
print "The expression is satisfied by the truth assignment:"
print cnf1.isSat(ta1)
