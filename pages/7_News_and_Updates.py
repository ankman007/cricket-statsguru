import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="News and Updates",
    page_icon="📰",
    layout="wide",
    # initial_sidebar_state="collapsed",
)
NEWS_API_KEY = '80a5ed8efc4a49c89d7efabe130d0716'
NEWS_API_ENDPOINT = 'https://newsapi.org/v2/everything'

@st.cache_data
def check_image_availability(image_url):
    try:
        response = requests.head(image_url)
        if response.status_code == 200:
            image_response = requests.get(image_url)
            image_bytes = BytesIO(image_response.content)
            image = Image.open(image_bytes)
            width, height = image.size
            # st.write(f'Image dimensions: {width} x {height}')
            return True
    except requests.ConnectionError:
        pass
    except Exception as e:
        st.error(f"Error: {e}")
    return False
@st.cache_data
def fetch_cricket_articles(news_category):
    count = 0
    params = {
        'apiKey': NEWS_API_KEY,
        'q': news_category,
        'language': 'en',
    }

    response = requests.get(NEWS_API_ENDPOINT, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data['articles']

        for article in articles:
            if count >= 30:
                    break
            count += 1
            if news_category == 'cricket nepal' and 'Nepal' not in article['title']:
                continue
            if news_category == 'cricket news' and 'cricket' not in article['title']:
                continue
            with st.container(border=True):
                title_html = f"<a href='{article['url']}' target='_blank' style='text-decoration: none; color: black;'>{article['title']}</a>"
                st.markdown(f"## {title_html}", unsafe_allow_html=True)    
                
                if 'urlToImage' in article:
                    image_url = article['urlToImage']
                    if check_image_availability(image_url):
                        st.image(image_url)
                    else:
                        st.write("Image unavailable")
                else:
                    st.write("No image available")
                
                st.write(article['description'])
                st.write("---")
    else:
        st.error('Failed to fetch cricket articles')

def main():
    st.header('Latest Cricket News & Editorials')

    tab_titles = [
        "National News",
        "International News",
    ]
    tabs = st.tabs(tab_titles)

    with tabs[0]:
        fetch_cricket_articles('cricket nepal')

    with tabs[1]:
        fetch_cricket_articles('cricket news')

if __name__ == "__main__":
    main()
