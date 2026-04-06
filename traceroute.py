import subprocess

def traceroute(host):

    try:  # below is the command to run tracert with specific options, and capture the output
        result = subprocess.run(
            ["tracert", "-d", "-h", "15", "-w", "1000", host],
    # -d → no dns lookup (IP's only)
    # -h 15 → max 15 hops (routers)
    # -w 500 → timeout per hop = 500 ms
            capture_output=True,  #collects output instead of printing to terminal
            text=True # returns output as string instead of bytes
        )

        lines = result.stdout.splitlines() #the collected output from  result.stdout due to capture_output=True, split into lines

        hops = []

        for line in lines: # Loop through each output line
            if line.strip().startswith(tuple(str(i) for i in range(1, 31))): #starts with a number (hop count)
                hops.append(line.strip())

        return hops

    except Exception as e:
        return [f"Traceroute error: {e}"]