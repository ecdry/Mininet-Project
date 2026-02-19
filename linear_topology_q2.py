from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.topo import Topo
import time

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

    h1, h2, h5, h6 = net.get('h1', 'h2', 'h5', 'h6')

    print("\n=== Starting bandwidth test: h1 -> h6 ===")
    h6.cmd('iperf -s &')
    result1 = h1.cmd('iperf -c h6 -t 10')
    print("Bandwidth h1 -> h6:\n", result1)
    h6.cmd('kill %iperf')

    print("\n=== [INFO] Starting simultaneous test: h1 -> h6 and h2 -> h5 ===")
    h6.cmd('iperf -s &')
    h5.cmd('iperf -s &')

    h1.cmd('iperf -c h6 -t 10 > h1_h6.txt &')
    h2.cmd('iperf -c h5 -t 10 > h2_h5.txt &')

    time.sleep(12)

    print("\n=== Bandwidth h1 -> h6 (with h2->h5 running) ===")
    print(h1.cmd('cat h1_h6.txt'))

    print("\n=== Bandwidth h2 -> h5 ===")
    print(h2.cmd('cat h2_h5.txt'))

    h5.cmd('kill %iperf')
    h6.cmd('kill %iperf')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
