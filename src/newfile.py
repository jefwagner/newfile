import pathlib
import datetime
from typing import Optional, TypedDict

import tomli
import click

VERSION = '0.2.0'

c_template = """\
/// @file {file_name} {file_descr}
//
// Copyright (c) {year}, {full_name} <{email}>
//
// This file is part of {project_name}.
//
// {project_name} is free software: you can redistribute it and/or modify it
// under the terms of the GNU General Public License as published by the Free
// Software Foundation, either version 3 of the License, or (at your option) any
// later version.
//
// {project_name} is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
// details.
//
// You should have received a copy of the GNU General Public License along with
// {project_name}. If not, see <https://www.gnu.org/licenses/>.
//
"""

py_template = '''\
## @file {file_name} 
"""\
{file_descr}
"""
# Copyright (c) {year}, {full_name} <{email}>
#
# This file is part of {project_name}.
#
# {project_name} is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# {project_name} is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# {project_name}. If not, see <https://www.gnu.org/licenses/>.
'''

class ProjectConf(TypedDict):
    project_name: str
    full_name: str
    email: str    
    year: int

def find_proj_conf(n: int) -> Optional[ProjectConf]:
    """Find the project configuration
    """
    cwd = pathlib.Path()
    conf_file = None
    if (cwd/'pyproject.toml').exists():
        conf_file = cwd/'pyproject.toml'
    else:
        for pdir,_ in zip(cwd.parents, range(n)):
            if (pdir/'pyproject.toml').exists():
                conf_file = cwd/'pyproject.toml'
                break
    if conf_file is None:
        return
    with conf_file.open('rb') as f:
        data = tomli.load(f)
    return dict(
        project_name = data['project']['name'],
        full_name = data['project']['authors'][0]['name'],
        email = data['project']['authors'][0]['email'],
        year = datetime.date.today().year
    )
        
@click.command()
@click.argument('file_name')
@click.option('-d', '--descr', default='', help='Description of file')
@click.version_option(VERSION)
def main(file_name, descr):
    """Create a new file with LGPL license"""
    conf = find_proj_conf(5)
    if conf is None:
        raise click.ClickException('Could not find pyproject.toml file.')
    newfile = pathlib.Path(file_name)
    if newfile.exists():
        raise click.ClickException(f'File {file_name} already exist.')
    conf.update({'file_name': file_name, 'file_descr': descr})
    if newfile.suffix in ['.c','.h']:
        with newfile.open('w') as f:
            f.write(c_template.format(**conf))
    elif newfile.suffix in ['.py']:
        with newfile.open('w') as f:
            f.write(py_template.format(**conf))
    else:
        raise click.ClickException(f'File {file_name} was not a recognized file-type')

