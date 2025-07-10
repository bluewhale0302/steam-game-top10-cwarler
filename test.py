from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
from rich.console import Console
from rich.style import Style
from rich.theme import Theme
from rich.syntax import Syntax
from rich.table import Table

def get_html_soup(url):
    try:
        html = urlopen(url)
    except:
        from requests import get
        response = get(url)
        html = response._content
    soup = bs(html, "html.parser")
    return soup

def print_html(soup):
    if not isinstance(soup, bs):
        soup = bs(str(soup), "html.parser")
    syntax = Syntax(soup.prettify(), "html", theme="monokai", line_numbers=True, word_wrap=True)
    pprint(syntax)

white = {
    'highlight': False,
    'style': Style(color="rgb(220,220,220)", italic=False, bold=True),
}

console = Console(theme=Theme({"repr.number": Style(color="bright_yellow", italic=True)}))
pprint = console.print

url = 'https://store.steampowered.com/search/?filter=topsellers'
print('가져올 페이지: ' + url)

soup = get_html_soup(url)
# print_html(soup)  # HTML 전체 출력은 주석 처리

games_block = soup.find_all('a', class_='search_result_row')

titles, prices, dates = [], [], []

for game in games_block[:10]:
    title = game.find('span', class_='title').text.strip()
    date = game.find('div', class_='search_released').text.strip()
    price_div = game.find('div', class_='search_price') or game.find('div', class_='search_price discounted') or game.find('div', class_='search_price_discount_combined')
    price = '가격 없음'
    if price_div:
        text = price_div.text.strip()
        price_lines = [line.strip() for line in text.split('\n') if line.strip()]
        if price_lines:
            price = price_lines[-1]
            if not price or price == '':
                price = price_lines[-2] if len(price_lines) > 1 else '가격 없음'
    titles.append(title)
    prices.append(price)
    dates.append(date)

table = Table(title="🔥 스팀 인기 게임 Top 10")
table.add_column("게임 제목", style="bold cyan")
table.add_column("출시일", style="green")
table.add_column("가격", style="magenta")

for title, date, price in zip(titles, dates, prices):
    table.add_row(title, date, price)

console.print(table)

import matplotlib
matplotlib.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(10, 5))
plt.barh(titles[::-1], list(range(1, 11)), color='skyblue')
plt.title("Top 10 Steam Games")
plt.xlabel("순위 (1~10)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()