from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

class DualSwitchTopo(Topo):
    def build(self):

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        for i in range(1, 4):
            self.addLink(self.addHost(f'h{i}'), s1)

        for i in range(4, 7):
            self.addLink(self.addHost(f'h{i}'), s2)

        self.addLink(s1, s2)

if __name__ == '__main__':
    setLogLevel('info')
    topo = DualSwitchTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    CLI(net)
    net.stop()
