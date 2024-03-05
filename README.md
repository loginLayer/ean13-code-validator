# EAN-13 Validator & Label Generator



## Introduction

EAN-13 Validator & Label Generator is a Python application designed to validate and print EAN-13 barcodes. The application provides a user-friendly graphical interface built with Tkinter and leverages the Code128 library to create barcode images. Additionally, the generated barcodes can be saved as PDF files, including information about the validity of the EAN-13 code.


## Features

1. User-Friendly Interface:

* Entry widget to input EAN-13 codes.
* Buttons to generate the barcode, save it as a PDF, and exit the application.

2. Validation:

* Validates the entered EAN-13 code based on a specified algorithm.

3. Barcode Generation:

* Generates barcode images using the Code128 library.
* Displays the generated barcode image on the interface.

4. PDF Export:

* Saves the barcode as a PDF file.
* Includes a message about the validity of the EAN-13 code in the PDF.

5. Footer Link:

* Clickable footer image that opens the GitHub repository when clicked.


## Usage

1. Clone the repository to your local machine.

```bash
git clone https://github.com/loginLayer/ean13-code-validator.git
cd ean13-code-validator
```
2. Create a virtual environment (optional but recommended).

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Run the application.

```bash
python app.py
```


## Dependencies

* Python 3.x
* Tkinter
* Pillow (PIL)
* Barcode
* ReportLab

## Notes

* The application uses the Code128 library to generate barcodes and the ReportLab library for PDF creation.
* Ensure that a valid EAN-13 code (13 digits) is entered for proper functionality.
* Generated barcode images are stored in the 'barcode' directory.


## Contributions

Feel free to contribute or report issues in the GitHub repository.


## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE.md file for details.




