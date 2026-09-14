# CV — Higor Luiz Araújo de Mesquita

Generated files:

- `Higor-Mesquita-CV.docx` — send this one when an application form asks for Word, or when
  the posting goes through an ATS. Most parsers handle `.docx` more reliably than PDF.
- `Higor-Mesquita-CV.pdf` — send this one for direct email and for anything a human reads
  first, since the layout cannot shift between machines.

## Regenerating

Both files are built from the same source, so they can never drift apart.

```bash
pip install python-docx reportlab
python3 cv/build_cv.py
```

Edit the text in `cv_content.py`, never in the `.docx` or `.pdf` — those are build outputs
and get overwritten. Layout and spacing live in `build_cv.py`.

## Layout rules being enforced

The two renderers share the same constants so the Word and PDF versions match:

- Single column, no text boxes, no layout tables around body content, standard section
  headings. This is what keeps applicant tracking systems able to read it.
- Arial in Word, Helvetica in the PDF. They are metrically equivalent, and both exist
  everywhere, so nothing reflows on someone else's machine.
- A role is never split across a page break, so a reader who lands on page 2 always sees
  the company, title, and dates above the bullets.
- Footer carries the name and page number, so a separated page stays identifiable.

## Verifying a change

After editing, confirm the output still parses the way an ATS would read it:

```bash
python3 -c "
import pymupdf
d = pymupdf.open('cv/Higor-Mesquita-CV.pdf')
print(d.page_count, 'pages')
print('\n'.join(p.get_text() for p in d))
"
```

The text should come out in reading order with accents intact. If it looks scrambled, the
layout broke something a parser depends on.
