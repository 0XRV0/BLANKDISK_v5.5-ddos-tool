# lost star DDOS tools and more 
ddos tool that uses open proxys to ddos based around bezerk took 2 days almost 3 have fun use at risk i am not responsible for anything that happens with this 
THIS IS W.I.P DW IT WILL ALL BE UPDATED
IT IS MADE FOR PYTHON



========V3.50 new update now lost star ========
new look and better proxys and WAY MORE OPTIONS OF DDOS SOME ARE IN THE WORK THE SAFE MODE NOW WORKS 

    ▌ LAYER 7  —  HTTP / proxy-routed
    ────────────────────────────────────────────────────────────
  [1]  GET          │ basic HTTP GET flood
  [2]  POST         │ HTTP POST with body
  [3]  HEAD         │ HTTP HEAD only
  [4]  NULL         │ empty User-Agent / headers
  [5]  COOKIE       │ random Cookie header
  [6]  PPS          │ minimal GET / HTTP/1.1
  [7]  EVEN         │ GET + extra browser headers
  [8]  BOT          │ Googlebot-style requests
  [9]  STRESS       │ high-byte POST payloads
  [10] DYN          │ random subdomain prefix
  [11] RHEX         │ random hex path
  [12] STOMP        │ chk_captcha-style headers
  [13] OVH          │ OVH-oriented header set
  [14] GSB          │ Google Shield-oriented
  [15] DGB          │ DDoS-Guard-oriented
  [16] AVB          │ ArvanCloud-oriented
  [17] CFB          │ Cloudflare-oriented
  [18] CFBUAM       │ CF Under Attack Mode-oriented
  [19] BYPASS       │ generic anti-DDoS header mix
  [20] APACHE       │ Apache-oriented POST
  [21] XMLRPC       │ WordPress /xmlrpc.php
  [22] DOWNLOADER   │ slow body read
  [23] SLOW         │ Slowloris partial headers
  [24] KILLER       │ mixed multi-thread blast

    ▌ LAYER 4 / 3  —  raw / amp-shape
    ────────────────────────────────────────────────────────────
  [30] TCP          │ TCP connect flood (proxied)
  [31] UDP          │ UDP datagram flood
  [32] SYN-shape    │ connect storm (userland)
  [33] OVH-UDP      │ UDP random binary payload
  [34] CPS          │ open/close connections
  [35] CONNECTION   │ hold connections briefly
  [50] DNS          │ DNS query-shaped UDP
  [51] NTP          │ NTP header-shaped UDP
  [52] CHAR         │ Chargen-style stream
  [53] MEM          │ Memcached-shaped UDP
  [54] CLDAP        │ CLDAP-shaped UDP

    ▌ GAMES  —  server query shapes
    ────────────────────────────────────────────────────────────
  [36] VSE          │ Valve Source Engine query
  [37] TS3          │ TeamSpeak 3 ping shape
  [38] FIVEM        │ FiveM getinfo UDP
  [39] FIVEM-TOKEN  │ FiveM getstatus UDP
  [40] FIVEM-PLAYERS│ FiveM getplayers UDP
  [41] MINECRAFT    │ Java — IP or domain (.net/.com:port)
  [42] MCBOT        │ Minecraft login-shaped TCP
  [43] MCPE         │ Bedrock RakNet ping
  [44] RUST         │ Rust A2S query
  [45] GMOD         │ Garry's Mod source query
  [46] ARK          │ ARK server query
  [47] SAMP         │ SA-MP query
  [48] CSGO         │ CS source query
  [49] DISCORD      │ Discord voice RTP-shape

    ▌ RDP / VPS / REMOTE  —  proxied sessions
    ────────────────────────────────────────────────────────────
  [55] RDP-TCP      │ full X.224/RDP negotiate (proxied)
  [56] VPS-HTTP     │ your VPS endpoint GET/POST (proxied)
  [57] SSH          │ SSH banner exchange (proxied)
  [58] TLS          │ TLS ClientHello-shaped TCP
  [59] R6-SIEGE     │ Rainbow Six — enter match id

    ▌ LAYER 6  —  session / app shapes
    ────────────────────────────────────────────────────────────
  [60] SOCKET      │ raw rapid socket open/close
  [61] HTTP2       │ HTTP/2 preface + frames shape
  [62] WS-FLOOD    │ WebSocket upgrade flood
  [63] GRPC        │ gRPC/HTTP2 content-type storm
  [64] MQTT        │ MQTT CONNECT packets
  [65] REDIS       │ Redis PING/INFO commands
  [66] MYSQL       │ MySQL handshake storm
  [67] SMTP        │ SMTP EHLO session flood
  [68] FTP         │ FTP USER/PASS storm
  [69] TELNET      │ Telnet option negotiation
  [70] MIX-L6      │ rotate L6 payloads

    ▌ PROXY BAY
    ────────────────────────────────────────────────────────────
  [90] Refresh proxies  │ re-fetch + probe open proxies
  [93] Proxy status     │ pool 7,142  live 80
  [94] Validate live    │ re-probe sample for working nodes

    ▌ SYSTEMS
    ────────────────────────────────────────────────────────────
  [91] History          │ past attacks this session
  [92] Soft area [OFF]  │ rate caps — keeps home WiFi up
  [0]  Shut Down
