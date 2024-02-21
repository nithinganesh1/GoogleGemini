# Amazon Review Summarizer

This application accepts Amazon links from users, analyzes the reviews of the products, and provides a summarized review and suggestions of each product.

### App link
https://amazonreviewsummarizer.streamlit.app/
---
also you can run this app usign your terminal run bellow code on your terminal

pip install --upgrade streamlit
streamlit run https://raw.githubusercontent.com/nithinganesh1/GoogleGemini/main/Amazon_Review_Summarizer/app.py

The app can only be used by entering Amazon product links.

### sample images
![image](https://github.com/nithinganesh1/GoogleGemini/assets/122164879/23c7f6e8-dff3-46af-89e2-b3d7d56f1658)
![image](https://github.com/nithinganesh1/GoogleGemini/assets/122164879/6478b562-226f-47ec-a0aa-84cecc6d9ba6)
![image](https://github.com/nithinganesh1/GoogleGemini/assets/122164879/039605d7-362d-413a-b415-cce240d70ea7)
![image](https://github.com/nithinganesh1/GoogleGemini/assets/122164879/c7c4cf43-f9be-4245-b782-1c649f210396)

I have removed my Gemini API keys. You can now use your own API keys and try.
https://ai.google.dev/?gad_source=1&gclid=CjwKCAiA29auBhBxEiwAnKcSqm5anTAxAO7OCYfDTiJKr0082QKLwu3xUtcPvkGR3Iwy55c9XTqjZhoCqmYQAvD_BwE

genai.configure(api_key=st.secrets.GEMINI_AI_KEY) ---> genai.configure(api_key = "Your API")
and run the app using streamlit

