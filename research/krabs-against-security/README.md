# Krabs Against Security: Research

Working research and engineering investigation notes for **Krabs Against Security** (K.A.S.), a web-native and print-and-play cybersecurity incident response card game inspired by Black Hills Information Security's *Backdoors & Breaches* (CC BY-SA 4.0).

## Investigation Documents

1. [`mechanics-and-thematics.md`](mechanics-and-thematics.md): Deep dive into Backdoors & Breaches core loop, d20 dice mechanics, MITRE ATT&CK and NIST SP 800-61r2 mapping, Creative Commons licensing compliance, and nautical satire thematics (the Krusty Krab SOC vs. the Plankton APT).
2. [`print-and-play-spec.md`](print-and-play-spec.md): Physical print-and-play engineering standards covering poker card dimensions ($2.5'' \times 3.5''$), 300 DPI resolution, 3mm bleed margins, safe insets, 3x3 sheet layouts on US Letter and A4, duplex column mirroring, 2x3 gutter-fold assembly, and client-side PDF rendering.
3. [`art-deferral-pipeline.md`](art-deferral-pipeline.md): Architecture for decoupled visual asset production, specifying a 3-tier system: Tier 0 procedural CSS/SVG vector fallback, Tier 1 typed art manifest with structured generative prompts, and Tier 2 asynchronous generation pipeline using local/spoke synthesis (`art-router` / `image-generator`).
4. [`vertical-slices.md`](vertical-slices.md): Execution roadmap decomposing the project into six testable vertical slices (Slices 0 through 5), with strict definitions of done, component boundaries, and testing criteria.
5. [`deployment-and-repositories.md`](deployment-and-repositories.md): Dual public repository topology (`krabs-against-security-web` and `krabs-against-security-cards`), Cloudflare Pages edge hosting architecture, and custom DNS routing under `krabs.ketron.dev` (mirroring `secpanic.ketron.dev`).

## Downstream Deliverables

- **Initiative Spec**: `../../projects/krabs-against-security/README.md`
- **Formal Research Dossier**: `../../results/research/krabs-against-security/2026-10-28/research-dossier.md`
- **Project Proposal**: `../../results/reports/proposal/krabs-against-security/2026-10-28/project-proposal.md`
