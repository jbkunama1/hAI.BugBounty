#!/usr/bin/env python3
"""
Bug Bounty Dashboard Agent – 100% kostenlos, kein API-Key nötig.

Datenquellen (alle frei):
  - HTTP Health Checks          → eigene Requests
  - CISA KEV Feed               → cisa.gov (JSON, kein Key)
  - NVD CVE Feed                → nvd.nist.gov (JSON, kein Key)
  - GitHub Trending Security    → github.com/trending (Scraping)
  - GitHub API                  → api.github.com (anonym, 60 req/h)
  - Reddit RSS                  → reddit.com/r/netsec + r/bugbounty
  - HackerOne Hacktivity RSS    → hackerone.com/hacktivity.rss
  - Packet Storm RSS            → packetstormsecurity.com RSS
"""

import json, os, time, datetime, re, xml.etree.ElementTree as ET
import requests, urllib.parse

# ─────────────────────────────────────────────
TOOLS_FILE  = "tools.json"
REPORT_FILE = "agent/report.md"
MODE        = os.environ.get("AGENT_MODE", "full")
TIMEOUT     = 12
DELAY       = 0.4

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; BBDashboardAgent/1.0)",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.9"
}
JSON_HEADERS = {**HEADERS, "Accept": "application/json"}

# ─────────────────────────────────────────────
# TOOLS LADEN / SPEICHERN
# ─────────────────────────────────────────────
def load_tools():
    if not os.path.exists(TOOLS_FILE):
        print(f"⚠️  {TOOLS_FILE} nicht gefunden.")
        return []
    with open(TOOLS_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_tools(tools):
    with open(TOOLS_FILE, "w", encoding="utf-8") as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)
    print(f"✅ {TOOLS_FILE} gespeichert ({len(tools)} Tools)")

# ─────────────────────────────────────────────
# 1. HEALTH CHECKS
# ─────────────────────────────────────────────
def check_url(href):
    if not href.startswith("http"):
        href = "https://" + href
    try:
        r = requests.get(href, headers=HEADERS, timeout=TIMEOUT,
                         allow_redirects=True)
        return {"online": r.status_code < 400, "status": r.status_code}
    except requests.exceptions.SSLError:
        return {"online": False, "error": "SSL-Fehler"}
    except requests.exceptions.ConnectionError:
        return {"online": False, "error": "Nicht erreichbar"}
    except requests.exceptions.Timeout:
        return {"online": False, "error": "Timeout"}
    except Exception as e:
        return {"online": False, "error": str(e)[:60]}

def run_health_checks(tools):
    print(f"\n🔍 Health Check: {len(tools)} Tools...")
    results = {}
    offline = []
    for i, t in enumerate(tools, 1):
        name = t.get("name", "?")
        href = t.get("href") or t.get("url", "")
        r = check_url(href)
        results[name] = r
        icon = "✅" if r["online"] else "❌"
        info = r.get("status") or r.get("error", "?")
        print(f"  [{i:>3}/{len(tools)}] {icon} {name}  ({info})")
        if not r["online"]:
            offline.append(name)
        time.sleep(DELAY)
    print(f"\n📊 Online: {len(tools)-len(offline)}/{len(tools)}  |  Offline: {len(offline)}")
    return results

# ─────────────────────────────────────────────
# 2. CISA KEV – aktiv ausgenutzte CVEs (kostenlos)
# ─────────────────────────────────────────────
def fetch_cisa_kev(limit=8):
    """
    CISA Known Exploited Vulnerabilities Catalog.
    Kein API-Key nötig – öffentliches JSON.
    """
    url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    print("\n⚠️  CISA KEV Feed abrufen...")
    try:
        r = requests.get(url, headers=JSON_HEADERS, timeout=20)
        data = r.json()
        vulns = data.get("vulnerabilities", [])
        # Neueste zuerst
        vulns_sorted = sorted(vulns, key=lambda v: v.get("dateAdded",""), reverse=True)
        results = []
        for v in vulns_sorted[:limit]:
            results.append({
                "id":       v.get("cveID", "?"),
                "product":  v.get("product", "?"),
                "vendor":   v.get("vendorProject", "?"),
                "desc":     v.get("shortDescription", "")[:120],
                "added":    v.get("dateAdded", "?"),
                "due":      v.get("dueDate", "?"),
            })
        print(f"  ✅ {len(results)} aktuelle KEV-Einträge geladen.")
        return results
    except Exception as e:
        print(f"  ⚠️  CISA KEV Fehler: {e}")
        return []

# ─────────────────────────────────────────────
# 3. NVD – neueste kritische CVEs (kostenlos)
# ─────────────────────────────────────────────
def fetch_nvd_critical(limit=5):
    """
    NVD CVE API v2 – kein Key für öffentliche Endpoints.
    Holt neueste CVEs mit CVSS >= 9.0 (Critical).
    """
    print("\n🏛️  NVD Critical CVEs abrufen...")
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {
        "cvssV3Severity": "CRITICAL",
        "resultsPerPage": limit,
        "startIndex": 0,
    }
    try:
        r = requests.get(url, params=params, headers=JSON_HEADERS, timeout=20)
        data = r.json()
        cves = []
        for item in data.get("vulnerabilities", []):
            cve = item.get("cve", {})
            cve_id = cve.get("id", "?")
            descs = cve.get("descriptions", [])
            desc_en = next((d["value"] for d in descs if d["lang"] == "en"), "")[:120]
            published = cve.get("published", "")[:10]
            metrics = cve.get("metrics", {})
            score = "?"
            for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
                if key in metrics and metrics[key]:
                    score = metrics[key][0].get("cvssData", {}).get("baseScore", "?")
                    break
            cves.append({"id": cve_id, "score": score, "published": published, "desc": desc_en})
        print(f"  ✅ {len(cves)} kritische CVEs geladen.")
        return cves
    except Exception as e:
        print(f"  ⚠️  NVD Fehler: {e}")
        return []

# ─────────────────────────────────────────────
# 4. GITHUB TRENDING – neue Security-Tools
# ─────────────────────────────────────────────
def fetch_github_trending_security():
    """
    GitHub API – sucht neue/populäre Security-Repos der letzten 30 Tage.
    Kein Token nötig (60 req/h anonym).
    """
    print("\n🐙 GitHub Trending Security-Tools abrufen...")
    since = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
    query = f"topic:security topic:pentesting stars:>50 pushed:>{since}"
    url   = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 10,
    }
    gh_headers = {**JSON_HEADERS, "Accept": "application/vnd.github+json"}
    try:
        r = requests.get(url, params=params, headers=gh_headers, timeout=15)
        if r.status_code == 403:
            print("  ⚠️  GitHub Rate Limit erreicht – übersprungen.")
            return []
        data = r.json()
        repos = []
        for repo in data.get("items", []):
            repos.append({
                "name":        repo["name"],
                "full_name":   repo["full_name"],
                "description": (repo.get("description") or "")[:100],
                "stars":       repo["stargazers_count"],
                "url":         repo["html_url"],
                "topics":      repo.get("topics", [])[:5],
                "language":    repo.get("language", "?"),
            })
        print(f"  ✅ {len(repos)} Repos gefunden.")
        return repos
    except Exception as e:
        print(f"  ⚠️  GitHub Fehler: {e}")
        return []

# ─────────────────────────────────────────────
# 5. REDDIT RSS – aktuelle Community-Themen
# ─────────────────────────────────────────────
def fetch_reddit_rss(subreddit, limit=5):
    """Reddit RSS – kein Key nötig."""
    url = f"https://www.reddit.com/r/{subreddit}/hot.rss?limit={limit}"
    try:
        r = requests.get(url, headers={**HEADERS, "Accept":"application/rss+xml"}, timeout=12)
        root = ET.fromstring(r.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        posts = []
        for entry in root.findall(".//atom:entry", ns)[:limit]:
            title = entry.findtext("atom:title", "", ns)
            link  = ""
            for l in entry.findall("atom:link", ns):
                if l.get("rel") == "alternate":
                    link = l.get("href", "")
            posts.append({"title": title, "url": link})
        return posts
    except Exception:
        return []

def fetch_reddit_security():
    print("\n👾 Reddit Security-Feeds abrufen...")
    netsec    = fetch_reddit_rss("netsec", 5)
    bugbounty = fetch_reddit_rss("bugbounty", 5)
    print(f"  ✅ r/netsec: {len(netsec)} | r/bugbounty: {len(bugbounty)}")
    return {"netsec": netsec, "bugbounty": bugbounty}

# ─────────────────────────────────────────────
# 6. HACKERONE HACKTIVITY RSS
# ─────────────────────────────────────────────
def fetch_hacktivity():
    """HackerOne öffentliche Hacktivity – keine Auth nötig."""
    print("\n🥷 HackerOne Hacktivity abrufen...")
    url = "https://hackerone.com/hacktivity/overview?querystring=&filter=type%3Aall&order_direction=DESC&order_field=popular&followed_only=false&collaboration_only=false"
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        # Nur Status prüfen – JSON-Parsing je nach Antwortformat
        if r.status_code == 200:
            print("  ✅ Hacktivity erreichbar.")
            return True
        return False
    except Exception:
        return False

# ─────────────────────────────────────────────
# 7. UPDATES ANWENDEN
# ─────────────────────────────────────────────
def apply_health_updates(tools, health_results):
    today = datetime.date.today().isoformat()
    changed = 0
    for t in tools:
        name = t.get("name","")
        if name in health_results:
            r = health_results[name]
            t["lastChecked"] = today
            t["isOnline"]    = r["online"]
            # War online, jetzt offline → active auf false setzen
            if not r["online"] and t.get("active", True):
                t["active"] = False
                print(f"  ⚠️  Offline → active:false gesetzt: {name}")
                changed += 1
            # War offline, jetzt wieder online → active zurück auf true
            elif r["online"] and not t.get("active", True):
                t["active"] = True
                print(f"  ✅ Wieder online → active:true: {name}")
                changed += 1
    return tools, changed

# ─────────────────────────────────────────────
# 8. REPORT SCHREIBEN
# ─────────────────────────────────────────────
def write_report(tools, health_results, kev_data, nvd_data,
                 gh_repos, reddit_data, stats):
    today  = datetime.date.today().isoformat()
    now_utc = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    offline = [n for n, r in health_results.items() if not r["online"]]
    online  = len(health_results) - len(offline)

    lines = [
        f"# 🤖 BB Agent Report – {today}",
        "",
        f"*Automatisch generiert: {now_utc}*",
        "",
        "---",
        "",
        "## 🔍 Health Check",
        "",
        f"| | Anzahl |",
        f"|---|---|",
        f"| ✅ Online | {online} |",
        f"| ❌ Offline / Fehler | {len(offline)} |",
        f"| 📦 Gesamt geprüft | {len(health_results)} |",
        "",
    ]

    if offline:
        lines += ["### ❌ Nicht erreichbare Tools", ""]
        for name in offline:
            err = health_results[name].get("error") or str(health_results[name].get("status","?"))
            lines.append(f"- **{name}** — {err}")
        lines.append("")

    # CISA KEV
    if kev_data:
        lines += [
            "---",
            "",
            "## 🚨 CISA Known Exploited Vulnerabilities (neu)",
            "",
            "> Diese CVEs werden aktiv in freier Wildbahn ausgenutzt – Patch-Priorität!",
            "",
            "| CVE | Produkt | Hinzugefügt | Patch-Frist |",
            "|-----|---------|-------------|-------------|",
        ]
        for v in kev_data:
            lines.append(f"| `{v['id']}` | {v['vendor']} – {v['product']} | {v['added']} | {v['due']} |")
        lines.append("")

    # NVD Critical
    if nvd_data:
        lines += [
            "---",
            "",
            "## 🏛️ Neueste kritische CVEs (NVD, CVSS ≥ 9.0)",
            "",
            "| CVE | Score | Veröffentlicht | Beschreibung |",
            "|-----|-------|----------------|--------------|",
        ]
        for c in nvd_data:
            desc_short = c["desc"][:80] + ("…" if len(c["desc"])>80 else "")
            lines.append(f"| `{c['id']}` | **{c['score']}** | {c['published']} | {desc_short} |")
        lines.append("")

    # GitHub Trending
    if gh_repos:
        lines += [
            "---",
            "",
            "## 🐙 GitHub Trending Security-Repos (letzte 30 Tage)",
            "",
        ]
        for r in gh_repos[:8]:
            topics = " ".join(f"`{t}`" for t in r["topics"][:3])
            lines.append(f"- ⭐ {r['stars']:,} &nbsp; **[{r['full_name']}]({r['url']})** — {r['description']} {topics}")
        lines.append("")

    # Reddit
    r_netsec    = reddit_data.get("netsec", [])
    r_bugbounty = reddit_data.get("bugbounty", [])
    if r_netsec or r_bugbounty:
        lines += [
            "---",
            "",
            "## 👾 Community-Highlights",
            "",
        ]
        if r_netsec:
            lines.append("**r/netsec**")
            lines.append("")
            for p in r_netsec:
                lines.append(f"- [{p['title']}]({p['url']})")
            lines.append("")
        if r_bugbounty:
            lines.append("**r/bugbounty**")
            lines.append("")
            for p in r_bugbounty:
                lines.append(f"- [{p['title']}]({p['url']})")
            lines.append("")

    # Stats
    lines += [
        "---",
        "",
        "## 📈 Änderungsstatistik",
        "",
        f"- Status-Updates (online/offline): **{stats.get('health_changed', 0)}**",
        f"- Tools gesamt im Dashboard: **{len(tools)}**",
        "",
        "---",
        "",
        "*BB Dashboard Agent v2.0 — 100% kostenlos, kein API-Key erforderlich*",
    ]

    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ Report geschrieben: {REPORT_FILE}")

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print(f"🤖 BB Dashboard Agent v2.0 — Modus: {MODE}")
    print(f"📅 {datetime.date.today()}")
    print("─" * 50)

    tools = load_tools()
    today = datetime.date.today().isoformat()

    health_results = {}
    kev_data       = []
    nvd_data       = []
    gh_repos       = []
    reddit_data    = {}
    stats          = {}

    # ── Health Checks
    if MODE in ("full", "health-only"):
        health_results = run_health_checks(tools)
        tools, changed = apply_health_updates(tools, health_results)
        stats["health_changed"] = changed

    # ── Externe Feeds
    if MODE in ("full", "research-only"):
        kev_data    = fetch_cisa_kev(limit=8)
        nvd_data    = fetch_nvd_critical(limit=5)
        gh_repos    = fetch_github_trending_security()
        reddit_data = fetch_reddit_security()
        fetch_hacktivity()

    # ── Speichern & Report
    save_tools(tools)
    write_report(tools, health_results, kev_data, nvd_data,
                 gh_repos, reddit_data, stats)

    print("\n✅ Agent abgeschlossen.")

if __name__ == "__main__":
    main()
