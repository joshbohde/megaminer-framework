# -*- coding: utf-8 -*-
"""

   Copyright (C) 2008 by Steven Wallace
   snwallace@gmail.com

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the
    Free Software Foundation, Inc.,
    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 """
from __future__ import with_statement
from networking.Server import *
from networking.Filter import *
from config import getUserInfo

import traceback

import lexpr.sexpr as sexpr
import lexpr.Statements as Statements
import lexpr.ServerStatements as ServerStatements
import threading
import sys
import time
import getopt
import threading
import itertools
from optparse import OptionParser


LOGIN_CONFIG = 'config/login.cfg'

class LogicFilter(Filter):
    ID = 0
    def _init(self, *args):
        self.user = None
        self.screenName = None
        self.password = None
        self.hash = None
        self.game = None
        self.type = None
        self.hasMap = None
        self.ID = str(LogicFilter.ID)
        LogicFilter.ID += 1
        self.run = True

    def writeSExpr(self, l):
        self.writeOut(sexpr.sexpr2str(l))

    def _readOut(self, data):
        try:
            self.readSExpr(sexpr.str2sexpr(data))
        except ValueError:
            self.writeSExpr(['malformed-message', data])

    def disconnect(self):
        self.run = False
        if self.game:
            pass
            #self.readSExpr("(leave-game)")

    def readSExpr(self, expression):
        for i in expression:
            self.evalStatement(i)

    def evalStatement(self, expression):
        if type(expression) != list:
            self.writeSExpr(['invalid-expression', expression])
            return False
        try:
            self.statements[expression[0]](self, expression)
        except Exception, e:
            print e
            self.writeSExpr(['malformed-statement', expression])

    def login(self, user, password):
        registered = False
        output = ""
        userInfo = getUserInfo(user, LOGIN_CONFIG)

        if not (userInfo is None):
            if userInfo['password'] == password:
                registered = True
                self.user = user
                self.password = password
                self.screenName = userInfo['screenName']

        if not registered:
            output = "user    :" + user + '\n'
            output += "password:" + password + '\n\n'
            outFile = open("badLogin.dat", "a")
            outFile.write(output)
            outFile.close()

        return registered

    def logout(self):
        self.user = None
        self.password = None
        self.hash = None
        return True

class MasterFilter(LogicFilter):
    Servers = {}

    def _init(self):
        LogicFilter._init(self)
        self.statements = ServerStatements.statements
        self.count = 0

    def disconnect(self):
        if self.ID:
            try:
                del MasterFilter.Servers[self.ID]
            except Exception:
                pass
            self.ID = None
        LogicFilter.disconnect(self)

    def registerAsServer(self):
        MasterFilter.Servers[self.ID] = self

    def getServers(self):
        return [[i, j.address] for i,j in MasterFilter.Servers.iteritems()]

    def chooseServer(self):
        return [[i,j.address] for i, j in itertools.islice(MasterFilter.Servers.iteritems(), 1)]

class SlaveFilter(LogicFilter):
    def _init(self):
        self.logged_in = False
        LogicFilter._init(self)

    def logic(self):
        self.writeSExpr(['login', 'slave', '12345'])
        while self.run:
            self.writeSExpr(['ping'])
            time.sleep(1)

def runMaster(telnet):
    try:
        print "Running master."
        filters = ([PacketizerFilter, CompressionFilter] if telnet else []) + [MasterFilter]
        master = TCPServer(19000,  *filters)
        master.run()
    except Exception, exception:
        print "runMaster - Unexpected error:", exception
        sys.exit(1)
    sys.exit(0)

def runSlave(master = ("127.0.0.1", 19000)):
    try:
        print "Running slave."
        slave = SlaveTCPServer(master, 19001,  PacketizerFilter, CompressionFilter, SlaveFilter)
        slave.run()
    except Exception, exception:
        print "runSlave - Unexpected error:", exception
        sys.exit(1)

def main():
    parser = OptionParser()
    parser.add_option("-r", "--redirect", action="store_true", dest="redirect")
    parser.add_option("-t", "--telnet-mode", action="store_false", dest="telnet", default=True)

    (options, args) = parser.parse_args()

    if options.redirect:
        runMaster(options.telnet)


if __name__ == "__main__":
    main()

