import subprocess

def traceroute(host, max_hops=8, timeout_ms=1000):

    try:  # below is the command to run tracert with specific options, and capture the output
        result = subprocess.run(
            ["tracert", "-d", "-h", str(max_hops), "-w", str(timeout_ms), host],
    # -d → no dns lookup (IP's only)
    # -h max_hops → max number of hops (routers)
    # -w timeout_ms → timeout per hop in milliseconds
            capture_output=True,  #collects output instead of printing to terminal
            text=True # returns output as string instead of bytes
        )

        lines = result.stdout.splitlines() #the collected output from  result.stdout due to capture_output=True, split into lines

        hops = []

# parses hop lines
        for line in lines: # Loop through each output line
            if line.strip().startswith(tuple(str(i) for i in range(1, 31))): #starts with a number (hop count)
                hops.append(line.strip())

        return hops

    except Exception as e:
        return [f"Traceroute error: {e}"]