# mininet_proactive_reditribute
Description:
Design, implement, and thoroughly test a software defined network (SDN) for a distributed server that is going to serve a variety of services, from regular HTTP web pages to real-time applications such as sensor streaming and video players. The network has to support protocols such as TCP/IP and UDP simultaneously.

OpenFlow rules that can adapt to network topologies changes and to traffic changes. Additionally, to be able to tests this rules, implement a host service in which you can control the traffic going in and out of that service. 

Functionalities:

Monitor
 print periodically, with period T1, the following information:
• Per port information:
• byte count
• drop count
• error count
• Per flow information:
• byte count
• duration
• timeouts
T1 is a parameter of the controller.

Topology Discovery
A graph of the topology that Ryu application is going to be controlling is made using igraph. This topology adapts to changes  when switches go up or down.Need to use the flag “—observe-links” when running the Ryu Controller, to be
able to see the changes.Each time a switch is discovered or deleted, a log should be written into the terminal.
Given that the Ryu Controller cannot detect the bandwidth and latencies of the connected links. We have define a configuration file “link_config” that is going to contain the information related to the
files, with each configuration as follow:
{“input_port”: <p1>, “output_port”: <p2>, “bandwidth”: <bw>, “latency”: <lat>}
where:
• p1: is the port in the source switch.
• p2: is the port on the destination switch.
• bw: is the bandwidth associated with the link in MB, e.g. 100 will mean 100 Mbps bandwidth
• lat: is the latency associated with the link in ms, e.g. 2 will mean 2 ms latency
The configuration file should be given as an input to both Mininet and the Ryu controller.
The bandwidth and latencies associated with the link connecting a host to a switch should be:
{“bandwidth”: 100, “latency”: 2} 

Shortest Path and Widest Path static rules 
based on config entry either shortest or widest path is taken as default for all packets, corresponding flows are installed in switches

Proactive Rule
The rules described previously are calculated once and don’t take into account statistics of network
usage as the ones obtained in the Monitoring section. You are going to add additional logic to the
Widest-path controller to be able to adapt based on changes in the network.
For each port in the network, you are going to maintain a list that contains the bandwidth that had been
used, as captured by the Monitor module. The size of the list, S1, should be a parameter of the controller
input, similar to T1 in the Monitor module.
Each time a new flow need to be installed (PacketIn event), subtract the average of the list for each link
from the total bandwidth available at each link in the original graph, and calculate the next hop using the
highest width available path. If the host seems unreachable fall back to the static rules.

Redistribute
Additionally, every T2 seconds you are going to redistribute the flow. The controller should maintain the
information related to the packets sent between two hosts (src,dst,packets), called comm_list. Using this
information the controller should implement the following scheme:
1. Initialize the topology graph with the default bandwidth values.
2. Initialize the list of rules to be installed to empty.
3. Sort the comm_list from more packets to fewer packets sent.
4. for each element in comm_list:
find the widest path and add the required rules to the list of rules to be installed.
Reduce the corresponding links of the topology graph with the current average of bytes sent for
the given (src,dst,packet) tuple.
5. Apply all the generated rules
T2 is also an input parameter of the controller.

Specific details
• If any host is unreachable after calculating the newer widest paths, then the new rules should not be
applied.
• S1 and T2 should be parameters of the controller


Note: Read the other readme for specific implementation instructions.
