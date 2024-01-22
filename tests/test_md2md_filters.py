import difflib
import pathlib
import logging 
import subprocess
import panflute as pf

import pandoc_filter

def _check_file_path(file_path:str)->pathlib.Path:
    file_path:pathlib.Path = pathlib.Path(file_path)
    assert file_path.exists()
    assert file_path.is_file()
    return file_path

def _check_the_same_content(file1_path, file2_path):
    with open(file1_path, 'r', encoding='utf-8') as file1:
        content1 = file1.readlines()
    with open(file2_path, 'r', encoding='utf-8') as file2:
        content2 = file2.readlines()
    differ = difflib.Differ()
    diff = list(differ.compare(content1, content2))
    if not any(line.startswith('- ') or line.startswith('+ ') for line in diff):
        return True
    else:
        for line in diff:
            logging.warning(line)
        return False

def test_md2md_footnote_filter():
    file_path = _check_file_path("./resources/inputs/test_md2md_footnote.md")
    pathlib.Path("./temp").mkdir(parents=True, exist_ok=True)
    output_path = pathlib.Path(f"./temp/{file_path.name}")
    answer_path = pathlib.Path(f"./resources/outputs/{file_path.name}")
    pandoc_command = [
        'pandoc',
        file_path,
        '-o',
        output_path,
        '-f',
        'markdown',
        '-t',
        'gfm',
        '-s',
        '--filter',
        'md2md-footnote'
    ]
    assert subprocess.run(pandoc_command, check=True).returncode == 0
    assert _check_the_same_content(output_path,answer_path)


def test_md2md_internal_link_filter():
    file_path = _check_file_path("./resources/inputs/test_md2md_internal_link.md")
    pathlib.Path("./temp").mkdir(parents=True, exist_ok=True)
    output_path = pathlib.Path(f"./temp/{file_path.name}")
    answer_path = pathlib.Path(f"./resources/outputs/{file_path.name}")
    pandoc_command = [
        'pandoc',
        file_path,
        '-o',
        output_path,
        '-f',
        'markdown',
        '-t',
        'gfm',
        '-s',
        '--filter',
        'md2md-internal-link'
    ]
    assert subprocess.run(pandoc_command, check=True).returncode == 0
    assert _check_the_same_content(output_path,answer_path)


def test_md2md_math_filter():
    file_path = _check_file_path("./resources/inputs/test_md2md_math.md")
    pathlib.Path("./temp").mkdir(parents=True, exist_ok=True)
    output_path = pathlib.Path(f"./temp/{file_path.name}")
    answer_path = pathlib.Path(f"./resources/outputs/{file_path.name}")
    pandoc_command = [
        'pandoc',
        file_path,
        '-o',
        output_path,
        '-f',
        'markdown',
        '-t',
        'gfm',
        '-s',
        '--filter',
        'md2md-math'
    ]
    assert subprocess.run(pandoc_command, check=True).returncode == 0
    assert _check_the_same_content(output_path,answer_path)

def test_md2md_figure_filter():
    file_path = _check_file_path("./resources/inputs/test_md2md_figure.md")
    pathlib.Path("./temp").mkdir(parents=True, exist_ok=True)
    output_path = pathlib.Path(f"./temp/{file_path.name}")
    answer_path = pathlib.Path(f"./resources/outputs/{file_path.name}")
    
    with open(file_path, "r", encoding='utf-8') as f:
        markdown_content = f.read()
    doc = pf.convert_text(markdown_content,input_format='markdown',output_format='panflute',standalone=True)
    doc = pandoc_filter.md2md_figure_filter(doc,doc_path=file_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pf.convert_text(doc,input_format='panflute',output_format='gfm',standalone=True))
    assert _check_the_same_content(output_path,answer_path)

