###########################################################################
#    Braile-Translator
#
#    Copyright (C) 2022-2023 Greeshna Sarath <greeshnamohan001@gmail.com>
#	 V T Bhattathiripad College, Sreekrishnapuram, Kerala, India
#
#    This project supervised by Zendalona(2022-2023) 
#
#	 Copyright (C) 2022-2023 Nalin Sathyan <nalin.x.linux@gmail.com>
#
#    Project Home Page : www.zendalona.com/braille-translator
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

import sys
import configparser

class Preferences():
	
	def __init__(self):		
		self.set_default_preferences();

	def set_default_preferences(self):
		self.language = 160
		self.font_1 = 'Sans Regular 18'
		self.font_2 = 'Sans Regular 18'
		self.theme_1 = 0
		self.theme_2 = 0
	
	def load_preferences_from_file(self, filename):
		try:
			cp = configparser.ConfigParser()
			cp.read(filename)
			
			self.language = int(cp.get('general',"language"))

			self.font_1  = cp.get('appearance','font-1')
			self.theme_1 = int(cp.get('appearance','theme-1'))

			self.font_2  = cp.get('appearance','font-2')
			self.theme_2 = int(cp.get('appearance','theme-2'))
			
		except:
			print("Configuration reading error : ", sys.exc_info()[0])
			self.set_default_preferences()

	def save_preferences_to_file(self, filename):
		
		cp = configparser.ConfigParser()

		cp.add_section('general')
		cp.add_section('appearance')

		cp.set('general',"language", str(int(self.language)))

		cp.set('appearance',"font-1",self.font_1)
		cp.set('appearance',"theme-1",str(int(self.theme_1)))

		cp.set('appearance',"font-2",self.font_2)
		cp.set('appearance',"theme-2",str(int(self.theme_2)))

		with open(filename , 'w') as configfile:
			cp.write(configfile)
