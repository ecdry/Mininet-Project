from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class StarTopo(Topo):
    def build(self):

        s1 = self.addSwitch('s1')

        for i in range(1, 7):
            host = self.addHost(f'h{i}')
            self.addLink(host, s1, cls=TCLink, bw=75, delay='1ms')

def run():
    topo = StarTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
