import os
import re
import sys
import traceback
import unicodedata
from textwrap import indent

SOURCE_FILE = "docs/awesome.md"
OUTPUT_FILE = "docs/global-grid-data.md"
FILTER_PLACEHOLDER = '<div id="tag-filters"></div>\n'
KNOWN_TAGS = {"dataset", "report", "map", "capacitydata"}

TYPE_EMOJI = {
    "dataset": "📊",
    "report": "📄",
    "map": "🗺️",
    "capacitydata": "📦",
    "date": "📅",
    "license": "⚖️",
}

LICENSES = {
        "mit": { "label": "MIT", "url": "https://opensource.org/licenses/MIT" },
        "apache-2.0": { "label": "Apache-2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0" },
        "gpl-3.0": { "label": "GPL-3.0", "url": "https://www.gnu.org/licenses/gpl-3.0.en.html" },
        "agpl-3.0": { "label": "AGPL-3.0", "url": "https://www.gnu.org/licenses/agpl-3.0.en.html" },
        "lgpl-3.0": { "label": "LGPL-3.0", "url": "https://www.gnu.org/licenses/lgpl-3.0.en.html" },
        "bsd-3-clause": { "label": "BSD-3-Clause", "url": "https://opensource.org/licenses/BSD-3-Clause" },
        "bsd-2-clause": { "label": "BSD-2-Clause", "url": "https://opensource.org/licenses/BSD-2-Clause" },
        "cc0": { "label": "CC0 1.0", "url": "https://creativecommons.org/publicdomain/zero/1.0/" },
        "cc-by-4.0": { "label": "CC-BY 4.0", "url": "https://creativecommons.org/licenses/by/4.0/" },
        "cc-by-sa-4.0": { "label": "CC-BY-SA 4.0", "url": "https://creativecommons.org/licenses/by-sa/4.0/" },
        "cc-by-nc-4.0": { "label": "CC-BY-NC 4.0", "url": "https://creativecommons.org/licenses/by-nc/4.0/" },
        "cc-by-nc-sa-4.0": { "label": "CC-BY-NC-SA 4.0", "url": "https://creativecommons.org/licenses/by-nc-sa/4.0/" },
        "odbl-1.0": { "label": "ODbL 1.0", "url": "https://opendatacommons.org/licenses/odbl/1-0/" },
        "cdla-permissive-2.0": { "label": "CDLA Permissive 2.0", "url": "https://cdla.dev/permissive-2-0/" },
        "proprietary": { "label": "Proprietary", "url": "https://en.wikipedia.org/wiki/Proprietary_software" }
    }

ALIAS_LICENSE = {
        "cc0-1.0": "cc0", "cc0": "cc0",
            "cc-by-4.0": "cc-by-4.0", "cc-by-sa 4.0": "cc-by-sa-4.0",
            "apache2": "apache-2.0", "apache-2": "apache-2.0",
            "gpl3": "gpl-3.0", "agpl3": "agpl-3.0", "lgpl3": "lgpl-3.0",
            "odbl": "odbl-1.0",
    }

GITHUB_BUTTON = """
You are looking for a way on how to download the power infrastructure data from OpenStreetMap? Here a different ways to get this data: 

1. If you are not interested in contributing to this dataset and are simply looking to export GIS-ready data, we kindly ask you to pay a fair price for a proper data export from [OpenInfraMap](https://www.infrageomatics.com/products/osm-export). This is particularly recommended if you are unfamiliar with OpenStreetMap or if you require an export of a large country.  
2. You want to use this data for energy system modelling like PyPSA-Earth, you know how to use Python and understand how to deal with large OpenStreetMap extracts. Please use [earth-osm](https://github.com/pypsa-meets-earth/earth-osm).
3. You are a contributor to OpenStreetMap, are able to filter data, and want to process this data on your machine for a small country, province, or a state? Please check out our [JOSM Starter-Kit](https://mapyourgrid.org/starter-kit/#josm-starter-kit) and you will learn how to download the data.

<div class="page-headers">
  <h2>Global Public Available Grid Data</h2>
</div>

<div class="awesome-github-btn">
  <a href="https://github.com/open-energy-transition/Awesome-Electrical-Grid-Mapping" target="_blank" rel="noopener">
    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
        width="20" height="20">
    <span>Contribute</span>
  </a>
</div>

<div class="awesome-github-btn">
  <a href="https://mapyourgrid.dynartio.com/files/awesomelist.csv" target="_blank" rel="noopener">
   <img src="https://raw.githubusercontent.com/open-energy-transition/MapYourGrid/refs/heads/main/docs/icons/download_icon.png"
         width="20" height="20">
    <span> Download in csv</span>
  </a>
</div>
"""


TAB_BLOCK_RE = re.compile(
    r"<!--\s*TABS:start\s*-->\s*(?P<body>.*?)\s*<!--\s*TABS:end\s*-->",
    re.DOTALL,
)
TAB_PANE_RE = re.compile(
    r"<!--\s*TAB:(?P<title>.*?)\s*-->\s*(?P<content>.*?)(?=(?:<!--\s*TAB:)|\Z)",
    re.DOTALL,
)

PAGE_HEADER_RE = re.compile(r'^#\s+(.+?)\s*$', re.MULTILINE)
HEADER_BLOCK_RE = re.compile(
    r'(<div class="page-headers">\s*<h1[^>]*>.*?</h1>\s*</div>)',
    re.DOTALL
)


TABLE_TEXT_RE = re.compile(r"<table>.*?<b>(.*?)</b>.*?</table>", re.DOTALL | re.IGNORECASE)

COLLAPSE_RE = re.compile(
    r'<!--\s*COLLAPSE:(?P<kind>[A-Za-z0-9_\-]+)\s*(?P<attrs>.*?)\s*-->\s*'
    r'(?P<body>.*?)'
    r'<!--\s*END\s+COLLAPSE\s*-->',
    re.DOTALL
)

ATTR_RE = re.compile(r'([A-Za-z0-9_\-]+)\s*=\s*"([^"]*)"')
RESOURCES_HEADER_RE = re.compile(r'^([ \t]*)####\s*(.+?)\s*$', re.MULTILINE)
EMOJI_RE = re.compile(r'^[ \t]*⚠️\s*', re.MULTILINE)

# ----------------------------
# Country flag injection (ISO2 aliases → emoji flags)
# ----------------------------
ISO2_ALIASES = [
    # --- Africa ---
    ("DZ", ["algeria"]), ("AO", ["angola"]),
    ("BJ", ["benin"]), ("BW", ["botswana"]), ("BF", ["burkina faso"]), ("BI", ["burundi"]),
    ("CV", ["cabo verde", "cape verde"]),
    ("CM", ["cameroon"]), ("CF", ["central african republic", "car"]),
    ("TD", ["chad"]), ("KM", ["comoros"]),
    ("CG", ["republic of the congo", "congo brazzaville", "brazzaville"]),
    ("CD", ["democratic republic of the congo", "drc", "dr congo", "congo kinshasa", "zaire"]),
    ("DJ", ["djibouti"]), ("EG", ["egypt"]), ("GQ", ["equatorial guinea"]),
    ("ER", ["eritrea"]), ("SZ", ["eswatini", "swaziland"]),
    ("ET", ["ethiopia"]), ("GA", ["gabon"]), ("GM", ["gambia", "the gambia"]),
    ("GH", ["ghana"]), ("GN", ["guinea"]),
    ("GW", ["guinea bissau", "guinea bisseau"]),
    ("CI", ["cote d'ivoire", "côte d'ivoire", "cote d ivoire", "cote divoire", "ivory coast", "cote d’ivoire"]),
    ("KE", ["kenya"]), ("LS", ["lesotho"]), ("LR", ["liberia"]), ("LY", ["libya"]),
    ("MG", ["madagascar"]), ("MW", ["malawi"]), ("ML", ["mali"]),
    ("MR", ["mauritania"]), ("MU", ["mauritius"]), ("MA", ["morocco", "kingdom of morocco"]),
    ("MZ", ["mozambique"]), ("NA", ["namibia"]), ("NE", ["niger"]), ("NG", ["nigeria"]),
    ("RW", ["rwanda"]), ("ST", ["sao tome and principe", "sao tome", "sao tome & principe"]),
    ("SN", ["senegal"]), ("SC", ["seychelles"]),
    ("SL", ["sierra leone"]), ("SO", ["somalia"]), ("ZA", ["south africa"]),
    ("SS", ["south sudan"]), ("SD", ["sudan"]),
    ("TZ", ["tanzania", "united republic of tanzania"]),
    ("TG", ["togo"]), ("TN", ["tunisia"]), ("UG", ["uganda"]),
    ("EH", ["western sahara"]), ("ZM", ["zambia"]), ("ZW", ["zimbabwe"]),

    # --- Europe ---
    ("AL", ["albania"]), ("AD", ["andorra"]), ("AM", ["armenia"]), ("AT", ["austria"]),
    ("BY", ["belarus"]), ("BE", ["belgium"]),
    ("BA", ["bosnia and herzegovina", "bosnia", "bosnia-herzegovina"]),
    ("BG", ["bulgaria"]), ("HR", ["croatia"]), ("CY", ["cyprus"]),
    ("CZ", ["czechia", "czech republic"]),
    ("DK", ["denmark"]), ("EE", ["estonia"]), ("FI", ["finland"]), ("FR", ["france"]),
    ("GE", ["georgia"]), ("DE", ["germany"]), ("GR", ["greece"]), ("HU", ["hungary"]),
    ("IS", ["iceland"]), ("IE", ["ireland"]), ("IT", ["italy"]),
    ("XK", ["kosovo"]),
    ("LV", ["latvia"]), ("LI", ["liechtenstein"]), ("LT", ["lithuania"]),
    ("LU", ["luxembourg"]), ("MT", ["malta"]),
    ("MD", ["moldova", "republic of moldova"]),
    ("MC", ["monaco"]), ("ME", ["montenegro"]), ("NL", ["netherlands", "holland", "the netherlands", "netherland"]),
    ("MK", ["north macedonia", "macedonia"]),
    ("NO", ["norway"]), ("PL", ["poland"]), ("PT", ["portugal"]),
    ("RO", ["romania"]), ("RU", ["russia", "russian federation"]),
    ("SM", ["san marino"]), ("RS", ["serbia"]), ("SK", ["slovakia"]), ("SI", ["slovenia"]),
    ("ES", ["spain"]), ("SE", ["sweden"]), ("CH", ["switzerland"]),
    ("TR", ["turkey", "türkiye", "turkiye"]),
    ("UA", ["ukraine"]),
    ("GB", ["united kingdom", "uk", "great britain", "britain", "england"]),
    ("VA", ["vatican city", "holy see"]),

    # --- Middle East & Asia ---
    ("AF", ["afghanistan"]), ("AZ", ["azerbaijan"]), ("BH", ["bahrain"]),
    ("BD", ["bangladesh"]), ("BT", ["bhutan"]),
    ("BN", ["brunei", "brunei darussalam"]),
    ("KH", ["cambodia", "kampuchea"]),
    ("CN", ["china", "prc"]), ("HK", ["hong kong"]), ("MO", ["macao", "macau"]),
    ("IN", ["india"]), ("ID", ["indonesia"]),
    ("IR", ["iran", "iran islamic republic of"]),
    ("IQ", ["iraq"]), ("IL", ["israel"]), ("JO", ["jordan"]),
    ("JP", ["japan"]), ("KZ", ["kazakhstan"]), ("KW", ["kuwait"]),
    ("KG", ["kyrgyzstan", "kyrgyz republic"]),
    ("LA", ["laos", "lao pdr", "lao people s democratic republic"]),
    ("LB", ["lebanon"]), ("MY", ["malaysia"]), ("MV", ["maldives"]),
    ("MN", ["mongolia"]), ("MM", ["myanmar", "burma"]),
    ("NP", ["nepal"]),
    ("KP", ["north korea", "dprk", "democratic people s republic of korea"]),
    ("OM", ["oman"]), ("PK", ["pakistan"]),
    ("PS", ["palestine", "state of palestine", "palestinian territories"]),
    ("PH", ["philippines"]), ("QA", ["qatar"]), ("SA", ["saudi arabia"]),
    ("SG", ["singapore"]),
    ("KR", ["south korea", "republic of korea"]),
    ("LK", ["sri lanka"]), ("SY", ["syria", "syrian arab republic"]),
    ("TW", ["taiwan", "roc", "republic of china"]),
    ("TJ", ["tajikistan"]), ("TH", ["thailand"]),
    ("TL", ["timor leste", "east timor"]),
    ("TM", ["turkmenistan"]), ("AE", ["united arab emirates", "uae"]),
    ("UZ", ["uzbekistan"]), ("VN", ["vietnam", "viet nam"]), ("YE", ["yemen"]),

    # --- Oceania ---
    ("AU", ["australia"]), ("FJ", ["fiji"]), ("KI", ["kiribati"]),
    ("MH", ["marshall islands"]),
    ("FM", ["micronesia", "federated states of micronesia"]),
    ("NR", ["nauru"]), ("NZ", ["new zealand", "aotearoa"]), ("PW", ["palau"]),
    ("PG", ["papua new guinea"]),
    ("WS", ["samoa"]), ("SB", ["solomon islands"]), ("TO", ["tonga"]),
    ("TV", ["tuvalu"]), ("VU", ["vanuatu"]),

    # --- Americas ---
    ("AR", ["argentina"]),
    ("BS", ["bahamas", "the bahamas"]), ("BB", ["barbados"]), ("BZ", ["belize"]),
    ("BO", ["bolivia", "bolivia plurinational state of"]), ("BR", ["brazil"]),
    ("CA", ["canada"]), ("CL", ["chile"]), ("CO", ["colombia"]),
    ("CR", ["costa rica"]), ("CU", ["cuba"]),
    ("DO", ["dominican republic"]), ("DM", ["dominica"]),
    ("EC", ["ecuador", "equador"]), ("SV", ["el salvador"]), ("GD", ["grenada"]),
    ("GT", ["guatemala"]), ("GY", ["guyana"]), ("HT", ["haiti"]),
    ("HN", ["honduras"]), ("JM", ["jamaica"]), ("MX", ["mexico"]),
    ("NI", ["nicaragua"]), ("PA", ["panama"]), ("PY", ["paraguay"]),
    ("PE", ["peru"]), ("PR", ["puerto rico"]),
    ("KN", ["saint kitts and nevis"]), ("LC", ["saint lucia"]),
    ("VC", ["saint vincent and the grenadines"]),
    ("SR", ["suriname"]),
    ("TT", ["trinidad and tobago"]),
    ("US", ["united states", "usa", "us", "united states of america"]),
    ("UY", ["uruguay"]),
    ("VE", ["venezuela", "bolivarian republic of venezuela"]),
]

APOS = {"’": "'", "ʻ": "'", "ʿ": "'", "´": "'", "`": "'"}

def _alias_to_pattern(alias: str) -> str:
    esc = re.escape(alias).replace(r"\ ", r"\s+")
    return rf"\b{esc}\b"

def iso2_to_flag(iso2: str) -> str:
    iso2 = iso2.upper()
    if iso2 == "XK":
        return "🇽🇰"
    if len(iso2) == 2 and iso2.isalpha():
        return "".join(chr(127397 + ord(c)) for c in iso2)
    return ""

def norm(s: str) -> str:
    s = s.lower().strip()
    s = unicodedata.normalize("NFKC", s)
    for a, b in APOS.items():
        s = s.replace(a, b)
    s = re.sub(r"[^\w\s&'-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


ALIAS_TO_FLAG = {}
for code, aliases in ISO2_ALIASES:
    flag = iso2_to_flag(code)
    if not flag:
        continue
    """if code:
        ALIAS_TO_FLAG[norm(code)] = flag"""
    for a in aliases:
        if a:
            ALIAS_TO_FLAG[norm(a)] = flag

ALIASES_SORTED = sorted(ALIAS_TO_FLAG.keys(), key=len, reverse=True)
COUNTRY_RE = re.compile("|".join(_alias_to_pattern(a) for a in ALIASES_SORTED), re.IGNORECASE)



def rewrite_for_js(md_line: str) -> str:
    groups = re.findall(r"\(([^)]+)\)", md_line)
    if not groups:
        return md_line

    save_groups = []
    for prt in groups:
        if re.fullmatch(r"\d{4}", prt):
            save_groups.append({"type":"date", "value":prt, "motif":prt,})
        elif prt in KNOWN_TAGS:
            save_groups.append({"type":prt, "value":prt, "motif":prt,})
        elif prt.lower() in ALIAS_LICENSE.keys():
            #print("   ---> ", prt, LICENSES[ALIAS_LICENSE[prt]])
            save_groups.append({"type":"license", "value":LICENSES[ALIAS_LICENSE[prt.lower()]]["label"],
"motif":prt, "url":LICENSES[ALIAS_LICENSE[prt.lower()]]["url"]})
        elif prt.lower() in LICENSES.keys():
            #print("   ---> ", prt, LICENSES[ALIAS_LICENSE[prt]])
            save_groups.append({"type":"license", "value":LICENSES[prt.lower()]["label"],
"motif":prt, "url":LICENSES[prt.lower()]["url"]})
            #print(" ---> ", save_groups[-1])


    motifs = {
        "date":f'<span class="meta-badge meta-date"> <span class="pill-ico" aria-hidden="true">{TYPE_EMOJI['date']}</span> <span class="pill-text">%s</span></span>',
        "license":f'<span class="meta-badge meta-license"><a href="%s" target="_blank"> <span class="pill-ico" aria-hidden="true">{TYPE_EMOJI['license']}</span> <span class="pill-text">%s</span></a></span>',
        }
    for tag in KNOWN_TAGS:
        motifs[tag] = f'<span class="meta-badge meta-{tag}"> <span class="pill-ico" aria-hidden="true">{TYPE_EMOJI[tag]}</span> <span class="pill-text">%s</span></span>'

    for el in save_groups:
        #print(el)
        #print(motifs[el['type']])

        if "url" in el:
            replace_value = motifs[el['type']] % (el['url'], el['value'])
        else:
            replace_value = motifs[el['type']] % el['value']

        md_line = md_line.replace(f"({el['motif']})", replace_value)

    return md_line


    year = None
    license_ = ""
    tags: list[str] = []

    # Walk from right → left to find year
    for i in range(len(groups) - 1, -1, -1):
        g = groups[i].strip()
        if re.fullmatch(r"\d{4}", g):
            year = g
            # license = next group to the right if not tags
            if i + 1 < len(groups):
                nxt = groups[i + 1]
                maybe_tags = [t.strip().lower() for t in re.split(r"[;,]", nxt)]
                if not any(t in KNOWN_TAGS for t in maybe_tags):
                    license_ = nxt.strip()
            # tags = rightmost group if any are known
            last = groups[-1]
            tag_tokens = [t.strip().lower() for t in re.split(r"[;,]", last)]
            tags = [t for t in tag_tokens if t in KNOWN_TAGS]
            break

    if not year:
        return md_line


    tag_str = ",".join(tags)
    marker = f" ::{year}|{license_}|{tag_str}::"
    # remove the old (…) blocks from end
    base = re.sub(r"\s*\([^)]*\)\s*$", "", md_line)
    return base + marker

def transform_page_header(text: str) -> str:
    def repl(m: re.Match) -> str:
        title = m.group(1).strip()
        return f'<div class="page-headers">\n  <h1>{title}</h1>\n</div>'
    return PAGE_HEADER_RE.sub(repl, text, count=1)



def extract_intro_text(text: str) -> str:
    def repl(m: re.Match) -> str:
        inner = m.group(1).strip()
        return inner
    return TABLE_TEXT_RE.sub(repl, text, count=1)



def parse_attrs(attr_str: str):
    return {k.lower(): v for k, v in ATTR_RE.findall(attr_str or "")}

def transform_tabs_block(match: re.Match) -> str:
    body = match.group("body") or ""
    panes = TAB_PANE_RE.findall(body)

    parts = []
    for i, (title, content) in enumerate(panes):
        t = (title or "").strip()
        c = (content or "").strip("\n")

        c = re.sub(
            r'^\s{0,3}#{1,6}\s*' + re.escape(t) + r'\s*#*\s*\n{1,2}',
            '',
            c,
            count=1,
            flags=re.IGNORECASE | re.MULTILINE,
        )

        if 'id="tag-filters"' not in c:
            c = FILTER_PLACEHOLDER + "\n" + c if c else FILTER_PLACEHOLDER

        indented = indent((c + "\n") if c else "\n", " " * 4)
        parts.append(f'=== "{t}"\n{indented}')

    marker = '<div class="awesome-tabs-scope"></div>\n\n'
    return marker + "\n".join(parts).rstrip() + "\n"

def to_collapsible_admonition(match: re.Match) -> str:
    kind = match.group("kind").lower()
    attrs = parse_attrs(match.group("attrs"))
    title = attrs.get("title", "")
    is_open = (attrs.get("open", "false").lower() in ("true", "1", "yes", "on"))
    body = (match.group("body") or "").strip("\n")

    body = re.sub(
        r'^\s{0,3}#{1,6}\s*' + re.escape(title) + r'\s*#*\s*\n{1,2}',
        '',
        body,
        count=1,
        flags=re.IGNORECASE | re.MULTILINE,
    )

    body = EMOJI_RE.sub('', body)

    fence = "???+" if is_open else "???"
    title_part = f' "{title}"' if title else ""

    indented_body = indent(body + "\n", " " * 4) if body.strip() else ""



    return f"{fence} {kind}{title_part}\n{indented_body}"


def inject_country_flags(text: str) -> str:
    PAREN_CONTENT_RE = re.compile(r"\* \(([^()]*)\)")

    def repl_paren(m: re.Match) -> str:
        inner = m.group(1)

        def repl_alias(n: re.Match) -> str:
            found = n.group(0)
            flag = ALIAS_TO_FLAG.get(norm(found), "")
            return f"{flag} {found}" if flag else found

        replaced = COUNTRY_RE.sub(repl_alias, inner)
        return f"* ({replaced})"

    return PAREN_CONTENT_RE.sub(repl_paren, text)


# ----------------------------

def transform(text: str) -> str:
    text = transform_page_header(text)
    text = extract_intro_text(text)

    yaml_block = "---\nhide:\n  - navigation\n  - toc\n---\n\n"

    text = TAB_BLOCK_RE.sub(transform_tabs_block, text)
    text = COLLAPSE_RE.sub(to_collapsible_admonition, text)

    text = RESOURCES_HEADER_RE.sub(
        r'\1#### <div class="resources-header">\2</div>',
        text,
    )

    injected = HEADER_BLOCK_RE.sub(r"\1\n" + GITHUB_BUTTON.strip() + "\n", text, count=1)
    text = injected if injected != text else (GITHUB_BUTTON + "\n" + text)

    imgreplace = "![](https://raw.githubusercontent.com/open-energy-transition/Awesome-Electrical-Grid-Mapping/refs/heads/main/scripts/countries_map_with_logo.png)"
    imgorigin = "![](scripts/countries_map_with_logo.png)"
    text = text.replace(imgorigin, imgreplace)

    text = inject_country_flags(text)
    text = rewrite_for_js(text)

    end_script = "<script>document.addEventListener('DOMContentLoaded', function () {  show_buttons_for_filter_tag();});</script>"

    text = text.replace("Awesome Electrical Grid Mapping","Global Grid Data")

    return yaml_block + text + "\n" + end_script

def main():
    try:
        print("Reading local source:", SOURCE_FILE, flush=True)
        if not os.path.isfile(SOURCE_FILE):
            raise FileNotFoundError(f"Source file not found: {SOURCE_FILE}")

        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        transformed = transform(content)

        out_dir = os.path.dirname(OUTPUT_FILE) or "."
        os.makedirs(out_dir, exist_ok=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
            f.write(transformed)

        print("Wrote:", OUTPUT_FILE, flush=True)
    except Exception as e:
        print("ERROR:", str(e), file=sys.stderr, flush=True)
        traceback.print_exc()

if __name__ == "__main__":
    main()
