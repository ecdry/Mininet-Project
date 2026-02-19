from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.topo import Topo

class LinearTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        link_host = dict(bw=75, delay='1ms')
        link_switch = dict(bw=100, delay='2ms')

        self.addLink(h1, s1, cls=TCLink, **link_host)
        self.addLink(h2, s1, cls=TCLink, **link_host)
        self.addLink(h3, s2, cls=TCLink, **link_host)
        self.addLink(h4, s2, cls=TCLink, **link_host)
        self.addLink(h5, s3, cls=TCLink, **link_host)
        self.addLink(h6, s3, cls=TCLink, **link_host)

        self.addLink(s1, s2, cls=TCLink, **link_switch)
        self.addLink(s2, s3, cls=TCLink, **link_switch)

def run():
    topo = LinearTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None)
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
