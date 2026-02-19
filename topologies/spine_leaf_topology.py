from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time

class LeafSpineSTPTopo(Topo):
    def build(self):
        spine1 = self.addSwitch('spine1')
        spine2 = self.addSwitch('spine2')

        leaf1 = self.addSwitch('leaf1')
        leaf2 = self.addSwitch('leaf2')
        leaf3 = self.addSwitch('leaf3')

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        hload = self.addHost('h_loadgen')

        self.addLink(h1, leaf1)
        self.addLink(h2, leaf1)
        self.addLink(h3, leaf2)
        self.addLink(h4, leaf2)
        self.addLink(h5, leaf3)
        self.addLink(h6, leaf3)
        self.addLink(hload, leaf1)

        for leaf in [leaf1, leaf2, leaf3]:
            self.addLink(leaf, spine1)
            self.addLink(leaf, spine2)


def run():
    topo = LeafSpineSTPTopo()
    net = Mininet(topo=topo, controller=Controller, switch=OVSSwitch)
    net.start()

    for sw in ['leaf1', 'leaf2', 'leaf3', 'spine1', 'spine2']:
        net.get(sw).cmd(f"ovs-vsctl set Bridge {sw} stp_enable=true")

    info("Waiting for STP to converge\n")
    time.sleep(60)

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
