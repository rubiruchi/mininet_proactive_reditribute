#!/usr/bin/env python

import os
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading
import subprocess
from time import time, sleep

from roles import *

cfd = os.path.dirname(os.path.abspath(__file__))
resdir = os.path.normpath(os.path.join(cfd, "../resources"))

class AppProfile(object):
    def __init__(self, numNodes):
        self.numNodes = numNodes
        self.vlan = -1
        self.apps = []
        self.nodes = []

    def assignVlan(self, vlan):
        self.vlan = vlan

    def start(self):
        map(lambda p: p.init(), self.apps)
        map(lambda p: p.start(), self.apps)

    def stop(self):
        map(lambda p: p.stop(), self.apps)

    def create(self, hosts):
        pass

    def __repr__(self):
        return self.__str__()

    def check_hostlen(self, hostlen):
        if (hostlen < self.numNodes):
            print "*** Warning: {0} expects {1} nodes, {2} given".format(
                self.__class__.__name__, self.numNodes, hostlen)

class EmptyProfile(AppProfile):
    def __init__(self, numNodes):
        super(EmptyProfile, self).__init__(numNodes)

    def create(self, hosts):
        self.check_hostlen(len(hosts))
        self.nodes.extend(hosts)
        self.apps.extend([EmptyRole(h) for h in hosts])

    def __str__(self):
        return "Empty"

class IperfProfile(AppProfile):
    def __init__(self, numNodes, bw, maxFlows=12, port = 12000):
        super(IperfProfile, self).__init__(numNodes)
        self.bw = bw
        self.time=time
        self.maxFlows = maxFlows
        self.port = port

    def iperfcmd(self, h1, h2, port):
        h1srv = "iperf -s -p {0} > /dev/null &".format(port)
        h2clnt = "iperf -M 9000 -c {0} -p {1} -u -b {2}M -t {3} > /dev/null &".format(h1.IP(), port, self.bw, self.time)

        print "Iperf: {0} -> {1}".format(h1, h2)
        h1.cmd(h1srv)
        h2.cmd(h2clnt)

    def start(self):
        print 'starting tenant'
        print self.nodes
        port_start = self.port
        count = 0
        for h1 in self.nodes:
            for h2 in self.nodes:
                if h1 != h2:
                    if count < self.maxFlows:
                        self.iperfcmd(h1, h2, port_start + count)
                        count += 1

    def stop(self):
        pass

    def create(self, hosts):
        self.check_hostlen(len(hosts))
        self.nodes.extend(hosts)
        for h in hosts:
            self.apps.append(EmptyRole(h, "Iperf Client"))

    def __str__(self):
        return "Iperf ({0})".format(self.bw)


class CommandProfile(object):

    port = 10000

    def dump_flows(self, switch_str):
        return "-----------dump-flows " + switch_str + "\n" + subprocess.check_output(["ovs-ofctl","-O","OpenFlow13","dump-flows",switch_str])

    def __init__(self, net, command):
        self.net = net
        self.command = command
        self.type = command["type"].lower()
        self.begin = command["begin"]

        if self.type == 'iperf':
            self.client = net.get(command["client"])
            self.server = net.get(command["server"])
            self.bw = command["bandwidth"]
            self.duration = command["duration"]
            self.isUdp = command["udp"]
        elif self.type == 'pingall':
            pass
        elif self.type == 'dump-flows':
            self.switch_str = command["switch"]
        else:
            print 'invalid type:', self.type
            raise Exception("invalid type!")

    def iperfcmd(self):
        port = CommandProfile.port
        CommandProfile.port += 1

        srv = "iperf -s -p {0} &> iperf{0}.srv.out &".format(port)
        if self.isUdp:
            clnt = "iperf -c {0} -p {1} -u -b {2}M -t {3} &> iperf{1}.clnt.out &".format(self.server.IP(), port, self.bw, self.duration)
        else:
            clnt = "iperf -c {0} -p {1} -t {2} &> iperf{1}.clnt.out &".format(self.server.IP(), port, self.duration)

        print "Iperf: {0} -> {1}".format(self.server, self.client)
        print srv
        self.server.cmd(srv)
        print clnt
        self.client.cmd(clnt)

    def start(self):
        print 'starting tenant', self
        if self.type == 'iperf':
            self.iperfcmd()
        elif self.type == 'pingall':
            self.net.pingAll()
        elif self.type == 'dump-flows':
            print self.dump_flows(self.switch_str)
        else:
            print 'invalid type:', self.type
            raise Exception("invalid type: " + self.type)

    def stop(self):
        pass

    def create(self):
        pass

    def __str__(self):
        return "CommandProfile ({0},{1})".format(self.type, self.begin)

class HostPrograms(object):

    def __init__(self):
        self.tenants = []

    def defineHost(self, net, hosts, commands):
        print 'self.hosts',hosts
        for command in commands:
            self.tenants.append(CommandProfile(net, command))

        print 'self.tenants', self.tenants,
        for tenant in self.tenants:
            tenant.create()
