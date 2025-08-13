# Python web tools module
import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import os
import time

def web_scraper():
    """Web scraping tool"""
    st.subheader("🕷️ Web Scraper")
    st.write("Extract information from websites")
    
    url = st.text_input("Enter URL to scrape:", placeholder="https://example.com")
    
    if st.button("🔍 Scrape Website"):
        if url:
            try:
                with st.spinner("Scraping website..."):
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    response = requests.get(url, headers=headers, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract title
                    title = soup.find('title')
                    title_text = title.get_text() if title else "No title found"
                    
                    # Extract headings
                    headings = soup.find_all(['h1', 'h2', 'h3'])
                    heading_texts = [h.get_text().strip() for h in headings if h.get_text().strip()]
                    
                    # Extract links
                    links = soup.find_all('a', href=True)
                    link_texts = [f"{a.get_text().strip()} -> {a['href']}" for a in links[:20]]
                    
                    # Extract text content
                    text_content = soup.get_text()[:1000] + "..." if len(soup.get_text()) > 1000 else soup.get_text()
                    
                    # Display results
                    st.success("✅ Website scraped successfully!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("📄 Page Title")
                        st.write(title_text)
                        
                        st.subheader("🔗 Links (First 20)")
                        for link in link_texts[:10]:
                            st.write(f"• {link}")
                    
                    with col2:
                        st.subheader("📝 Headings")
                        for heading in heading_texts[:10]:
                            st.write(f"• {heading}")
                    
                    st.subheader("📖 Text Content (First 1000 chars)")
                    st.text_area("Content:", value=text_content, height=200, disabled=True)
                    
                    # Download option
                    if st.button("💾 Download Scraped Data"):
                        data = {
                            "url": url,
                            "title": title_text,
                            "headings": heading_texts,
                            "links": link_texts,
                            "content": text_content
                        }
                        st.download_button(
                            label="📥 Download JSON",
                            data=json.dumps(data, indent=2),
                            file_name=f"scraped_data_{int(time.time())}.json",
                            mime="application/json"
                        )
                        
            except Exception as e:
                st.error(f"❌ Error scraping website: {str(e)}")
        else:
            st.warning("Please enter a URL")

def web_search():
    """Web search tool"""
    st.subheader("🔍 Web Search")
    st.write("Search the web for information")
    
    search_query = st.text_input("Enter search query:", placeholder="Python programming")
    search_engine = st.selectbox("Select search engine:", ["Google", "Bing", "DuckDuckGo"])
    
    if st.button("🔍 Search"):
        if search_query:
            try:
                with st.spinner("Searching..."):
                    if search_engine == "Google":
                        search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                        st.success(f"🔍 Search completed! Click below to view results:")
                        st.markdown(f"[View Google Search Results]({search_url})")
                        
                    elif search_engine == "Bing":
                        search_url = f"https://www.bing.com/search?q={search_query.replace(' ', '+')}"
                        st.success(f"🔍 Search completed! Click below to view results:")
                        st.markdown(f"[View Bing Search Results]({search_url})")
                        
                    elif search_engine == "DuckDuckGo":
                        search_url = f"https://duckduckgo.com/?q={search_query.replace(' ', '+')}"
                        st.success(f"🔍 Search completed! Click below to view results:")
                        st.markdown(f"[View DuckDuckGo Search Results]({search_url})")
                        
            except Exception as e:
                st.error(f"❌ Error during search: {str(e)}")
        else:
            st.warning("Please enter a search query")

def api_tester():
    """API testing tool"""
    st.subheader("🧪 API Tester")
    st.write("Test REST APIs and view responses")
    
    api_url = st.text_input("Enter API URL:", placeholder="https://api.example.com/endpoint")
    method = st.selectbox("HTTP Method:", ["GET", "POST", "PUT", "DELETE"])
    
    # Headers input
    st.subheader("📋 Headers (Optional)")
    headers_input = st.text_area("Enter headers as JSON:", value='{"Content-Type": "application/json"}', height=100)
    
    # Body input for POST/PUT
    body_input = ""
    if method in ["POST", "PUT"]:
        st.subheader("📝 Request Body (Optional)")
        body_input = st.text_area("Enter request body as JSON:", height=150)
    
    if st.button("🚀 Test API"):
        if api_url:
            try:
                with st.spinner("Testing API..."):
                    headers = {}
                    if headers_input:
                        try:
                            headers = json.loads(headers_input)
                        except json.JSONDecodeError:
                            st.error("❌ Invalid headers JSON format")
                            return
                    
                    body = None
                    if body_input and method in ["POST", "PUT"]:
                        try:
                            body = json.loads(body_input)
                        except json.JSONDecodeError:
                            st.error("❌ Invalid body JSON format")
                            return
                    
                    # Make request
                    if method == "GET":
                        response = requests.get(api_url, headers=headers, timeout=30)
                    elif method == "POST":
                        response = requests.post(api_url, headers=headers, json=body, timeout=30)
                    elif method == "PUT":
                        response = requests.put(api_url, headers=headers, json=body, timeout=30)
                    elif method == "DELETE":
                        response = requests.delete(api_url, headers=headers, timeout=30)
                    
                    # Display results
                    st.success(f"✅ API call completed! Status: {response.status_code}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("📊 Response Info")
                        st.write(f"**Status Code:** {response.status_code}")
                        st.write(f"**Response Time:** {response.elapsed.total_seconds():.2f}s")
                        st.write(f"**Content Type:** {response.headers.get('content-type', 'Unknown')}")
                        st.write(f"**Content Length:** {len(response.content)} bytes")
                    
                    with col2:
                        st.subheader("📋 Response Headers")
                        for key, value in response.headers.items():
                            st.write(f"**{key}:** {value}")
                    
                    # Response content
                    st.subheader("📄 Response Content")
                    try:
                        if response.headers.get('content-type', '').startswith('application/json'):
                            json_response = response.json()
                            st.json(json_response)
                        else:
                            st.text(response.text[:2000] + "..." if len(response.text) > 2000 else response.text)
                    except:
                        st.text(response.text[:2000] + "..." if len(response.text) > 2000 else response.text)
                        
            except Exception as e:
                st.error(f"❌ Error testing API: {str(e)}")
        else:
            st.warning("Please enter an API URL")

def web_tools_menu():
    """Main web tools menu"""
    st.title("🌐 Web Tools")
    
    tab1, tab2, tab3 = st.tabs(["Web Scraper", "Web Search", "API Tester"])
    
    with tab1:
        web_scraper()
    
    with tab2:
        web_search()
    
    with tab3:
        api_tester()
