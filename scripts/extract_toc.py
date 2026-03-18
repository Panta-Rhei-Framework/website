#!/usr/bin/env python3
"""Extract part/chapter abstracts from LaTeX manuscripts → YAML for Jekyll TOC pages."""

import os
import re
import sys
import yaml

BOOKS_DIR = "/Users/thorfuchs/Books/PantaRhei/books"
OUTPUT_DIR = "/Users/thorfuchs/Books/panta-rhei-books.org/website/_data/toc"

BOOK_MAP = [
    ("I-CategoricalFoundations",    "categorical-foundations",  "Volume I",   "Categorical Foundations"),
    ("II-CategoricalHolomorphy",    "categorical-holomorphy",   "Volume II",  "Categorical Holomorphy"),
    ("III-CategoricalSpectrum",     "categorical-spectrum",     "Volume III", "Categorical Spectrum"),
    ("IV-CategoricalMicrocosm",     "categorical-microcosm",   "Volume IV",  "Categorical Microcosm"),
    ("V-CategoricalMacrocosm",      "categorical-macrocosm",   "Volume V",   "Categorical Macrocosm"),
    ("VI-CategoricalLife",          "categorical-life",         "Volume VI",  "Categorical Life"),
    ("VII-CategoricalMetaphysics",  "categorical-metaphysics",  "Volume VII", "Categorical Metaphysics"),
]

# Greek letter mapping (LaTeX command → UTF-8)
GREEK = {
    r'\alpha': 'α', r'\beta': 'β', r'\gamma': 'γ', r'\delta': 'δ',
    r'\epsilon': 'ε', r'\varepsilon': 'ε', r'\zeta': 'ζ', r'\eta': 'η',
    r'\theta': 'θ', r'\iota': 'ι', r'\kappa': 'κ', r'\lambda': 'λ',
    r'\mu': 'μ', r'\nu': 'ν', r'\xi': 'ξ', r'\pi': 'π',
    r'\rho': 'ρ', r'\sigma': 'σ', r'\tau': 'τ', r'\upsilon': 'υ',
    r'\phi': 'φ', r'\varphi': 'φ', r'\chi': 'χ', r'\psi': 'ψ',
    r'\omega': 'ω', r'\omicron': 'ο',
    r'\Gamma': 'Γ', r'\Delta': 'Δ', r'\Theta': 'Θ', r'\Lambda': 'Λ',
    r'\Xi': 'Ξ', r'\Pi': 'Π', r'\Sigma': 'Σ', r'\Phi': 'Φ',
    r'\Psi': 'Ψ', r'\Omega': 'Ω',
    # Custom macros from preamble
    r'\mittau': 'τ', r'\mitpi': 'π', r'\mitalpha': 'α',
    r'\mitrho': 'ρ', r'\mitomega': 'ω', r'\mitomicron': 'ο',
    r'\mitiota': 'ι', r'\mitGamma': 'Γ',
}

# Blackboard bold mapping
BBOLD = {
    'N': 'ℕ', 'Z': 'ℤ', 'Q': 'ℚ', 'R': 'ℝ', 'C': 'ℂ',
    'F': '𝔽', 'P': 'ℙ', 'H': 'ℍ',
}

# Mathfrak mapping
FRAK = {
    'B': '𝔅', 'S': '𝔖', 'A': '𝔄', 'M': '𝔐',
}


def extract_braced(text, start):
    """Extract content of a brace-balanced {…} group starting at position start.
    Returns (content, end_pos) or (None, start) if not found."""
    if start >= len(text) or text[start] != '{':
        return None, start
    depth = 0
    i = start
    while i < len(text):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
        i += 1
    return None, start


def latex_to_markdown(text):
    """Convert LaTeX abstract text to clean Markdown."""
    if not text:
        return ""

    s = text.strip()

    # Remove \index{...} (may be nested)
    s = re.sub(r'\\index\{[^}]*\}', '', s)
    # Remove \label{...}
    s = re.sub(r'\\label\{[^}]*\}', '', s)
    # Remove \cite{...}
    s = re.sub(r'\\cite\{[^}]*\}', '', s)
    # Remove \nocite{...}
    s = re.sub(r'\\nocite\{[^}]*\}', '', s)

    # Strip itemize/enumerate environment markers
    s = re.sub(r'\\begin\{(itemize|enumerate)\}(\[nosep\])?', '', s)
    s = re.sub(r'\\end\{(itemize|enumerate)\}', '', s)
    # Strip \item markers
    s = re.sub(r'\\item\b\s*', '', s)

    # Handle \texorpdfstring{latex}{plaintext} — use plaintext version (brace-aware)
    max_iters = 50
    while r'\texorpdfstring' in s and max_iters > 0:
        max_iters -= 1
        idx = s.find(r'\texorpdfstring')
        if idx == -1:
            break
        brace_start = idx + len(r'\texorpdfstring')
        arg1, pos1 = extract_braced(s, brace_start)
        if arg1 is None:
            # Can't parse — remove the command text to avoid infinite loop
            s = s[:idx] + s[brace_start:]
            break
        arg2, pos2 = extract_braced(s, pos1)
        if arg2 is None:
            s = s[:idx] + s[brace_start:]
            break
        # Replace with LaTeX version (arg1) so we get proper UTF-8 symbols
        # (arg2 is the plaintext fallback for PDF bookmarks)
        s = s[:idx] + arg1 + s[pos2:]

    # Handle \textbf{...} → **...**
    def replace_braced_cmd(s, cmd, fmt_fn):
        """Replace \\cmd{content} using brace-aware parsing."""
        result = []
        i = 0
        while i < len(s):
            idx = s.find(cmd, i)
            if idx == -1:
                result.append(s[i:])
                break
            # Check it's a real command (preceded by non-alpha or start)
            if idx > 0 and s[idx - 1].isalpha():
                result.append(s[i:idx + len(cmd)])
                i = idx + len(cmd)
                continue
            result.append(s[i:idx])
            brace_start = idx + len(cmd)
            if brace_start < len(s) and s[brace_start] == '{':
                content, end = extract_braced(s, brace_start)
                if content is not None:
                    result.append(fmt_fn(content))
                    i = end
                    continue
            # No valid braces — skip the command text
            result.append(s[idx:idx + len(cmd)])
            i = idx + len(cmd)
        return ''.join(result)

    s = replace_braced_cmd(s, r'\textbf', lambda c: f'**{c}**')
    s = replace_braced_cmd(s, r'\emph', lambda c: f'*{c}*')
    s = replace_braced_cmd(s, r'\textit', lambda c: f'*{c}*')
    s = replace_braced_cmd(s, r'\textsc', lambda c: c.upper())
    s = replace_braced_cmd(s, r'\text', lambda c: c)

    # Handle inline math $...$
    def convert_math(match):
        math = match.group(1)
        # Apply Greek letter conversions
        for cmd, char in sorted(GREEK.items(), key=lambda x: -len(x[0])):
            math = math.replace(cmd, char)
        # \mathbb{X} → UTF-8 blackboard bold
        math = re.sub(r'\\mathbb\{(\w)\}', lambda m: BBOLD.get(m.group(1), m.group(1)), math)
        # \mathfrak{X} → UTF-8 fraktur
        math = re.sub(r'\\mathfrak\{(\w)\}', lambda m: FRAK.get(m.group(1), m.group(1)), math)
        # \mathrm{text} → text
        math = re.sub(r'\\mathrm\{([^}]*)\}', r'\1', math)
        # \mathcal{X} → X
        math = re.sub(r'\\mathcal\{([^}]*)\}', r'\1', math)
        # \operatorname{text} → text
        math = re.sub(r'\\operatorname\{([^}]*)\}', r'\1', math)
        # Superscripts: ^{n} → ^n, ^3 → ³
        math = re.sub(r'\^\{([^}]*)\}', r'^\1', math)
        sup_map = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
                    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
                    '+': '⁺', '-': '⁻', 'n': 'ⁿ'}
        def replace_sup(m):
            sup = m.group(1)
            return ''.join(sup_map.get(c, c) for c in sup)
        math = re.sub(r'\^(\w+)', replace_sup, math)
        math = re.sub(r'\^(\d)', replace_sup, math)
        # Subscripts: _{n} → _n (keep as-is for readability)
        math = re.sub(r'_\{([^}]*)\}', r'_\1', math)
        # Common symbols
        math = math.replace(r'\times', '×')
        math = math.replace(r'\wedge', '∧')
        math = math.replace(r'\vee', '∨')
        math = math.replace(r'\infty', '∞')
        math = math.replace(r'\subset', '⊂')
        math = math.replace(r'\subseteq', '⊆')
        math = math.replace(r'\in', '∈')
        math = math.replace(r'\notin', '∉')
        math = math.replace(r'\cup', '∪')
        math = math.replace(r'\cap', '∩')
        math = math.replace(r'\to', '→')
        math = math.replace(r'\rightarrow', '→')
        math = math.replace(r'\leftarrow', '←')
        math = math.replace(r'\mapsto', '↦')
        math = math.replace(r'\Rightarrow', '⇒')
        math = math.replace(r'\Leftrightarrow', '⇔')
        math = math.replace(r'\cong', '≅')
        math = math.replace(r'\simeq', '≃')
        math = math.replace(r'\approx', '≈')
        math = math.replace(r'\neq', '≠')
        math = math.replace(r'\leq', '≤')
        math = math.replace(r'\geq', '≥')
        math = math.replace(r'\perp', '⊥')
        math = math.replace(r'\otimes', '⊗')
        math = math.replace(r'\oplus', '⊕')
        math = math.replace(r'\hbar', 'ℏ')
        math = math.replace(r'\ell', 'ℓ')
        math = math.replace(r'\partial', '∂')
        math = math.replace(r'\nabla', '∇')
        math = math.replace(r'\forall', '∀')
        math = math.replace(r'\exists', '∃')
        math = math.replace(r'\mid', '|')
        math = math.replace(r'\langle', '⟨')
        math = math.replace(r'\rangle', '⟩')
        # Clean up remaining backslash commands
        math = re.sub(r'\\[a-zA-Z]+', '', math)
        # Clean up braces
        math = math.replace('{', '').replace('}', '')
        return math.strip()

    s = re.sub(r'\$([^$]+)\$', convert_math, s)

    # Handle \(...\) inline math delimiters (same conversion as $...$)
    s = re.sub(r'\\\((.+?)\\\)', convert_math, s)

    # Handle \[...\] display math delimiters
    s = re.sub(r'\\\[(.+?)\\\]', convert_math, s)

    # Apply Greek letters outside math (for custom macros like \mittau)
    for cmd, char in sorted(GREEK.items(), key=lambda x: -len(x[0])):
        # Only replace if followed by non-alpha (word boundary)
        s = re.sub(re.escape(cmd) + r'(?=[^a-zA-Z]|$)', char, s)

    # LaTeX accent commands → UTF-8 (handle both \'e and \'{e} forms)
    accent_map_braced = {
        "\\'{e}": 'é', "\\'{a}": 'á', "\\'{i}": 'í', "\\'{o}": 'ó', "\\'{u}": 'ú',
        "\\'{E}": 'É', "\\`{e}": 'è', "\\`{a}": 'à', '\\"{o}': 'ö', '\\"{u}': 'ü',
        '\\"{a}': 'ä', '\\^{e}': 'ê', '\\^{o}': 'ô', '\\~{n}': 'ñ',
        "\\c{c}": 'ç', "\\v{s}": 'š', "\\v{c}": 'č',
    }
    accent_map_bare = {
        "\\'e": 'é', "\\'a": 'á', "\\'i": 'í', "\\'o": 'ó', "\\'u": 'ú',
        "\\'E": 'É', "\\`e": 'è', "\\`a": 'à', '\\"o': 'ö', '\\"u': 'ü',
        '\\"a': 'ä', '\\^e': 'ê', '\\^o': 'ô', '\\~n': 'ñ',
    }
    for latex_acc, utf8 in accent_map_braced.items():
        s = s.replace(latex_acc, utf8)
    for latex_acc, utf8 in accent_map_bare.items():
        s = s.replace(latex_acc, utf8)

    # Common LaTeX special characters
    s = s.replace(r'\&', '&')
    s = s.replace(r'\%', '%')
    s = s.replace(r'\#', '#')
    s = s.replace(r'\$', '$')
    s = s.replace(r'\_', '_')

    # Dashes
    s = s.replace('---', '—')
    s = s.replace('--', '–')

    # Tilde (non-breaking space)
    s = s.replace('~', ' ')

    # LaTeX double-backtick quotes → Unicode double quotes (DOTALL for multi-line)
    s = re.sub(r"``(.+?)''", r'"\1"', s, flags=re.DOTALL)

    # Abbreviation trailing backslash (e.g.\ → e.g.)
    s = re.sub(r'((?:e\.g|i\.e|cf|viz|vs|etc)\.)\\(?=\s|$)', r'\1', s)

    # Clean up remaining LaTeX commands that we missed
    s = re.sub(r'\\[a-z]+\{([^}]*)\}', r'\1', s)  # \cmd{text} → text

    # Remove remaining backslash-commands without braces
    s = re.sub(r'\\[a-zA-Z]+(?=[^a-zA-Z{]|$)', '', s)

    # Strip ch:label cross-references AFTER \ref{} cleanup (Chapter ch:foo → Chapter)
    s = re.sub(r'(Chapters?)\s+ch:[a-z0-9-]+(?:\s*[-–—]+\s*ch:[a-z0-9-]+)?', r'\1', s)
    # Strip any remaining standalone ch:label references (e.g., "and ch:foo")
    s = re.sub(r'\bch:[a-z0-9-]+', '', s)

    # Strip def:label cross-references (Definition def:foo → Definition)
    s = re.sub(r'(Definitions?)\s+def:[a-z0-9-]+', r'\1', s)

    # Strip sec:label cross-references (Section sec:foo → Section)
    s = re.sub(r'(Sections?)\s+sec:[a-z0-9-]+', r'\1', s)

    # Strip thm:label, lem:label, prop:label cross-references
    s = re.sub(r'(Theorems?|Lemmas?|Propositions?|Corollar(?:y|ies))\s+(?:thm|lem|prop|cor):[a-z0-9-]+', r'\1', s)

    # Clean up multiple spaces
    s = re.sub(r'  +', ' ', s)

    # Clean up any remaining empty braces
    s = s.replace('{}', '')
    s = s.replace('{', '').replace('}', '')

    # Normalize whitespace (collapse newlines within a paragraph)
    lines = s.split('\n')
    paragraphs = []
    current = []
    for line in lines:
        stripped = line.strip()
        if stripped == '':
            if current:
                paragraphs.append(' '.join(current))
                current = []
        else:
            current.append(stripped)
    if current:
        paragraphs.append(' '.join(current))

    return '\n\n'.join(paragraphs).strip()


def extract_env(text, env_name):
    """Extract content of a LaTeX environment."""
    pattern = re.compile(
        r'\\begin\{' + env_name + r'\}(.*?)\\end\{' + env_name + r'\}',
        re.DOTALL
    )
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return ""


def extract_braced_command(text, command):
    """Extract the brace-balanced argument of \\command{...} from text.
    Also handles \\command*{...}. Returns the content or empty string."""
    # Find the command
    pattern = re.compile(re.escape(command) + r'\*?\s*\{')
    m = pattern.search(text)
    if not m:
        return ""
    brace_pos = m.end() - 1  # position of the opening {
    content, _ = extract_braced(text, brace_pos)
    return content if content else ""


def extract_chapter_title(text):
    """Extract \chapter{Title} from a .tex file."""
    title = extract_braced_command(text, r'\chapter')
    if title:
        return latex_to_markdown(title)
    return ""


def extract_part_title(line):
    """Extract title from a \part{...} line."""
    title = extract_braced_command(line, r'\part')
    if title:
        return latex_to_markdown(title)
    return ""


def parse_main_tex(book_dir):
    """Parse main.tex to extract parts, their abstracts, and chapter ordering."""
    main_tex_path = os.path.join(book_dir, "latex", "main.tex")
    if not os.path.exists(main_tex_path):
        print(f"  WARNING: {main_tex_path} not found")
        return []

    with open(main_tex_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into lines for sequential parsing
    lines = content.split('\n')

    parts = []
    current_part = None
    in_mainmatter = False
    chapter_inputs = []
    part_abstract_buffer = []
    in_part_abstract = False

    # Roman numeral counter for parts
    roman_numerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII',
                      'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI',
                      'XVII', 'XVIII', 'XIX', 'XX']
    part_counter = 0

    # Track prologue chapters (before first \part{})
    prologue_inputs = []
    found_first_part = False

    for line in lines:
        stripped = line.strip()

        # Track mainmatter
        if r'\mainmatter' in stripped:
            in_mainmatter = True
            continue

        if not in_mainmatter:
            continue

        # Stop at \appendix or \backmatter
        if stripped.startswith(r'\appendix') or stripped.startswith(r'\backmatter'):
            break

        # Detect \input or \include for chapter files
        m_input = re.match(r'\\(?:input|include)\{(sections/[^}]+)\}', stripped)
        if m_input:
            path = m_input.group(1)
            # Skip frontmatter, backmatter, appendix inputs
            if any(skip in path for skip in ['frontmatter', 'backmatter', 'appendix']):
                continue
            if not found_first_part:
                prologue_inputs.append(path)
            elif current_part is not None:
                chapter_inputs.append(path)
            continue

        # Detect \part{Title}
        if re.match(r'\\part\{', stripped) or re.match(r'\\part\[', stripped):
            # Don't process \part{Appendices}
            if 'Appendic' in stripped:
                break

            # Save previous part
            if current_part is not None:
                current_part['_chapter_paths'] = chapter_inputs
                parts.append(current_part)
                chapter_inputs = []

            # Handle prologue chapters (if any) before first real part
            if not found_first_part and prologue_inputs:
                # Check if this first \part is "Prologue" itself
                title = extract_part_title(stripped)
                if 'prologue' in title.lower():
                    # Prologue is a real \part{} — assign chapters to it
                    found_first_part = True
                    current_part = {
                        'number': 'Prologue',
                        'title': title,
                        'abstract': '',
                        '_chapter_paths': [],
                    }
                    chapter_inputs = list(prologue_inputs)
                    prologue_inputs = []
                    continue
                else:
                    # There are chapters before the first non-Prologue \part{}
                    # Create a synthetic "Prologue" part for them
                    found_first_part = True
                    prologue_part = {
                        'number': 'Prologue',
                        'title': 'Prologue',
                        'abstract': '',
                        '_chapter_paths': prologue_inputs,
                    }
                    parts.append(prologue_part)
                    prologue_inputs = []

            found_first_part = True
            title = extract_part_title(stripped)

            # Determine numbering
            if 'prologue' in title.lower():
                number = 'Prologue'
            elif 'epilogue' in title.lower():
                number = 'Epilogue'
            else:
                if part_counter < len(roman_numerals):
                    number = roman_numerals[part_counter]
                else:
                    number = str(part_counter + 1)
                part_counter += 1

            current_part = {
                'number': number,
                'title': title,
                'abstract': '',
                '_chapter_paths': [],
            }
            continue

        # Detect \begin{partabstract}
        if r'\begin{partabstract}' in stripped:
            in_part_abstract = True
            part_abstract_buffer = []
            # Check if content is on the same line
            after = stripped.split(r'\begin{partabstract}', 1)[1]
            if r'\end{partabstract}' in after:
                abstract_text = after.split(r'\end{partabstract}')[0]
                if current_part is not None:
                    current_part['abstract'] = abstract_text
                in_part_abstract = False
            elif after.strip():
                part_abstract_buffer.append(after.strip())
            continue

        if in_part_abstract:
            if r'\end{partabstract}' in stripped:
                before = stripped.split(r'\end{partabstract}')[0]
                if before.strip():
                    part_abstract_buffer.append(before.strip())
                if current_part is not None:
                    current_part['abstract'] = '\n'.join(part_abstract_buffer)
                in_part_abstract = False
            else:
                part_abstract_buffer.append(stripped)
            continue

    # Save last part
    if current_part is not None:
        current_part['_chapter_paths'] = chapter_inputs
        parts.append(current_part)

    # Handle case where there are only prologue inputs and no parts found
    if not parts and prologue_inputs:
        parts.append({
            'number': 'Prologue',
            'title': 'Prologue',
            'abstract': '',
            '_chapter_paths': prologue_inputs,
        })

    return parts


def process_chapter_file(book_dir, chapter_path):
    """Read a chapter .tex file and extract title + abstract."""
    # Try with and without .tex extension
    full_path = os.path.join(book_dir, "latex", chapter_path)
    if not full_path.endswith('.tex'):
        full_path += '.tex'

    if not os.path.exists(full_path):
        print(f"  WARNING: Chapter file not found: {full_path}")
        return None

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    title = extract_chapter_title(content)
    abstract = extract_env(content, 'chapterabstract')

    if not title:
        # Try to extract from filename
        basename = os.path.basename(chapter_path)
        title = basename.replace('.tex', '').replace('-', ' ').replace('_', ' ')
        # Remove chapter number prefix
        title = re.sub(r'^(chapter|ch)\s*\d+\s*', '', title, flags=re.IGNORECASE).strip()
        title = title.title()

    return {
        'title': title,
        'abstract': abstract,
    }


def process_book(book_dir_name, slug, volume_label, book_title):
    """Process a single book: extract all parts + chapters."""
    book_dir = os.path.join(BOOKS_DIR, book_dir_name)
    print(f"\n{'='*60}")
    print(f"Processing: {book_dir_name} → {slug}")
    print(f"{'='*60}")

    parts = parse_main_tex(book_dir)
    print(f"  Found {len(parts)} parts")

    total_chapters = 0
    yaml_parts = []

    for part in parts:
        abstract_md = latex_to_markdown(part['abstract'])
        chapters = []
        for ch_path in part.get('_chapter_paths', []):
            ch_data = process_chapter_file(book_dir, ch_path)
            if ch_data:
                total_chapters += 1
                chapters.append({
                    'number': total_chapters,
                    'title': ch_data['title'],
                    'abstract': latex_to_markdown(ch_data['abstract']),
                })

        yaml_part = {
            'number': part['number'],
            'title': part['title'],
            'abstract': abstract_md,
            'chapters': chapters,
        }
        yaml_parts.append(yaml_part)
        print(f"  Part {part['number']}: {part['title']} — {len(chapters)} chapters")

    # Build the full YAML document
    intro = f"Complete chapter-level table of contents for {volume_label}: {book_title}. Each part includes its abstract and all chapters with their descriptions."

    doc = {
        'title': 'Table of Contents',
        'intro': intro,
        'chapter_count': total_chapters,
        'part_count': len(yaml_parts),
        'parts': yaml_parts,
    }

    # Write YAML
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"{slug}.yml")

    # Custom YAML dumper that handles multi-line strings nicely
    class MultilineDumper(yaml.SafeDumper):
        pass

    def str_representer(dumper, data):
        if '\n' in data:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        if len(data) > 80 or any(c in data for c in ['"', "'", ':', '#', '{', '}', '[', ']', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`']):
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)

    MultilineDumper.add_representer(str, str_representer)

    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(doc, f, Dumper=MultilineDumper, default_flow_style=False,
                  allow_unicode=True, width=120, sort_keys=False)

    print(f"\n  ✓ Written {output_path}")
    print(f"  ✓ {len(yaml_parts)} parts, {total_chapters} chapters")

    return total_chapters


def main():
    print("LaTeX TOC Extraction Script")
    print("=" * 60)

    grand_total = 0
    for book_dir_name, slug, volume_label, book_title in BOOK_MAP:
        count = process_book(book_dir_name, slug, volume_label, book_title)
        grand_total += count

    print(f"\n{'='*60}")
    print(f"TOTAL: {grand_total} chapters across {len(BOOK_MAP)} books")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
