# agent_selection
Submission for VMES x Universal Hackathon
Prepare by: A Kone Kyuan
Date: 09 / 11 / 2024

Introduction
The purpose of this report is to provide an overview of the challenges encountered and the lessons learned throughout the course of this project over the past month. During this period, we faced various obstacles and made several mistakes, each of which helped us learn valuable lessons. This report will outline the key issues we encountered, the approaches taken to resolve them, and the steps we took to improve our performance.

Thought
We found this challenge advanced for our current skill level, as we had limited experience with many of the functions required for this project. Additionally, the project’s timing was difficult, as it began during the summer break when many team members were out of town, making it hard to find enough time to work on it. Even so, we did our best with the time we had and are pleased with our effort.

Challenge
There are a variety of challenges. However, we were able to solve those problems together by researching and asking our seniors. The challenges are:

About Embedding Systems
Finding the right embedding systems is more difficult than you think. As for most of the embedding system has to be paid to be used and some are not accurate as it should. After we find the right embedding system we have to learn how to use it.

Vector Database
We didn’t realize at first that we needed to use a vector database, so we created three demo models without it. When we found out about this requirement, we had only a little time left, which made it challenging, especially since we weren’t familiar with this function.

Finding the right Formulas
We did not encounter issues with the distance formula. However, we faced challenges with the weighting formula, as we were uncertain which approach would be most suitable. Initially, we considered using the TF-IDF formula, but it did not give the results we wanted. We then decided to use the provided data, though this proved to be inaccurate. As a result, we had to do a lot of brainstorming. Ultimately, we decided to use the cosine distance formula.

Code Efficiency
We encountered a challenge when running our code for the first time, as it initially took significantly longer than expected. We later found that the delay happened only during the first run; after that, it was much faster than we expected.

About Streamlit (UI/UX)
Originally, we planned to present our code in a simple Python file. However, upon further consideration, we decided to make our work stand out by using a UI/UX interface to showcase our code through Streamlit. Since we were unfamiliar with Streamlit, one team member took the lead in researching its functionality, another focused on the design, and a third member continued working on the agent selection code.

Solution
Our first step was to brainstorm ideas. After multiple discussions, we decided to start by tokenizing words and converting them into vectors to calculate distances and weights. We built three demo models based on this approach, but we soon ran into a problem: our format didn’t meet the project requirements, so we needed to develop a new model.

We began by exploring different embedding functions, such as OpenAI, Gemini, and Cohere, before ultimately choosing a sentence transformer. We chose this model because it provided accurate and meaningful results, was easy to work with, and mostly because it’s free. We also decided to use the cosine distance formula and to rely on the provided data (Popularity, rated response, average rating response time) for weighting.

However, we encountered another issue: the adjusted scores were too high and inaccurate, as they produced negative values. To solve this, we decided to calculate the weights using cosine distance. With this setup, we were able to find similarities, calculate distances, and assign weights effectively. The formulas are provided below:


Furthermore, we decided to present our code through a UI/UX interface using Streamlit to make our work easier to understand. Since we had no previous experience with Streamlit, we needed to do a lot of research to use it properly.

Conclusion
In conclusion, although we successfully completed the project, we still consider it to be beyond our current skill level. However, we believe that we gave our best effort, and any mistakes made will provide valuable learning experiences. This, after all, was the primary objective of our participation in this competition. Regardless, we are grateful for the opportunity to have been part of this project.

References
1. https://www.sbert.net
2. https://www.youtube.com/watch?v=viZrOnJclY0\&t=14s
3. https://www.trychroma.com
4. https://www.youtube.com/watch?v=O3xbVmpdJwU\&t=3s
5. https://www.google.com
