#!/usr/bin/env python3
import os
import shutil
import subprocess
import logging
import sys
import re

# Set project root (one directory up from this script)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Export and temp directories
EXPORT_DIR = os.path.join(PROJECT_ROOT, "export_pdfs")
TMP_MD_DIR = os.path.join(EXPORT_DIR, "tmp_md")
OUTPUT_DIR = os.path.join(EXPORT_DIR, "pdf_outputs")

# Ensure dirs exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TMP_MD_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(EXPORT_DIR, 'build_pdfs.log'), mode='w')
    ]
)
logger = logging.getLogger(__name__)

# Directories to copy (relative to project root)
SOURCE_DIRS = [
    os.path.join(PROJECT_ROOT, 'implementations/academic'),
    os.path.join(PROJECT_ROOT, 'implementations/industry')
]

LATEX_PREAMBLE = r"""
% --- Custom title and TOC ---
\makeatletter
\renewcommand{\maketitle}{
  \begin{center}
    {\Huge \bfseries \sffamily \@title \par}
    \vspace{2em}
  \end{center}
}
\renewcommand{\sphinxmaketitle}{
  \begin{center}
    {\Huge \bfseries \sffamily \@title \par}
    \vspace{2em}
  \end{center}
}
\renewcommand{\tableofcontents}{}
\setcounter{tocdepth}{0}
\makeatother

% --- Page style ---
\usepackage{fancyhdr}
\pagestyle{plain}
\fancypagestyle{plain}{
  \fancyhf{}
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0pt}
}
\setcounter{secnumdepth}{0}
"""

def copy_implementations_folders():
    """
    For each markdown file, create a subdirectory in TMP_MD_DIR named after the file (without extension),
    and copy ONLY the .md file and the folder (with its content) in the same directory that has exactly the same name (e.g. ./cytely.md, ./cytely/).
    Also copies references.bib into each work_dir.
    Returns a list of (md_path, work_dir) tuples.
    """
    if os.path.exists(TMP_MD_DIR):
        shutil.rmtree(TMP_MD_DIR)
    os.makedirs(TMP_MD_DIR, exist_ok=True)
    md_workdirs = []
    bib_src = os.path.join(PROJECT_ROOT, "references.bib")
    for source_dir in SOURCE_DIRS:
        if not os.path.exists(source_dir):
            logger.warning(f"Directory does not exist: {source_dir}")
            continue
        for root, _, files in os.walk(source_dir):
            for filename in files:
                if filename.endswith('.md'):
                    src_md_path = os.path.join(root, filename)
                    base_name = os.path.splitext(filename)[0]
                    work_dir = os.path.join(TMP_MD_DIR, base_name)
                    os.makedirs(work_dir, exist_ok=True)
                    # Copy the .md file
                    shutil.copy2(src_md_path, os.path.join(work_dir, filename))
                    # Copy the asset folder with the same name as the .md file (if it exists)
                    asset_folder = os.path.join(root, base_name)
                    if os.path.isdir(asset_folder):
                        dest_asset_dir = os.path.join(work_dir, base_name)
                        if not os.path.exists(dest_asset_dir):
                            shutil.copytree(asset_folder, dest_asset_dir)
                    # Copy references.bib if it exists
                    if os.path.isfile(bib_src):
                        shutil.copy2(bib_src, os.path.join(work_dir, "references.bib"))
                    md_workdirs.append((os.path.join(work_dir, filename), work_dir))
    logger.info(f"Prepared {len(md_workdirs)} markdown work directories in {TMP_MD_DIR}")
    return md_workdirs

def extract_first_header(md_file):
    """Extract the first top-level header from the markdown file."""
    try:
        with open(md_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    title = line.lstrip("# ").strip()
                    title = title.replace('"', '\\"')
                    #title = title.replace("'", "''")
                    return title
    except Exception as e:
        logger.warning(f"Could not extract title from {md_file}: {e}")
    return "Untitled Document"

def create_temp_config(title):
    config_path = os.path.join(EXPORT_DIR, "_config.yml")
    preamble_indented = LATEX_PREAMBLE.replace("\n", "\n      ")
    config_content = f"""\
title: "{title}"
author: ""
latex:
  keep_tex: true
  latex_documents:
    targetname: book.tex
  latex_elements:
    preamble: |
      {preamble_indented}
    maketitle: ''
    tableofcontents: ''
"""
    with open(config_path, "w") as f:
        f.write(config_content)
    return config_path

def patch_tex_citations(tex_path):
    """
    Replace all \textbackslash{}cite{...} (with optional spaces, line breaks, or stray backslashes)
    with clean \cite{...} in the .tex file. Prints the number of patched citations.
    """
    if not os.path.isfile(tex_path):
        logger.warning(f"TeX file not found for citation patching: {tex_path}")
        return

    with open(tex_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Pattern to match malformed \textbackslash{}cite{...} citations
    pattern = r'\\textbackslash\s*\{\s*\}\s*cite\s*\\{\s*([^}]+?)\\?\s*\}'

    # Clean and format the matched citation key
    def clean_citation(match):
        key = match.group(1).rstrip('\\').strip()
        return f'\\cite{{{key}}}'

    # Apply substitution
    patched_text, patched_count = re.subn(pattern, clean_citation, text)

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(patched_text)

    logger.info(f"Patched {patched_count} citations in {tex_path}")

def patch_tex_font(tex_path):
    """
    Patch the generated .tex file to force FreeSans/FreeMono fonts with block syntax,
    and remove all other fontspec font settings.
    """
    if not os.path.isfile(tex_path):
        logger.warning(f"TeX file not found for patching: {tex_path}")
        return

    with open(tex_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    inserted = False
    skip_block = False

    for line in lines:
        # Remove any setmainfont/setsansfont/setmonofont blocks (commented or not)
        if (
            (line.strip().startswith("\\setmainfont") or line.strip().startswith("\\setsansfont") or line.strip().startswith("\\setmonofont") or
             line.strip().startswith("% \\setmainfont") or line.strip().startswith("% \\setsansfont") or line.strip().startswith("% \\setmonofont"))
            and "[" in line
        ):
            skip_block = True
            continue
        if skip_block:
            if "]" in line:
                skip_block = False
            continue

        # Insert our block after fontspec is loaded, only once
        if not inserted and "\\usepackage{fontspec}" in line:
            new_lines.append(line)
            new_lines.append(
                "\\setmainfont{FreeSans}[\n"
                "  Extension      = .otf,\n"
                "  UprightFont    = *,\n"
                "  ItalicFont     = *Oblique,\n"
                "  BoldFont       = *Bold,\n"
                "  BoldItalicFont = *BoldOblique\n"
                "]\n\n"
                "\\setsansfont{FreeSans}[\n"
                "  Extension      = .otf,\n"
                "  UprightFont    = *,\n"
                "  ItalicFont     = *Oblique,\n"
                "  BoldFont       = *Bold,\n"
                "  BoldItalicFont = *BoldOblique,\n"
                "]\n"
                "\\setmonofont{FreeMono}[\n"
                "  Extension      = .otf,\n"
                "  UprightFont    = *,\n"
                "  ItalicFont     = *Oblique,\n"
                "  BoldFont       = *Bold,\n"
                "  BoldItalicFont = *BoldOblique,\n"
                "]\n"
            )
            inserted = True
            continue

        # Comment out any single-line fontspec font settings
        if (
            line.strip().startswith("\\setmainfont") or
            line.strip().startswith("\\setsansfont") or
            line.strip().startswith("\\setmonofont")
        ):
            new_lines.append(f"% {line}")
            continue

        new_lines.append(line)

    with open(tex_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    logger.info(f"Patched fontspec font settings in {tex_path}")

def patch_tex_bibliography(tex_path):
    """
    Add biblatex package and \addbibresource to the header (after polyglossia),
    and add an inlined bibliography section before \end{document},
    but only if there is at least one \cite{...} in the file.
    """
    if not os.path.isfile(tex_path):
        logger.warning(f"TeX file not found for bibliography patching: {tex_path}")
        return

    with open(tex_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        tex_content = ''.join(lines)

    # Only add bibliography if there is at least one \cite{...}
    if r'\cite{' not in tex_content:
        logger.info(f"No citations found in {tex_path}, skipping bibliography patch.")
        return

    # Insert biblatex after \usepackage{polyglossia}
    new_lines = []
    bib_inserted = False
    for i, line in enumerate(lines):
        new_lines.append(line)
        if not bib_inserted and line.strip().startswith(r"\usepackage{polyglossia}"):
            new_lines.append(r"\usepackage[backend=biber,style=numeric]{biblatex}" + "\n")
            new_lines.append(r"\addbibresource{references.bib}" + "\n")
            bib_inserted = True

    # Insert inlined bibliography section before \end{document}
    bib_section = (
        r"\begingroup" + "\n" +
        r"\providecommand{\bibsection}{}" + "\n" +
        r"\renewcommand{\bibsection}{\section*{References}}" + "\n" +
        r"\let\clearpage\relax" + "\n" +
        r"\printbibliography" + "\n" +
        r"\endgroup" + "\n"
    )
    for i in range(len(new_lines)):
        if new_lines[i].strip() == r"\end{document}":
            if not any(r"\printbibliography" in l for l in new_lines[max(0, i-10):i]):
                new_lines.insert(i, bib_section)
            break

    with open(tex_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    logger.info(f"Patched bibliography in {tex_path}")

def patch_tex_remove_toc_and_empty(tex_path):
    """
    Remove ToC, pagestyle empty, and page breaks after title from the generated .tex file.
    """
    if not os.path.isfile(tex_path):
        logger.warning(f"TeX file not found for patching: {tex_path}")
        return
    with open(tex_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    new_lines = []
    skip_next_pagebreak = False
    for idx, line in enumerate(lines):
        # Remove ToC
        if "\\sphinxtableofcontents" in line or "\\tableofcontents" in line:
            continue
        # Remove all pagestyle empty
        if "\\pagestyle{empty}" in line:
            continue
        # Remove clearpage/cleardoublepage/newpage immediately after maketitle
        if skip_next_pagebreak and (
            "\\clearpage" in line or "\\cleardoublepage" in line or "\\newpage" in line
        ):
            skip_next_pagebreak = False
            continue
        # Detect maketitle and set flag to skip next pagebreak
        if "\\sphinxmaketitle" in line or "\\maketitle" in line:
            new_lines.append(line)
            skip_next_pagebreak = True
            continue
        # Remove any clearpage/cleardoublepage/newpage at the very start
        if idx < 10 and (
            "\\clearpage" in line or "\\cleardoublepage" in line or "\\newpage" in line
        ):
            continue
        new_lines.append(line)
    with open(tex_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    logger.info(f"Removed ToC, empty page, and page breaks after title in {tex_path}")

def patch_tex_insert_custom_title(tex_path):
    """
    Ensure the custom \sphinxmaketitle is present in the .tex file.
    """
    custom_title = r"""
\makeatletter
\renewcommand{\sphinxmaketitle}{
  \begin{center}
    {\Huge \bfseries \sffamily \@title \par}
    \vspace{2em}
  \end{center}
}
\makeatother
"""
    with open(tex_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Insert after \begin{document}, unless already present
    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line)
        if not inserted and line.strip() == r"\begin{document}":
            new_lines.append(custom_title + "\n")
            inserted = True
    with open(tex_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    logger.info(f"Inserted custom \\sphinxmaketitle in {tex_path}")

def build_pdf(md_file, work_dir):
    filename_without_ext = os.path.splitext(os.path.basename(md_file))[0]
    toc_path = os.path.join(work_dir, "_toc.yml")
    config_path = os.path.join(work_dir, "_config.yml")
    try:
        # Write _toc.yml/_config.yml in work_dir
        toc_content = f"format: jb-book\nroot: {os.path.basename(md_file)}\n"
        with open(toc_path, "w", encoding="utf-8") as f:
            f.write(toc_content)
        title = extract_first_header(md_file)
        # Write config in work_dir
        preamble_indented = LATEX_PREAMBLE.replace("\n", "\n      ")
        config_content = f"""\
title: "{title}"
author: ""
latex:
  keep_tex: true
  latex_documents:
    targetname: book.tex
  latex_elements:
    preamble: |
      {preamble_indented}
    maketitle: ''
    tableofcontents: ''
"""
        with open(config_path, "w") as f:
            f.write(config_content)

        # Build from work_dir
        cmd = ["jupyter-book", "build", work_dir, "--builder", "pdflatex"]
        logger.info(f"Building PDF for {md_file} with title '{title}' ...")
        print(f"Running command: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            if result.returncode != 0:
                logger.error(f"jupyter-book build failed for {md_file}")
                logger.error(f"stdout: {result.stdout}")
                logger.error(f"stderr: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            logger.error(f"Build process timed out after 600 seconds for {md_file}")
            return False
        except Exception as e:
            logger.error(f"Error during build process for {md_file}: {e}")
            return False

        # Patch the .tex file in place
        build_output_dir = os.path.join(work_dir, "_build", "latex")
        book_tex = os.path.join(build_output_dir, "book.tex")

        # Copy references.bib to the LaTeX build folder
        bib_src = os.path.join(PROJECT_ROOT, "references.bib")
        bib_dest = os.path.join(build_output_dir, "references.bib")
        if os.path.isfile(bib_src):
            shutil.copy2(bib_src, bib_dest)
            logger.info(f"Copied references.bib to {bib_dest}")
        else:
            logger.warning(f"references.bib not found for copying to LaTeX build folder: {bib_src}")

        if os.path.isfile(book_tex):
            patch_tex_font(book_tex)
            patch_tex_insert_custom_title(book_tex)
            patch_tex_remove_toc_and_empty(book_tex)
            patch_tex_citations(book_tex)
            patch_tex_bibliography(book_tex)
        else:
            logger.warning(f"LaTeX source 'book.tex' not found for {md_file}")
            return False

        # Rebuild PDF from patched .tex
        logger.info(f"Rebuilding PDF from patched TeX for {md_file} ...")
        try:
            result = subprocess.run(
                ["latexmk", "-xelatex", "-quiet", "book.tex"],
                cwd=build_output_dir,
                capture_output=True,
                text=True,
                timeout=600
            )
            if result.returncode != 0:
                logger.error(f"latexmk failed for {md_file}")
                logger.error(f"stdout: {result.stdout}")
                logger.error(f"stderr: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            logger.error(f"latexmk process timed out after 600 seconds for {md_file}")
            return False
        except Exception as e:
            logger.error(f"Error during latexmk process for {md_file}: {e}")
            return False

        # Copy the PDF and tex to OUTPUT_DIR
        book_pdf = os.path.join(build_output_dir, "book.pdf")
        pdf_dest = os.path.join(OUTPUT_DIR, f"{filename_without_ext}.pdf")
        #tex_dest = os.path.join(OUTPUT_DIR, f"{filename_without_ext}.tex")

        if os.path.isfile(book_pdf):
            shutil.copy2(book_pdf, pdf_dest)
            logger.info(f"Copied PDF to {pdf_dest}")
        else:
            logger.error(f"PDF not found at expected location after patch: {book_pdf}")
            return False

        #shutil.copy2(book_tex, tex_dest)
        #logger.info(f"Copied LaTeX source to {tex_dest}")

        return True

    except Exception as e:
        logger.error(f"Error building PDF for {md_file}: {e}")
        return False

def convert_myst_cite_to_latex(md_path):
    """
    Convert MyST citations ({cite:p}`key`) to LaTeX citations (\cite{key}) in-place in the given markdown file.
    """
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Replace {cite:p}`key1,key2` or {cite}`key1,key2` with \cite{key1,key2}
    text = re.sub(r"\{cite:[^\}]*\}`([^`]+)`", r"\\cite{\1}", text)
    text = re.sub(r"\{cite\}`([^`]+)`", r"\\cite{\1}", text)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(text)

def main():
    logger.info("Starting PDF build process")
    md_workdirs = copy_implementations_folders()
    # Convert MyST citations to LaTeX citations
    for md_file, _ in md_workdirs:
        convert_myst_cite_to_latex(md_file)
    success = 0
    failure = 0
    for idx, (md_file, work_dir) in enumerate(md_workdirs, 1):
        logger.info(f"Processing file {idx}/{len(md_workdirs)}: {md_file}")
        if build_pdf(md_file, work_dir):
            success += 1
        else:
            failure += 1
    logger.info(f"Finished processing. Successes: {success}, Failures: {failure}")
    logger.info(f"All output saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()