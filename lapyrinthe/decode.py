#!/usr/bin/python
# -*-coding: utf-8 -*-

# decode.py
#
# Copyright 2008 François Magimel, aka Linkid <cucumania@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

from Tkinter import *


def bar_hori(can, x, y, cara):
    """Horizontal wall"""
    ww = can.create_line(1+(25*x), 1+(15*y), 26+(25*x), 1+(15*y))
    if cara == "M":
        can.itemconfig(ww, tags=("Wall_r"), fill="red")  # aa6464


def bar_verti(can, x, y, cara):
    """Vertical wall"""
    ww = can.create_line(1+(25*x), -14+(15*y), 1+(25*x), 16+(15*y))
    if cara == "N":
        can.itemconfig(ww, tags=("Wall_r"), fill="red")


def ab(root, can, x, y, z):
    """Horizontal departure arrow
    z : variable indicating direction arrow"""
    global DepFin
    tagos = ""
    DepFin.append([-15+(25*x), -7+(15*y), 12+(25*x), 1+(15*y)])
    if (len(DepFin) == 1):
        root.unbind('<Up>')
        root.unbind('<Down>')
        if (z == "first"):
            root.unbind('<Right>')
        if (z == "last"):
            root.unbind('<Left>')
    if (len(DepFin) == 2):
        tagos = "End"
    can.create_line(-25+(25*x), 1+(15*y), 2+(25*x), 1+(15*y), arrow=z, fill="#A52A2A", tags=(tagos))  # -15+(25*x),1+(15*y), 12+(25*x),1+(15*y)


def cd(root, can, x, y, z):
    """Vertical departure arrow"""
    global DepFin
    tagos = ""
    DepFin.append([-15+(25*x), -7+(15*y), 12+(25*x), 1+(15*y)])
    if (len(DepFin) == 1):
        root.unbind('<Right>')
        root.unbind('<Left>')
        if (z == "first"):
            root.unbind('<Down>')
        if (z == "last"):
            root.unbind('<Up>')
    if (len(DepFin) == 2):
        tagos = "End"
    can.create_line(-11+(25*x), -5+(15*y), -11+(25*x), 20+(15*y), arrow=z, fill="#A52A2A", tags=(tagos))


def telo(can, cara, x, y):
    """Teleportor"""
    global Telep
    trouv, cpt = 0, 0
    nbTelep = len(Telep)
    coord = [-19+(25*x), -7+(15*y), -4+(25*x), 8+(15*y)]  # coordinate of the pawn
    ovalos = can.create_oval(-21+(25*x), -10+(15*y), -2+(25*x), 11+(15*y), fill="#E6E6FA")
    if nbTelep > 0:
        for i in Telep:
            if (len(i[1]) == 1 and i[1][0] == cara):
                i[1] = coord
                trouv = 1
                num = cpt
                break
            cpt = cpt + 1
    if trouv == 1:
        # if you find the same teleportor in Telep, then tag the new one with 0
        # print str(num)+"1", cpt, cara, 'oooo'
        can.itemconfig(ovalos, tags=(str(num), "0"))
    else:
        Telep.append([coord, [cara]])
        can.itemconfig(ovalos, tags=(str(nbTelep), "1"))
        # print nbTelep, len(Telep), cara, 'aaa', can.gettags(ovalos)


def redep(can, x, y, iredep):
    """Return to the beginning"""
    can.create_image(-12+(25*x), 2+(15*y), image=iredep, tags=("redep"))
    # can.create_polygon((40,40, 55,50, 70,40, 60,55, 70,70, 55,60, 40,70, 50,55),fill="green")


def oneway(can, x, y, caro):
    """One way direction"""
    # avant  :  W:r; X:l; Y:d; Z:u
    if caro == "W":
        # "one way : left"
        can.create_line(-24+(25*x), 1+(15*y), -1+(25*x), 1+(15*y),
                        arrow="first", width=4, fill="blue", tags=("Left"))
    if caro == "X":
        # "one way : right"
        can.create_line(-21+(25*x), 1+(15*y), 2+(25*x), 1+(15*y),
                        arrow="last", width=4, fill="blue", tags=("Right"))
    if caro == "Y":
        # "one way : up"
        can.create_line(-11+(25*x), -14+(15*y), -11+(25*x), 12+(15*y),
                        arrow="first", width=4, fill="blue", tags=("Up"))
    if caro == "Z":
        # "one way : down"
        can.create_line(-11+(25*x), -11+(15*y), -11+(25*x), 15+(15*y),
                        arrow="last", width=4, fill="blue", tags=("Down"))


def aff_key(can, x, y, keyy):
    """A key to open a way"""
    can.create_image(-12+(25*x), 2+(15*y), image=keyy, tags=("key_r"))


def stop_propulse(can, x, y, stopt):
    """Stop the pawn propeled"""
    can.create_image(-11+(25*x), 1+(15*y), image=stopt, tags=("stop"))


def propulse(can, x, y, cari):
    """Propel the pawn"""
    if cari == "G":
        # "prop : left"
        can.create_line(-11+(25*x), -5+(15*y), -21+(25*x), 1+(15*y), -11+(25*x),7+(15*y), width=2, fill="#A020F0", tags="pleft")  # gauche
        can.create_line(-3+(25*x), -5+(15*y), -13+(25*x), 1+(15*y), -3+(25*x), 7+(15*y), width=2, fill="#A020F0")  # droite
    if cari == "H":
        # "prop : right"
        can.create_line(-13+(25*x), -5+(15*y), -3+(25*x), 1+(15*y), -13+(25*x), 7+(15*y), width=2, fill="#A020F0", tags="pright")  # droite
        can.create_line(-21+(25*x), -5+(15*y), -11+(25*x), 1+(15*y), -21+(25*x), 7+(15*y), width=2, fill="#A020F0")  # gauche
    if cari == "I":
        # "prop : up"
        can.create_line(-17+(25*x), 1+(15*y), -12+(25*x), -10+(15*y), -7+(25*x), 1+(15*y), width=2, fill="#A020F0", tags="pup")  # haut B6A624
        can.create_line(-17+(25*x), 11+(15*y), -12+(25*x), 0+(15*y), -7+(25*x), 11+(15*y), width=2, fill="#A020F0")  # bas
    if cari == "J":
        # "prop : down"
        can.create_line(-17+(25*x), 0+(15*y), -12+(25*x), 11+(15*y), -7+(25*x), 0+(15*y), width=2, fill="#A020F0", tags="pdown")  # bas
        can.create_line(-17+(25*x), -10+(15*y), -12+(25*x), 1+(15*y), -7+(25*x), -10+(15*y), width=2, fill="#A020F0")  # haut

#######################################################################


def lecture(line, root, can, x, iredep, keyy, stopt):
    """Read the line"""
    k = len(line) - 1

    for i in range(k):
        # print ord(line[i]), chr(ord(line[i]))
        j = i
        if k > 30:
            j = i / 2 + 1  # the number of line must be <= 30

        if (line[i] == '-' or line[i] == 'M'):
            # print "bar_hori"
            bar_hori(can, j, x, line[i])  # ok

        if (line[i] == '|' or line[i] == 'N'):
            # print "bar_verti"
            bar_verti(can, j, x, line[i])  # ok

        if (line[i] == 'A'):
            # towards the left
            ab(root, can, j, x, 'first')

        if (line[i] == 'B'):
            # towards the right
            ab(root, can, j, x, 'last')

        if (line[i] == 'C'):
            # upwards
            cd(root, can, j, x, 'first')

        if (line[i] == 'D'):
            # downwards
            cd(root, can, j, x, 'last')

        if ((ord(line[i]) >= 48 and ord(line[i]) <= 57) or
                (ord(line[i]) >= 97 and ord(line[i]) <= 122)):
            # Teleportor
            telo(can, line[i], j, x)

        if (line[i] == '*'):
            # Return to the beginning
            redep(can, j, x, iredep)

        if (ord(line[i]) >= 87 and ord(line[i]) <= 90):
            # One way dir
            oneway(can, j, x, line[i])

        if (ord(line[i]) >= 71 and ord(line[i]) <= 74):
            # Propellers
            propulse(can, j, x, line[i])

        if (line[i] == 'L'):
            # Display a key
            aff_key(can, j, x, keyy)

        if (line[i] == 'K'):
            # Stop propellers
            stop_propulse(can, j, x, stopt)

global DepFin
global Telep

DepFin = []  # list with departure and arrival
Telep = []  # list with the teleportor's coords
