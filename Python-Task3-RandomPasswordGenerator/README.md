# OASIS INFOBYTE — Python Task 3

## Advanced Random Password Generator

### Project Overview

This project is an advanced graphical password generator developed using Python and Tkinter. It generates strong and secure passwords based on user-selected requirements.

The application uses Python's `secrets` module for cryptographically secure password generation.

## Features

- Graphical user interface using Tkinter
- Password length control from 8 to 64 characters
- Uppercase character selection
- Lowercase character selection
- Number selection
- Symbol selection
- Cryptographically secure password generation using `secrets`
- Password strength indicator
- Weak, Medium, and Strong strength levels
- Guarantees at least one character from every selected character type
- Automatic clipboard copying after password generation
- Manual Copy Password button
- Option to exclude ambiguous characters
- Displays the last five generated passwords during the current session
- Input validation and error handling
- Password history is not saved to a file

## Technologies Used

- Python
- Tkinter
- secrets
- string
- pyperclip

## Requirements

Python 3.x

Install the required external package:

```bash
python -m pip install pyperclip