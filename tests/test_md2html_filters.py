import difflib
import pathlib
import subprocess
import functools
import pandoc_filter
def _check_file_path(file_path:str)->pathlib.Path:
    file_path:pathlib.Path = pathlib.Path(file_path)
    assert file_path.exists()
    assert file_path.is_file()
    return file_path

def _compare_files(file1_path, file2_path):
    with open(file1_path, 'r', encoding='utf-8') as file1:
        content1 = file1.readlines()

    with open(file2_path, 'r', encoding='utf-8') as file2:
        content2 = file2.readlines()

    differ = difflib.Differ()
    diff = list(differ.compare(content1, content2))
    if not any(line.startswith('- ') or line.startswith('+ ') for line in diff):
        return True
    else:
        return False

def test_md2html_anchor_link_filter():
    file_path = _check_file_path("./resources/inputs/test_md2html_anchor_and_link.md")
    pathlib.Path("./temp").mkdir(parents=True, exist_ok=True)
    output_path = pathlib.Path(f"./temp/{file_path.stem}.html")
    answer_path = pathlib.Path(f"./resources/outputs/{file_path.stem}.html")
    pandoc_command = [
        'pandoc',
        file_path,
        '-o',
        output_path,
        '-f',
        'markdown',
        '-t',
        'html',
        '-s',
        '--filter',
        'md2md-norm-internal-link-filter',
        '--filter',
        'md2html-hash-anchor-and-internal-link-filter',
        '--filter',
        'md2html-enhance-link-like-filter',
    ]
    assert subprocess.run(pandoc_command, check=True).returncode == 0
    assert _compare_files(output_path,answer_path)
    
def test_md2html_anchor_link_filter_pyio():
    file_path = _check_file_path("./resources/inputs/test_md2html_anchor_and_link.md")
    pathlib.Path("./temp").mkdir(parents=True, exist_ok=True)
    output_path = pathlib.Path(f"./temp/{file_path.stem}.html")
    answer_path = pathlib.Path(f"./resources/outputs/{file_path.stem}.html")
    
    pandoc_filter.run_filters_pyio(
        file_path,
        output_path,
        'markdown','html',
        [pandoc_filter.md2md_norm_internal_link_filter,
         pandoc_filter.md2html_hash_anchor_and_internal_link_filter,
         pandoc_filter.md2html_enhance_link_like_filter])
    assert _compare_files(output_path,answer_path)