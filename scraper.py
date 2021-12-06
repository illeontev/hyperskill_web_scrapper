import os
import string
import requests
import bs4

def convert_title_to_filename(title):
    filename = title
    for i in string.punctuation:
        if i in filename:
            filename = filename.replace(i, "")
    filename = filename.replace("—", "")
    filename = filename.replace(" ", "_")
    while "__" in filename:
        filename = filename.replace("__", "_")
    return filename

num_of_pages = int(input())
type_of_article = input()

for num_of_page in range(1, num_of_pages + 1):
    url = f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page={num_of_page}"
    url_base = "https://www.nature.com"
    try:
        dirname = f"{os.getcwd()}/Page_{num_of_page}"
        os.mkdir(dirname)
    except:
        pass
    response = requests.get(url)
    if response:
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        for article in soup.find_all("article"):
            article_type = article.find("span", {"data-test": "article.type"})

            if article_type.text.lower().strip() == type_of_article.lower():

                a = article.find("a")
                title = a.text

                link = article.find("a", {"data-track-action": "view article"})
                link_href = url_base + link["href"]

                content = ""
                response = requests.get(link_href)
                if response:
                    soup = bs4.BeautifulSoup(response.content, "html.parser")
                    body = soup.find("body")
                    div = body.find("div", {"class": "c-article-body u-clearfix"})
                    content = div.text.strip()
                    # filename = title
                    # for i in string.punctuation:
                    #     if i in title:
                    #         filename = filename.replace(i, "")
                    # filename = filename.replace("—", "")
                    # filename = filename.replace(" ", "_")
                    # while "__" in filename:
                    #     filename = filename.replace("__", "_")
                    filename = convert_title_to_filename(title)
                    with open(dirname + "/" + filename + ".txt", "wb") as fout:
                        fout.write(content.encode())
    else:
        print(f"The URL returned {response.status_code}")

print("Saved all articles.")