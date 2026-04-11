# Bug Bounty Resources Dashboard

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
