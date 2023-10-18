from web import get_page

if __name__ == '__main__':
    url = 'http://slowwly.robertomurray.co.uk'
    html_content = get_page(url)
    print(html_content)
