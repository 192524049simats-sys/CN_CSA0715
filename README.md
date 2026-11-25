# CSA0715 – Computer Networks (Assignments CO1 – CO5)

**Student Name:** Santhosh S  
**Register Number:** 192525049  
**Course Code & Name:** CSA0715 – Computer Networks  
**Class Slot:** Slot A  
**Institution:** SIMATS Engineering, Saveetha Institute of Medical and Technical Sciences  
**Department:** Department of Computer Science & Engineering  
**Bloom's Taxonomy Level Assessed:** K5 – Evaluate  
**Target Repository:** `https://github.com/192524049simats-sys/CN_CSA0715.git`  

## Environment Details
- **Operating System:** Windows 11 (x64)
- **Python Version:** Python 3.12.10 (`python-docx`, `pillow`, `matplotlib`)
- **Simulation & Measurement Tools:** Cisco Packet Tracer 9.0.0 (IOS configurations provided in `.cfg`), Wireshark/TShark 4.6.0, Windows `ping`/`tracert`/`curl`/`netstat`, Python `socket`/`ssl`

---

## Repository Structure & Task Index

### 1. CO1 — `ASSIGNMNET CO1/` (Make the Data of a Smart Manufacturing Plant Arrive Correctly and On Time)
| Task | Description | Script / Config | Log & Screenshot |
|------|-------------|-----------------|------------------|
| Task01 | Plant Traffic Sizing & Bottleneck Analysis | [task01_traffic_sizing.py](ASSIGNMNET%20CO1/Task01/task01_traffic_sizing.py) | `experiment_task01.log`, `output_ss/task01_output.png` |
| Task02 | Collision/Broadcast Domains & Standards | [task02_domains_diagram.py](ASSIGNMNET%20CO1/Task02/task02_domains_diagram.py), [office_r1_config.cfg](ASSIGNMNET%20CO1/Task02/office_r1_config.cfg) | `experiment_task02.log`, `output_ss/task02_output.png` |
| Task03 | Layer-by-Layer Frame Dissection & Encapsulation (Complete the Code) | [task03_encapsulation.py](ASSIGNMNET%20CO1/Task03/task03_encapsulation.py) | `experiment_task03.log`, `output_ss/task03_output.png` |
| Task04 | Transmission Media, Nyquist & Shannon Limits (Complete the Code) | [task04_nyquist_shannon.py](ASSIGNMNET%20CO1/Task04/task04_nyquist_shannon.py) | `experiment_task04.log`, `output_ss/task04_output.png` |
| Task05 | Wi-Fi 6 vs Private 5G AGV Handover & Slices | [task05_agv_handover.py](ASSIGNMNET%20CO1/Task05/task05_agv_handover.py) | `experiment_task05.log`, `output_ss/task05_output.png` |
| Task06 | Ethernet Port Report, Duplex Mismatch & Jumbo Frames | [task06_ethernet_port.py](ASSIGNMNET%20CO1/Task06/task06_ethernet_port.py) | `experiment_task06.log`, `output_ss/task06_output.png` |
| Task07 | CRC-3, 2D Parity & Internet Checksum (Complete the Code) | [task07_crc_checksum.py](ASSIGNMNET%20CO1/Task07/task07_crc_checksum.py) | `experiment_task07.log`, `output_ss/task07_output.png` |
| Task08 | Hamming(7,4) FEC vs ARQ (Complete the Code) | [task08_hamming.py](ASSIGNMNET%20CO1/Task08/task08_hamming.py) | `experiment_task08.log`, `output_ss/task08_output.png` |
| Task09 | Sliding Window Utilisation & Sequence Bits (Complete the Code) | [task09_sliding_window.py](ASSIGNMNET%20CO1/Task09/task09_sliding_window.py) | `experiment_task09.log`, `output_ss/task09_output.png` |
| Task10 | Traceroute Delay Analysis & Live Windows Ping/Tracert | [task10_delay_measurements.py](ASSIGNMNET%20CO1/Task10/task10_delay_measurements.py) | `experiment_task10.log`, `output_ss/task10_output.png` |
| Task11 | End-to-End Plant Network Design Defence | [task11_design_defence.py](ASSIGNMNET%20CO1/Task11/task11_design_defence.py) | `experiment_task11.log`, `output_ss/task11_output.png` |
| Task12 | Day-4 Design Challenge: 50 AGVs + Private 5G | [task12_design_challenge.py](ASSIGNMNET%20CO1/Task12/task12_design_challenge.py), [revised_core_config.cfg](ASSIGNMNET%20CO1/Task12/revised_core_config.cfg) | `experiment_task12.log`, `output_ss/task12_output.png` |

### 2. CO2 — `ASSIGNMENT CO2/` (Addressing, Subnetting and Routing)
| Task | Description | Script / Config | Log & Screenshot |
|------|-------------|-----------------|------------------|
| Q1 | IPv4 Addressing Traps, NAT/PAT & Switching | [q1_address_audit.py](ASSIGNMENT%20CO2/Q1/q1_address_audit.py) | `experiment_q1.log`, `output_ss/q1_output.png` |
| Q2 | FLSM vs VLSM, Hostel Trap & Route Summarisation (Complete the Code) | [q2_vlsm_campus.py](ASSIGNMENT%20CO2/Q2/q2_vlsm_campus.py) | `experiment_q2.log`, `output_ss/q2_output.png` |
| Q3 | Longest-Prefix Match & Floating Static Failover (Complete the Config) | [q3_longest_prefix_static.py](ASSIGNMENT%20CO2/Q3/q3_longest_prefix_static.py), [r1_static_floating.cfg](ASSIGNMENT%20CO2/Q3/r1_static_floating.cfg) | `experiment_q3.log`, `output_ss/q3_output.png` |
| Q4 | Bellman-Ford Distance Vector & Count-to-Infinity (Complete the Code) | [q4_bellman_ford.py](ASSIGNMENT%20CO2/Q4/q4_bellman_ford.py) | `experiment_q4.log`, `output_ss/q4_output.png` |
| Q5 | OSPF Reference Bandwidth & Dijkstra 6-Router SPT | [q5_ospf_dijkstra.py](ASSIGNMENT%20CO2/Q5/q5_ospf_dijkstra.py), [ospf_r1_refbw.cfg](ASSIGNMENT%20CO2/Q5/ospf_r1_refbw.cfg) | `experiment_q5.log`, `output_ss/q5_output.png` |
| Q6 | IPv6 Compression, EUI-64, Multicast MAC & OpenFlow SDN | [q6_ipv6_sdn.py](ASSIGNMENT%20CO2/Q6/q6_ipv6_sdn.py) | `experiment_q6.log`, `output_ss/q6_output.png` |
| Q7 | Day-4 Design Challenge: RIP-to-OSPF Migration | [q7_redesign_challenge.py](ASSIGNMENT%20CO2/Q7/q7_redesign_challenge.py), [q7_ospf_routerA.cfg](ASSIGNMENT%20CO2/Q7/q7_ospf_routerA.cfg) | `experiment_q7.log`, `output_ss/q7_output.png` |

### 3. CO3 — `ASSIGNMENT CO3/` (Analyse and Compare Core Network Protocols)
| Task | Description | Script | Log & Screenshot |
|------|-------------|--------|------------------|
| Q1 | Socket Demultiplexing, Overhead & Loss (Complete the Code) | [q1_sockets_demux.py](ASSIGNMENT%20CO3/Q1/q1_sockets_demux.py) | `experiment_q1.log`, `output_ss/q1_output.png` |
| Q2 | TCP Tahoe vs Reno Congestion Window (Complete the Code) | [q2_congestion_window.py](ASSIGNMENT%20CO3/Q2/q2_congestion_window.py) | `experiment_q2.log`, `output_ss/q2_output.png` |
| Q3 | HTTP/1.1 vs HTTP/2 vs HTTP/3 & Live HTTPS Probes | [q3_http_performance.py](ASSIGNMENT%20CO3/Q3/q3_http_performance.py) | `experiment_q3.log`, `output_ss/q3_output.png` |
| Q4 | Iterative DNS Resolution, TTL Cache & Live Resolvers (Complete the Code) | [q4_dns_resolution.py](ASSIGNMENT%20CO3/Q4/q4_dns_resolution.py) | `experiment_q4.log`, `output_ss/q4_output.png` |
| Q5 | M/M/1 Router Queueing, Token Bucket & DiffServ (Complete the Code) | [q5_mm1_qos.py](ASSIGNMENT%20CO3/Q5/q5_mm1_qos.py) | `experiment_q5.log`, `output_ss/q5_output.png` |
| Q6 | QUIC vs TLS 1.2/1.3 Round Trips & Live Handshake Check | [q6_quic_tls13.py](ASSIGNMENT%20CO3/Q6/q6_quic_tls13.py) | `experiment_q6.log`, `output_ss/q6_output.png` |
| Q7 | Rural 4G Telemedicine Protocol Design & Socket Test | [q7_telemedicine_design.py](ASSIGNMENT%20CO3/Q7/q7_telemedicine_design.py) | `experiment_q7.log`, `output_ss/q7_output.png` |

### 4. CO4 — `ASSIGNMENT CO4/` (Designing Network Topologies)
| Task | Description | Script / Config | Log & Screenshot |
|------|-------------|-----------------|------------------|
| Task01 | Office Coax-to-Star Redesign & Bandwidth Calculation | [task01_office_redesign.py](ASSIGNMENT%20CO4/Task01/task01_office_redesign.py) | `experiment_task01.log`, `output_ss/task01_output.png` |
| Task02 | Hospital Topology Cost & BFS Link-Failure Verifier (Complete the Code) | [task02_hospital_topologies.py](ASSIGNMENT%20CO4/Task02/task02_hospital_topologies.py), [hospital_core_rstp.cfg](ASSIGNMENT%20CO4/Task02/hospital_core_rstp.cfg) | `experiment_task02.log`, `output_ss/task02_output.png` |
| Task03 | Outpatient TIA/EIA-568 Audit, BOM & T568B | [task03_cabling_bom.py](ASSIGNMENT%20CO4/Task03/task03_cabling_bom.py) | `experiment_task03.log`, `output_ss/task03_output.png` |
| Task04 | ALOHA, CSMA/CD, Wi-Fi 6 Channels & ATM/MPLS WAN | [task04_aloha_wlan_wan.py](ASSIGNMENT%20CO4/Task04/task04_aloha_wlan_wan.py) | `experiment_task04.log`, `output_ss/task04_output.png` |
| Task05 | VLAN Segmentation, 802.1Q Trunk & Guest ACL (Complete the Config) | [task05_vlans_acl.py](ASSIGNMENT%20CO4/Task05/task05_vlans_acl.py), [sw_admin_vlans.cfg](ASSIGNMENT%20CO4/Task05/sw_admin_vlans.cfg) | `experiment_task05.log`, `output_ss/task05_output.png` |
| Task06 | 40-Acre University Campus Design Challenge | [task06_university_campus.py](ASSIGNMENT%20CO4/Task06/task06_university_campus.py), [campus_core_ospf.cfg](ASSIGNMENT%20CO4/Task06/campus_core_ospf.cfg) | `experiment_task06.log`, `output_ss/task06_output.png` |

### 5. CO5 — `ASSSIGNMENT CO5/` (Measuring Network Performance and Securing Applications)
| Task | Description | Script | Log & Screenshot |
|------|-------------|--------|------------------|
| TaskA1 | End-to-End Delay Breakdown, BDP & SLA Targets | [taska1_delay_bdp.py](ASSSIGNMENT%20CO5/TaskA1/taska1_delay_bdp.py) | `experiment_taska1.log`, `output_ss/taska1_output.png` |
| TaskA2 | SMTP, POP3 vs IMAP, FTP/SFTP, SNMP & DevTools | [taska2_app_protocols.py](ASSSIGNMENT%20CO5/TaskA2/taska2_app_protocols.py) | `experiment_taska2.log`, `output_ss/taska2_output.png` |
| TaskA3 | 4 GB P2P vs Client-Server, G.711 VoIP & CDN/VPN | [taska3_p2p_voip.py](ASSSIGNMENT%20CO5/TaskA3/taska3_p2p_voip.py) | `experiment_taska3.log`, `output_ss/taska3_output.png` |
| TaskA4 | TLS/HTTPS & Stateless Firewall Rule Filter (Complete the Code) | [taska4_firewall_tls.py](ASSSIGNMENT%20CO5/TaskA4/taska4_firewall_tls.py) | `experiment_taska4.log`, `output_ss/taska4_output.png` |
| TaskA5 | SYN-Flood Sizing, SYN Cookies & DNS Amplification | [taska5_dos_protection.py](ASSSIGNMENT%20CO5/TaskA5/taska5_dos_protection.py) | `experiment_taska5.log`, `output_ss/taska5_output.png` |
| TaskB1 | Real Ping/Throughput & Trace Metrics (Complete the Code) | [taskb1_real_network.py](ASSSIGNMENT%20CO5/TaskB1/taskb1_real_network.py) | `experiment_taskb1.log`, `output_ss/taskb1_output.png` |
| TaskB2 | Varying Bandwidth/Load & Voice Priority Queue Sim | [taskb2_varying_sim.py](ASSSIGNMENT%20CO5/TaskB2/taskb2_varying_sim.py) | `experiment_taskb2.log`, `output_ss/taskb2_output.png` |
| TaskB3 | Delay/Loss Stress, Window Size & Flood Rate-Limit Test | [taskb3_stress_attack.py](ASSSIGNMENT%20CO5/TaskB3/taskb3_stress_attack.py) | `experiment_taskb3.log`, `output_ss/taskb3_output.png` |
| TaskB4 | Final Engineering Decision (2x Scale & Intercontinental) | [taskb4_final_decision.py](ASSSIGNMENT%20CO5/TaskB4/taskb4_final_decision.py) | `experiment_taskb4.log`, `output_ss/taskb4_output.png` |

---

## Official Word Submission Reports (`Reports/`)
- `Reports/Santhosh_S_192525049_CSA0715_Assignment1_Answers.docx`
- `Reports/Santhosh_S_192525049_CSA0715_Assignment2_Answers.docx`
- `Reports/Santhosh_S_192525049_CSA0715_Assignment3_Answers.docx`
- `Reports/Santhosh_S_192525049_CSA0715_Assignment4_Answers.docx`
- `Reports/Santhosh_S_192525049_CSA0715_Assignment5_Answers.docx`

## Running All Tasks
Run the unified test harness from the repository root:
```bash
./run_all_tasks.sh
```
Or run individual course outcomes via `python "ASSIGNMNET CO1/run_co1.py"`, `python "ASSIGNMENT CO2/run_co2.py"`, etc.
