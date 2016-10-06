from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController
from mininet.cli import CLI

from time import clock, sleep
from threading import Thread
from host_type import *

import sys
import subprocess
import ast

from collections import defaultdict

def get_link_config():
    # configure link parameters
    default_link_opts = dict(bw=100, delay="2ms")
    link_config = defaultdict(lambda: defaultdict(lambda: dict(default_link_opts)))
    with open('link_config') as f:
        for line in f:
            try:
                config = ast.literal_eval(line)
            except:
                continue
            link_config[config["input_port"]][config["output_port"]] = dict(bw=config["bandwidth"], delay=str(config["latency"]) + str("ms"))

    return link_config

host_link_config = dict(bw=100, delay="2ms")
link_config = get_link_config()

class LoopyTopo(Topo):
    "Simple loop topology example."

    def __init__(self):
        "Create custom loop topo."

        # Initialize topology
        Topo.__init__(self)

        link_config = get_link_config()

        # Add hosts and switches
        ## Add hosts
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')
        host3 = self.addHost('h3')
        host4 = self.addHost('h4')
        # host5 = self.addHost('h5')
        # host6 = self.addHost('h6')
        # host7 = self.addHost('h7')
        # host8 = self.addHost('h8')

        ## Add switches
        switch1 = self.addSwitch("s1")
        switch2 = self.addSwitch("s2")
        switch3 = self.addSwitch("s3")
        switch4 = self.addSwitch("s4")

        # Add links (Use switches in the node1 parameter)
        self.addLink(switch1, host1, 1, **host_link_config)
        self.addLink(switch2, host2, 1, **host_link_config)
        self.addLink(switch3, host3, 1, **host_link_config)
        self.addLink(switch4, host4, 1, **host_link_config)
        # self.addLink(switch1, host5, 2)
        # self.addLink(switch2, host6, 2)
        # self.addLink(switch3, host7, 2)
        # self.addLink(switch4, host8, 2)

        self.addLink(switch1, switch2, 3, 3, **link_config[3][3])
        self.addLink(switch2, switch3, 4, 3, **link_config[4][3])
        self.addLink(switch2, switch4, 5, 3, **link_config[5][3])
        self.addLink(switch3, switch4, 4, 4, **link_config[4][4])

class SimpleTopo(Topo):
    "Simple loop topology example."

    def __init__(self):
        "Create custom loop topo."

        # Initialize topology
        Topo.__init__(self)

        link_config = get_link_config()

        # Add hosts and switches
        ## Add hosts
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')
        host3 = self.addHost('h3')
        ## Add switches
        switch1 = self.addSwitch("s1")
        switch2 = self.addSwitch("s2")
        switch3 = self.addSwitch("s3")
        switch4 = self.addSwitch("s4")

        # Add links (Use switches in the node1 parameter)
        self.addLink(switch1, host1, 1, **host_link_config)
        self.addLink(switch1, host2, 2, **host_link_config)
        self.addLink(switch4, host3, 1, **host_link_config)

        self.addLink(switch1, switch2, 3, 1, **link_config[3][1])
        self.addLink(switch1, switch3, 4, 2, **link_config[4][2])
        self.addLink(switch2, switch4, 4, 3, **link_config[4][3])
        self.addLink(switch3, switch4, 1, 2, **link_config[1][2])

class TrickyTopo(Topo):
    "Simple loop topology example."

    def __init__(self):
        "Create custom loop topo."

        # Initialize topology
        Topo.__init__(self)

        link_config = get_link_config()

        # Add hosts and switches
        h1 = self.addHost('h1') #, mac='11:11:11:11:11:11')
        h2 = self.addHost('h2') #, mac='22:22:22:22:22:22')
        h3 = self.addHost('h3') #, mac='33:33:33:33:33:33')
        h4 = self.addHost('h4') #, mac='44:44:44:44:44:44')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # add host to switch links
        self.addLink(s1, h1, 1, **host_link_config)
        self.addLink(s2, h2, 1, **host_link_config)
        self.addLink(s3, h3, 1, **host_link_config)
        self.addLink(s4, h4, 1, **host_link_config)

        # add switch to switch links
        self.addLink(s1, s2, 2, 2, **link_config[2][2])
        self.addLink(s1, s3, 3, 4, **link_config[3][4])
        self.addLink(s2, s3, 4, 2, **link_config[4][2])
        self.addLink(s2, s4, 3, 2, **link_config[3][2])
        self.addLink(s3, s4, 3, 3, **link_config[3][3])

class WidestTestTopo(Topo):
    "Simple loop topology example."

    def __init__(self):
        "Create custom loop topo."

        # Initialize topology
        Topo.__init__(self)

        # Add hosts and switches
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')

        # add host to switch links
        self.addLink(s1, h1, 1, **host_link_config)
        self.addLink(s2, h2, 1, **host_link_config)
        self.addLink(s3, h3, 1, **host_link_config)
        self.addLink(s4, h4, 1, **host_link_config)
        self.addLink(s5, h5, 1, **host_link_config)
        self.addLink(s6, h6, 1, **host_link_config)
        self.addLink(s7, h7, 1, **host_link_config)

        # add switch to switch links
        self.addLink(s1, s2, 2, 2, **link_config[2][2])
        self.addLink(s2, s3, 3, 2, **link_config[3][2])
        self.addLink(s3, s4, 3, 4, **link_config[3][4])
        self.addLink(s4, s5, 3, 2, **link_config[3][2])
        self.addLink(s6, s5, 2, 4, **link_config[2][4])
        self.addLink(s1, s6, 3, 3, **link_config[3][3])
        self.addLink(s1, s7, 4, 2, **link_config[4][2])
        self.addLink(s5, s7, 3, 3, **link_config[3][3])
        self.addLink(s6, s7, 4, 4, **link_config[4][4])

topos = {'topology': (lambda: WidestTestTopo())}

def loopyTest():
    topo = LoopyTopo()
    net = Mininet(topo=topo,
                  host=CPULimitedHost, link=TCLink, controller=RemoteController, autoSetMacs=True)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    # print "Testing network connectivity"
    # net.pingAll()
    # print "Testing bandwidth between h1 and h4"
    # h1, h4 = net.get('h1', 'h4')
    # net.iperf((h1, h4))
    CLI(net)
    net.stop()

def WidestTest():
    topo = WidestTestTopo()
    net = Mininet(topo=topo,
                  host=CPULimitedHost, link=TCLink, controller=RemoteController, autoSetMacs=True)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    h1, h2 = net.get('h1', 'h2')
    print "Testing latency between h1 and h2"
    net.pingFull((h1,h2))
    print "Testing bandwidth between h1 and h2"
    net.iperf((h1, h2), seconds=60)
    for i in xrange(7):
        dstr = dump_flows('s' + str(i+1))
        lines = dstr.split('\n')
        print lines[0]
        for line in lines[1:]:
            if 'dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:02' in line:
                print line

    CLI(net)
    net.stop()

def simpleTest():
    topo = SimpleTopo()
    net = Mininet(topo=topo,
                  host=CPULimitedHost, link=TCLink, controller=RemoteController, autoSetMacs=True)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)

    hostPrograms = HostPrograms()

    hostPrograms.defineHost(net.hosts, 100 ,20 )

    tenants = hostPrograms.tenants
    net.start()

    for tenant in tenants:
      tenant.start()

    # print "Testing network connectivity"
    # net.pingAll()
    # print "Testing bandwidth between h1 and h3"
    # h1, h3 = net.get('h1', 'h3')
    # net.iperf((h1, h3))

    CLI(net)
    for tenant in tenants:
        tenant.stop()
    net.stop()

def proactiveTest():
    "Create network and run simple performance test"
    topo = SimpleTopo()
    net = Mininet(topo=topo,
                  host=CPULimitedHost, link=TCLink, controller=RemoteController, autoSetMacs=True)
    net.start()

    print "Dumping host connections"
    dumpNodeConnections(net.hosts)

    print "Testing bandwidth between h1, h2, and h3"
    h1, h2, h3 = net.get('h1', 'h2', 'h3')

    net.iperf((h1, h3), l4Type='TCP', udpBw='100M', seconds=20)
    print dump_flows("s1")

    net.iperf((h2, h3), l4Type='TCP', udpBw='75M', seconds=20)
    print dump_flows("s1")

    CLI(net)
    net.stop()

def dump_flows(switch_str):
    return "-----------dump-flows " + switch_str + "\n" + subprocess.check_output(["ovs-ofctl","-O","OpenFlow13","dump-flows",switch_str])

def redistTest():
    "Create network and run simple performance test"
    topo = SimpleTopo()
    net = Mininet(topo=topo,
                  host=CPULimitedHost, link=TCLink, controller=RemoteController, autoSetMacs=True)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    h1, h2, h3 = net.get('h1', 'h2', 'h3')

    # ping all to make sure all flows get installed
    print "Testing network connectivity"
    net.pingAll()

    print dump_flows("s1")

    net.iperf((h1,h3), l4Type='TCP', udpBw=100, seconds=5)

    net.iperf((h2,h3), l4Type='TCP', udpBw=100, seconds=10)

    sleep(15)

    print dump_flows("s1")

    # net.iperf((h1,h3), l4Type='TCP', udpBw=100, seconds=5)
    # net.iperf((h2,h3), l4Type='TCP', udpBw=100, seconds=10)

    net.pingAll()


    CLI(net)


def trickyTest():
    topo = TrickyTopo()
    net = Mininet(topo=topo,
                  host=CPULimitedHost, link=TCLink, controller=RemoteController, autoSetMacs=True)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    # print "Testing network connectivity"
    # net.pingAll()
    CLI(net)
    net.stop()


def bigTest():
    topo = WidestTestTopo()
    net = Mininet(topo=topo,
                  host=CPULimitedHost, link=TCLink, controller=RemoteController, autoSetMacs=True)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    # print "Testing network connectivity"
    # net.pingAll()
    CLI(net)
    net.stop()


def cli():
    topo = LoopyTopo()
    net = Mininet(topo=topo,
                  host=CPULimitedHost, link=TCLink, controller=RemoteController)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    CLI(net)
    net.stop()

def test_from_config(topo_name, commands):
    # initialize topology
    if topo_name == 'SimpleTopo':
        topo = SimpleTopo()
    elif topo_name == 'LoopyTopo':
        topo = LoopyTopo()
    elif topo_name == 'TrickyTopo':
        topo = TrickyTopo()
    elif topo_name == 'WidestTestTopo':
        topo = WidestTestTopo()
    else:
        print 'invalid topology name supplied'
        return

    net = Mininet(topo=topo,
                  host=CPULimitedHost, link=TCLink, controller=RemoteController, autoSetMacs=True)

    hostPrograms = HostPrograms()
    hostPrograms.defineHost(net, net.hosts, commands)

    tenants = hostPrograms.tenants
    print 'tn:mn', tenants
    net.start()

    initial_time = clock()
    for tenant in tenants:
        timestamp = clock() - initial_time
        time_to_wait = max(0, tenant.begin - timestamp)
        sleep(time_to_wait)
        tenant.start()

    CLI(net)
    for tenant in tenants:
        tenant.stop()
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')

    if len(sys.argv) <= 0:
        cli()

    tests = [loopyTest, simpleTest, proactiveTest, redistTest, trickyTest, bigTest, WidestTest]
    for i in xrange(len(tests)):
        print "%d: %s" % (i, str(tests[i]))

    try:
        test_ind = int(sys.argv[1])
    except:
        pass
    else:
        tests[test_ind]()
        exit()

    try:
        filename = sys.argv[1]
        # configure link parameters
        commands = []
        with open(filename) as f:
            lines = f.readlines()
        topo_name = lines[0].strip()
        for line in lines[1:]:
            print line
            try:
                command = ast.literal_eval(line)
            except:
                continue
            else:
                commands.append(command)
    except Exception, e:
        print 'configuration file', filename, 'was invalid'
        raise e
    else:
        for c in commands:
            print c
        commands = sorted(commands, key=lambda cmd: cmd["begin"])
        print 'using topology', topo_name
        for c in commands:
            print c
        test_from_config(topo_name, commands)
