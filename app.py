# import essential dependencies
import streamlit as st
from streamlit_lottie import st_lottie
import fitz
import json
from PIL import Image
import io
import zipfile

# Streamlit page configuration
st.set_page_config(page_title = 'PDF Image Extractor',
                   page_icon = ':open_file_folder:',
                   layout = 'centered',
                   initial_sidebar_state = 'auto')

# function to load the lottie file
def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)

# function to extract images
def extract_images_from_page(page):
    image_list = page.get_images(full=True)
    images = []
    for img_index, img in enumerate(image_list, start=1):
        xref = img[0]
        base_image = pdf.extract_image(xref)
        image_bytes = base_image['image']
        image_ext = base_image['ext']
        image = Image.open(io.BytesIO(image_bytes))
        images.append((image, image_ext))
    return images

description = '''
A tool for extracting image(s) from PDF file. 
'''

# title
container = st.container(border=True)
container.title(':open_file_folder: PDF Image Extractor')
container.write(description)
container.markdown('##### Potential Use Cases:')


container.markdown('''
- **Academic Research**: Researchers can extract graphs, charts, and figures from academic papers and journals for analysis or inclusion in their own research publications.
- **Business Reports**: Professionals in finance and business can extract charts and tables from PDF reports to use in presentations, reports, or data analysis.
- **Educational Materials**: Educators can extract images from PDF textbooks and resources to create engaging learning materials and presentations for students.
- **Content Creation**: Content creators and social media managers can extract visuals from PDFs for use in articles, posts, and digital content across various platforms.
''', unsafe_allow_html = True)


lottie_cover = load_lottiefile('img/cover.json')
with container:
    st.lottie(lottie_cover, speed=2, reverse=False, loop=True, quality='low', height=500, key='first_animate')

# sidebar
st.sidebar.title('File Uploader')
upload_file = st.sidebar.file_uploader('Upload a PDF file for image extraction', accept_multiple_files=False, type='pdf')

# extracting image(s) from the uploaded PDF file
if upload_file:
    file_name = upload_file.name
    st.markdown(f'#### File Uploaded: {file_name}')
    image_list = []
    pdf = fitz.open(stream=upload_file.read(), filetype='pdf')

    for page_index in range(len(pdf)):
        page = pdf[page_index]
        
        # extract images from the page
        images = extract_images_from_page(page)
        if images:
            image_list.extend(images)

    st.markdown(f'### Found total of {len(image_list)} image(s) in the PDF document.')

    # create a zip file of the extracted images
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for img_index, (image, image_ext) in enumerate(image_list, start=1):
            img_filename = f'image_{img_index}.{image_ext}'
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=image_ext.upper())
            zip_file.writestr(img_filename, img_byte_arr.getvalue())
    
    zip_buffer.seek(0)
    
    # provide a download link for the zip file
    st.download_button(
        label="Download all images as ZIP",
        data=zip_buffer,
        file_name="extracted_images.zip",
        mime="application/zip"
    )

else:
    st.write('Upload a PDF file.')
