import os
from datetime import datetime
from reportlab.lib.pagesizes import legal
from reportlab.platypus import SimpleDocTemplate, Image, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

START_DECADE = 2020
END_DECADE = 2020


IMAGES = 'downloaded_images'
IMAGES_PER_PAGE = 100  # Number of images per page
PAGE_WIDTH, PAGE_HEIGHT = legal
PAGE_WIDTH = PAGE_WIDTH / 2

def parse_date_from_filename(filename):
    prefix = filename[:2]
    year = int(filename[2:4])
    if year < 50:
        year += 2000
    else:
        year += 1900
    month = int(filename[4:6])
    day = int(filename[6:8])
    return datetime(year, month, day)

def generate_pdf_for_decade(start_year, end_year, images):
    pdf_file = f'garfield_collection_{start_year}s.pdf'

    doc = SimpleDocTemplate(pdf_file, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    story = []

    # Filter images for the specified decade
    decade_images = [image for image in images if start_year <= parse_date_from_filename(image).year < end_year]

    # Calculate number of pages needed
    num_pages = len(decade_images) // IMAGES_PER_PAGE
    if len(decade_images) % IMAGES_PER_PAGE != 0:
        num_pages += 1

    for page_num in range(num_pages):
        images_and_dates = []
        for i in range(IMAGES_PER_PAGE):
            index = page_num * IMAGES_PER_PAGE + i
            if index >= len(decade_images):
                break

            image_file = decade_images[index]
            image_path = os.path.join(IMAGES, image_file)

            img = Image(image_path)
            img.drawWidth = img.drawWidth / 2
            img.drawHeight = img.drawHeight / 2

            # Adding text annotation with the date just below the image
            date_text = parse_date_from_filename(image_file).strftime('%Y-%b-%d')
            date_paragraph = Paragraph(date_text, getSampleStyleSheet()['BodyText'])
            
            images_and_dates.append((date_paragraph, img))

        # Interleave dates and images
        for date_paragraph, img in images_and_dates:
            story.append(date_paragraph)
            story.append(Spacer(1, 10))
            story.append(img)

        if page_num < num_pages - 1:
            story.append(Spacer(1, PAGE_HEIGHT // 20))  # Spacer between pages

    doc.build(story)
    print(f"PDF created: {pdf_file}")

image_files = os.listdir(IMAGES)
image_files.sort(key=parse_date_from_filename)

# Generate PDFs for each decade
for decade in range(START_DECADE, END_DECADE + 10, 10):
    generate_pdf_for_decade(decade, decade + 10, image_files)
