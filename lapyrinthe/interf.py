#!/usr/bin/python
# -*-coding: utf-8 -*-

# interf.py
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
import tkFileDialog as Selector
import tkMessageBox
import os
import sys
import gettext
import locale
import webbrowser
import decode
import deplace

__version__ = "0.5.08.07"
__aprog__ = "François Magimel (Linkid)"
__ainvent__ = "Deletre Matthieu"


class AutoScrollbar(Scrollbar):
    """Show or not Canvas'Scrollbars"""
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
            Scrollbar.set(self, lo, hi)


class Interface:
    """Graphical User Interface (GUI)"""
    def __init__(self, root):
        self.root = root  # we preserve root
        self.pion = IntVar()
        self.lang_cho = StringVar()
        self.crinter()  # call the def crinter

    def crinter(self):
        global programDir
        # Images
        try:
            self.iiii = os.path.join(programDir, 'images')
        except:
            pass
        try:
            self.icon_help = PhotoImage(file=os.path.join(self.iiii, 'help-browser.gif')) # 16x16
            self.icon_about = PhotoImage(file=os.path.join(self.iiii, 'gtk-about.gif')) # 16x16
            self.icon_op = PhotoImage(file=os.path.join(self.iiii, 'document-open.gif')) # 16x16
            self.icon_quit = PhotoImage(file=os.path.join(self.iiii, 'application-exit.gif')) # 16x16
            self.icon_cred = PhotoImage(file=os.path.join(self.iiii, 'info-i.gif')) # 24x24
            self.icon_ferm = PhotoImage(file=os.path.join(self.iiii, 'gtk-close.gif')) # 24x24
            self.iredep = PhotoImage(file=os.path.join(self.iiii, 'croix_dep.gif')) # 18x18
            self.keyy = PhotoImage(file=os.path.join(self.iiii, 'cle_r.gif')) # 18x10
            self.stopt = PhotoImage(file=os.path.join(self.iiii, 'carres.gif')) #18x16
        except:
            self.icon_help = ''
            self.icon_about = ''
            self.icon_op = ''
            self.icon_quit = ''
            self.icon_cred = ''
            self.icon_ferm = ''
            self.iredep = ''
            self.keyy = ''
            self.stopt = ''

        # Menus
        self.crea_men()

        # Scrollbar
        self.vscroll = AutoScrollbar(self.root, orient=VERTICAL)  ## Vertical scrollbar creation
        self.hscroll = AutoScrollbar(self.root, orient=HORIZONTAL)  ## Horizontal scrollbar creation
        haut = self.root.winfo_screenheight() / 1.3

        # Canvas
        self.can0 = Canvas(self.root, bg="white", height=haut, width=550, xscrollcommand=self.hscroll.set, yscrollcommand=self.vscroll.set)  ## creation canvas
        self.can0.grid(row=0, column=0, sticky=N+S+E+W) ## show canvas
        self.vscroll.config(command=self.can0.yview)  ## link canvas/scrollbar (vertical)
        self.hscroll.config(command=self.can0.xview)  ## link canvas/scrollbar (horizontal)
        self.vscroll.grid(row=0, column=1, sticky=N+S)  ## show vscroll
        self.hscroll.grid(row=1, column=0, sticky=E+W)  ## show hscroll

        self.root.geometry("580x%d" %haut)
        self.can0.config(scrollregion=self.can0.bbox("all")) ## show scrollbars if needed

        self.root.bind_all("<Control-o>", self.op)
        self.root.bind_all('<F1>', self.help_)
        self.root.update()
        self.root.rowconfigure(0,weight=1)
        self.root.columnconfigure(0,weight=1)

    def crea_men(self):
        """Create menus (File, ...)"""
        lang_op = [["Arabic","ar"], ["Danish","da"], ["English","en"], ["French","fr"], ["German","de"], ["Hebrew","he"], ["Brazilian Portuguese","pt_BR"]]
        lang_op += [["Russian","ru"], ["Slovak","sk"]]

        self.menubar = Menu(self.root, relief=GROOVE)
        self.root.config(menu=self.menubar)

        self.filem = Menu(self.menubar, tearoff=1, relief=GROOVE)
        self.menubar.add_cascade(label=_("File"), menu=self.filem)
        self.filem.add_command(compound=LEFT, image=self.icon_op, label=_("Open"), underline=0, command=self.op, accelerator="Ctrl+O")
        self.filem.add_separator()
        self.filem.add_command(compound=LEFT, image=self.icon_quit, label=_("Quit"), underline=0, command=self.root.destroy, accelerator="Alt+F4") ##destroy => quit

        self.optionsm = Menu(self.root, tearoff=1, relief=GROOVE)
        self.menubar.add_cascade(label=_("Options"), menu=self.optionsm)
        self.languagem = Menu(self.optionsm, tearoff=0, relief=GROOVE)
        self.optionsm.add_cascade(label=_("Language"), menu=self.languagem)
        for i in lang_op:
            self.languagem.add_radiobutton(label=_(i[0]), variable=self.lang_cho, value=i[1], command=self.change_lang)

        self.helpm = Menu(self.root, tearoff=0, relief=GROOVE)
        self.menubar.add_cascade(label=_("Help"), menu=self.helpm)
        self.helpm.add_command(compound=LEFT, image=self.icon_help, label=_("Help (French)"), underline=0, command=self.help_, accelerator="F1")
        self.helpm.add_separator()
        self.helpm.add_command(compound=LEFT, image=self.icon_about, label=_("About..."), underline=2, command=self.about)

    def op(self, event=None):
        """Open a file"""
        self.can0.delete(ALL)
        txt_op = ''
        decode.DepFin = []
        deplace.mvt = 0
        formats = [(_('Text file'), '*.txt')]
        file_op = Selector.askopenfilename(filetypes=formats)
        try:
            # tout cela, on pourrait le mettre dans decode... nan ?
            titre = "- " + os.path.basename(file_op[:file_op.index(".")]) ## Keep the file name in memory...
            file_op = open(os.path.join(file_op))
            numline = 1
            self.root.bind('<Left>', lambda event: deplace.gauche(self.root, self.can0, self.pion))
            self.root.bind('<Right>', lambda event: deplace.droite(self.root, self.can0, self.pion))
            self.root.bind('<Up>', lambda event: deplace.haut(self.root, self.can0, self.pion))
            self.root.bind('<Down>', lambda event: deplace.bas(self.root, self.can0, self.pion))
            for line in file_op.readlines():
                decode.lecture(line, self.root, self.can0, numline, self.iredep, self.keyy, self.stopt)
                numline += 1
            file_op.close()
            print decode.DepFin
            self.x0, self.y0 = decode.DepFin[0][0], decode.DepFin[0][1]
            self.pion = self.can0.create_oval(self.x0-4,self.y0, self.x0+11,self.y0+15, fill="red")
        except:
            titre = ""
            pass
        self.can0.config(scrollregion=self.can0.bbox("all"))  # show scrollbars if needed
        self.root.title('Lapyrinthe %s' % titre)

    def about(self):
        """Mini window"""
        t0 = Toplevel()
        #t0.geometry("310x150")
        t0.title(_("About Lapyrinthe"))

        txt_titre = Label(t0, text='Lapyrinthe %s' %__version__, font=("Arial", 20, "bold"))
        txt_descr = Label(t0, text=_("Lapyrinthe is a reflexion game\n") +
                _("made up of several levels."), font=("Arial", 10))
        txt_copy = Label(t0, text=_("Copyright %s 2008 The Lapyrinthe Authors") %"©", font=("Arial", 9))
        txt_titre.grid(row=0, column=0, sticky=N+S+E+W, columnspan=3)
        txt_descr.grid(row=1, column=0, sticky=N+S+E+W, columnspan=3)
        txt_copy.grid(row=2, column=0, sticky=N+S+E+W, columnspan=3)

        btn_cred = Button(t0, compound=LEFT, image=self.icon_cred, text=_("Credits"), command=self.credit, height=24)
        btn_lic = Button(t0, compound=LEFT, bitmap='info', text=_("License"), command=self.licence, height=24)
        btn_quit = Button(t0, compound=LEFT, image=self.icon_ferm, text=_("Close"), command=t0.destroy, height=24)
        btn_cred.grid(row=4, column=0, sticky=W, padx=5)
        btn_lic.grid(row=4, column=1, pady=5)
        btn_quit.grid(row=4, column=2, sticky=E, padx=5)

        t0.grid_columnconfigure(1, weight=1)

    def licence(self):
        """License"""
        global programDir
        global lang
        txt_licence = _('''This program is free software; you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation; either version 2 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program; if not, write to the Free Software
        Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
        MA 02110-1301, USA.\n\n''')

        try:
            dirhel = os.path.join(programDir, 'Help')
            if lang[:2] == "fr":
                file_licence = open(os.path.join(dirhel, 'COPYING_fr'))
            else:
                file_licence = open(os.path.join(dirhel, 'COPYING'))
            for line in file_licence.readlines():
                txt_licence += line
            file_licence.close()
        except:
            pass

        t_lic = Toplevel()
        t_lic.title = "License"
        sc1 = Scrollbar(t_lic, orient=VERTICAL)
        #sc2 = Scrollbar(t_lic, orient=HORIZONTAL)
        txt_0 = Text(t_lic, wrap=None, bg="white")
        txt_0.insert(END, '\n')
        txt_0.insert(END, txt_licence)
        txt_0.insert(END, '\n')
        sc1.config(command=txt_0.yview)
        #sc2.config(command=txt_0.xview)
        txt_0.config(yscrollcommand=sc1.set, state=DISABLED)
        btn_quit = Button(t_lic, compound=LEFT, image=self.icon_ferm,
                          text=_("Close"), command=t_lic.destroy)

        txt_0.grid(row=0, column=0)
        sc1.grid(row=0, column=1, sticky=S + N)
        #sc2.grid(row=1, column=0, sticky=W+E)
        btn_quit.grid(row=3, sticky=E, pady=5)

    def credit(self):
        """Credits"""
        t_cred = Toplevel()
        t_cred.title = "Credits"
        txt_0 = Label(t_cred, text=_("Program coded by: %s" % __aprog__))
        txt_1 = Label(t_cred, text=_("Game invented by: %s" % __ainvent__))
        txt_2 = Label(t_cred, text=_("And a big thanks to the translators"))
        btn_quit = Button(t_cred, compound=LEFT, image=self.icon_ferm,
                          text=_("Close"), command=t_cred.destroy)
        txt_0.grid(row=0, pady=10)
        txt_1.grid(row=1, padx=10)
        txt_2.grid(row=2, pady=10)
        btn_quit.grid(row=3, pady=10)

    def help_(self, event=None):
        """ Doc """
        global programDir
        try:
            dirhel = os.path.join(programDir, 'Help')
            help_fi = os.path.join(dirhel, 'help.html')
            webbrowser.open(help_fi)
        except:
            self.root.bell()
            tkMessageBox.showerror("", _("Help file not found"))

    def change_lang(self):
        global localdir
        global lang
        lang = self.lang_cho.get()
        lang1 = gettext.translation('messages', localedir=localdir, languages=[lang], fallback=True)
        lang1.install()
        self.crea_men()


def main():
    root = Tk()
    root.title('Lapyrinthe')
    root.config(bg="grey")
    app = Interface(root)
    root.mainloop()
    root.quit()


if __name__ == "__main__":
    global programDir
    global localdir
    global lang
    lang = locale.getdefaultlocale()[0][:2]

    try:
        programDir = os.path.dirname(sys.argv[0])
    except:
        programDir = '.'

    # translations Folder
    localdir = os.path.abspath(programDir) + "/locale"
    gettext.install("messages", localdir)
    main()
