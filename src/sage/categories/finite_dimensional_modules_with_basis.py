# sage_setup: distribution = sagemath-categories
r"""
Finite dimensional modules with basis
"""
# ****************************************************************************
#  Copyright (C) 2008 Teresa Gomez-Diaz (CNRS) <Teresa.Gomez-Diaz@univ-mlv.fr>
#                2011 Nicolas M. Thiery <nthiery at users.sf.net>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
# *****************************************************************************

import operator
from sage.categories.category_with_axiom import CategoryWithAxiom_over_base_ring
from sage.categories.fields import Fields
from sage.categories.tensor import TensorProductsCategory
from sage.misc.cachefunc import cached_method

class FiniteDimensionalModulesWithBasis(CategoryWithAxiom_over_base_ring):
    """
    The category of finite dimensional modules with a distinguished basis

    EXAMPLES::

      sage: C = FiniteDimensionalModulesWithBasis(ZZ); C
      Category of finite dimensional modules with basis over Integer Ring
      sage: sorted(C.super_categories(), key=str)
      [Category of finite dimensional modules over Integer Ring,
       Category of modules with basis over Integer Ring]
      sage: C is Modules(ZZ).WithBasis().FiniteDimensional()
      True

    TESTS::

        sage: TestSuite(C).run()
    """

    class ParentMethods:

        def gens(self) -> tuple:
            """
            Return the generators of ``self``.

            OUTPUT:

            A tuple containing the basis elements of ``self``.

            EXAMPLES::

                sage: F = CombinatorialFreeModule(ZZ, ['a', 'b', 'c'])                  # needs sage.modules
                sage: F.gens()                                                          # needs sage.modules
                (B['a'], B['b'], B['c'])
            """
            return tuple(self.basis())

        def annihilator(self, S, action=operator.mul, side='right', category=None):
            r"""
            Return the annihilator of a finite set.

            INPUT:

            - ``S`` -- a finite set

            - ``action`` -- a function (default: :obj:`operator.mul`)

            - ``side`` -- 'left' or 'right' (default: 'right')

            - ``category`` -- a category

            Assumptions:

            - ``action`` takes elements of ``self`` as first argument
              and elements of ``S`` as second argument;

            - The codomain is any vector space, and ``action`` is
              linear on its first argument; typically it is bilinear;

            - If ``side`` is 'left', this is reversed.

            OUTPUT:

            The subspace of the elements `x` of ``self`` such that
            ``action(x,s) = 0`` for all `s\in S`. If ``side`` is
            'left' replace the above equation by ``action(s,x) = 0``.

            If ``self`` is a ring, ``action`` an action of ``self`` on
            a module `M` and `S` is a subset of `M`, we recover the
            :wikipedia:`Annihilator_%28ring_theory%29`. Similarly this
            can be used to compute torsion or orthogonals.

            .. SEEALSO:: :meth:`annihilator_basis` for lots of examples.

            EXAMPLES::

                sage: # needs sage.modules
                sage: F = FiniteDimensionalAlgebrasWithBasis(QQ).example(); F
                An example of a finite dimensional algebra with basis:
                the path algebra of the Kronecker quiver
                (containing the arrows a:x->y and b:x->y) over Rational Field
                sage: x, y, a, b = F.basis()
                sage: A = F.annihilator([a + 3*b + 2*y]); A
                Free module generated by {0} over Rational Field
                sage: [b.lift() for b in A.basis()]
                [-1/2*a - 3/2*b + x]

            The category can be used to specify other properties of
            this subspace, like that this is a subalgebra::

                sage: # needs sage.modules
                sage: center = F.annihilator(F.basis(), F.bracket,
                ....:                        category=Algebras(QQ).Subobjects())
                sage: (e,) = center.basis()
                sage: e.lift()
                x + y
                sage: e * e == e
                True

            Taking annihilator is order reversing for inclusion::

                sage: # needs sage.modules
                sage: A   = F.annihilator([]);    A  .rename("A")
                sage: Ax  = F.annihilator([x]);   Ax .rename("Ax")
                sage: Ay  = F.annihilator([y]);   Ay .rename("Ay")
                sage: Axy = F.annihilator([x,y]); Axy.rename("Axy")
                sage: P = Poset(([A, Ax, Ay, Axy], attrcall("is_submodule")))           # needs sage.combinat sage.graphs
                sage: sorted(P.cover_relations(), key=str)                              # needs sage.combinat sage.graphs
                [[Ax, A], [Axy, Ax], [Axy, Ay], [Ay, A]]
            """
            return self.submodule(self.annihilator_basis(S, action, side),
                                  already_echelonized=True,
                                  category=category)

        def annihilator_basis(self, S, action=operator.mul, side='right'):
            """
            Return a basis of the annihilator of a finite set of elements.

            INPUT:

            - ``S`` -- a finite set of objects

            - ``action`` -- a function (default: :obj:`operator.mul`)

            - ``side`` -- 'left' or 'right' (default: 'right'):
              on which side of ``self`` the elements of `S` acts.

            See :meth:`annihilator` for the assumptions and definition
            of the annihilator.

            EXAMPLES:

            By default, the action is the standard `*` operation. So
            our first example is about an algebra::

                sage: # needs sage.graphs sage.modules
                sage: F = FiniteDimensionalAlgebrasWithBasis(QQ).example(); F
                An example of a finite dimensional algebra with basis:
                the path algebra of the Kronecker quiver
                (containing the arrows a:x->y and b:x->y) over Rational Field
                sage: x,y,a,b = F.basis()

            In this algebra, multiplication on the right by `x`
            annihilates all basis elements but `x`::

                sage: x*x, y*x, a*x, b*x                                                # needs sage.graphs sage.modules
                (x, 0, 0, 0)

            So the annihilator is the subspace spanned by `y`, `a`, and `b`::

                sage: F.annihilator_basis([x])                                          # needs sage.graphs sage.modules
                (y, a, b)

            The same holds for `a` and `b`::

                sage: x*a, y*a, a*a, b*a                                                # needs sage.graphs sage.modules
                (a, 0, 0, 0)
                sage: F.annihilator_basis([a])                                          # needs sage.graphs sage.modules
                (y, a, b)

            On the other hand, `y` annihilates only `x`::

                sage: F.annihilator_basis([y])                                          # needs sage.graphs sage.modules
                (x,)

            Here is a non trivial annihilator::

                sage: F.annihilator_basis([a + 3*b + 2*y])                              # needs sage.graphs sage.modules
                (-1/2*a - 3/2*b + x,)

            Let's check it::

                sage: (-1/2*a - 3/2*b + x) * (a + 3*b + 2*y)                            # needs sage.graphs sage.modules
                0

            Doing the same calculations on the left exchanges the
            roles of `x` and `y`::

                sage: # needs sage.graphs sage.modules
                sage: F.annihilator_basis([y], side="left")
                (x, a, b)
                sage: F.annihilator_basis([a], side="left")
                (x, a, b)
                sage: F.annihilator_basis([b], side="left")
                (x, a, b)
                sage: F.annihilator_basis([x], side="left")
                (y,)
                sage: F.annihilator_basis([a + 3*b + 2*x], side="left")
                (-1/2*a - 3/2*b + y,)

            By specifying an inner product, this method can be used to
            compute the orthogonal of a subspace::

                sage: # needs sage.graphs sage.modules
                sage: x,y,a,b = F.basis()
                sage: def scalar(u,v):
                ....:     return vector([sum(u[i]*v[i] for i in F.basis().keys())])
                sage: F.annihilator_basis([x + y, a + b], scalar)
                (x - y, a - b)

            By specifying the standard Lie bracket as action, one can
            compute the commutator of a subspace of `F`::

                sage: F.annihilator_basis([a + b], action=F.bracket)                    # needs sage.graphs sage.modules
                (x + y, a, b)

            In particular one can compute a basis of the center of the
            algebra. In our example, it is reduced to the identity::

                sage: F.annihilator_basis(F.algebra_generators(), action=F.bracket)     # needs sage.graphs sage.modules
                (x + y,)

            But see also
            :meth:`FiniteDimensionalAlgebrasWithBasis.ParentMethods.center_basis`.
            """
            # TODO: optimize this!
            from sage.matrix.constructor import matrix
            if side == 'right':
                action_left = action
                action = lambda b,s: action_left(s, b)

            mat = matrix(self.base_ring(), self.dimension(), 0)
            for s in S:
                mat = mat.augment(matrix(self.base_ring(),
                                         [action(s, b)._vector_() for b in self.basis()]))
            return tuple(map(self.from_vector, mat.left_kernel().basis()))

        @cached_method
        def _dense_free_module(self, base_ring=None):
            """
            Return a dense free module of the same dimension as ``self``.

            INPUT:

            - ``base_ring`` -- a ring or ``None``

            If ``base_ring`` is ``None``, then the base ring of ``self``
            is used.

            This method is mostly used by ``_vector_``

            EXAMPLES::

                sage: C = CombinatorialFreeModule(QQ['x'], ['a','b','c']); C            # needs sage.modules
                Free module generated by {'a', 'b', 'c'} over
                 Univariate Polynomial Ring in x over Rational Field
                sage: C._dense_free_module()                                            # needs sage.modules
                Ambient free module of rank 3 over the principal ideal domain
                 Univariate Polynomial Ring in x over Rational Field
                sage: C._dense_free_module(QQ['x,y'])                                   # needs sage.modules
                Ambient free module of rank 3 over the integral domain
                 Multivariate Polynomial Ring in x, y over Rational Field
            """
            if base_ring is None:
                base_ring = self.base_ring()
            from sage.modules.free_module import FreeModule
            return FreeModule(base_ring, self.dimension())

        def from_vector(self, vector, order=None, coerce=True):
            """
            Build an element of ``self`` from a vector.

            EXAMPLES::

                sage: # needs sage.modules
                sage: p_mult = matrix([[0,0,0], [0,0,-1], [0,0,0]])
                sage: q_mult = matrix([[0,0,1], [0,0,0], [0,0,0]])
                sage: A = algebras.FiniteDimensional(
                ....:         QQ, [p_mult, q_mult, matrix(QQ, 3, 3)], 'p,q,z')
                sage: A.from_vector(vector([1,0,2]))
                p + 2*z
            """
            if order is None:
                try:
                    order = sorted(self.basis().keys())
                except AttributeError: # Not a family, assume it is list-like
                    order = range(self.dimension())
            if not coerce or vector.base_ring() is self.base_ring():
                return self._from_dict({order[i]: c for i,c in vector.items()},
                                       coerce=False)
            R = self.base_ring()
            return self._from_dict({order[i]: R(c) for i,c in vector.items() if R(c)},
                                   coerce=False, remove_zeros=False)

        def echelon_form(self, elements, row_reduced=False, order=None):
            r"""
            Return a basis in echelon form of the subspace spanned by
            a finite set of elements.

            INPUT:

            - ``elements`` -- a list or finite iterable of elements of ``self``
            - ``row_reduced`` -- (default: ``False``) whether to compute the
              basis for the row reduced echelon form
            - ``order`` -- (optional) either something that can
              be converted into a tuple or a key function

            OUTPUT:

            A list of elements of ``self`` whose expressions as vectors
            form a matrix in echelon form. If ``base_ring`` is specified,
            then the calculation is achieved in this base ring.

            EXAMPLES::

                sage: # needs sage.modules
                sage: X = CombinatorialFreeModule(QQ, range(3), prefix="x")
                sage: x = X.basis()
                sage: V = X.echelon_form([x[0]-x[1], x[0]-x[2], x[1]-x[2]]); V
                [x[0] - x[2], x[1] - x[2]]
                sage: matrix(list(map(vector, V)))
                [ 1  0 -1]
                [ 0  1 -1]

            ::

                sage: # needs sage.modules
                sage: F = CombinatorialFreeModule(ZZ, [1,2,3,4])
                sage: B = F.basis()
                sage: elements = [B[1]-17*B[2]+6*B[3], B[1]-17*B[2]+B[4]]
                sage: F.echelon_form(elements)
                [B[1] - 17*B[2] + B[4], 6*B[3] - B[4]]

            ::

                sage: F = CombinatorialFreeModule(QQ, ['a','b','c'])                    # needs sage.modules
                sage: a,b,c = F.basis()                                                 # needs sage.modules
                sage: F.echelon_form([8*a+b+10*c, -3*a+b-c, a-b-c])                     # needs sage.modules
                [B['a'] + B['c'], B['b'] + 2*B['c']]

            ::

                sage: R.<x,y> = QQ[]
                sage: C = CombinatorialFreeModule(R, range(3), prefix='x')              # needs sage.modules
                sage: x = C.basis()                                                     # needs sage.modules
                sage: C.echelon_form([x[0] - x[1], 2*x[1] - 2*x[2], x[0] - x[2]])       # needs sage.modules sage.rings.function_field
                [x[0] - x[2], x[1] - x[2]]

            ::

                sage: M = MatrixSpace(QQ, 3, 3)                                         # needs sage.modules
                sage: A = M([[0, 0, 2], [0, 0, 0], [0, 0, 0]])                          # needs sage.modules
                sage: M.echelon_form([A, A])                                            # needs sage.modules
                [
                [0 0 1]
                [0 0 0]
                [0 0 0]
                ]

            TESTS:

            We convert the input elements to ``self``::

                sage: E.<x,y,z> = ExteriorAlgebra(QQ)                                   # needs sage.modules
                sage: E.echelon_form([1, x + 2])                                        # needs sage.modules
                [1, x]
            """
            # Make sure elements consists of elements of ``self``
            elements = [self(y) for y in elements]
            if order is not None:
                order = self._compute_support_order(elements, order)
            from sage.matrix.constructor import matrix
            mat = matrix(self.base_ring(), [g._vector_(order=order) for g in elements])
            # Echelonizing a matrix over a field returned the rref
            if row_reduced and self.base_ring() not in Fields():
                try:
                    mat = mat.rref().change_ring(self.base_ring())
                except (ValueError, TypeError):
                    raise ValueError("unable to compute the row reduced echelon form")
            else:
                mat.echelonize()
            ret = [self.from_vector(vec, order=order) for vec in mat if vec]
            return ret

        def invariant_module(self, S, action=operator.mul, action_on_basis=None,
                             side="left", **kwargs):
            r"""
            Return the submodule of ``self`` invariant under the action
            of ``S``.

            For a semigroup `S` acting on a module `M`, the invariant
            submodule is given by

            .. MATH::

                M^S = \{m \in M : s \cdot m = m,\, \forall s \in S\}.

            INPUT:

            - ``S`` -- a finitely-generated semigroup
            - ``action`` -- a function (default: :obj:`operator.mul`)
            - ``side`` -- ``'left'`` or ``'right'`` (default: ``'right'``);
              which side of ``self`` the elements of ``S`` acts
            - ``action_on_basis`` -- (optional) define the action of ``S``
              on the basis of ``self``

            OUTPUT:

            - :class:`~sage.modules.with_basis.invariant.FiniteDimensionalInvariantModule`

            EXAMPLES:

            We build the invariant module of the permutation representation
            of the symmetric group::

                sage: # needs sage.groups sage.modules
                sage: G = SymmetricGroup(3); G.rename('S3')
                sage: M = FreeModule(ZZ, [1,2,3], prefix='M'); M.rename('M')
                sage: action = lambda g, x: M.term(g(x))
                sage: I = M.invariant_module(G, action_on_basis=action); I
                (S3)-invariant submodule of M
                sage: I.basis()
                Finite family {0: B[0]}
                sage: [I.lift(b) for b in I.basis()]
                [M[1] + M[2] + M[3]]
                sage: G.rename(); M.rename()  # reset the names

            We can construct the invariant module of any module that has
            an action of ``S``. In this example, we consider the dihedral
            group `G = D_4` and the subgroup `H < G` of all rotations. We
            construct the `H`-invariant module of the group algebra `\QQ[G]`::

                sage: # needs sage.groups
                sage: G = groups.permutation.Dihedral(4)
                sage: H = G.subgroup(G.gen(0))
                sage: H
                Subgroup generated by [(1,2,3,4)]
                 of (Dihedral group of order 8 as a permutation group)
                sage: H.cardinality()
                4

                sage: # needs sage.groups sage.modules
                sage: A = G.algebra(QQ)
                sage: I = A.invariant_module(H)
                sage: [I.lift(b) for b in I.basis()]
                [() + (1,2,3,4) + (1,3)(2,4) + (1,4,3,2),
                 (2,4) + (1,2)(3,4) + (1,3) + (1,4)(2,3)]
                sage: all(h * I.lift(b) == I.lift(b)
                ....:     for b in I.basis() for h in H)
                True
            """
            if action_on_basis is not None:
                from sage.modules.with_basis.representation import Representation
                M = Representation(S, self, action_on_basis, side=side)
            else:
                M = self

            from sage.modules.with_basis.invariant import FiniteDimensionalInvariantModule
            return FiniteDimensionalInvariantModule(M, S, action=action, side=side, **kwargs)

        def twisted_invariant_module(self, G, chi,
                                     action=operator.mul,
                                     action_on_basis=None,
                                     side='left',
                                     **kwargs):
            r"""
            Create the isotypic component of the action of ``G`` on
            ``self`` with irreducible character given by ``chi``.

            .. SEEALSO::

                -:class:`~sage.modules.with_basis.invariant.FiniteDimensionalTwistedInvariantModule`

            INPUT:

            - ``G`` -- a finitely-generated group
            - ``chi`` -- a list/tuple of character values or an instance of
              :class:`~sage.groups.class_function.ClassFunction_gap`
            - ``action`` -- a function (default: :obj:`operator.mul`)
            - ``action_on_basis`` -- (optional) define the action of ``g``
              on the basis of ``self``
            - ``side`` -- ``'left'`` or ``'right'`` (default: ``'right'``);
              which side of ``self`` the elements of ``S`` acts

            OUTPUT:

            - :class:`~sage.modules.with_basis.invariant.FiniteDimensionalTwistedInvariantModule`

            EXAMPLES::

                sage: # needs sage.groups sage.modules
                sage: M = CombinatorialFreeModule(QQ, [1,2,3])
                sage: G = SymmetricGroup(3)
                sage: def action(g,x): return(M.term(g(x)))  # permute coordinates
                sage: T = M.twisted_invariant_module(G, [2,0,-1],
                ....:                                action_on_basis=action)
                sage: import __main__; __main__.action = action
                sage: TestSuite(T).run()
            """

            if action_on_basis is not None:
                from sage.modules.with_basis.representation import Representation
                from sage.categories.modules import Modules
                category = kwargs.pop('category', Modules(self.base_ring()).WithBasis())
                M = Representation(G, self, action_on_basis, side=side, category=category)
            else:
                M = self

            from sage.modules.with_basis.invariant import FiniteDimensionalTwistedInvariantModule
            return FiniteDimensionalTwistedInvariantModule(M, G, chi,
                                                          action, side, **kwargs)

    class ElementMethods:
        def dense_coefficient_list(self, order=None):
            """
            Return a list of *all* coefficients of ``self``.

            By default, this list is ordered in the same way as the
            indexing set of the basis of the parent of ``self``.

            INPUT:

            - ``order`` -- (optional) an ordering of the basis indexing set

            EXAMPLES::

                sage: # needs sage.modules
                sage: v = vector([0, -1, -3])
                sage: v.dense_coefficient_list()
                [0, -1, -3]
                sage: v.dense_coefficient_list([2,1,0])
                [-3, -1, 0]
                sage: sorted(v.coefficients())
                [-3, -1]
            """
            if order is None:
                try:
                    order = sorted(self.parent().basis().keys())
                except AttributeError: # Not a family, assume it is list-like
                    order = range(self.parent().dimension())
            return [self[i] for i in order]

        def _vector_(self, order=None):
            r"""
            Return ``self`` as a vector.

            EXAMPLES::

                sage: # needs sage.modules
                sage: v = vector([0, -1, -3])
                sage: v._vector_()
                (0, -1, -3)
                sage: C = CombinatorialFreeModule(QQ['x'], ['a','b','c'])
                sage: C.an_element()._vector_()
                (2, 2, 3)
            """
            if order is None:
                dense_free_module = self.parent()._dense_free_module()
            else:
                from sage.modules.free_module import FreeModule
                dense_free_module = FreeModule(self.parent().base_ring(), len(order))
            # We slightly break encapsulation for speed reasons
            return dense_free_module.element_class(dense_free_module,
                                                   self.dense_coefficient_list(order),
                                                   coerce=True, copy=False)

    class MorphismMethods:
        def matrix(self, base_ring=None, side="left"):
            r"""
            Return the matrix of this morphism in the distinguished
            bases of the domain and codomain.

            INPUT:

            - ``base_ring`` -- a ring (default: ``None``, meaning the
              base ring of the codomain)

            - ``side`` -- "left" or "right" (default: "left")

            If ``side`` is "left", this morphism is considered as
            acting on the left; i.e. each column of the matrix
            represents the image of an element of the basis of the
            domain.

            The order of the rows and columns matches with the order
            in which the bases are enumerated.

            .. SEEALSO:: :func:`Modules.WithBasis.ParentMethods.module_morphism`

            EXAMPLES::

                sage: # needs sage.modules
                sage: X = CombinatorialFreeModule(ZZ, [1,2]); x = X.basis()
                sage: Y = CombinatorialFreeModule(ZZ, [3,4]); y = Y.basis()
                sage: phi = X.module_morphism(on_basis={1: y[3] + 3*y[4],
                ....:                                   2: 2*y[3] + 5*y[4]}.__getitem__,
                ....:                         codomain=Y)
                sage: phi.matrix()
                [1 2]
                [3 5]
                sage: phi.matrix(side="right")
                [1 3]
                [2 5]

                sage: phi.matrix().parent()                                             # needs sage.modules
                Full MatrixSpace of 2 by 2 dense matrices over Integer Ring
                sage: phi.matrix(QQ).parent()                                           # needs sage.modules
                Full MatrixSpace of 2 by 2 dense matrices over Rational Field

            The resulting matrix is immutable::

                sage: phi.matrix().is_mutable()                                         # needs sage.modules
                False

            The zero morphism has a zero matrix::

                sage: Hom(X, Y).zero().matrix()                                         # needs sage.modules
                [0 0]
                [0 0]

            .. TODO::

                Add support for morphisms where the codomain has a
                different base ring than the domain::

                    sage: Y = CombinatorialFreeModule(QQ, [3,4]); y = Y.basis()         # needs sage.modules
                    sage: phi = X.module_morphism(on_basis={1: y[3] + 3*y[4],           # needs sage.modules
                    ....:                                   2: 2*y[3] + 5/2*y[4]}.__getitem__,
                    ....:                         codomain=Y)
                    sage: phi.matrix().parent()         # not implemented               # needs sage.modules
                    Full MatrixSpace of 2 by 2 dense matrices over Rational Field

                This currently does not work because, in this case,
                the morphism is just in the category of commutative
                additive groups (i.e. the intersection of the
                categories of modules over `\ZZ` and over `\QQ`)::

                    sage: phi.parent().homset_category()                                # needs sage.modules
                    Category of commutative additive semigroups
                    sage: phi.parent().homset_category()        # not implemented, needs sage.modules
                    Category of finite dimensional modules with basis over Integer Ring

            TESTS:

            Check that :issue:`23216` is fixed::

                sage: # needs sage.modules
                sage: X = CombinatorialFreeModule(QQ, [])
                sage: Y = CombinatorialFreeModule(QQ, [1,2,3])
                sage: Hom(X, Y).zero().matrix()
                []
                sage: Hom(X, Y).zero().matrix().parent()
                Full MatrixSpace of 3 by 0 dense matrices over Rational Field
            """
            if base_ring is None:
                base_ring = self.codomain().base_ring()

            on_basis = self.on_basis()
            basis_keys = self.domain().basis().keys()
            from sage.matrix.matrix_space import MatrixSpace
            if isinstance(basis_keys, list):
                nrows = len(basis_keys)
            else:
                nrows = basis_keys.cardinality()
            MS = MatrixSpace(base_ring, nrows, self.codomain().dimension())
            m = MS([on_basis(x)._vector_() for x in basis_keys])
            if side == "left":
                m = m.transpose()
            m.set_immutable()
            return m

        def __invert__(self):
            """
            Return the inverse morphism of ``self``.

            This is achieved by inverting the ``self.matrix()``.
            An error is raised if ``self`` is not invertible.

            EXAMPLES::

                sage: # needs sage.modules
                sage: category = FiniteDimensionalModulesWithBasis(ZZ)
                sage: X = CombinatorialFreeModule(ZZ, [1,2], category=category); X.rename("X"); x = X.basis()
                sage: Y = CombinatorialFreeModule(ZZ, [3,4], category=category); Y.rename("Y"); y = Y.basis()
                sage: phi = X.module_morphism(on_basis={1: y[3] + 3*y[4], 2: 2*y[3] + 5*y[4]}.__getitem__,
                ....:                         codomain=Y, category=category)
                sage: psi = ~phi
                sage: psi
                Generic morphism:
                  From: Y
                  To:   X
                sage: psi.parent()
                Set of Morphisms from Y to X in Category of finite dimensional modules with basis over Integer Ring
                sage: psi(y[3])
                -5*B[1] + 3*B[2]
                sage: psi(y[4])
                2*B[1] - B[2]
                sage: psi.matrix()
                [-5  2]
                [ 3 -1]
                sage: psi(phi(x[1])), psi(phi(x[2]))
                (B[1], B[2])
                sage: phi(psi(y[3])), phi(psi(y[4]))
                (B[3], B[4])

            We check that this function complains if the morphism is not invertible::

                sage: phi = X.module_morphism(on_basis={1: y[3] + y[4], 2: y[3] + y[4]}.__getitem__,                    # needs sage.modules
                ....:                         codomain=Y, category=category)
                sage: ~phi                                                              # needs sage.modules
                Traceback (most recent call last):
                ...
                RuntimeError: morphism is not invertible

                sage: phi = X.module_morphism(on_basis={1: y[3] + y[4], 2: y[3] + 5*y[4]}.__getitem__,                  # needs sage.modules
                ....:                         codomain=Y, category=category)
                sage: ~phi                                                              # needs sage.modules
                Traceback (most recent call last):
                ...
                RuntimeError: morphism is not invertible
            """
            mat = self.matrix()
            try:
                inv_mat = mat.parent()(~mat)
            except (ZeroDivisionError, TypeError):
                raise RuntimeError("morphism is not invertible")
            return self.codomain().module_morphism(
                matrix=inv_mat,
                codomain=self.domain(), category=self.category_for())

        def kernel_basis(self):
            """
            Return a basis of the kernel of ``self`` in echelon form.

            EXAMPLES::

                sage: SGA = SymmetricGroupAlgebra(QQ, 3)                                # needs sage.groups sage.modules
                sage: f = SGA.module_morphism(lambda x: SGA(x**2), codomain=SGA)        # needs sage.groups sage.modules
                sage: f.kernel_basis()                                                  # needs sage.groups sage.modules
                ([1, 2, 3] - [3, 2, 1], [1, 3, 2] - [3, 2, 1], [2, 1, 3] - [3, 2, 1])
            """
            return tuple(map( self.domain().from_vector,
                              self.matrix().right_kernel_matrix().rows() ))

        def kernel(self):
            """
            Return the kernel of ``self`` as a submodule of the domain.

            EXAMPLES::

                sage: # needs sage.groups sage.modules
                sage: SGA = SymmetricGroupAlgebra(QQ, 3)
                sage: f = SGA.module_morphism(lambda x: SGA(x**2), codomain=SGA)
                sage: K = f.kernel()
                sage: K
                Free module generated by {0, 1, 2} over Rational Field
                sage: K.ambient()
                Symmetric group algebra of order 3 over Rational Field
            """
            D = self.domain()
            return D.submodule(self.kernel_basis(), already_echelonized=True,
                               category=self.category_for())

        def image_basis(self):
            """
            Return a basis for the image of ``self`` in echelon form.

            EXAMPLES::

                sage: SGA = SymmetricGroupAlgebra(QQ, 3)                                # needs sage.groups sage.modules
                sage: f = SGA.module_morphism(lambda x: SGA(x**2), codomain=SGA)        # needs sage.groups sage.modules
                sage: f.image_basis()                                                   # needs sage.groups sage.modules
                ([1, 2, 3], [2, 3, 1], [3, 1, 2])
            """
            C = self.codomain()
            return tuple(C.echelon_form( map(self, self.domain().basis()) ))

        def image(self):
            """
            Return the image of ``self`` as a submodule of the codomain.

            EXAMPLES::

                sage: SGA = SymmetricGroupAlgebra(QQ, 3)                                # needs sage.groups sage.modules
                sage: f = SGA.module_morphism(lambda x: SGA(x**2), codomain=SGA)        # needs sage.groups sage.modules
                sage: f.image()                                                         # needs sage.groups sage.modules
                Free module generated by {0, 1, 2} over Rational Field
            """
            C = self.codomain()
            return C.submodule(self.image_basis(), already_echelonized=True,
                               category=self.category_for())

    class TensorProducts(TensorProductsCategory):

        def extra_super_categories(self):
            """
            Implement the fact that a (finite) tensor product of
            finite dimensional modules is a finite dimensional module.

            EXAMPLES::

                sage: C = ModulesWithBasis(ZZ).FiniteDimensional().TensorProducts()
                sage: C.extra_super_categories()
                [Category of finite dimensional modules with basis over Integer Ring]
                sage: C.FiniteDimensional()
                Category of tensor products of
                 finite dimensional modules with basis over Integer Ring

            """
            return [self.base_category()]
