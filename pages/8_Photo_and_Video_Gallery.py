import os
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Photo & Video Gallery",
    page_icon="📸",
    layout="centered",
)

def fetch_videos():
    df = pd.read_csv('data/youtube_links.csv')
    df = df.sample(frac=1).reset_index(drop=True)
    max_chars = 200
    for index, row in df.iterrows():
        container = st.container(border=True)
        container.markdown(f"### {row['video_title']}")
        description = str(row['description'])[:max_chars] + ('...' if len(str(row['description'])) > max_chars else '')

        container.write(description)
        container.video(row['link'])
        st.write('---')

def fetch_images():
    image_dir = "./images"
    image_files = os.listdir(image_dir)
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(image_dir, x)))

    num_columns = 1
    image_chunks = [image_files[i:i + num_columns] for i in range(0, len(image_files), num_columns)]

    for image_chunk in image_chunks:
        cols = st.columns(num_columns)
        for col, image_file in zip(cols, image_chunk):
            filename, extension = os.path.splitext(image_file)
            col.image(os.path.join(image_dir, image_file), caption=filename)

def main():
    tab_titles = [
        "Photos",
        "Videos",
    ]
    tabs = st.tabs(tab_titles)

    with tabs[0]:
        fetch_images()
    with tabs[1]:
        fetch_videos()

if __name__ == "__main__":
    main()