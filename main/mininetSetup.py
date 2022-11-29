'''

Set up the single switch topology in Mininet

'''

from mininet.topo import Topo, SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI

# Function, sets up a single switch which is connected to 3 hosts
# Controller, Renderer and Server


def main():
    setLogLevel('info')
    # Create a single switch which is connected to k hosts
    net = Mininet(SingleSwitchTopo(k=3))
    net.start()
    # Show the mininet command line interface
    CLI(net)
    # Stop the network after closing the CLI
    net.stop()


if __name__ == '__main__':
    main()
