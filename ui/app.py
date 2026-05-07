import streamlit as st
import requests
import re
import time


# API_URL = "http://localhost:8000" uncomment this if running locally
API_URL = "http://backend:8000"

st.set_page_config(layout="wide")

# LEFT PANEL
with st.sidebar:
    st.title("Blog Generator")

    openrouter_key = st.text_input("OpenRouter API Key", type="password")
    tavily_key = st.text_input("Tavily API Key", type="password")

    topic = st.text_area("Enter topic")

    


    if st.button("Generate"):
        if not topic:
            st.warning("Please enter a topic")

        elif not openrouter_key:
            st.warning("Please enter OpenRouter API key")

        else:
            with st.spinner("🚀 Generating your blog... Hang tight!"):
                try:
                    res = requests.post(
                        f"{API_URL}/generate",
                        json={
                            "topic": topic,
                            "openrouter_key": openrouter_key,
                            "tavily_key": tavily_key
                        }
                    )

                    # ✅ STEP 1: Check HTTP status
                    if res.status_code != 200:
                        try:
                            error_msg = res.json().get("detail", "Something went wrong")
                        except:
                            error_msg = res.text

                        if "tavily" in error_msg.lower():
                            st.error("⚠️ This topic requires internet research.\nPlease provide a Tavily API key.")
                        else:
                            st.error(f"❌ Failed to generate blog:\n{error_msg}")

                    else:
                        data = res.json()

                        # ✅ STEP 3: Check if content actually exists
                        if not data.get("content"):
                            st.error("⚠️ Blog generation failed internally. Please try again.")
                        else:
                            st.success("✅ Blog Generated Successfully!")

                except Exception as e:
                    st.error(f"🚨 Connection error: {e}")









    # if st.button("Generate"):
    #     if not topic:
    #         st.warning("Please enter a topic")
    #     elif not openrouter_key:
    #         st.warning("Please enter OpenRouter API key")
    #     else:
    #         with st.spinner("Generating blog..."):
    #             res = requests.post(
    #                 f"{API_URL}/generate",
    #                 json={
    #                     "topic": topic,
    #                     "openrouter_key": openrouter_key,
    #                     "tavily_key": tavily_key
    #                 }
    #             )
    #         st.success("Blog Generated!")
            



    st.divider()
    st.subheader("Saved Blogs")

    blogs_res = requests.get(f"{API_URL}/blogs").json()
    blogs = blogs_res.get("blogs", [])


    if blogs:
        selected_blog = st.selectbox("Select blog", blogs)
    else:
        selected_blog = None
        st.info("No blogs generated yet")

# RIGHT PANEL
st.title("Blog Viewer")

if selected_blog:


    res = requests.get(f"{API_URL}/blog/{selected_blog}")

    if res.status_code != 200:
        st.error(f"Failed to load blog: {res.status_code}")
    else:
        try:
            data = res.json()
        except Exception:
            st.error("Invalid response from server (not JSON)")
            st.text(res.text)  # show raw response for debugging
        else:
            if "content" not in data:
                st.error("No content found in response")
                st.write(data)
            else:
                content = data["content"]
                st.markdown(content)

                # Extract links
                links = list(set(re.findall(r'https?://[^\s)]+', content)))

                st.subheader("🔗 Links")
                for link in links:
                    st.write(link)