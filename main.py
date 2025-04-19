#!/usr/bin/env python3

import os
import sys
from datetime import datetime
import garfield_site_scraper
import images_to_pdf
import config

def main():
    # Configure scraping
    garfield_site_scraper.START_YEAR = config.START_YEAR
    garfield_site_scraper.END_YEAR = config.END_YEAR
    
    # Configure PDF generation
    images_to_pdf.START_DECADE = config.START_DECADE
    images_to_pdf.END_DECADE = config.END_DECADE
    
    print(f"\nConfiguration:")
    print(f"- Downloading comics from {config.START_YEAR} to {config.END_YEAR}")
    print(f"- Generating PDFs for decades: {config.START_DECADE}s to {config.END_DECADE}s")
    
    print("\nStep 1: Downloading Garfield comics...")
    # Create the output directory if it doesn't exist
    os.makedirs(garfield_site_scraper.output_directory, exist_ok=True)
    
    # Run the scraper
    for year in range(garfield_site_scraper.START_YEAR, garfield_site_scraper.END_YEAR + 1):
        for month in range(1, 13):
            url = f"{garfield_site_scraper.base_url}{year}/{month}"
            print(f"Downloading images from: {url}")
            garfield_site_scraper.get_images(url)
    
    print("\nStep 2: Generating PDF collections...")
    # Get list of downloaded images
    image_files = os.listdir(images_to_pdf.IMAGES)
    if not image_files:
        print("No images found in the downloaded_images directory!")
        sys.exit(1)
        
    image_files.sort(key=images_to_pdf.parse_date_from_filename)
    
    # Generate PDFs for each decade in range
    for decade in range(config.START_DECADE, config.END_DECADE + 10, 10):
        images_to_pdf.generate_pdf_for_decade(
            decade,
            decade + 10,
            image_files
        )
    
    print("\nProcess completed successfully!")
    print(f"- New comics downloaded to: {garfield_site_scraper.output_directory}/")
    print("- PDFs generated:")
    for decade in range(config.START_DECADE, config.END_DECADE + 10, 10):
        print(f"  - garfield_collection_{decade}s.pdf")

if __name__ == "__main__":
    main()
