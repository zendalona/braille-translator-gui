##########################################################################
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

from distutils.core import setup
from glob import glob
setup(name='BrailleTranslator',
      version='1.0',
      description='Text to Braille Translator',
      author='Greeshna Sarath',
      author_email='greeshnamohan001@gmail.com',
      url='https://github.com/greeshnasarath/braille-translator',
      license = 'GPL-3',
      packages=['BrailleTranslator'],
      data_files=[('share/BrailleTranslator/',['data/icon.png', 'data/language-table-dict.txt']),
      ('share/applications/',['braille-translator.desktop']),
      ('bin/',['braille-translator'])]
      )
# sudo python3 setup.py install --install-data=/usr
