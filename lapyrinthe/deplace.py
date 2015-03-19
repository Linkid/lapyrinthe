#!/usr/bin/python
#-*-coding: utf-8 -*-

#       deplace.py
#       
#       Copyright 2008 François Magimel, aka Linkid <cucumania@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from Tkinter import *
import tkMessageBox
import os, sys
import gettext, locale #for translation
import decode

def gauche(root, can, pion, event=None):
	"""Move the pawn towards the left"""
	global mvt
	can.move(pion, -25, 0)
	mvt += 1
	print mvt
	#print can.find_closest(can.bbox(pion)[0], can.bbox(pion)[1], 5)
	x1, y1 = decode.DepFin[1][0], decode.DepFin[1][1]
	unbord(root, can, pion)
	actu(root, can, pion)
	#if ((can.bbox(pion)[0] == x1+20) and (can.bbox(pion)[1]==y1-1)):
		#print "FI"
		#unfin(root)
	
def droite(root, can, pion, event=None):
	"""Move the pawn towards the right"""
	global mvt
	can.move(pion, 25, 0)
	mvt += 1
	print mvt
	x1, y1 = decode.DepFin[1][0], decode.DepFin[1][1]
	unbord(root, can, pion)
	actu(root, can, pion)
	#if ((can.bbox(pion)[0] == x1+20) and (can.bbox(pion)[1]==y1-1)):
		#print "FI"
		#unfin(root)

def haut(root, can, pion, event=None):
	"""Move the pawn upwards"""
	global mvt
	can.move(pion, 0, -30)
	mvt += 1
	print mvt
	x1, y1 = decode.DepFin[1][0], decode.DepFin[1][1]
	unbord(root, can, pion)
	actu(root, can, pion)
	#if ((can.bbox(pion)[0] == x1+20) and (can.bbox(pion)[1]==y1-1)):
		#print "FI"
		#unfin(root)

def bas(root, can, pion, event=None):
	"""Move the pawn downwards"""
	global mvt
	can.move(pion, 0, 30)
	mvt += 1
	print mvt
	x1, y1 = decode.DepFin[1][0], decode.DepFin[1][1]
	unbord(root, can, pion)
	actu(root, can, pion)
	#if ((can.bbox(pion)[0] == x1+1) and (can.bbox(pion)[1]==y1-20)):
		#print "FI"
		#unfin(root)

def propers(root, can, pion, dir, prop):
	"""Move the pawn thanks to propellers"""
	global mvt
	if dir == "pleft":
		can.move(pion, -25, 0)
	if dir == "pright":
		can.move(pion, 25, 0)
	if dir == "pup":
		can.move(pion, 0, -30)
	if dir == "pdown":
		can.move(pion, 0, 30)
	mvt += 1
	print mvt
	finden2 = can.find_overlapping(can.bbox(pion)[0], can.bbox(pion)[1], can.bbox(pion)[2], can.bbox(pion)[3])
	getings2 = can.gettags(finden2[0])
	if (len(finden2) > 1 and len(getings2) > 0):
		if (getings2[0] != "stop" and getings2[0] not in prop):
			can.after(100, propers, root, can, pion, dir, prop)
		if (getings2[0] in prop):
			dir = getings2[0]
			can.after(100, propers, root, can, pion, dir, prop)
		if (getings2[0] == "stop"):
			unbord(root, can, pion)
	else:
		can.after(100, propers, root, can, pion, dir, prop)
		

def actu(root, can, pion):
	"""Manage the pawn position : telep, redep, oneway, key, propellers"""
	finden = can.find_overlapping(can.bbox(pion)[0], can.bbox(pion)[1], can.bbox(pion)[2], can.bbox(pion)[3])
	getings = can.gettags(finden[0]) ## We are sure there is at least one item in finden : the pawn !
	way = ["Left", "Right", "Up", "Down"]
	prop = ["pleft", "pright", "pup", "pdown"]
	unb = 0
	if (len(finden) > 1 and len(getings) > 0):
		if (can.type(finden[0]) == "line" and getings[0] == "End"):
			## The End
			unfin(root)
		if (can.type(finden[0]) == "line" and getings[0] in way):
			## One Way
			for i in way:
				if i != getings[0]:
					root.unbind('<%s>' %i)
		if (can.type(finden[0]) == "oval"):
			## Teleportors
			new_coord = decode.Telep[int(getings[0])][int(getings[1])]
			can.after(200, can.coords, pion, new_coord[0]-1, new_coord[1]-1, new_coord[2]+1, new_coord[3]+1)
			#can.coords(pion, new_coord[0]-1, new_coord[1]-1, new_coord[2]+1, new_coord[3]+1)
			unb = 1 ## for unbinding
		if (can.type(finden[0]) == "image" and getings[0] == "redep"):
			## Redep
			can.after(200, can.coords, pion, decode.DepFin[0][0]-4,decode.DepFin[0][1], decode.DepFin[0][0]+11,decode.DepFin[0][1]+15)
			unb = 1 ## for unbinding
		if (can.type(finden[0]) == "image" and getings[0] == "key_r"):
			## Key
			can.delete("Wall_r")
			can.delete("key_r")
		if (can.type(finden[0]) == "line" and getings[0] in prop):
			## Propellers
			pdir = getings[0]
			root.unbind('<Left>')
			root.unbind('<Right>')
			root.unbind('<Up>')
			root.unbind('<Down>')
			can.after(200, propers, root, can, pion, pdir, prop)
	if unb == 1:
		can.after(200, unbord, root, can, pion) ## if after in teleportor
		#unbord(root, can, pion) ## if can.coords in teleportor

def unbord(root, can, pion):
	"""Manage contact with walls"""
	try:
		if can.type(can.find_overlapping(can.bbox(pion)[0]-10,can.bbox(pion)[1]-1, can.bbox(pion)[0],can.bbox(pion)[1])[0]) == "line":
			root.unbind('<Left>')
			#root.bind('<Left>', lambda event: gauche(root, can, pion)) ## => for tests
		else: root.bind('<Left>', lambda event: gauche(root, can, pion))
	except: root.bind('<Left>', lambda event: gauche(root, can, pion))
	
	try:
		if can.type(can.find_overlapping(can.bbox(pion)[2],can.bbox(pion)[3], can.bbox(pion)[2]+8,can.bbox(pion)[3]+1)[0]) == "line":
			root.unbind('<Right>')#+10
			#root.bind('<Right>', lambda event: droite(root, can, pion)) ## => for tests
		else: root.bind('<Right>', lambda event: droite(root, can, pion))
	except: root.bind('<Right>', lambda event: droite(root, can, pion))
	
	try:
		if can.type(can.find_overlapping(can.bbox(pion)[0]-1,can.bbox(pion)[1]-8, can.bbox(pion)[0],can.bbox(pion)[1])[0]) == "line":
			root.unbind('<Up>')#-15 => -8
		else: root.bind('<Up>', lambda event: haut(root, can, pion))
	except: root.bind('<Up>', lambda event: haut(root, can, pion))
	
	try:
		if can.type(can.find_overlapping(can.bbox(pion)[2],can.bbox(pion)[3], can.bbox(pion)[2]+1,can.bbox(pion)[3]+15)[0]) == "line":
			root.unbind('<Down>')
		else: root.bind('<Down>', lambda event: bas(root, can, pion))
	except: root.bind('<Down>', lambda event: bas(root, can, pion))
		
def unfin(root):
	root.unbind('<Left>')
	root.unbind('<Right>')
	root.unbind('<Up>')
	root.unbind('<Down>')
	root.bell()
	tkMessageBox.showwarning("", _("Bravo ! You have at last found the exit !\n")+
						_("You have moved yourself %d time(s)") %mvt)
	print _("The end")


global pathdir
global mvt
mvt = 0

try :
	pathdir = os.path.dirname(sys.argv[0])
except:
	pathdir = '.'

# translations Folder
localdir = os.path.abspath(pathdir) + "/locale"
gettext.install("messages", localdir)
