pip install -r "${PSScriptRoot}/requirements.txt"
pip install -U setuptools build pytest twine
python -m build
pip install ./dist/*.whl
pytest