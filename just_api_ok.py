#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import openai
import creds

# Set your OpenAI API key
openai.api_key = creds.OPENAI_API_KEY

def generate_news(selected_date):
    prompt = f"What happened on {selected_date}?\nGive me a good news with a 😄, a neutral news with a 😐, and a bad news with a 😔. Do not mention good news, neutral news, bad news: just use the icons. Insert related Wikipedia links."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )

    return response.choices[0].text.strip()

selected_date = "1960-03-09"  # Replace this with your desired date
news_summary = generate_news(selected_date)
st.write(news_summary)

