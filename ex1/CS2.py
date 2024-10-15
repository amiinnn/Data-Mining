import requests
from bs4 import BeautifulSoup
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_tasnim_links(main_url):
    response = requests.get(main_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            if '/news/' in link and link not in links:
                links.append(link)
        full_links = ['https://www.tasnimnews.com' + link if link.startswith('/') else link for link in links]
        return full_links
    else:
        print("Failed to retrieve the Tasnim main page.")
        return []


def get_mehrnews_links(main_url):
    response = requests.get(main_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            if '/news/' in link and link not in links:
                links.append(link)
        full_links = ['https://www.mehrnews.com' + link if link.startswith('/') else link for link in links]
        return full_links
    else:
        print("Failed to retrieve the Mehr News main page.")
        return []


def get_news_content_tasnim(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('h1')  # تیتر در تسنیم
        title_text = title.text.strip() if title else "Title not found"
        
        content = soup.find_all('p')  # جستجو در تگ‌های پاراگراف
        news_text = ' '.join([p.text for p in content])
        
        return title_text, news_text
    else:
        return None, f"Failed to retrieve the page. Status code: {response.status_code}"


def get_news_content_mehrnews(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('h1')  # تیتر در مهر نیوز
        title_text = title.text.strip() if title else "Title not found"
        
        content = soup.find_all('p')  # جستجو در تگ‌های پاراگراف
        news_text = ' '.join([p.text for p in content])
        
        return title_text, news_text
    else:
        return None, f"Failed to retrieve the page. Status code: {response.status_code}"


tasnim_url = 'https://www.tasnimnews.com/'
mehrnews_url = 'https://www.mehrnews.com/'


tasnim_news_urls = get_tasnim_links(tasnim_url)
mehrnews_news_urls = get_mehrnews_links(mehrnews_url)


if tasnim_news_urls and mehrnews_news_urls:
    tasnim_random_url = random.choice(tasnim_news_urls)
    mehrnews_random_url = random.choice(mehrnews_news_urls)
    
    tasnim_title, tasnim_content = get_news_content_tasnim(tasnim_random_url)
    mehrnews_title, mehrnews_content = get_news_content_mehrnews(mehrnews_random_url)


    print("Tasnim News:")
    print("=" * 80)
    print(f"Title: {tasnim_title}")
    print(f"Content: {tasnim_content}\n")
    
    print("Mehr News:")
    print("=" * 80)
    print(f"Title: {mehrnews_title}")
    print(f"Content: {mehrnews_content}\n")

    # محاسبه شباهت کسینوسی
    vectorizer = TfidfVectorizer().fit_transform([tasnim_content, mehrnews_content])
    vectors = vectorizer.toarray()
    cosine_sim = cosine_similarity(vectors)
    print(f"Cosine Similarity between the two news articles: {cosine_sim[0][1]}")
else:
    print("Could not retrieve news links from one or both websites.")
