from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time
import threading

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

import threading
import time

def run_iperf_pair(client, server, results, key):
    server.cmd('iperf -s &')
    time.sleep(1)
    result = client.cmd(f'iperf -c {server.IP()} -t 30')
    server.cmd('kill %iperf')
    results[key] = result

def parse_iperf(output):
    lines = output.strip().split('\n')
    for line in lines[::-1]:
        if "bits/sec" in line:
            return line.strip()
    return "No data"

def extract_bandwidth(result_line):
    if "bits/sec" in result_line:
        try:
            parts = result_line.split()
            value, unit = float(parts[-2]), parts[-1]
            if unit == 'Mbits/sec':
                return value
            elif unit == 'Kbits/sec':
                return value / 1000
            elif unit == 'Gbits/sec':
                return value * 1000
        except:
            return 0.0
    return 0.0

def stress_test(net):
    results = {}

    print("Test A")
    h1, h3, h5 = net.get('h1'), net.get('h3'), net.get('h5')
    h4, h6, h2 = net.get('h4'), net.get('h6'), net.get('h2')

    for srv in [h4, h6, h2]:
        srv.cmd('iperf -s &')
    time.sleep(1)

    threads = []
    threads.append(threading.Thread(target=run_iperf_pair, args=(h1, h4, results, 'A1')))
    threads.append(threading.Thread(target=run_iperf_pair, args=(h3, h6, results, 'A2')))
    threads.append(threading.Thread(target=run_iperf_pair, args=(h5, h2, results, 'A3')))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    for srv in [h4, h6, h2]:
        srv.cmd('kill %iperf')

    bw_a_total = 0
    for k in ['A1', 'A2', 'A3']:
        parsed = parse_iperf(results[k])
        bw = extract_bandwidth(parsed)
        bw_a_total += bw
        print(f"Result {k}: {parsed}")

    print(f"\nTest A - Total Bandwidth: {bw_a_total:.2f} Mbits/sec")

    time.sleep(2)

    print("\nTest B")
    h1, h2, h5, h6 = net.get('h1'), net.get('h2'), net.get('h5'), net.get('h6')

    for srv in [h5, h6]:
        srv.cmd('iperf -s &')
    time.sleep(1)

    threads = []
    threads.append(threading.Thread(target=run_iperf_pair, args=(h1, h5, results, 'B1')))
    threads.append(threading.Thread(target=run_iperf_pair, args=(h2, h6, results, 'B2')))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    for srv in [h5, h6]:
        srv.cmd('kill %iperf')

    bw_b_total = 0
    for k in ['B1', 'B2']:
        parsed = parse_iperf(results[k])
        bw = extract_bandwidth(parsed)
        bw_b_total += bw
        print(f"Result {k}: {parsed}")

    print(f"\nTest B - Total Bandwidth: {bw_b_total:.2f} Mbits/sec")

    print("\nSummary")
    print("************")
    print("Test A")
    print(f"A1 (h1 -> h4): {extract_bandwidth(parse_iperf(results['A1'])):.2f} Mbits/sec")
    print(f"A2 (h3 -> h6): {extract_bandwidth(parse_iperf(results['A2'])):.2f} Mbits/sec")
    print(f"A3 (h5 -> h2): {extract_bandwidth(parse_iperf(results['A3'])):.2f} Mbits/sec")
    print(f"Total Bandwidth (Test A): {bw_a_total:.2f} Mbits/sec")

    print("\n************")
    print("Test B")
    print(f"B1 (h1 -> h5): {extract_bandwidth(parse_iperf(results['B1'])):.2f} Mbits/sec")
    print(f"B2 (h2 -> h6): {extract_bandwidth(parse_iperf(results['B2'])):.2f} Mbits/sec")
    print(f"Total Bandwidth (Test B): {bw_b_total:.2f} Mbits/sec")



def run():
    topo = LeafSpineSTPTopo()
    net = Mininet(topo=topo, controller=Controller, switch=OVSSwitch)
    net.start()

    for sw in ['leaf1', 'leaf2', 'leaf3', 'spine1', 'spine2']:
        net.get(sw).cmd(f"ovs-vsctl set Bridge {sw} stp_enable=true")

    info("Waiting for STP to converge\n")
    time.sleep(60)

    stress_test(net)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()