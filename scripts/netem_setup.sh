#!/bin/bash
# tc/netem setup for controlled network impairments
# Usage: sudo ./netem_setup.sh [interface] [condition]

IFACE=${1:-eth0}
CONDITION=${2:-normal}

case $CONDITION in
  normal)
    tc qdisc del dev $IFACE root 2>/dev/null
    echo "Normal conditions restored"
    ;;
  latency_high)
    tc qdisc del dev $IFACE root 2>/dev/null
    tc qdisc add dev $IFACE root netem delay 150ms 10ms
    echo "High latency applied (150ms ±10ms)"
    ;;
  packet_loss)
    tc qdisc del dev $IFACE root 2>/dev/null
    tc qdisc add dev $IFACE root netem loss 2% 25%
    echo "Packet loss applied (2% ±25%)"
    ;;
  jitter_instability)
    tc qdisc del dev $IFACE root 2>/dev/null
    tc qdisc add dev $IFACE root netem delay 50ms 30ms distribution normal
    echo "Jitter/instability applied"
    ;;
  *)
    echo "Usage: $0 <interface> [normal|latency_high|packet_loss|jitter_instability]"
    exit 1
    ;;
esac
