#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import openai

# Set your OpenAI API key
openai.api_key = "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"

def generate_news(selected_date):
    prompt = f"What happened on {selected_date}?\nGive me a good news with a 😄, a neutral news with a 😐, and a bad news with a 😔. Insert related Wikipedia links."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )

    return response.choices[0].text.strip()
    
    
news_summary = generate_news(selected_date)
print(news_summary)

st.write(news_summary)

