
# Braille Translator GUI





## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Translating Text to Braille](#translating-text-to-braille)
  - [Customizing the Interface](#customizing-the-interface)
  - [Setting Line Limits](#setting-line-limits)
- [Project Information](#project-information)

## Features

- **Multilingual Support**: Translator covers 40+ languages, even with unique Braille contractions.
- **Text Editing Functions**: Access standard text tools: cut, copy, paste, undo, redo, and a quick search for easy word changes.
- **Document Handling**: Create or open documents, and when done, save it.
- **Customise the interface for your comforts**: You can increase your reading comforts by adjusting font size and choosing text and background colors for your comfort.
- **Select and translate**: A particular portion of a file can be selected and translated.
- **Line limit**: Adjust Braille line length to your needs effortlessly.

## Getting Started

### Prerequisites

Before running the Braille-Translator-GUI, make sure you have the following prerequisites installed:

- Python3 
- GTK


### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/zendalona/braille-translator-gui
   ```

2. Navigate to the project directory:

   ```bash
   
   cd braille-translator-gui
   ```

3. To run:
    ```bash
    
    Python3 setup.py install --install-data=/usr
     
    ```



   



## Usage

### Translating Text to Braille

1. Upon opening the application, you'll see two text areas: one for input and one for the translated Braille.

2. Choose the target language from the language combo-box.

3. Set the desired line length for Braille output to fit your preferences.

4. Type or paste the text you want to translate into the input area.

5. Click 'Translate,' and your text will be transformed into Braille in the second text box.

### Customizing the Interface

- You can customize the font style, color, and background to enhance readability and make your experience more comfortable.

### Setting Line Limits

- Use the spin button at the bottom of the Braille editor to set the desired number of lines for your Braille output. 




## Project Information

- **Operating System**: Linux
- **Programing language**: Python
- **FrameWork**:GTK

For more details on the project setup, configuration, and development, please refer to the project's code and documentation.
