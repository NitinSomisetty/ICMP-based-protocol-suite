import subprocess

def traceroute(host):

    try:
        result = subprocess.run(
            ["tracert", "-d", "-h", "15", "-w", "500", host],
# -d → don’t resolve hostnames (faster, shows only IPs)
# -h 15 → max 15 hops (routers)
# -w 500 → timeout per hop = 500 ms
            capture_output=True,
            text=True
        )

        lines = result.stdout.splitlines()

        hops = []

        for line in lines: # Loop through each output line
            if line.strip().startswith(tuple(str(i) for i in range(1, 31))):
                hops.append(line.strip())

        return hops

    except Exception as e:
        return [f"Traceroute error: {e}"]