from mininet.net import Mininet
from mininet.topo import LinearTopo

Linear = LinearTopo(k=3)

net = Mininet(topo=Linear)

net.start()
net.pingAll()
net.stop()
