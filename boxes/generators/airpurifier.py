#!/usr/bin/env python3
# Copyright (C) 2013-2016 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *

class AirPurifier(Boxes):
    """Housing for the Nukit Open Air Purifier"""

    ui_group = "Unstable" # see ./__init__.py for names

    description = """Still untested"""
    
    def __init__(self) -> None:
        Boxes.__init__(self)


        self.addSettingsArgs(edges.FingerJointSettings)
        
        self.buildArgParser(x=500., y=500.)

        self.argparser.add_argument(
            "--filter_height",  action="store", type=float, default=45.,
            help="height of the filter along the flow direction (in mm)")
        self.argparser.add_argument(
            "--rim",  action="store", type=float, default=40.,
            help="rim around the filter holing it in place (in mm)")
        self.argparser.add_argument(
            "--fan_diameter",  action="store", type=float, default=120.,
            help="diameter of the fans (in mm)")
        self.argparser.add_argument(
            "--filters",  action="store", type=int, default=2,
            choices=(1, 2),
            help="")
        self.argparser.add_argument(
            "--sides_with_fans",  action="store", type=int, default=1,
            choices=(0, 1, 2, 3, 4),
            help="how many side should have fan holes")

    def fanCB(self, n, h, l, fingerHoles=True):
        fh = self.filter_height
        t = self.thickness
        def cb():
            if fingerHoles:
                self.fingerHolesAt(0, fh + t/2, l, 0)
                if self.filters > 1:
                    self.fingerHolesAt(0, h- fh - t/2, l, 0)
            if n > self.sides_with_fans:
                return
            x = self.fan_diameter/2 + (l % self.fan_diameter) / 2 
            for i in range(int(l // self.fan_diameter)):
                self.hole(x+i*self.fan_diameter, h/2, d=self.fan_diameter)

        return cb

    def render(self):
        x, y, d = self.x, self.y, self.fan_diameter
        t = self.thickness

        fh = self.filter_height
        h = d + self.filters * (fh + t)

        edge = edges.CompoundEdge(self, "eFe", (fh + t, d, fh + t))
        
        self.rectangularWall(x, d, "ffff", callback=[
            self.fanCB(4, d, x, False)], move="up")
        self.rectangularWall(x, h, "ffff", callback=[
            self.fanCB(3, h, x)], move="up")

        for _ in range(2):
            self.rectangularWall(y, h, ["f", "h", "f", edge],
                                 callback=[self.fanCB(_+1, h, y)], move="up")

        r = 40.0
        self.rectangularWall(x, y, "ehhh", callback=[
            lambda:self.rectangularHole(x/2, y/2, x - r, y - r, r=10)], move="up")
        self.rectangularWall(x, y, "Ffff", callback=[
            lambda:self.rectangularHole(x/2, y/2, x - r, y - r, r=10)], move="up")
        if self.filters==2:
            self.rectangularWall(x, y, "Ffff", callback=[
                lambda:self.rectangularHole(x/2, y/2, x - r, y - r, r=10)], move="up")
            self.rectangularWall(x, y, "ehhh", callback=[
                lambda:self.rectangularHole(x/2, y/2, x - r, y - r, r=10)], move="up")
        else:
            self.rectangularWall(x, y, "hhhh", move="up")
