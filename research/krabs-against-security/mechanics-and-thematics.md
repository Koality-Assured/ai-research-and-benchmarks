---
doc_kind: research_note
canonical_id: kas-mechanics-and-thematics
topics: [game-design, cyber-security, tabletop-mechanics, parody-thematics, licensing]
---

# Krabs Against Security: Mechanics & Thematics Research

## 1. Backdoors & Breaches Mechanics Analysis

*Backdoors & Breaches* (B&B), created by Black Hills Information Security (BHIS) under lead designer John Strand, is the industry standard tabletop card game for teaching and practicing cybersecurity incident response (IR).

### 1.1 The Core Game Loop

B&B operates on an asymmetric cooperative model where an **Incident Master** (facilitator / game master) leads one or more **Defenders** (SOC analysts, incident handlers, managers) through an unfolding cyber incident:

1. **Scenario Setup**:
   - The Incident Master secretly draws one card from each of four core attack decks to assemble the unseen breach vector:
     - **Initial Compromise** (Entry vector)
     - **Pivot & Escalate** (Lateral movement / privilege escalation)
     - **Persistence** (Maintaining footholds)
     - **C2 & Exfiltration** (Command & control / data egress / impact)
   - These four cards are placed face-down on the table in order.
2. **Defensive Investigation & Containment**:
   - Defenders choose which phase or asset to investigate and select an applicable **Procedure Card** (e.g., *Endpoint Analysis*, *Network Analysis*, *Log Analysis*, *Technical Controls*).
   - The Defender rolls a standard twenty-sided die ($d20$).
   - Each Procedure Card specifies difficulty check targets (typically $11+$ for basic detection, $15+$ or $16+$ for root-cause attribution or containment, with specific conditional modifiers).
3. **Outcome Resolution**:
   - **Success (Roll $\ge$ Target)**: The Incident Master reveals relevant cards, provides tactical telemetry clues, or marks an attack phase as contained/neutralized.
   - **Failure (Roll $<$ Target)**: The defenders gain no new intelligence, and a **Strike** is recorded on the escalation counter.
4. **Inject Complications**:
   - At predetermined trigger points (e.g., every 2 strikes, or on rolling a natural 1), the Incident Master draws an **Inject Card**.
   - Injects simulate real-world incident friction: regulatory subpoenas, micromanaging C-level executives, media leaks, expired SSL certificates, corrupted backups, or key responders being unreachable.
5. **Win / Loss Conditions**:
   - **Defenders Win**: All four attack phases are identified, contained, and eradicated before the strike counter reaches the maximum threshold (typically 10 strikes).
   - **Attacker Wins (Enterprise Failure)**: The strike counter hits 10, or a critical timeout/ransomware deadline passes, resulting in data loss, regulatory shutdown, or complete compromise.

### 1.2 Educational Alignment: NIST SP 800-61r2 & MITRE ATT&CK

The power of B&B lies in grounding lighthearted tabletop play in standard incident handling frameworks:
- **NIST SP 800-61r2 Phases**: Preparation $\rightarrow$ Detection & Analysis $\rightarrow$ Containment, Eradication & Recovery $\rightarrow$ Post-Incident Activity.
- **MITRE ATT&CK TTPs**: Every attack card directly references an authentic ATT&CK technique ID (e.g., T1566 Phishing, T1078 Valid Accounts, T1059 Command and Scripting Interpreter, T1055 Process Injection).

---

## 2. Thematic Adaptation: Krabs Against Security (K.A.S.)

"Krabs Against Security" recontextualizes the high-stress environment of enterprise security operations into a satirical, undersea corporate infrastructure.

### 2.1 Narrative Premise & Setting

- **Enterprise**: *The Krusty Krab Corporation* (operating across the Bikini Bottom metropolitan basin).
- **The Crown Jewel**: The legendary *Krabby Patty Secret Formula*—held in an encrypted vault, backed up across barnacle-encrusted legacy NAS drives, and transmitted to automated kitchen frying apparatuses via underwater SCADA telemetry.
- **The Leadership**: Eugene H. Krabs serves as CEO and nominal CISO. Driven by extreme penny-pinching, Mr. Krabs refuses to pay for enterprise EDR licenses, insists on using end-of-life operating systems to avoid upgrade fees, and demands that incident responders work overtime without additional pay.
- **The Threat Actor**: *APT-Chum* (The Plankton Threat Actor Group). Led by Sheldon J. Plankton, a microscopic but relentlessly creative adversary utilizing custom exploits, automated botnets, living-off-the-reef binaries, and social engineering.

### 2.2 Card Decks Breakdown

| Deck Type | Color Identifier | Count | Thematic Focus | Mechanical Role |
| :--- | :--- | :--- | :--- | :--- |
| **Initial Compromise** | Red / Crimson | 12 | Infiltration vectors into undersea network | Scenario card 1: First point of breach |
| **Pivot & Escalate** | Amber / Yellow | 12 | Internal lateral movement across reefs | Scenario card 2: Host & privilege sprawl |
| **Persistence** | Purple / Violet | 12 | Hidden footholds in underwater nodes | Scenario card 3: Surviving reboots/scrubs |
| **C2 & Exfiltration** | Deep Brown / Bronze | 12 | Undersea beacons and formula exfil | Scenario card 4: Crown jewel extraction |
| **Procedures** | Ocean Blue / Teal | 16 | Defender investigative & containment play | Active d20 roll cards used by players |
| **Injects** | Kelp Green / Slate | 16 | Maritime operational chaos and friction | Event modifiers drawn on strikes or turns |

### 2.3 Representative Card Inventory

#### A. Initial Compromise (Red)
1. **Spear Phishing with Actual Chum**: An email offering a 90% discount on kelp flour contains an attachment named `invoice_october.xlsm` with an embedded malicious macro.
2. **Unpatched Kelp-Facing Server**: An ancient HTTP daemon from 1999 running on a sunken shipwreck router exposed to public sub-sea web traffic.
3. **Salty Insider Threat**: A disgruntled, underpaid cashier leaves a USB rubber ducky disguised as an oyster shell plugged into the front register.
4. **Physical Trench Intrusion**: A tiny operative physically crawls through the kitchen floor drainage pipes directly into the server closet.
5. **Supply Chain Kelp Poisoning**: Malicious npm packages injected into the third-party ordering portal utilized by undersea delivery drivers.

#### B. Pivot & Escalate (Yellow)
1. **Pass-the-Kelp-Hash**: Insecure legacy NTLM authentication allows the adversary to reuse the shift manager's credentials across all fryer IoT sensors.
2. **Living Off the Coral (LOLBins)**: Executing native undersea PowerShell and WMI scripts to evade basic signature-based antivirus.
3. **Sponge-in-the-Middle (SITM)**: ARP cache poisoning on the internal dining room switchboard intercepts cleartext kitchen order tickets.
4. **Anemone Privilege Escalation**: Exploiting unquoted service paths in the automated deep-fryer temperature regulation daemon.
5. **Active Directory Trench Forest Compromise**: Escalating from a standard kitchen display unit to domain admin on `dc01.bikini.local`.

#### C. Persistence (Purple)
1. **Barnacle Registry Run Keys**: Writing autostart triggers in the POS terminal registry to survive daily restaurant opening restarts.
2. **Deep Trench Web Shell**: A tiny obfuscated PHP backdoor hidden in `/var/www/krusty/menu_upload.php`.
3. **Cron Job of the Depths**: A scheduled midnight cron task running as root that beacons back to `chumbucket.onion`.
4. **Backdoored Submersible Firmware**: Tampering with the bootloader of the deep-sea formula backup submarine.
5. **Golden Clam Ticket**: Forged Kerberos Ticket Granting Tickets (TGT) providing perpetual, stealthy access across all underwater subnets.

#### D. C2 & Exfiltration (Brown)
1. **DNS Tunneling via Barnacle DNS**: Exfiltrating base64-encoded secret formula salt ratios through low-volume DNS TXT queries.
2. **Encrypted Cloud Trench Bucket**: Pushing compressed tarballs of proprietary recipes directly to an unmonitored external AWS S3 bucket over TLS 443.
3. **Red Snapper Ransomware**: Encrypting all point-of-sale databases right before the Friday lunch rush and demanding 50,000 Barnacle Bitcoins.
4. **Dead Man's Chest Steganography**: Embedding formula specs inside innocent JPEG photos of jellyfish posted to public social media accounts.
5. **Slow-and-Low Sonar ICMP Exfil**: Crafting custom echo requests that mimic standard marine acoustic telemetry to slip past network egress filters.

#### E. Defensive Procedures (Blue - d20 Checks)
1. **Endpoint Analysis**: Volatility memory dumps and Autopsy disk forensics on compromised cash registers ($11+$ basic detection, $15+$ full triage).
2. **Network Packet Sniffing**: Deploying Zeek / Wireshark on underwater fiber taps ($11+$ identify beaconing, $14+$ decode payload).
3. **Barnacle Log Analysis**: SIEM aggregation of Windows Event Logs and syslog from POS registers ($11+$ trace IP, $15+$ timeline correlation).
4. **Technical Controls & Isolation**: Revoking Kerberos tickets, isolating VLANs, or resetting administrative passwords ($12+$ successful containment).
5. **Threat Intelligence & Attribution**: Querying Ocean-OSINT feeds to confirm APT-Chum TTPs and known C2 IP ranges ($10+$ attribution).
6. **Executive & Legal PR Handling**: Navigating regulatory disclosure under the Undersea Privacy Act while stopping Mr. Krabs from firing the SOC to save cash ($13+$ PR mitigation).

#### F. Injects (Kelp Green / Slate)
1. **Squidward's Shift Ended**: The senior responder clocks out at exactly 5:00 PM and enables 'Do Not Disturb' on their shell phone ($+3$ difficulty to next 2 checks).
2. **Mr. Krabs Screams About the Electric Bill**: The CEO physically unplugs the secondary SIEM monitor wall to save three cents an hour (Lose 1 player action).
3. **Over-Enthusiastic Spongebob Containment**: A junior analyst physically severs the main undersea fiber conduit with kitchen shears (Widespread network outage; counts as 2 strikes).
4. **Health Inspector Surprise Audit**: Government regulators arrive unannounced, demanding documentation while active ransomware is detonating.
5. **Backups on Underwater Tape**: The backups exist and are verified, but the tape drive was accidentally dropped into the Mariana Trench.

---

## 3. Legal & Intellectual Property Analysis

### 3.1 Creative Commons (CC BY-SA 4.0) Compliance
Black Hills Information Security releases *Backdoors & Breaches* under **CC BY-SA 4.0 International**.
- **Attribution (BY)**: K.A.S. must explicitly state: *"Based on Backdoors & Breaches by Black Hills Information Security, licensed under CC BY-SA 4.0."* with links to the license and original project.
- **ShareAlike (SA)**: Any rules, mechanics, or derivative gameplay elements published by K.A.S. must also be licensed under CC BY-SA 4.0.
- **Commercial & Open Source Freedom**: The license permits digital sharing, custom derivative decks, web applications, and print distribution as long as the SA and BY obligations are honored.

### 3.2 Trademark & Parody Fair Use Boundaries
- **Parody Protection**: Under U.S. copyright and trademark law (e.g., *Campbell v. Acuff-Rose Music*, *Jack Daniel's Properties, Inc. v. VIP Products LLC*), commentary, humor, and educational parody are protected, provided confusion regarding official affiliation is minimized.
- **Trademark Hygiene Guidelines**:
  - The game is an original educational parody.
  - Do not use copyrighted audio clips, verbatim trade names, or proprietary studio logos (e.g., Nickelodeon, Paramount).
  - Use original satirical naming (*"Krusty Krab Enterprises"*, *"Plankton APT"*, *"Bikini Bottom SOC"* in satirical contexts).
  - All original card illustrations generated or commissioned must be distinct, stylized parody art, not ripped frames from animated television broadcasts.
