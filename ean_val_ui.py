import os
import tkinter as tk
from PIL import Image, ImageTk
from barcode import Code128
from barcode.writer import ImageWriter
from reportlab.pdfgen import canvas
import webbrowser


class ValidatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EAN-13 Validator & Label Generator")
        self.root.geometry("600x390")
        self.root.resizable(width=False, height=False)

        # Variables for input fields
        self.code_var = tk.StringVar()
        self.validation_result_var = tk.StringVar()

        # Global reference to prevent garbage collection
        # Instance variable to store the barcode image
        self.barcode_img = None

        # User interface
        self.create_widgets()

    def create_widgets(self):
        """
        Create the user interface with buttons, labels, and entry fields.

        This function initializes and places the Entry widget for entering
        the EAN-13 code, as well as buttons for generating the barcode,
        saving it as a PDF, and exiting the application. It also creates
        labels for displaying validation results and the barcode image.

        Returns:
            None
        """
        # LabelFrame for EAN-13
        ean_frame = tk.LabelFrame(self.root, text="EAN-13 Code", padx=10, pady=10)
        ean_frame.place(x=30, y=20)

        # Entry for EAN Code
        self.code_entry = tk.Entry(ean_frame, textvariable=self.code_var)
        self.code_entry.grid(row=0, column=0, padx=5, pady=15)

        # Button to generate Barcode
        tk.Button(ean_frame, text="Generate Barcode", command=self.generate_and_display_barcode, width=20).grid(
            row=2, column=0, padx=5, pady=15)

        # Button to save Barcode as PDF
        tk.Button(ean_frame, text="Save as PDF", command=self.save_as_pdf, width=20).grid(
            row=3, column=0, padx=5, pady=15)

        # Exit button
        tk.Button(self.root, text="Exit", command=self.exit_app, width=20).place(x=45, y=280, anchor="w")

        # Label for validation result
        tk.Label(self.root, textvariable=self.validation_result_var, fg="black").place(x=350, y=30, anchor="w")

        # Label to display Barcode image
        self.barcode_image_label = tk.Label(self.root)
        self.barcode_image_label.place(x=300, y=160, anchor="w")

        # Add a footer
        footer_frame = tk.Frame(self.root, bg="white", height=60, width=600)
        footer_frame.place(x=0, y=330)


        # Open the link when the user clicks on the footer image
        def open_github_link(event):
            webbrowser.open("https://github.com/loginLayer")

        # Load and display the footer image
        footer_img_path = os.path.join(os.path.dirname(__file__), 'img', 'footer.png')
        footer_img = Image.open(footer_img_path)
        # Resize to fit the frame
        footer_img = footer_img.resize((600, 60), Image.BICUBIC)
        footer_img = ImageTk.PhotoImage(footer_img)
        # Use a Label with a link to open the URL
        footer_label = tk.Label(footer_frame, image=footer_img, bg="white", cursor="hand2")
        # Keep a reference to the image to prevent garbage collection
        footer_label.image = footer_img
        # Bind the click event to the function that opens the link
        footer_label.bind("<Button-1>", open_github_link)
        footer_label.pack()

    def generate_and_display_barcode(self):
        """
        Generate and display the barcode based on user input.

        This function retrieves the EAN-13 code from the entry field,
        generates the corresponding barcode image, validates the EAN-13
        code, updates the validation result label, and displays the barcode
        image on the graphical interface.

        Returns:
            None
        """
        code = self.code_var.get()

        if not code:
            # If the input field is empty, show a warning message
            self.validation_result_var.set("Please enter an EAN-13 code")
            return
        elif len(code) != 13:
            # If the code length is not 13, show a warning message
            self.validation_result_var.set("Please enter an EAN-13 code")
            return

        # Generate the barcode
        barcode_image = self.generate_barcode(code)

        # Validate the EAN-13 code and show the result
        if self.validate_ean13(code):
            self.validation_result_var.set("Valid EAN-13 Code")
        else:
            self.validation_result_var.set("Invalid EAN-13 Code")

        # Display the barcode image after generating it
        self.show_barcode(barcode_image)

    def generate_barcode(self, code):
        """
        Generate a barcode image and display it on the interface.

        This function takes an EAN-13 code as input, generates a barcode
        image using the Code128 library, and displays the barcode image
        on the graphical interface using Tkinter.

        Parameters:
            code (str): EAN-13 code

        Returns:
            str or None: Full path to the saved barcode image or None if an error occurs.
        """
        try:
            # Create the 'barcode' directory if it doesn't exist
            image_path = os.path.join(os.path.dirname(__file__), 'barcode')
            os.makedirs(image_path, exist_ok=True)

            # Generate the barcode using the 'Code128' library
            code128 = Code128(code, writer=ImageWriter())
            full_path = os.path.join(image_path, code)
            # Save the barcode as an image
            code128.save(full_path)

            # Attempt to open the image and display it using the tkinter PhotoImage method
            try:
                img = Image.open(full_path + '.png')
                # Calculate the new size while maintaining the original aspect ratio
                new_width = 250
                w_percent = (new_width / float(img.size[0]))
                new_height = int((float(img.size[1]) * float(w_percent)))
                # Resize the image
                img = img.resize((new_width, new_height), Image.BICUBIC)
                self.barcode_img = ImageTk.PhotoImage(img)

                # Show the barcode image on the graphical interface
                self.barcode_image_label.config(image=self.barcode_img)
            except Exception as img_error:
                print(f"Error displaying barcode image: {img_error}")

            return full_path
        except Exception as e:
            print(f"Error generating barcode: {e}")
            return None

    def show_barcode(self, image_path):
        """
        Show the barcode image on the graphical interface.

        This function displays the barcode image on the graphical interface
        using Tkinter's PhotoImage method.

        Parameters:
            image_path (str): Full path to the barcode image

        Returns:
            None
        """
        if self.barcode_img:
            # Use the image stored in the instance variable
            self.barcode_image_label.config(image=self.barcode_img)
        else:
            print("No barcode image to display.")

    def get_image_size(self):
        """
        Get the size of the barcode image.

        This function retrieves the size of the generated barcode image.

        Returns:
            tuple: Width and height of the barcode image
        """
        try:
            img_path = os.path.join(os.path.dirname(__file__), 'barcode', f"{self.code_var.get()}.png")
            if os.path.exists(img_path):
                img = Image.open(img_path)
                return img.size
            else:
                print(f"Barcode image not found: {img_path}")
                return 0, 0
        except Exception as img_error:
            print(f"Error getting barcode image size: {img_error}")
            return 0, 0

    def exit_app(self):
        """
        Cleanup and exit the application.

        This function removes the generated barcode images before closing
        the application and destroys the Tkinter root window.

        Returns:
            None
        """
        # Remove the generated barcode images before closing the application
        try:
            import shutil
            shutil.rmtree('barcode')
        except FileNotFoundError:
            pass

        self.root.destroy()

    def validate_ean13(self, ean):
        """
        Validate if the given EAN-13 code is valid.

        This function performs the validation of the provided EAN-13 code
        using the specified algorithm and returns True if the code is valid,
        and False otherwise.

        Parameters:
            ean (str): EAN-13 code

        Returns:
            bool: True if the EAN-13 code is valid, False otherwise
        """
        err = 0
        even = 0
        odd = 0
        # Get the check bit (last bit)
        check_bit = ean[len(ean) - 1]
        # Get all values except the check bit
        check_val = ean[:-1]
        # Check the input length
        if len(ean) != 13:
            return False
        else:
            # Gather Odd and Even Bits
            for index, num in enumerate(check_val):
                if index % 2 == 0:
                    even += int(num)
                else:
                    odd += int(num)
            # Check if the algorithm (3 * odd parity + even parity + check bit) matches
            if ((3 * odd) + even + int(check_bit)) % 10 == 0:
                return True
            else:
                return False

    def save_as_pdf(self):
        """
        Save the barcode as a PDF with additional information about its validity.

        This function saves the barcode as a PDF file, including the barcode
        image and a message indicating whether the EAN-13 code is valid or
        invalid. The PDF is saved with the same filename as the barcode image.

        Returns:
            None
        """
        # Get the barcode image size
        img_width, img_height = self.get_image_size()

        # Check if the code is empty or not 13 digits before saving as PDF
        code = self.code_var.get()
        if not code:
            self.validation_result_var.set("Please enter an EAN-13 code")
            return
        elif len(code) != 13:
            self.validation_result_var.set("Please enter an EAN-13 code")
            return

        # Set up the PDF file
        pdf_path = os.path.join(os.path.dirname(__file__), f"{code}_barcode.pdf")
        pdf = canvas.Canvas(pdf_path, pagesize=(img_width, img_height))

        # Draw the barcode image on the PDF
        try:
            img_path = os.path.join(os.path.dirname(__file__), 'barcode', f"{code}.png")
            pdf.drawInlineImage(img_path, 0, 0, width=img_width, height=img_height)

            # Add a message below the barcode indicating its validity
            if self.validate_ean13(code):
                message = "This EAN-13 code is VALID."
            else:
                message = "This EAN-13 code is INVALID."

            pdf.setFont("Helvetica", 10)
            # Adjust the y-coordinate to move the message 300 pixels down
            pdf.drawString(10, 15, message)

            pdf.save()
        except Exception as pdf_error:
            print(f"Error saving barcode as PDF: {pdf_error}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ValidatorApp(root)
    root.mainloop()
