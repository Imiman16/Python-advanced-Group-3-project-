# Import required libraries:
# - requests: For making HTTP requests to websites
# - BeautifulSoup: For parsing and extracting data from HTML/XML
# - cmp_to_key: Utility for converting comparison functions to key functions (used in sorting)
import requests
from bs4 import BeautifulSoup
from functools import cmp_to_key

class JobScraper:
    # Initialize the scraper with job search term and page number
    def __init__(self, job_input, page):
        self.job_input = job_input  # Store the job search term (e.g., "software engineer")
        self.page = page            # Store the page number for paginated results
        self.jobs = []             # Initialize empty list to store scraped jobs

    # Main method to coordinate scraping from all websites
    def scrape_all(self):
        self.scrape_graduate_jobs()  # Scrape graduate-jobs.com
        self.scrape_reed()           # Scrape reed.co.uk
        self.scrape_jobs_ac_uk()     # Scrape jobs.ac.uk
        return self.jobs             # Return all collected jobs

    # Helper method to clean and normalize text
    def clean(self, text):
        # Remove extra whitespace by:
        # 1. strip(): Remove leading/trailing whitespace
        # 2. split(): Split into words (handles multiple spaces)
        # 3. join(): Recombine with single spaces
        return ' '.join(text.strip().split())

    # Method to scrape graduate-jobs.com
    def scrape_graduate_jobs(self):
        # Construct URL with search query
        url = f"https://www.graduate-jobs.com/search?q={self.job_input}"
        
        # Fetch the webpage HTML content
        html = requests.get(url).text
        
        # Parse HTML using BeautifulSoup with lxml parser
        soup = BeautifulSoup(html, "lxml")
        
        # Find all job listing elements by their CSS class
        listings = soup.find_all("a", class_="c-job__item-new job-list__item")
        
        # Process each job listing
        for job in listings:
            try:
                # Extract and clean job title from specific element
                title = self.clean(job.find("p", class_="c-job__title-new").text)
                
                # Extract and clean job location
                location = self.clean(job.find("span", class_="c-job__locations").text)
                
                # Extract and clean salary information
                salary = self.clean(job.find("p", class_="c-job__locations").text)
                
                # Add job data to the jobs list as a dictionary
                self.jobs.append({
                    "title": title,
                    "location": location,
                    "salary": salary,
                    "source": "Graduate Jobs"  # Track which website this came from
                })
            except:
                # Skip any listings that cause errors during processing
                continue

    # Method to scrape reed.co.uk
    def scrape_reed(self):
        # Construct URL with search query and page number
        url = f"https://www.reed.co.uk/jobs/engineering-jobs?keywords={self.job_input}&pageno={self.page}"
        
        # Fetch webpage content
        html = requests.get(url).text
        
        # Parse HTML
        soup = BeautifulSoup(html, "lxml")
        
        # Find all job cards by their HTML structure
        listings = soup.find_all("article", class_="card job-card_jobCard__MkcJD")
        
        # Process each job card
        for job in listings:
            try:
                # Extract and clean job title (from h2 tag)
                title = self.clean(job.find("h2").text)
                
                # Extract location from element with specific data attribute
                location = self.clean(job.find("li", attrs={'data-qa': "job-card-location"}).text)
                
                # Extract salary from specific class element
                salary = self.clean(job.find("li", class_="job-card_jobMetadata__item___QNud").text)
                
                # Add to jobs list
                self.jobs.append({
                    "title": title,
                    "location": location,
                    "salary": salary,
                    "source": "Reed"  # Track source
                })
            except:
                # Skip problematic listings
                continue

    # Method to scrape jobs.ac.uk
    def scrape_jobs_ac_uk(self):
        # Construct URL with search parameters
        url = f"https://www.jobs.ac.uk/search/?keywords={self.job_input}&page={self.page}"
        
        # Fetch webpage
        html = requests.get(url).text
        
        # Parse HTML
        soup = BeautifulSoup(html, "lxml")
        
        # Find all job result elements
        listings = soup.find_all("div", class_="j-search-result__result ie-border-left")
        
        # Process each job result
        for job in listings:
            try:
                # Extract title from anchor tag
                title = self.clean(job.find("a").text)
                
                # Find location element by searching for text containing "Location:"
                location_div = job.find("div", string=lambda t: t and "Location:" in t)
                
                # Clean location text and remove "Location:" prefix if found
                location = self.clean(location_div.text.replace("Location:", "")) if location_div else "N/A"
                
                # Find the info div containing salary
                info = job.find("div", class_="j-search-result__info")
                
                # Extract salary by splitting text at "Salary:" marker
                salary = self.clean(info.text.split("Salary:")[-1].strip()) if "Salary:" in info.text else "N/A"
                
                # Add to jobs list
                self.jobs.append({
                    "title": title,
                    "location": location, 
                    "salary": salary,
                    "source": "Jobs.ac.uk"  # Track source
                })
            except:
                # Skip problematic listings
                continue