# SIO Postdoc
---

Contians Python code for Rich Inman's post-doctoral work at Scripps Institute of Oceanography.

NOTE: If you need to reinstall poetry on a mac:
  From https://github.com/python-poetry/install.python-poetry.org/issues/71.
  curl -sSL https://install.python-poetry.org | python3 - --uninstall
  curl -sSL https://install.python-poetry.org | python3

NOTE: Configure poetry to use in-project virtual envs:
  poetry config virtualenvs.in-project true


When poetry is not installing on windows you need to run
py -m pip install certifi


On a windows machine when installing poetry you need to run
python -m pip install certifi
before tyring to install it
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/fdcastel/install-poetry/main/install-poetry.py -UseBasicParsing).Content | py -
Then install it and add
%APPDATA%\pypoetry\venv\Scripts
to the path
