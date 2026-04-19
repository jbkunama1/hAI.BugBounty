# Bug Bounty Resources Dashboard

Ein interaktives, offline-fähiges Tool-Verzeichnis für Bug-Bounty-Hunter und Security-Researcher – mit Workflow-Guide, Pentest-Checkliste, Glossar, passwortgeschützter Verwaltung und täglichem Auto-Update durch einen GitHub Actions Agent.

Kein Backend. Kein Build-Step. Eine einzige HTML-Datei + optionaler Agent.

---

## Features

### 🛠️ Tools-Tab
- **60+ Tools** aus 12 Kategorien mit Emoji, Beschreibung, URL und Direktlink
- Echtzeit-Suche über Name, URL und Beschreibung
- **Keyboard-Shortcut** `/` – fokussiert die Suche sofort aus jedem Tab heraus
- **Quick-Filter:** Kostenlos, Favoriten, Schwierigkeitsgrad, Aktiv gepflegt
- **Kategorie-Filter** per Klick
- **Free / Freemium / Paid** Badge auf jeder Karte
- **Schwierigkeitsgrad** pro Tool: 🟢 Einsteiger · 🟡 Fortgeschritten · 🔴 Experte
- **⚠️ Veraltet**-Badge für nicht mehr aktiv gepflegte Tools
- ⭐ **Favoriten** – gespeichert per `localStorage`
- 📋 **URL kopieren** – Button auf jeder Tool-Karte
- 📚 Begleitseiten-Abschnitt: TryHackMe, HackTheBox, OWASP Top 10, CISA KEV u.v.m.

### 🗺️ Workflow-Tab
- 7-Phasen-Ablauf: Scope → Passive Recon → Fuzzing → Proxy → Testing → CVE-Check → Report
- Jede Phase mit verlinkten Tools, Beschreibung und farbigem Tipp-Kasten

### ☑️ Checkliste-Tab
- **55+ OWASP-basierte Testpunkte** in 8 Kategorien
- Kategorien: Recon, Injection, Auth & Session, Autorisierung, Web-Spezifisch, Business Logic, API-Testing, Cloud & Infrastruktur
- HIGH / MEDIUM / LOW / INFO Schwere-Badges
- Fortschrittsbalken – bleibt per `localStorage` erhalten
- 🖨️ **Drucken / PDF-Export** – direkt aus dem Browser, optimiertes Print-Layout

### 📖 Glossar-Tab
- 30+ Begriffe: XSS, SQLi, IDOR, SSRF, BOLA, Mass Assignment, GraphQL Introspection u.v.m.
- Vollname, Definition und Beispiel pro Begriff
- Eigenes Suchfeld

### 🌙 Dark Mode
- Toggle oben rechts neben der Sprachauswahl
- Gespeichert per `localStorage` – bleibt beim nächsten Öffnen erhalten

### 🌍 Sprachen
- **Deutsch / Englisch** – umschaltbar oben rechts
- Alle UI-Texte, Tool-Beschreibungen, Checklisten-Einträge und Glossar-Definitionen in beiden Sprachen
- Gespeichert per `localStorage`

### ⚙️ Verwaltung-Tab (passwortgeschützt)
- **Passwortschutz** mit SHA-256-Hash, Standard-Passwort: `admin`
- ✏️ Bearbeiten, ➕ Hinzufügen, 🙈 Ausblenden, 🗑️ Löschen
- ⬇️ JSON-Export / ⬆️ JSON-Import eigener Tools

### 🤖 BB Agent (GitHub Actions)
- Läuft **täglich automatisch** – kein API-Key, völlig kostenlos
- Health Check aller Tool-URLs
- CISA KEV Feed – aktiv ausgenutzte CVEs
- NVD Feed – neueste kritische CVEs (CVSS ≥ 9.0)
- GitHub Trending – neue Security-Repos
- Reddit RSS – r/netsec + r/bugbounty
- Schreibt Tages-Report nach `agent/report.md`

---

## Repo-Struktur

```
bug-bounty-dashboard/
├── index.html                        ← Web-App (alles in einer Datei)
├── tools.json                        ← Tool-Daten (wird vom Agent gepflegt)
├── README.md
├── agent/
│   ├── bb_agent.py                   ← Agent-Skript (Python, kein Key nötig)
│   └── report.md                     ← Tages-Report (auto-generiert)
└── .github/
    └── workflows/
        └── bb-agent.yml              ← GitHub Actions Workflow
```

---

## Schnellstart

```bash
git clone https://github.com/DEIN-USERNAME/bug-bounty-dashboard.git
cd bug-bounty-dashboard
# index.html direkt im Browser öffnen – fertig
```

### GitHub Pages

1. Repo auf GitHub pushen
2. Settings → Pages → Branch: `main`, Ordner: `/ (root)`
3. Erreichbar unter `https://DEIN-USERNAME.github.io/bug-bounty-dashboard`

---

## 🤖 Agent einrichten

### Dateien ins Repo legen

```
.github/workflows/bb-agent.yml
agent/bb_agent.py
tools.json
```

### Keinen API-Key nötig

Der Agent nutzt ausschließlich kostenlose öffentliche Quellen:

| Quelle | Inhalt |
|---|---|
| HTTP-Check | Alle Tool-URLs auf Erreichbarkeit |
| CISA KEV | Täglich aktualisierte Liste aktiv ausgenutzter CVEs |
| NVD API v2 | Neueste kritische CVEs (CVSS ≥ 9.0) |
| GitHub API | Neue Security-Repos (anonym, 60 req/h) |
| Reddit RSS | r/netsec + r/bugbounty Top-Posts |

### Ersten Lauf starten

```
GitHub → Actions → Bug Bounty Dashboard Agent → Run workflow
```

Danach läuft er automatisch täglich um **08:00 MEZ**.

### Manuell mit bestimmtem Modus starten

| Modus | Was passiert |
|---|---|
| `full` | Health Check + alle Feeds (Standard) |
| `health-only` | Nur URL-Checks |
| `research-only` | Nur externe Feeds, kein Health Check |

---

## Verwaltung & Passwort

| | |
|---|---|
| **Standard-Passwort** | `admin` |
| **Passwort ändern** | Verwaltung → 🔑 Passwort ändern |
| **Speicherung** | SHA-256-Hash im `localStorage` |
| **Session** | Offen solange Tab offen, manuell sperrbar |

---

## Eigene Tools hinzufügen

**Via UI:** ⚙️ Verwaltung → ➕ Neues Tool

**Direkt in `tools.json`:**

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
  "desc": "Kurze Beschreibung auf Deutsch."
}
```

---

## Datenspeicherung

Alle Nutzerdaten bleiben lokal im Browser – kein Server, keine Cloud.

| Daten | Speicherort |
|---|---|
| Favoriten | `localStorage` |
| Checklisten-Fortschritt | `localStorage` |
| Eigene Tools | `localStorage` |
| Passwort-Hash | `localStorage` |
| Login-Session | `sessionStorage` |
| Tool-Stammdaten + Agent-Updates | `tools.json` im Repo |

---

## Lizenz

MIT – frei nutzbar, frei erweiterbar.

---

> Erstellt mit [Highfish AI](https://highfish.ai)

Ein interaktives, offline-fähiges Tool-Verzeichnis für Bug-Bounty-Hunter und Security-Researcher – mit Workflow-Guide, Pentest-Checkliste, Glossar und passwortgeschützter Verwaltung.

Kein Backend. Kein Build-Step. Eine einzige HTML-Datei.

---

## Features

### 🛠️ Tools-Tab
- **50+ Tools** aus 11 Kategorien mit Emoji, Beschreibung, URL und Direktlink
- Echtzeit-Suche über Name, URL und Beschreibung
- **Quick-Filter:** Kostenlos, Favoriten, Schwierigkeitsgrad, Aktiv gepflegt
- **Kategorie-Filter** per Klick
- **Free / Freemium / Paid** Badge auf jeder Karte
- **Schwierigkeitsgrad** pro Tool: 🟢 Einsteiger · 🟡 Fortgeschritten · 🔴 Experte
- **⚠️ Veraltet**-Badge für nicht mehr aktiv gepflegte Tools
- ⭐ **Favoriten** – gespeichert per `localStorage`
- 📚 Begleitseiten-Abschnitt: TryHackMe, HackTheBox, OWASP Top 10, GTFOBins u.v.m.

### 🗺️ Workflow-Tab
- 7-Phasen-Ablauf: Scope → Passive Recon → Fuzzing → Proxy → Testing → CVE-Check → Report
- Jede Phase mit verlinkten Tools, Beschreibung und farbigem Tipp-Kasten

### ☑️ Checkliste-Tab
- **40+ OWASP-basierte Testpunkte** in 6 Kategorien
- Kategorien: Recon, Injection, Auth & Session, Autorisierung, Web-Spezifisch, Business Logic
- HIGH / MEDIUM / LOW / INFO Schwere-Badges
- Fortschrittsbalken mit Prozentwert
- Fortschritt wird per `localStorage` gespeichert – bleibt beim nächsten Öffnen erhalten
- Zurücksetzen-Button

### 📖 Glossar-Tab
- 23 Begriffe: XSS, SQLi, IDOR, SSRF, CSRF, XXE, SSTI, RCE, LFI, CVSS, CVE, JWT, OWASP u.v.m.
- Vollname, Definition und Beispiel pro Begriff
- Eigenes Suchfeld

### ⚙️ Verwaltung-Tab (passwortgeschützt)
- **Passwortschutz** mit SHA-256-Hash, Passwort änderbar
- Session bleibt offen solange der Tab aktiv ist, manuell sperrbar mit 🔒
- **Alle Tools** in einer Tabelle – built-in und eigene
- ✏️ **Bearbeiten** – Formular mit allen Feldern vorausgefüllt
- ➕ **Hinzufügen** – eigene Tools mit Emoji, Name, URL, Kategorie, Kosten, Level, Beschreibung
- 🙈 **Ausblenden / Einblenden** – Tools aus dem Tools-Tab verstecken ohne sie zu löschen
- 🗑️ **Löschen** – eigene Tools dauerhaft löschen; built-in Tools werden ausgeblendet
- ⬇️ **JSON-Export** eigener Tools
- ⬆️ **JSON-Import** auf neuem Gerät

---

## Kategorien

| Kategorie | Inhalt |
|---|---|
| 🔭 Recon & OSINT | Subdomain-Enumeration, DNS, Cert Logs, Webarchiv, Shodan |
| 🧪 Security Testing | OWASP Testing Guide, Burp Suite Academy, Exploit-DB, Cheat Sheets |
| 🌀 Fuzzing & Scanner | Nuclei, ffuf, Gobuster, Nikto, Amass |
| 🔀 Proxy & Intercept | Burp Suite, OWASP ZAP, Caido, mitmproxy |
| 🗄️ Vulnerability DBs | FOFA, Netlas, BuiltWith, Wappalyzer |
| ⚠️ CVE & Advisories | NVD (NIST), Mitre CVE, Packet Storm |
| 🏅 Bounty Platforms | HackerOne, Bugcrowd, Intigriti, YesWeHack |
| ⚙️ Prog & Misc | HTTPie, Whois Lookup, Webhook.site |
| 📋 Directory Tools | BBRadar, BBScope, RapidDNS, Pentest-Tools |
| 🏆 Platforms | Bug Bounty Daily, Forum, Payload Playground, Hacktivity |

---

## Schnellstart

```bash
git clone https://github.com/DEIN-USERNAME/bug-bounty-dashboard.git
cd bug-bounty-dashboard
# index.html direkt im Browser öffnen – fertig
```

### GitHub Pages

1. Repo auf GitHub pushen
2. Einstellungen → Pages → Branch: `main`, Ordner: `/ (root)`
3. Erreichbar unter `https://DEIN-USERNAME.github.io/bug-bounty-dashboard`

### Lokaler Dev-Server

```bash
npx serve .
# oder
python3 -m http.server 8080
```

---

## Verwaltung & Passwort

Der Verwaltungs-Tab ist passwortgeschützt.

| | |
|---|---|
| **Standard-Passwort** | `admin` |
| **Passwort ändern** | Verwaltung → 🔑 Passwort ändern |
| **Speicherung** | SHA-256-Hash im `localStorage` |
| **Session** | Offen solange Browser-Tab offen, manuell sperrbar |

> **Hinweis:** Da die App als statische HTML-Datei läuft, ist der Schutz clientseitig. Für den Einsatz auf einem eigenen Gerät oder privaten GitHub Pages ist das ausreichend.

---

## Eigene Tools hinzufügen (via Verwaltung)

Kein Code-Editing nötig – einfach im ⚙️ Verwaltungs-Tab auf **＋ Neues Tool** klicken und das Formular ausfüllen. Eigene Tools werden per `localStorage` gespeichert und können als JSON exportiert/importiert werden.

**Alternativ direkt im Code** – `tools`-Array in `index.html` erweitern:

```js
{
  name:   "Tool Name",
  emoji:  "🔍",
  url:    "example.com",
  href:   "https://example.com",
  cat:    "Recon & OSINT",       // eine der 10 Kategorien
  cost:   "free",                // free | freemium | paid
  diff:   "beginner",            // beginner | intermediate | advanced
  active: true,                  // true = aktiv gepflegt
  desc:   "Kurze Beschreibung."
},
```

---

## Datenspeicherung

Alle Nutzerdaten bleiben lokal im Browser – kein Server, keine Cloud.

| Daten | Speicherort |
|---|---|
| Favoriten | `localStorage` |
| Checklisten-Fortschritt | `localStorage` |
| Eigene Tools | `localStorage` |
| Ausgeblendete Tools | `localStorage` |
| Passwort-Hash | `localStorage` |
| Login-Session | `sessionStorage` |

---

## Lizenz

MIT – frei nutzbar, frei erweiterbar.

---

> Erstellt mit [Highfish AI](https://highfish.ai)
