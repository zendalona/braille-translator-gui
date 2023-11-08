###########################################################################
#    Braile-Translator
#
#    Copyright (C) 2022-2023 Greeshna Sarath <greeshnamohan001@gmail.com>
#    
#    V T Bhattathiripad College, Sreekrishnapuram, Kerala, India
#
#    This project supervised by Zendalona(2022-2023) 
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

# Define a dictionary to map Braille Unicode characters to Braille ASCII characters
braille_unicode_to_braille_ASCII_map = {
    '⠮': '!', '⠐': '"', '⠼': '#', '⠫': '$', '⠩': '%', '⠯': '&', '⠄': "'", '⠷': '(', '⠾': ')', '⠡': '*',
    '⠬': '+', '⠠': ',', '⠤': '-', '⠨': '.', '⠌': '/', '⠴': '0', '⠂': '1', '⠆': '2', '⠒': '3', '⠲': '4',
    '⠢': '5', '⠖': '6', '⠶': '7', '⠦': '8', '⠔': '9', '⠱': ':', '⠰': ';', '⠣': '<', '⠿': '=', '⠜': '>',
    '⠹': '?', '⠈': '@', '⠁': 'A', '⠃': 'B', '⠉': 'C', '⠙': 'D', '⠑': 'E', '⠋': 'F', '⠛': 'G', '⠓': 'H',
    '⠊': 'I', '⠚': 'J', '⠅': 'K', '⠇': 'L', '⠍': 'M', '⠝': 'N', '⠕': 'O', '⠏': 'P', '⠟': 'Q', '⠗': 'R',
    '⠎': 'S', '⠞': 'T', '⠥': 'U', '⠧': 'V', '⠺': 'W', '⠭': 'X', '⠽': 'Y', '⠵': 'Z', '⠪': '[', '⠳': '\\',
    '⠻': ']', '⠘': '^', '⠸': '_'
}

braille_ASCII_to_braille_unicode_map = {v: k for k, v in braille_unicode_to_braille_ASCII_map.items()}


# Function to convert Braille Unicode to Braille ASCII
def braille_unicode_to_braille_ASCII(input_text):
    braille_ASCII_text = ""
    for char in input_text:
        if char in braille_unicode_to_braille_ASCII_map:
            braille_ASCII_text += braille_unicode_to_braille_ASCII_map[char]
        else:
            braille_ASCII_text += char  # Keep non-Braille Unicode characters as is
    return braille_ASCII_text


# Function to convert Braille ASCII to Braille Unicode
def braille_ASCII_to_braille_unicode(input_text):
    unicode_text = ""
    for char in input_text.upper():
        if char in braille_ASCII_to_braille_unicode_map:
            unicode_text += braille_ASCII_to_braille_unicode_map[char]
        else:
            unicode_text += char  # Keep non-Braille ASCII characters as is
    return unicode_text
