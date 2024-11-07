import socket
from itertools import zip_longest
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from unicodedata import normalize
from tqdm import tqdm
# - - - - - - - - - - - - - - -
from lib.general_funcs import solve_captcha_and_get_cookie


def get_ip_address(url):
    """Get IP address from url"""
    try:
        return socket.gethostbyname(url)
    except Exception as error:
        # print(f"An exception occurred while retrieving '{url}' IP address:\n", error)
        return None


def get_for_all(list_of_list):
    """Get for all list of list"""
    print("Please wait, Getting IP addresses out of the urls")
    [list_component.append(get_ip_address(list_component[2]))
     for list_component in tqdm(list_of_list, desc="Getting URLs IP addresses")]


def write_to_sql(data, sql_file_name):
    """Write data to sql file"""
    with open(sql_file_name + '.sql', 'w') as sql_file:
        # Write the SQL syntax
        sql_file.write("INSERT INTO site_contacts (date, notifier, url, os, ip) VALUES\n")
        for i in range(len(data)):
            date, notifier, url, os, ip = data[i]
            # Remove ASCII chars from the group name
            notifier = normalize('NFKD', notifier).encode('ascii', 'ignore').decode()
            # Write the data to the SQL file
            sql_file.write(f"('{date}', '{notifier}', '{url}', '{os}', '{ip}')")
            # Add a comma and newline if this is not the last item
            if i != len(data) - 1:
                sql_file.write(",\n")
        # Add a semicolon at the end of the SQL command
        sql_file.write(";\n")


def remove_http_https_and_after_coil(url):
    """Remove http:// or https:// and after .co.il from url"""
    parsed = urlparse(url)
    schemaless_url = parsed.netloc + parsed.path
    coil_index = schemaless_url.find('.co.il')
    if coil_index != -1:
        schemaless_url = schemaless_url[:coil_index + len('.co.il')]

    return schemaless_url


def get_page(page, url, all_website, cookie):
    domains = []
    verif = requests.get(url[:url.find("page=")+len("page=")] + str(page + 1), cookies=cookie).content
    soup = BeautifulSoup(verif, 'html.parser')
    time = [word for word in ["".join(i.text.split()) for i in soup.select('#ldeface tr td:nth-child(1)')] if
            word != 'Time' and word != 'Date']
    notifier = [word for word in ["".join(i.text.split()) for i in soup.select('#ldeface tr td:nth-child(2)')]
                if
                word != 'Notifier']

    for i in soup.select('#ldeface tr td:nth-child(8)'):
        if i.text != 'Domain':
            domains.append(remove_http_https_and_after_coil(i.text))

    os = [word for word in ["".join(i.text.split()) for i in soup.select('#ldeface tr td:nth-child(9)')] if
          word != 'OS']
    del time[-2:]

    new_list = [list(item) for item in zip_longest(time, notifier, domains, os)]
    all_website += new_list
    for web in new_list:
        print(web)


def get_site_from_zone(url, sql_file_name, config):
    """Get site from zone-h.org"""
    all_website = []
    # Update the cookie dictionary
    zhe, phpsessid = solve_captcha_and_get_cookie()
    cookie = {
        "ZHE": zhe,
        "PHPSESSID": phpsessid
    }
    # To scan all pages, change "pages_to_scan" to 50
    for j in range(config.website()['pages_to_scan']):
        get_page(j, url, all_website, cookie)

    get_for_all(all_website)
    write_to_sql(all_website, sql_file_name)
