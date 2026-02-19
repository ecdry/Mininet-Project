from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time


class RingWithRedundancyTopo(Topo):
    def build(self):
        switches = {}
        for i in range(1, 7):
            sw = self.addSwitch(f's{i}')
            switches[i] = sw

        for i in range(1, 7):
            host = self.addHost(f'h{i}')
            self.addLink(host, switches[i])

        ring_links = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)]
        for a, b in ring_links:
            self.addLink(switches[a], switches[b])

        redundancy_links = [(1, 4), (2, 5), (3, 6)]
        for a, b in redundancy_links:
            self.addLink(switches[a], switches[b])


def run():
    topo = RingWithRedundancyTopo()
    net = Mininet(
        topo=topo,
        controller=OVSController,
        switch=OVSSwitch,
        autoSetMacs=True,
        autoStaticArp=True,
        waitConnected=True
    )
    net.start()

    for sw in net.switches:
        sw.cmd(f'ovs-vsctl set Bridge {sw.name} stp_enable=true')

    info("Waiting for STP to converge\n")
    time.sleep(60)

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
