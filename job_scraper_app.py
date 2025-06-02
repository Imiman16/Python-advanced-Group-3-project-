# Import required libraries:
# - tkinter: Standard Python interface to Tk GUI toolkit
# - ttk: Themed widgets that provide better looking UI elements
# - scrolledtext: Text widget with built-in scrollbars
# - cmp_to_key: Converts comparison functions to key functions for sorting
# - JobScraper: Our custom job scraping class from job_scraper.py
import tkinter as tk
from tkinter import ttk, scrolledtext
from functools import cmp_to_key
from job_scraper import JobScraper

class JobScraperApp:
    # Initialize the application window
    def __init__(self, root):
        self.root = root  # Store the root window reference
        self.root.title("Job Scraper")  # Set window title
        self.root.geometry("800x600")  # Set initial window size (800x600 pixels)
        self.root.configure(bg="#f0f0f0")  # Set light gray background color

        self.setup_ui()  # Call method to create all UI elements

    # Method to set up all user interface components
    def setup_ui(self):
        # Create a frame container for search controls
        frame = ttk.Frame(self.root)
        # Pack the frame with padding and make it expand horizontally
        frame.pack(padx=10, pady=10, fill=tk.X)

        # Create and pack a label for job title input
        tk.Label(frame, text="Job Title:").pack(side=tk.LEFT, padx=(0, 5))
        # Create an entry field for job title search
        self.job_entry = ttk.Entry(frame)
        # Pack the entry field to expand horizontally
        self.job_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Create and pack a label for page number input
        tk.Label(frame, text="Page:").pack(side=tk.LEFT, padx=(10, 5))
        # Create an entry field for page number (width=5 characters)
        self.page_entry = ttk.Entry(frame, width=5)
        # Set default page number to "1"
        self.page_entry.insert(0, "1")
        # Pack the page entry field
        self.page_entry.pack(side=tk.LEFT)

        # Create search button that triggers perform_search method
        self.search_btn = ttk.Button(frame, text="Search", command=self.perform_search)
        # Pack the button with padding on the left
        self.search_btn.pack(side=tk.LEFT, padx=(10, 0))

        # Create another frame for sort/filter controls
        sort_frame = ttk.Frame(self.root)
        # Pack with padding and horizontal expansion
        sort_frame.pack(padx=10, fill=tk.X)

        # Create and pack label for sort options
        tk.Label(sort_frame, text="Sort by:").pack(side=tk.LEFT)
        # Create combobox (dropdown) for sort options
        self.sort_option = ttk.Combobox(sort_frame, values=["Title", "Location", "Salary"])
        # Set default sort option to "Title"
        self.sort_option.set("Title")
        # Pack the combobox with padding
        self.sort_option.pack(side=tk.LEFT, padx=5)

        # Create entry field for filtering results
        self.filter_entry = ttk.Entry(sort_frame)
        # Set placeholder text
        self.filter_entry.insert(0, "Filter by keyword...")
        # Pack to expand horizontally
        self.filter_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Create filter button that triggers filter_results method
        self.filter_btn = ttk.Button(sort_frame, text="Filter", command=self.filter_results)
        # Pack the filter button
        self.filter_btn.pack(side=tk.LEFT)

        # Create scrolled text area for displaying results:
        # - wrap=tk.WORD: Wrap at word boundaries
        # - bg="white": White background
        # - font=("Arial", 10): Arial 10pt font
        self.result_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, bg="white", font=("Arial", 10))
        # Pack the text area with padding and make it expand in both directions
        self.result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Method to perform job search and display results
    def perform_search(self):
        # Clear previous results (from line 1, character 0 to END)
        self.result_text.delete(1.0, tk.END)
        # Get job title from entry field
        job_input = self.job_entry.get()
        # Get page number and convert to integer
        page = int(self.page_entry.get())

        # Create JobScraper instance with user inputs
        scraper = JobScraper(job_input, page)
        # Scrape jobs from all websites
        jobs = scraper.scrape_all()

        # Get selected sort option and convert to lowercase
        sort_by = self.sort_option.get().lower()

        # Define comparison function for sorting
        def compare(a, b):
            # Returns -1 if a < b, 0 if equal, 1 if a > b
            return (a[sort_by] > b[sort_by]) - (a[sort_by] < b[sort_by])

        # Sort jobs using our comparison function (converted to key function)
        jobs.sort(key=cmp_to_key(compare))

        # Store jobs for potential filtering later
        self.jobs = jobs
        # Display each job in the results area
        for job in jobs:
            self.display_job(job)

    # Method to display a single job in the results area
    def display_job(self, job):
        # Insert job title with "title" tag (blue and bold)
        self.result_text.insert(tk.END, f"{job['title']}\n", "title")
        # Insert location with "location" tag (green)
        self.result_text.insert(tk.END, f"Location: {job['location']}\n", "location")
        # Insert salary with "salary" tag (purple)
        self.result_text.insert(tk.END, f"Salary: {job['salary']}\n", "salary")
        # Insert source with "source" tag (gray)
        self.result_text.insert(tk.END, f"Source: {job['source']}\n\n", "source")

        # Configure text tags for styling:
        # Title styling: blue, bold, Helvetica 11pt
        self.result_text.tag_config("title", foreground="blue", font=("Helvetica", 11, "bold"))
        # Location styling: green text
        self.result_text.tag_config("location", foreground="green")
        # Salary styling: purple text
        self.result_text.tag_config("salary", foreground="purple")
        # Source styling: gray text
        self.result_text.tag_config("source", foreground="gray")

    # Method to filter displayed results by keyword
    def filter_results(self):
        # Get filter keyword and convert to lowercase
        keyword = self.filter_entry.get().lower()
        # Clear current results
        self.result_text.delete(1.0, tk.END)
        # Display only jobs matching the keyword in title, location or salary
        for job in self.jobs:
            if (keyword in job['title'].lower() or 
                keyword in job['location'].lower() or 
                keyword in job['salary'].lower()):
                self.display_job(job)

# Standard Python idiom to check if this is the main program
if __name__ == "__main__":
    root = tk.Tk()  # Create main window
    app = JobScraperApp(root)  # Create application instance
    root.mainloop()  # Start the GUI event loop