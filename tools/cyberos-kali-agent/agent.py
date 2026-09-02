#!/usr/bin/env python3
import json
import os
import subprocess
import time
import urllib.request
import urllib.error

CONTROL_PLANE=os.environ.get("CYBEROS_CONTROL_PLANE","http://localhost:8100")
CONNECTOR_ID=os.environ.get("CYBEROS_CONNECTOR_ID","")
ENROLLMENT_TOKEN=os.environ.get("CYBEROS_ENROLLMENT_TOKEN","")
INTERVAL=int(os.environ.get("CYBEROS_POLL_SECONDS","8"))
VERSION="0.1.0"

if not CONNECTOR_ID or not ENROLLMENT_TOKEN:
    raise SystemExit("CYBEROS_CONNECTOR_ID and CYBEROS_ENROLLMENT_TOKEN are required")

def request(path, method="GET", payload=None):
    data=json.dumps(payload).encode() if payload is not None else None
    req=urllib.request.Request(CONTROL_PLANE+path,data=data,method=method,headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req,timeout=20) as r: return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode(errors='ignore')}")

def heartbeat():
    return request("/api/v1/agent/heartbeat","POST",{"connector_id":CONNECTOR_ID,"enrollment_token":ENROLLMENT_TOKEN,"agent_version":VERSION,"capabilities":["authorized.network.discovery","authorized.vulnerability.assessment","evidence.collection"]})

def run_job(job):
    target=job["target"]
    capability=job["capability"]
    # The control plane is authoritative: the agent never accepts a target from a local CLI.
    if capability in ("authorized.network.discovery","authorized.vulnerability.assessment"):
        cmd=["nmap","-sT","-sV","--top-ports","100","-oX","-",target]
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=180)
        return {"tool":"nmap","mode":"connect-scan","ports":"top-100","returncode":p.returncode,"xml":p.stdout[-200000:],"stderr":p.stderr[-8000:]}
    if capability=="authorized.web.assessment":
        cmd=["curl","-k","-I","--max-time","20",target]
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
        return {"tool":"curl","mode":"authorized-header-check","returncode":p.returncode,"headers":p.stdout[-30000:],"stderr":p.stderr[-8000:]}
    raise RuntimeError("Unsupported execution capability")

def main():
    print(f"CyberOS customer agent {VERSION} connected to {CONTROL_PLANE}")
    while True:
        try:
            heartbeat()
            data=request(f"/api/v1/agent/jobs/{CONNECTOR_ID}?enrollment_token={urllib.parse.quote(ENROLLMENT_TOKEN)}")
            job=data.get("job")
            if not job:
                time.sleep(INTERVAL); continue
            try:
                result=run_job(job)
                state="completed"
            except Exception as exc:
                result={"error":str(exc)}; state="failed"
            request("/api/v1/agent/result","POST",{"connector_id":CONNECTOR_ID,"enrollment_token":ENROLLMENT_TOKEN,"job_id":job["id"],"state":state,"result":result})
        except Exception as exc:
            print("agent loop:",exc)
            time.sleep(INTERVAL)

if __name__=="__main__":
    import urllib.parse
    main()
