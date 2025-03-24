# Importing necessary libraries
import requests  # For making HTTP requests to fetch web pages
from bs4 import BeautifulSoup  # For parsing and extracting data from HTML
import customtkinter as ctk  # A modern, customizable GUI library based on Tkinter
from tkinter import filedialog, messagebox  # For file operations and displaying messages
from playsound import playsound  # For adding sound effects
import threading  # For handling background tasks without freezing the GUI

# Class for creating the web scraper application
class ModernWebScraperApp:
    def __init__(self, root):
        # Initialize the application window
        self.root = root
        self.root.title("Samriddha's Web Scraper")  # Set the title of the window
        self.root.geometry("700x500")  # Set the dimensions of the window
        ctk.set_appearance_mode("System")  # Match the app theme with the system theme
        ctk.set_default_color_theme("dark-blue")  # Set a color theme for the app

        # Call a method to create all the widgets (UI components)
        self.create_widgets()

    def create_widgets(self):
        # Title Label: Displays the title at the top of the app
        self.title_label = ctk.CTkLabel(self.root, text="Samriddha's Web Scraper", font=("Arial", 24))
        self.title_label.pack(pady=10)  # Add some space around the label

        # URL Entry: Input field for the user to enter the website URL
        self.url_entry = ctk.CTkEntry(self.root, placeholder_text="Enter the URL", width=400)
        self.url_entry.pack(pady=10)

        # Options Frame: Contains radio buttons for selecting what to scrape (Text, Images, or Links)
        self.options_frame = ctk.CTkFrame(self.root)
        self.options_frame.pack(pady=10)

        # Variable to store the selected option
        self.option_var = ctk.StringVar(value="text")  # Default value is "text"
        # Radio buttons for the options
        self.text_option = ctk.CTkRadioButton(self.options_frame, text="Text", variable=self.option_var, value="text")
        self.image_option = ctk.CTkRadioButton(self.options_frame, text="Images", variable=self.option_var, value="images")
        self.links_option = ctk.CTkRadioButton(self.options_frame, text="Links", variable=self.option_var, value="links")

        # Arrange the radio buttons in a grid layout
        self.text_option.grid(row=0, column=0, padx=10, pady=5)
        self.image_option.grid(row=0, column=1, padx=10, pady=5)
        self.links_option.grid(row=0, column=2, padx=10, pady=5)

        # Scrape Button: Starts the scraping process when clicked
        self.scrape_button = ctk.CTkButton(self.root, text="Start Scraping", command=self.start_scraping)
        # Adding sound effects for hover and click events
        self.scrape_button.bind("<Enter>", lambda e: threading.Thread(target=lambda: playsound("hover.mp3")).start())
        self.scrape_button.bind("<Button-1>", lambda e: threading.Thread(target=lambda: playsound("click.mp3")).start())
        self.scrape_button.pack(pady=10)

        # Progress Bar: Displays the progress of the scraping process
        self.progress = ctk.CTkProgressBar(self.root, orientation="horizontal", mode="determinate", width=400)
        self.progress.pack(pady=10)

        # Results Text Box: Displays the scraped data
        self.result_text = ctk.CTkTextbox(self.root, height=150, width=600)
        self.result_text.pack(pady=10)

        # Export Button: Allows the user to save the scraped data to a file
        self.export_button = ctk.CTkButton(self.root, text="Export Results", command=self.export_results, state=ctk.DISABLED)
        self.export_button.pack(pady=10)

        # Theme Toggle: Switches between light and dark themes
        self.theme_switch = ctk.CTkSwitch(self.root, text="Light Mode", command=self.toggle_theme)
        self.theme_switch.pack(pady=10)

    # Method to toggle between light and dark themes
    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current_mode == "Dark" else "Dark")

    # Method to start the web scraping process
    def start_scraping(self):
        # Get the URL entered by the user
        url = self.url_entry.get()
        # Get the selected scraping option (Text, Images, or Links)
        option = self.option_var.get()

        # If no URL is entered, show an error message
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return

        # Update the progress bar
        self.progress.set(0.2)
        # Clear the previous results from the text box
        self.result_text.delete(1.0, "end")

        try:
            # Further progress update
            self.progress.set(0.5)
            # Make an HTTP GET request to fetch the webpage
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for unsuccessful requests
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract data based on the selected option
            if option == "text":
                results = soup.get_text()  # Get all the text from the webpage
            elif option == "images":
                # Get all image URLs
                results = "\n".join(img["src"] for img in soup.find_all("img") if "src" in img.attrs)
            elif option == "links":
                # Get all hyperlink URLs
                results = "\n".join(a["href"] for a in soup.find_all("a") if "href" in a.attrs)

            # Set progress to 100% (complete)
            self.progress.set(1.0)
            # Display the scraped data in the text box
            self.result_text.insert("1.0", results)
            # Enable the export button to allow saving results
            self.export_button.configure(state=ctk.NORMAL)

        except Exception as e:
            # Show an error message if scraping fails
            messagebox.showerror("Error", f"Failed to scrape: {str(e)}")
            self.progress.set(0)  # Reset progress bar

    # Method to export the scraped data to a file
    def export_results(self):
        # Open a file dialog for the user to select a save location and file type
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"),
                                                            ("CSV Files", "*.csv"),
                                                            ("All Files", "*.*")])
        if file_path:
            # Write the scraped data to the selected file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.result_text.get(1.0, "end"))
            # Show a success message
            messagebox.showinfo("Export Successful", f"Results exported to {file_path}")

# Main entry point of the program
if __name__ == "__main__":
    # Create the main application window
    root = ctk.CTk()
    # Initialize the web scraper application
    app = ModernWebScraperApp(root)
    # Run the application
    root.mainloop()
