# Bug Bounty Resources Dashboard

An interactive, offline-capable tool directory for bug bounty hunters and security researchers – with workflow guide, pentest checklist, glossary, password-protected admin panel, and daily auto-updates via a GitHub Actions agent.

No backend. No build step. A single HTML file + optional agent.

---

## Features

### 🛠️ Tools Tab
- **60+ tools** across 12 categories with emoji, description, URL and direct link
- Real-time search across name, URL and description
- **Keyboard shortcut** `/` – focuses the search instantly from any tab
- **Quick filters:** Free only, Favorites, Difficulty level, Actively maintained
- **Category filter** via click
- **Free / Freemium / Paid** badge on every card
- **Difficulty level** per tool: 🟢 Beginner · 🟡 Intermediate · 🔴 Expert
- **⚠️ Outdated** badge for tools no longer actively maintained
- ⭐ **Favorites** – saved via `localStorage`
- 📋 **Copy URL** button on every tool card
- 📚 Resources section: TryHackMe, HackTheBox, OWASP Top 10, CISA KEV and more

### 🗺️ Workflow Tab
- 7-phase workflow: Scope → Passive Recon → Fuzzing → Proxy → Testing → CVE Check → Report
- Each phase with linked tools, description and a highlighted tips box

### ☑️ Checklist Tab
- **55+ OWASP-based test items** across 8 categories
- Categories: Recon, Injection, Auth & Session, Authorization, Web-Specific, Business Logic, API Testing, Cloud & Infrastructure
- HIGH / MEDIUM / LOW / INFO severity badges
- Progress bar – persisted via `localStorage`
- 🖨️ **Print / PDF export** – browser-native, optimized print layout

### 📖 Glossary Tab
- 30+ terms: XSS, SQLi, IDOR, SSRF, BOLA, Mass Assignment, GraphQL Introspection and more
- Full name, definition and example per term
- Dedicated search field

### 🌙 Dark Mode
- Toggle in the top-right corner next to the language selector
- Persisted via `localStorage` – remembered on next visit

### 🌍 Languages
- **German / English** – switchable top-right
- All UI text, tool descriptions, checklist items and glossary definitions in both languages
- Persisted via `localStorage`

### ⚙️ Admin Tab (password-protected)
- **Password protection** with SHA-256 hash, default password: `admin`
- ✏️ Edit, ➕ Add, 🙈 Hide, 🗑️ Delete tools
- ⬇️ JSON export / ⬆️ JSON import of custom tools

### 🤖 BB Agent (GitHub Actions)
- Runs **automatically every day** – no API key required, completely free
- Health check of all tool URLs
- CISA KEV feed – actively exploited CVEs
- NVD feed – latest critical CVEs (CVSS ≥ 9.0)
- GitHub Trending – new security repositories
- Reddit RSS – r/netsec + r/bugbounty
- Writes a daily report to `agent/report.md`

---

## Repo Structure

```
bug-bounty-dashboard/
├── index.html                        ← Web app (everything in one file)
├── tools.json                        ← Tool data (maintained by the agent)
├── README.md                         ← This file (English)
├── README.de.md                      ← German version
├── agent/
│   ├── bb_agent.py                   ← Agent script (Python, no key needed)
│   └── report.md                     ← Daily report (auto-generated)
└── .github/
    └── workflows/
        └── bb-agent.yml              ← GitHub Actions workflow
```

---

## Quick Start

```bash
git clone https://github.com/jbkunama1/hAI.BugBounty.git
cd hAI.BugBounty
# Open index.html directly in your browser – done
```

### GitHub Pages

1. Push repo to GitHub
2. Settings → Pages → Branch: `main`, Folder: `/ (root)`
3. Available at `https://jbkunama1.github.io/hAI.BugBounty/`

### Local Dev Server

```bash
npx serve .
# or
python3 -m http.server 8080
```

---

## 🤖 Agent Setup

### Add these files to the repo

```
.github/workflows/bb-agent.yml
agent/bb_agent.py
tools.json
```

### No API key required

The agent uses only free public data sources:

| Source | Content |
|---|---|
| HTTP check | All tool URLs checked for availability |
| CISA KEV | Daily-updated list of actively exploited CVEs |
| NVD API v2 | Latest critical CVEs (CVSS ≥ 9.0) |
| GitHub API | New security repos (anonymous, 60 req/h) |
| Reddit RSS | r/netsec + r/bugbounty top posts |

### Trigger the first run

```
GitHub → Actions → Bug Bounty Dashboard Agent → Run workflow
```

After that it runs automatically every day at **08:00 CET**.

### Run modes

| Mode | What happens |
|---|---|
| `full` | Health check + all feeds (default) |
| `health-only` | URL checks only |
| `research-only` | External feeds only, no health check |

---

## Admin & Password

| | |
|---|---|
| **Default password** | `admin` |
| **Change password** | Admin tab → 🔑 Change password |
| **Storage** | SHA-256 hash in `localStorage` |
| **Session** | Open while tab is active, manually lockable with 🔒 |

> **Note:** Since the app runs as a static HTML file, protection is client-side. For use on your own device or private GitHub Pages this is sufficient.

---

## Adding Custom Tools

**Via UI:** ⚙️ Admin → ➕ New Tool

**Directly in `tools.json`:**

```json
{
  "name": "Tool Name",
  "emoji": "🔍",
  "url": "example.com",
  "href": "https://example.com",
  "cat": "Recon & OSINT",
  "cost": "free",
  "diff": "beginner",
  "active": true,
  "desc": "Short description of what the tool does."
}
```

---

## Data Storage

All user data stays local in the browser – no server, no cloud.

| Data | Storage |
|---|---|
| Favorites | `localStorage` |
| Checklist progress | `localStorage` |
| Custom tools | `localStorage` |
| Password hash | `localStorage` |
| Login session | `sessionStorage` |
| Tool data + agent updates | `tools.json` in the repo |

---

## Categories

| Category | Content |
|---|---|
| 🔭 Recon & OSINT | Subdomain enumeration, DNS, cert logs, web archive, Shodan |
| 🧪 Security Testing | OWASP Testing Guide, Burp Suite Academy, Exploit-DB, Cheat Sheets |
| 🌀 Fuzzing & Scanner | Nuclei, ffuf, Gobuster, Nikto, Amass, Subfinder |
| 🔀 Proxy & Intercept | Burp Suite, OWASP ZAP, Caido, mitmproxy |
| 🔌 API & Exploitation | SQLmap, dalfox, Interactsh, SecLists, PayloadsAllTheThings, Nmap |
| 🗄️ Vulnerability DBs | FOFA, Netlas, BuiltWith, Wappalyzer |
| ⚠️ CVE & Advisories | NVD (NIST), Mitre CVE, Packet Storm |
| 🏅 Bounty Platforms | HackerOne, Bugcrowd, Intigriti, YesWeHack, Synack |
| ⛓️ Web3 & Blockchain | Immunefi, HackenProof, Code4rena |
| ⚙️ Prog & Misc | HTTPie, Whois Lookup, Webhook.site |
| 📋 Directory Tools | BBRadar, BBScope, RapidDNS, Pentest-Tools |
| 🏆 Platforms | Bug Bounty Daily, Forum, Payload Playground, Hacktivity |

---

## License

MIT – free to use, free to extend.

---

> [GitHub Repository](https://github.com/jbkunama1/hAI.BugBounty) · Sources: OWASP, HackerOne, Bugcrowd & Community
