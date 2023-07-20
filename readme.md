# newfile script

This is a tiny script used for templated new file creation with boilerplate copyright and license text.

I have no plans on publishing this on pypi. I wrote this for myself to help with creating new files in a c extension I'm working on for python, so it relies on the existence of a `pyproject.toml` file and only scaffolds .h, .c, and .py files. However it should be fairly easily customizable and extensible.

## To use

1. Clone the repo and enter directory
```
> git clone https://github.com/jefwagner/newfile.git
> cd newfile
```

2. Edit the `newfile.py` to match your needs

3. Create virtual env, install build dependency, then build the project
```
> python -m venv .venv
> source .venv/bin/activate
(venv) > pip install build
(venv) > python -m build
```

4. Install the resulting  wheel file in your normal environment
```
(venv) > deactivate
> pip install dist/newfile-0.2.0-py3-none-any.whl
```

5. Use to create new files!
```
> cd my_awesome_python_project/
> newfile foo.h
> newfile bar.c
> newfile baz.py
```
