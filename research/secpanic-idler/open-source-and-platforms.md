---
doc_kind: research
canonical_id: secpanic-idler-open-source-and-platforms
topics: [games, incremental, idler, cloudflare, capacitor, mobile]
researched_on: 2026-09-08
---

# SecPanic Idler: open-source and platform research

## Scope

This first-pass review looked for open-source incremental/idler projects with useful save, offline-progress, and simulation patterns, then checked current primary-source hosting and mobile-packaging guidance. Source activity and platform requirements should be rechecked at release time.

## Comparable open-source projects

| Project | License / activity signal | Useful pattern for SecPanic Idler |
| --- | --- | --- |
| [Clicker Engine](https://github.com/blixxurd/clicker-engine) | MIT; visible activity through January 2026 | Deterministic TypeScript core, fixed-step loop, versioned JSON saves, and offline-progress calculation. Keep rules separate from UI, timers, and persistence. |
| [SynergismOfficial](https://github.com/Pseudo-Corp/SynergismOfficial) | MIT; visible activity through September 2026 | Typed save schemas, import/export, queued writes, browser/mobile storage adapters, and lifecycle flushing. Add `visibilitychange`/`pagehide` persistence as the prototype grows. |
| [Trimps](https://github.com/Trimps/Trimps.github.io) | GPL-3.0; visible activity through March 2025 | Treat away-time reconciliation as a first-class gameplay phase, with caps and player-facing summaries. |
| [The Modding Tree](https://github.com/Acamaeda/The-Modding-Tree) | MIT; visible commit through October 2024; maintenance appears comparatively stale | Namespaced saves, import/export, migration/version checks, corruption repair, and autosave. Use explicit migrations instead of silently reshaping state. |

These projects are references, not dependencies. Their code and assets remain under their own licenses; no third-party code or assets were copied into the prototype.

## Design takeaways

1. Keep a pure, deterministic simulation boundary. The prototype starts this in `src/game-state.js`, leaving the DOM and persistence adapter in `src/game.js`.
2. Make saves explicit envelopes with `gameId`, `schemaVersion`, `savedAt`, and validated state. Future schema changes should be migrations keyed by version.
3. Model away-time from timestamps, cap it, and show the player what happened. The prototype caps offline accrual at seven days.
4. Flush saves on lifecycle events once the UI expands; a one-second prototype timer is not sufficient for backgrounding or mobile suspension.
5. Treat local saves as player-owned sandbox state. Do not introduce server authority, leaderboards, or shared state until a gameplay requirement justifies the complexity.

## Cloudflare direction

Pages is the best first deployment fit for the static browser build: [Deploy anything to Cloudflare Pages](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/) covers static HTML deployment, and [Pages Git integration](https://developers.cloudflare.com/pages/get-started/git-integration/) covers automatic builds and previews. Use [Workers Static Assets](https://developers.cloudflare.com/workers/static-assets/) only when a Worker route or edge logic is needed alongside the assets. [Static asset headers](https://developers.cloudflare.com/workers/static-assets/headers/) provide the later path for cache and security headers.

The deployment should serve the static game only. Saves remain in browser storage/files and must never be treated as deploy artifacts or embedded secrets.

## Android and Apple direction

[Capacitor’s setup guide](https://capacitorjs.com/docs/getting-started) supports building the web assets once, configuring `webDir`, and adding Android/iOS projects with `npx cap add android`, `npx cap add ios`, and `npx cap sync`. The current platform guides list Android API 24+ and iOS 15+ with Xcode 26+; those versions are release-time facts and must be rechecked before shipping.

[Capacitor storage guidance](https://capacitorjs.com/docs/guides/storage) warns that browser storage can be evicted; small durable settings can move to Preferences, while larger saves may justify SQLite. Preserve the JSON export as the player-facing interchange format even if the mobile adapter changes.

Store packaging is not just a webview wrapper: [Apple’s App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) guideline 4.2 disfavors a merely repackaged website. Plan meaningful mobile value such as offline play, native sharing, haptics, notifications, or platform-specific UX. Android publishing uses a signed [Android App Bundle](https://developer.android.com/studio/publish/); current [Google target API requirements](https://developer.android.com/google/play/requirements/target-sdk) should be checked again at release time.

## Recommended architecture

```text
Pure game core (deterministic state transitions)
        ├── Browser UI + localStorage adapter + JSON export/import
        ├── Static Cloudflare Pages deployment
        └── Capacitor shell + platform storage adapter (future)
```

The first prototype follows this split and leaves platform-specific behavior outside the core.

