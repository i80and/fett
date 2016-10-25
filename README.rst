.. |travis| image:: https://travis-ci.org/i80and/fett.svg?branch=master
            :target: https://travis-ci.org/i80and/fett

=============
Fett |travis|
=============

Overview
--------

Example
-------

.. code-block:: python

   import fett

   fett.Template('''{{ for customer in customers }}
   {{ if i even }}
   Even: {{ customer.name }}
   {{ else }}
   Odd: {{ customer.name }}
   {{ end }}
   {{ else }}
   No customers :(
   {{ end }}''').render({'customers': [
       {'name': 'Bob'},
       {'name': 'Elvis'},
       {'name': 'Judy'}
   ]})

Syntax
------

==========================================   ===========
Tag Format                                   Description
==========================================   ===========
``{{ <expression> }}``                       `Substitution <subsblock>`_
``{{ if <expression> }}``                    `Conditional <ifblock>`_
``{{ for <expression> in <expression> }}``   `Loop <forblock>`_
``{{ else }}``
``{{ end }}``                                Block termination
``{{ # <comment> }}``                        `Comment <comment>`_
==========================================   ===========

Spaces between tag opening/closing delimiters are optional.

Expressions
~~~~~~~~~~~

An **expression** is given for `substitutions <subsblock>`,
`conditionals <ifblock>`, and `loops <forblock>`.

Expressions take the following form:

``<name>[.<subfield>...] [<filter> [<filter2>...]]``

You can use **filters** to modify a single value in simple ways. For example,
the loop iteration counter ``i`` counts from ``0``, but users often wish to
count from ``1``. You can obtain a count-from-1 value with the expression
``i inc``.

The full list of available filters follows.

===========  ======
Filter Name  Effect
===========  ======
odd          Returns true iff its input is representable as an odd integer.
even         Returns true iff its input is representable as an even integer.
car          Returns the first element of a list.
cdr          Returns all but the first element of a list.
len          Returns the length of a list.
strip        Returns the input string with surrounding whitespace removed.
inc          Increments a value representable as an integer by one.
not          Returns the inverse of a boolean.
===========  ======

.. _subsblock:

Substitutions
~~~~~~~~~~~~~

.. _ifblock:

Conditionals
~~~~~~~~~~~~

.. _forblock:

Loops
~~~~~

.. _comment:

Comments
~~~~~~~~
