#This program traces a traceroute dump and prints out the summary of the trace.
# CSCI 4760 63232 
# Firas Astwani, November 3rd 2025

import re  # if you want to use regular expression to parse the data
import sys

from typing import Dict, List, Tuple, Optional

# using regex
TCP_TS_LINE_RE = re.compile(r"^(?P<ts>\d+\.\d+)\s+IP\s+\(.*?ttl\s+(?P<ttl>\d+),\s+id\s+(?P<id>\d+)\b.*?proto\s+TCP\s+\(6\)")
ICMP_TS_LINE_RE = re.compile(r"^(?P<ts>\d+\.\d+)\s+IP\s+\(.*?proto\s+ICMP\s+\(1\)")
ICMP_DESC_LINE_RE = re.compile(r"^\s*(?P<src_ip>\d+\.\d+\.\d+\.\d+)\s+>\s+(?P<dst_ip>\d+\.\d+\.\d+\.\d+):\s+ICMP\s+time\s+exceeded")
EMBEDDED_IP_LINE_RE = re.compile(r"^\s*IP\s+\(.*?ttl\s+\d+,\s+id\s+(?P<id>\d+)\b.*?proto\s+TCP\s+\(6\)")


def main(dump_filename: str) -> None:
    # mapping packet id to (send time, ttl)
    id_to_send: Dict[int, Tuple[float, int]] = {}

    # aggregate results per TTL
    ttl_times: Dict[int, List[float]] = {}
    ttl_router: Dict[int, str] = {}

    pending_icmp_ts: Optional[float] = None
    pending_router: Optional[str] = None

    next_ttl = 1
    out: List[str] = []

    def flush_ready() -> None:
        nonlocal next_ttl
        while next_ttl in ttl_times and len(ttl_times[next_ttl]) >= 3:
            out.append(f'TTL {next_ttl}')
            out.append(ttl_router.get(next_ttl, '*'))
            for t in ttl_times[next_ttl][:3]:
                out.append(f'{t:.3f} ms')
            next_ttl += 1

    with open(dump_filename, 'r') as f:
        for line in f:
            m = TCP_TS_LINE_RE.search(line)
            if m:
                id_to_send[int(m.group('id'))] = (float(m.group('ts')), int(m.group('ttl')))
                continue

            m = ICMP_TS_LINE_RE.search(line)
            if m:
                pending_icmp_ts = float(m.group('ts'))
                pending_router = None
                continue

            if pending_icmp_ts is not None and pending_router is None:
                m = ICMP_DESC_LINE_RE.search(line)
                if m:
                    pending_router = m.group('src_ip')
                    continue

            if pending_icmp_ts is not None and pending_router is not None:
                m = EMBEDDED_IP_LINE_RE.search(line)
                if m:
                    ref_id = int(m.group('id'))
                    if ref_id in id_to_send:
                        send_ts, ttl = id_to_send[ref_id]
                        rtt = max(0.0, (pending_icmp_ts - send_ts) * 1000.0)
                        ttl_times.setdefault(ttl, []).append(rtt)
                        ttl_router.setdefault(ttl, pending_router)
                        flush_ready()
                    pending_icmp_ts = None
                    pending_router = None
                    continue

    # Flush partial TTL at EOF (if any)
    while next_ttl in ttl_times and ttl_times[next_ttl]:
        out.append(f'TTL {next_ttl}')
        out.append(ttl_router.get(next_ttl, '*'))
        for t in ttl_times[next_ttl][:3]:
            out.append(f'{t:.3f} ms')
        next_ttl += 1

    text = '\n'.join(out) + ('\n' if out else '')
    if text:
        sys.stdout.write(text)
    with open('output.txt', 'w') as wf:
        wf.write(text)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'sampletcpdump.txt')
