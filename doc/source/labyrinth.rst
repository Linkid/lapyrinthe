Labyrinths
==========

Location
--------

Mazes are in the folder ``labyrintheque``.


Levels
------

There are 5 levels, from A to E:

* level A (easy): the easiest one, with no obstacles.
* level B (medium): with special objects (teleporters, one-way, return to the
  beginning)
* level C (medium): the same as level B
* level D (medium): the same as level B
* level E (hard): with more special objects (propellers, stop)


Symbols
-------

================================= ======================== ===========
Symbol                            Name                     Level
================================= ======================== ===========
.. image:: _static/deb1.gif       Start                    All
.. image:: _static/fin1.gif       End                      All
.. image:: _static/telep.gif      Teleporter [#teleport]_  B, C, D, E
.. image:: _static/oneway1.gif    One-way                  B, C, D, E
.. image:: _static/croix_dep0.gif Return to the beginning  B, C, D, E
.. image:: _static/cle_r.gif      Key [#key]_              B, C, D, E
.. image:: _static/propR.gif      Propeller [#propeller]_  E
.. image:: _static/carres0.gif    Stop [#stop]_            E
================================= ======================== ===========

.. rubric:: Footnotes

.. [#teleport] Teleport the pawn to the teleporter's twin
.. [#key] The key is to open a red wall
.. [#propeller] Go through every obstacle (teleporter, one-way, wall) to one direction
.. [#stop] Stop the propelled pawn


Legend
------

Each symbol is separated by ``,``.

For every symbol with 4 possibilities, the order is: left, right, up, down.

For wall, the order is: vertical, horizontal.

======================== ========================== ==========
Symbol                   Legend                     Level
======================== ========================== ==========
Start / End              ``A``, ``B``, ``C``, ``D`` All
Empty                    ``.``                      All
Wall                     ``|`` or ``-``             All
Teleporter               integer                    B, C, D, E
One-way                  ``W``, ``X``, ``Y``, ``Z`` B, C, D, E
Return to the beginning  ``*``                      B, C, D, E
Key                                                 B, C, D, E
Propeller                ``G``, ``H``, ``I``, ``J`` E
Stop                     ``K``                      E
======================== ========================== ==========
