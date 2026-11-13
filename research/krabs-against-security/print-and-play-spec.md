---
doc_kind: research_note
canonical_id: kas-print-and-play-spec
topics: [print-and-play, physical-prototyping, card-geometry, duplex-alignment, pdf-generation]
---

# Krabs Against Security: Print-and-Play (PnP) Engineering Specification

## 1. Physical Geometry & Dimensions

To ensure compatibility with standard tabletop accessories (card sleeves, deck boxes, and commercial print-on-demand services like MakePlayingCards and DriveThruCards), all cards conform to the international standard Poker Card format.

### 1.1 Card Dimensions Matrix

| Boundary Zone | Dimensions (Inches) | Dimensions (Millimeters) | Pixel Size @ 300 DPI | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Trim Size (Finished Card)** | $2.500'' \times 3.500''$ | $63.5 \times 88.9\text{ mm}$ | $750 \times 1050\text{ px}$ | The exact cut line where the physical card is separated. |
| **Bleed Margin (Overbleed)** | $+0.125''$ per side | $+3.175\text{ mm}$ per side | $+37.5\text{ px}$ per side | Background graphics and borders extend into this zone. |
| **Full Canvas (with Bleed)** | $2.750'' \times 3.750''$ | $69.85 \times 95.25\text{ mm}$ | $825 \times 1125\text{ px}$ | Total raw card canvas required before trimming. |
| **Safe Zone (Inner Margin)** | $-0.125''$ inside trim | $-3.175\text{ mm}$ inside trim | $-37.5\text{ px}$ inside trim | Critical text, icons, d20 numbers, and titles stay inside. |
| **Safe Area Box** | $2.250'' \times 3.250''$ | $57.15 \times 82.55\text{ mm}$ | $675 \times 975\text{ px}$ | Absolute boundary for non-bleed visual elements. |
| **Corner Radius** | $0.125''$ (1/8") | $3.5\text{ mm}$ | $37.5\text{ px}$ | Standard die-cut corner radius. |

---

## 2. Sheet Layout Standards (3x3 Grid)

A single standard deck of 80 cards can be packaged into 9 physical sheets (8 sheets of 9 cards, 1 sheet of 8 cards + 1 quick reference rules card).

```text
Sheet Layout (3 columns x 3 rows = 9 cards per page):
+-----------+-----------+-----------+
| Card [0]  | Card [1]  | Card [2]  |  Row 1
+-----------+-----------+-----------+
| Card [3]  | Card [4]  | Card [5]  |  Row 2
+-----------+-----------+-----------+
| Card [6]  | Card [7]  | Card [8]  |  Row 3
+-----------+-----------+-----------+
```

### 2.1 US Letter Sheet Specifications ($8.5'' \times 11.0''$ / $215.9 \times 279.4\text{ mm}$)
- **Total Card Grid Width**: $3 \times 2.50'' = 7.50''$ (trim) or $3 \times 2.75'' = 8.25''$ (with bleed).
- **Total Card Grid Height**: $3 \times 3.50'' = 10.50''$ (trim).
- **Margins (Centering)**:
  - Horizontal Margins: $(8.50'' - 7.50'') / 2 = 0.50''$ ($12.7\text{ mm}$).
  - Vertical Margins: $(11.00'' - 10.50'') / 2 = 0.25''$ ($6.35\text{ mm}$).
- **Hardware Margin Compliance**: Modern consumer inkjet and laser printers require a minimum unprintable hardware margin of $0.1875''$ to $0.25''$. The $0.25''$ vertical margin fits strictly within standard printer margins.

### 2.2 ISO A4 Sheet Specifications ($210.0 \times 297.0\text{ mm}$)
- **Total Card Grid Width**: $3 \times 63.5\text{ mm} = 190.5\text{ mm}$ (trim).
- **Total Card Grid Height**: $3 \times 88.9\text{ mm} = 266.7\text{ mm}$ (trim).
- **Margins (Centering)**:
  - Horizontal Margins: $(210.0\text{ mm} - 190.5\text{ mm}) / 2 = 9.75\text{ mm}$.
  - Vertical Margins: $(297.0\text{ mm} - 266.7\text{ mm}) / 2 = 15.15\text{ mm}$.

---

## 3. Duplex (Double-Sided) Printing & Alignment Rules

Double-sided printing on consumer hardware presents two major failure modes: **horizontal axis flipping** and **hardware registration drift** ($1\text{ mm} - 2\text{ mm}$).

### 3.1 The Horizontal Mirroring Rule
When duplex printing flips along the **Long Edge** (the standard portrait orientation mode), page 2 is flipped horizontally relative to page 1. Therefore, the back-face grid must reverse the horizontal column order:

$$\text{Front Page: } \begin{bmatrix} C_1 & C_2 & C_3 \end{bmatrix} \iff \text{Back Page: } \begin{bmatrix} C_3 & C_2 & C_1 \end{bmatrix}$$

```text
Front Sheet (Page 1)            Back Sheet (Page 2 - Long Edge Flip)
+-------+-------+-------+       +-------+-------+-------+
|  [0]  |  [1]  |  [2]  |       |  [2]  |  [1]  |  [0]  |
+-------+-------+-------+       +-------+-------+-------+
|  [3]  |  [4]  |  [5]  |       |  [5]  |  [4]  |  [3]  |
+-------+-------+-------+       +-------+-------+-------+
|  [6]  |  [7]  |  [8]  |       |  [8]  |  [7]  |  [6]  |
+-------+-------+-------+       +-------+-------+-------+
```

### 3.2 Crop Marks & Cutting Guides
- **Crosshair Crop Marks**: Placed in the outer margins extending from the corner trim lines (length $5\text{ mm}$, stroke width $0.5\text{ pt}$ / $0.18\text{ mm}$, color `#333333`).
- **Crop marks appear on both front and back sheets** so users can align rotary paper trimmers or steel rulers from either side.
- **Shared Cut Line Mode**: Cards are abutted without bleed gaps between cards on the sheet, allowing a single straight razor cut to separate adjacent cards without double-trimming scrap slivers.

### 3.3 The "Gutter-Fold" Craft Method (Duplex-Free Alternative)
For users whose printers suffer severe duplex registration skew ($>3\text{ mm}$):
- Provide an alternate **2x3 Gutter-Fold Layout** (6 cards per sheet).
- Front cards and their corresponding backs are printed directly adjacent along a vertical center fold line.
- The user scores the center line, folds the paper back-to-back over a core sheet of cardstock ($110\text{ lb}$ / $300\text{ gsm}$) using spray adhesive or glue stick, and cuts along the perimeter guides. Alignment is 100% physically guaranteed regardless of printer mechanics.

---

## 4. Ink-Saver / Eco-Print Mode

Home ink cartridges are expensive. K.A.S. includes a dedicated **Eco-Print Toggle**:
- **Full Color Mode**: Rich ocean gradients, weathered parchment textures, colored deck borders, and saturated card illustrations.
- **Eco Mode (Low Ink)**:
  - Background textures disabled (pure `#ffffff` white).
  - Deck colors reduced to $1.5\text{ pt}$ crisp line borders and small color-coded badge tags.
  - Card illustration boxes converted to high-contrast monochrome line art or omitted in favor of expanded text descriptions.
  - Reduces printer ink consumption by $\approx 78\%$ according to standard coverage models.

---

## 5. Web-to-Print Technical Architecture

### 5.1 CSS Paged Media (`@media print`)
```css
@media print {
  @page {
    size: letter portrait;
    margin: 0;
  }
  body {
    background: transparent;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .no-print {
    display: none !important;
  }
  .print-page {
    page-break-after: always;
    break-after: page;
    width: 8.5in;
    height: 11in;
    position: relative;
    overflow: hidden;
  }
}
```

### 5.2 Programmatic Client-Side PDF Engine (`pdf-lib`)
To bypass browser-specific print preview scaling bugs (such as Chrome auto-shrinking pages by 97% or margins shifting):
- Embed `pdf-lib` (pure JavaScript, zero server roundtrip).
- Generate a pre-compiled, mathematically perfect PDF document with exact millimeter coordinates ($1\text{ pt} = 1/72\text{ in}$).
- Users click **"Download Print-Ready PDF"** and receive a vector-sharp document configured with default `PrintScaling = None`.

### 5.3 Virtual Tabletop (VTT) & Digital Asset Exports
In addition to 9-card print sheets, the export engine provides:
- **Zip of Single Cards (PNG)**: $750 \times 1050\text{ px}$ trimmed at 300 DPI for digital card sleeves and Roll20 / Foundry VTT decks.
- **Tabletop Simulator (TTS) Deck Sheet**: Standard $10 \times 7$ grid image composite (70 cards per image) compatible with Tabletop Simulator's custom deck importer.
