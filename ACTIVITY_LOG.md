Date: 2025-11-03

Prompt Summary:
- Implement a traceroute parser that processes a textual tcpdump trace line-by-line, correlates TCP probe packets to ICMP time-exceeded responses, computes per-hop RTTs, and outputs results per TTL to both console and output.txt. Use best practices and maintain a streaming approach.

Steps Taken:
1) Reviewed existing files and sample tcpdump format to understand line structure for TCP probes and ICMP replies.
2) Implemented a streaming parser in `traceRouteSkeleton.py` using compiled regular expressions to:
   - Capture outbound TCP probe timestamp, TTL, and id.
   - Detect ICMP time-exceeded blocks and extract router IP and embedded original packet id.
   - Compute RTT in milliseconds per TTL and aggregate three probes per hop.
   - Emit results in order of TTL and write to both stdout and `output.txt`.
3) Ensured code handles mixed ordering by buffering per TTL and flushing when three timings are available.
4) Verified no linter issues.

Outputs:
- `output.txt`: Generated when running the script, containing the formatted traceroute results.


