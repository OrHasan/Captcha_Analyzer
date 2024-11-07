from lib.load_analyzer_config_file import LoadConfig
from lib.ron_code import get_website as gw


def main():
    config = LoadConfig()
    website_config = config.website()
    url = website_config['website_url']
    sql_file_name = website_config['sql_file_name']
    gw.get_site_from_zone(url, sql_file_name, config)


if __name__ == "__main__":
    main()
