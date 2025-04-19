# Garfield Comic Strip Archiver

This project downloads and archives Garfield comic strips into decade-wise PDF collections. It consists of two main scripts that handle downloading the comics and converting them into organized PDF files.

## Features

- Downloads Garfield comics from specified years and months
- Organizes comics into decade-based PDF collections
- Includes date annotations for each comic
- Avoids re-downloading existing images
- Creates well-formatted PDFs with multiple comics per page

## Requirements

```
beautifulsoup4
requests
reportlab
```

## Project Structure

- `garfield_site_scraper.py` - Downloads comic images from the web
- `images_to_pdf.py` - Converts downloaded images into organized PDF collections
- `main.py` - Runs the complete process (downloading and PDF generation)
- `downloaded_images/` - Directory where comic images are stored
- Generated PDFs are named as `garfield_collection_[DECADE]s.pdf`

## Usage

1. Configure the script:
Edit `config.py` to set your desired years and decades:
```python
# Years to download comics from
START_YEAR = 2024    # First year to download
END_YEAR = 2024     # Last year to download

# Decades to generate PDFs for
START_DECADE = 2020  # Will generate PDFs starting from 2020s
END_DECADE = 2020   # Will generate PDFs up to 2020s
```

2. Run the script:
```bash
python main.py
```
This will:
- Download comics for the years specified in config.py
- Generate PDF collections for the decades specified in config.py

3. Alternatively, you can run the scripts separately:
```bash
python garfield_site_scraper.py
```
You can adjust the `START_YEAR` and `END_YEAR` variables in the script to specify which years to download.

```bash
python images_to_pdf.py
```
You can adjust the `START_DECADE` and `END_DECADE` variables to specify which decades to process.

## PDF Output

The script generates PDF files for each decade:
- `garfield_collection_1970s.pdf`
- `garfield_collection_1980s.pdf`
- `garfield_collection_1990s.pdf`
- `garfield_collection_2000s.pdf`
- `garfield_collection_2010s.pdf`
- `garfield_collection_2020s.pdf`

Each PDF contains:
- 100 comics per page
- Date annotations for each comic
- Optimized image sizes for better viewing

## Configuration

### garfield_site_scraper.py
- `START_YEAR` and `END_YEAR`: Define the range of years to download
- `output_directory`: Where downloaded images are saved (default: 'downloaded_images')

### images_to_pdf.py
- `START_DECADE` and `END_DECADE`: Define which decades to process into PDFs
- `IMAGES_PER_PAGE`: Number of comics per PDF page (default: 100)

## Note

This project downloads comics from pt.jikos.cz/garfield/. Please ensure you have permission to download and use the comics, and respect the website's terms of service and copyright laws.
