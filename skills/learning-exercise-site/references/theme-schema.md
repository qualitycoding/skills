# Theme file format

`data/manifest.json` lists theme files in display order: `{ "themes": ["themes/<id>.json", ...] }`.
Each theme file holds four exercises keyed `lasa` (reading), `lyssna` (listening), `skriva` (writing) and
`tala` (speaking). Every exercise has exactly 10 scored items (`questions` for reading and listening, `tasks` for
writing and speaking). The excerpt below is shortened from the reference implementation; real files carry 10 items.

## Item types

| type | used in | fields |
|---|---|---|
| `mc` | reading, listening | `q`, `options` (≥3), `answer` (index), `explain` |
| `tf` | reading, listening | `q`, `answer` (boolean), `explain` |
| `dictation` | listening | `text` (no digits) |
| `gap` | writing | `q` containing `___`, `hint`, `accept` (first = canonical), `explain` |
| `order` | writing | `en` (meaning), `accept` (first = canonical sentence; chips are its words) |
| `translate` | writing | `en`, `keywords` (list of stem groups), `model` |
| `read` | speaking | `text` (no digits) |
| `respond` | speaking | `q`, `hint`, `keywords`, `model` |

Text fields accept the markup `[[shown|explanation|label]]`, label ∈ `slang`, `vardagligt`, `idiom`, or empty.

## Example (shortened)

```json
{
  "id": "regeringen",
  "title": "Regeringsbildningen efter valet",
  "short": "Regeringen",
  "dateLabel": "2 november 2026",
  "level": "B1–B2",
  "summary": "Sju veckor efter valet har Sverige fortfarande ingen ny regering. Nu ska riksdagen rösta om Centerpartiets ledare.",
  "sources": [
    {
      "title": "SVT: Valmyndigheten har fastställt resultatet",
      "url": "https://www.svt.se/nyheter/inrikes/senaste-nytt-om-val-2026"
    }
  ],
  "exercises": {
    "lasa": {
      "title": "Ny omröstning om statsminister på tisdag",
      "intro": "Läs texten. Tryck på de understrukna orden för förklaringar. Svara sedan på frågorna.",
      "text": [
        "Så kan det låta i fikarummet (påhittat exempel): – [[Hänger du med|förstår du, följer du|vardagligt]] i det här? – Nej, det är [[sjukt|väldigt, jättemycket|slang]] [[rörigt|krångligt, oordnat|vardagligt]]. Jag är rätt [[less|trött på något, irriterad|vardagligt]] på allt [[tjafs|onödigt bråk, gnäll|vardagligt]]. – Samma här. Men det är väl så demokrati funkar när ingen får egen majoritet."
      ],
      "questions": [
        {
          "type": "mc",
          "q": "I samtalet i fikarummet: vad betyder ”jag är less”?",
          "options": [
            "Jag är glad",
            "Jag är trött på det",
            "Jag är sjuk",
            "Jag förstår inte"
          ],
          "answer": 1,
          "explain": "”Less” är vardagligt och betyder trött på något."
        },
        {
          "type": "tf",
          "q": "Socialdemokraterna blev största parti i valet.",
          "answer": true,
          "explain": "S fick 28 procent av rösterna."
        }
      ]
    },
    "lyssna": {
      "title": "Så går en statsministeromröstning till",
      "intro": "…",
      "vocab": [
        "[[talmannen|riksdagens ordförande, som leder regeringsbildningen]]"
      ],
      "script": [
        "Hej och välkommen till Ekonomi och politik. I dag förklarar vi hur det går till när Sverige får en ny statsminister."
      ],
      "questions": [
        {
          "type": "dictation",
          "text": "Talmannen pratar med alla partier."
        }
      ]
    },
    "skriva": {
      "title": "Skriv om regeringsfrågan",
      "tasks": [
        {
          "type": "gap",
          "q": "Riksdagen ___ (rösta) nej till förslaget i oktober.",
          "hint": "Preteritum (dåtid).",
          "accept": [
            "röstade"
          ],
          "explain": "rösta – röstade – har röstat"
        },
        {
          "type": "order",
          "en": "On Tuesday the Riksdag votes again.",
          "accept": [
            "På tisdag röstar riksdagen igen."
          ],
          "explain": "Tidsuttryck först → verbet på plats två (V2)."
        },
        {
          "type": "translate",
          "en": "Sweden still has no new government.",
          "keywords": [
            [
              "sverige"
            ],
            [
              "fortfarande",
              "än"
            ],
            [
              "ingen",
              "inte någon",
              "inte en"
            ],
            [
              "ny"
            ],
            [
              "regering"
            ]
          ],
          "model": "Sverige har fortfarande ingen ny regering."
        }
      ],
      "free": {
        "prompt": "…",
        "words": "50–80",
        "checklist": [
          "…"
        ],
        "model": "…"
      }
    },
    "tala": {
      "title": "Prata om politiken",
      "tasks": [
        {
          "type": "read",
          "text": "Sverige har fortfarande ingen ny regering."
        },
        {
          "type": "respond",
          "q": "Vem leder övergångsregeringen?",
          "hint": "Svara med namnet och verbet ”leder”.",
          "keywords": [
            [
              "kristersson"
            ],
            [
              "leder",
              "ledde"
            ]
          ],
          "model": "Ulf Kristersson leder övergångsregeringen."
        }
      ]
    }
  }
}
```
