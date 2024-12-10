# import requests
# from bs4 import BeautifulSoup
# import csv

# def scrape_clinido_data(base_url, max_pages):
#     all_data = []  # To store data from all pages
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
#     }

#     for page in range(1, max_pages + 1):
#         url = f"{base_url}?page={page}"
#         print(f"Scraping page {page}...")

#         response = requests.get(url, headers=headers)
#         if response.status_code != 200:
#             print(f"Failed to retrieve page {page}")
#             continue

#         # Decode the response content explicitly
#         response.encoding = 'utf-8'  # Set the encoding to UTF-8
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Find doctor entries
#         doctors = soup.find_all('div', class_='doc-nmsp')  # Update this selector as per the actual site

#         if not doctors:
#             print(f"No doctors found on page {page}")
#             continue

#         for doctor in doctors:
#             try:
#                 # Extract doctor name (now included in the scraped data)
#                 name_tag = doctor.find('h4')
#                 name = name_tag.text.strip() if name_tag else "N/A"

#                 # Extract title
#                 title_tag = doctor.find('p', class_='title')
#                 title = title_tag.text.strip() if title_tag else "N/A"

#                 # Extract about section
#                 about_tag = doctor.find('p', class_='doc-about')
#                 about = about_tag.text.strip() if about_tag else "N/A"

#                 # Append data to the list
#                 all_data.append({
#                     'name': name,
#                     'title': title,
#                     'about': about,
#                 })

#             except AttributeError as e:
#                 print(f"Skipping a doctor entry due to missing data: {e}")

#     return all_data


# def save_to_csv(data, filename):
#     if not data:
#         print("No data to save.")
#         return

#     keys = data[0].keys()  # Get column names from the first item
#     with open(filename, 'w', newline='', encoding='utf-8-sig') as output_file:
#         dict_writer = csv.DictWriter(output_file, fieldnames=keys)
#         dict_writer.writeheader()
#         dict_writer.writerows(data)
#     print(f"Data saved to {filename}")


# # Usage
# base_url = "https://clinido.com/ar/search/نساء-وتوليد/كل-المناطق/كل-المناطق"
# max_pages = 10  # Number of pages to scrape
# data = scrape_clinido_data(base_url, max_pages)

# # Save the data to an Excel-compatible CSV
# save_to_csv(data, 'clinido_doctors.csv')
import requests 
from bs4 import BeautifulSoup 
import csv

def scrape_clinido_data(base_url, max_pages):
    all_data = []  # To store data from all pages
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        print(f"Scraping page {page}...")

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}")
            continue

        response.encoding = 'utf-8'  # Set the encoding to UTF-8
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find doctor entries
        doctor_entries = soup.find_all('div', class_='doc-nmsp')
        location_entries = soup.find_all('div', class_='img-loca')
        phone_entries = soup.find_all('div', class_='col-lg-4 col-md-4 col-sm-4 col-xs-4')  # For additional info
        profile_img_entries = soup.find_all('div', class_='img-circle prof-img')  # For profile images

        if not doctor_entries:
            print(f"No doctor entries found on page {page}")
            continue

        # Iterate over all matched entries
        for doctor, location_entry, phone, profile_img_entry in zip(doctor_entries, location_entries, phone_entries, profile_img_entries):
            try:
                # Extract doctor name
                name_tag = doctor.find('h4')
                name = name_tag.text.strip() if name_tag else "N/A"

                # Extract title
                title_tag = doctor.find('p', class_='title')
                title = title_tag.text.strip() if title_tag else "N/A"

                # Extract about section
                about_tag = doctor.find('p', class_='doc-about')
                about = about_tag.text.strip() if about_tag else "N/A"

                # Extract location
                location_tag = location_entry.find('p', class_='clin-loc')
                location = location_tag.text.strip() if location_tag else "N/A"

                # Default value for consultation fee
                consultation_fee = "N/A"

                for text_tag, value_tag in zip(phone.find_all('p', class_='text'), phone.find_all('p', class_='value')):
                    if text_tag and value_tag and text_tag.text.strip() == "سعر الكشف": 
                        consultation_fee = value_tag.text.strip()  
                        break

                # Extract background image URL from style
                if profile_img_entry and 'style' in profile_img_entry.attrs:
                    style_content = profile_img_entry['style']
                    start = style_content.find("url('") + len("url('")
                    end = style_content.find("')", start)
                    profile_img_url = style_content[start:end]
                else:
                    profile_img_url = "N/A"

                # Append data to the list
                all_data.append({
                    'name': name,
                    'title': title,
                    'about': about,
                    'location': location,
                    'consultation_fee': consultation_fee,  # Save the extracted value
                    'profile_image': profile_img_url
                })

            except AttributeError as e:
                print(f"Skipping an entry due to missing data: {e}")

    return all_data


def save_to_csv(data, filename):
    if not data:
        print("No data to save.")
        return

    keys = data[0].keys()  # Get column names from the first item
    with open(filename, 'w', newline='', encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Data saved to {filename}")


# Usage
base_url = "https://clinido.com/ar/search/نساء-وتوليد/كل-المناطق/كل-المناطق"
max_pages = 123  # Number of pages to scrape
data = scrape_clinido_data(base_url, max_pages)

# Save the data to an Excel-compatible CSV
save_to_csv(data, 'clinido_doctors_ar.csv')
