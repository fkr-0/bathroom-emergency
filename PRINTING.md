# Booklet printing

The booklet PDFs are **already imposed** for folding. Do not enable a printer
driver's own booklet/reordering mode a second time.

## One-command print files

After `npm run build`, use one of these complete print runs containing the Shelf
intro booklet followed by all eleven books:

- `build/booklet/all-subguides_booklet-print.pdf` — colour;
- `build/booklet/all-subguides_booklet-print_mono.pdf` — monochrome.

For a single book, use the corresponding file below
`build/booklet/subguides/<BOOK>/` instead.

`build/booklet/PRINTING.md` is generated with the build and adds the exact PDF
side ranges and physical sheet ranges for every book in the combined files.

## Printer settings

Use these settings unless the printer itself requires a documented equivalent:

1. paper: **A4, portrait**;
2. scale: **100% / Actual size** — do not use Fit, Shrink, or Scale to page;
3. duplex: **on**;
4. duplex binding: **flip on long edge**;
5. page order: normal/front-to-back;
6. booklet mode in the print dialog: **off**.

The source pages are A4/2 (105 × 297 mm). The build places two logical pages on
each A4 side at 1:1 and shuffles them into saddle-stitch order. Every individual
book is padded only to the next multiple of four logical pages.

## After printing

The Shelf introduction and each colour book remain their **own booklets** even
when the combined PDF is used.
The combined file concatenates complete imposed booklets; every component has an
even number of printed sides, so a duplex sheet never crosses from one book into
the next.

Separate the printed sheet groups at the boundaries listed in
`build/booklet/PRINTING.md`, keep each group in printed order, fold each group on
the vertical centre line, then staple or bind that book separately.

Before a large run, print one short book first and verify that:

- the front cover is on the outside after folding;
- page 2 follows page 1 when opened;
- text is not scaled;
- front/back orientation is upright;
- the centre fold lands between the two A4/2 pages.

If the back side is upside down, the usual cause is short-edge duplexing: switch
to **long-edge** flipping and repeat the one-book test.
