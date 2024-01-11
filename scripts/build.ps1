conda activate pandoc
conda install --update-deps pandoc -c conda-forge 
pip install -r "./scripts/requirements.txt"
pip install -U setuptools build
python -m build
