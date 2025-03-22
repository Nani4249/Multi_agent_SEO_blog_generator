# Importing  required libraries
import requests  # For making HTTP requests to fetch web content
from bs4 import BeautifulSoup  # For parsing HTML and extracting data
from transformers import GPT2LMHeadModel, GPT2Tokenizer  # For using GPT-2 model for text generation
import torch  # PyTorch, required for GPT-2 model
import nltk  # Natural Language Toolkit for text processing
import os  # For interacting with the operating system (not used in this script)

# Downloaded NLTK data packages required for sentence tokenization
nltk.download('punkt')  # Punkt tokenizer for splitting text into sentences
nltk.download('punkt_tab')  # Additional tokenizer data for NLTK

# Research Agent: Finds trending HR topics and gathers information
class ResearchAgent:
    def __init__(self):
        # Initialize an empty list to store trending topics
        self.trending_topics = []

    def search_trending_topics(self):
        # URL of the LinkedIn Talent Blog to scrape trending HR topics
        url = "https://www.linkedin.com/business/talent/blog"
        try:
            # Set headers to mimic a browser request
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            print("Fetching data from:", url)
            # Send a GET request to the URL
            response = requests.get(url, headers=headers, timeout=10)
            # Raise an exception if the request fails (e.g., 404 or 500 errors)
            response.raise_for_status()
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extracting article titles from the blog
            # Look for <h2> tags with class 'blog-post__title'
            articles = soup.find_all('h2', class_='blog-post__title')
            if not articles:
                # If no articles are found, try an alternative structure
                print("No articles found. Trying alternative structure...")
                # Look for <a> tags with class 'blog-post__title-link'
                articles = soup.find_all('a', class_='blog-post__title-link')
            
            # Extract the text from each article title and strip whitespace
            self.trending_topics = [article.text.strip() for article in articles]
            print("Trending topics found:", self.trending_topics)
            return self.trending_topics
        except requests.exceptions.RequestException as e:
            #  It Handles any errors during the request (e.g., network issues)
            print(f"Error fetching data: {e}")
            return []

    def gather_information(self, topic):
        # Placeholder method to gather information about a topic
        print(f"Gathering information for topic: {topic}")
        # Return placeholder data for the blog post
        return [
            f"Remote work is becoming increasingly popular in 2023, with companies adopting hybrid models to balance flexibility and collaboration.",
            f"Employee well-being is a top priority for HR departments, with a focus on mental health support and work-life balance."
        ]

# Content Planning Agent: Creates a structured outline for the blog post
class ContentPlanningAgent:
    def create_outline(self, topic, research_data):
        # Creating an outline for the blog post
        print("Creating outline for topic:", topic)
        outline = {
            "Title": f"Top Trends in {topic} for 2023",  # Blog title
            "Sections": [
                {"Heading": "Introduction", "Content": "Brief overview of the topic."},
                {"Heading": "Trend 1", "Content": research_data[0] if research_data else "No data available."},
                {"Heading": "Trend 2", "Content": research_data[1] if len(research_data) > 1 else "No data available."},
                {"Heading": "Conclusion", "Content": "Summary and future outlook."}
            ]
        }
        return outline

# Content Generation Agent: Writes the blog content using GPT-2
class ContentGenerationAgent:
    def __init__(self):
        # Load the GPT-2 model and tokenizer
        self.model_name = "gpt2"  # Model name
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)  # Tokenizer for GPT-2
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)  # GPT-2 model

    def generate_content(self, outline):
        # Generate blog content based on the outline
        blog_content = ""
        print("Generating content for outline...")
        for section in outline["Sections"]:
            # Creating a prompt for GPT-2 based on the section heading and content
            prompt = f"Write a detailed section for a blog post about HR trends. Heading: {section['Heading']}. Content: {section['Content']}"
            try:
                print(f"Generating section: {section['Heading']}")
                # Tokenize the prompt and convert it to PyTorch tensors
                inputs = self.tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
                # Generate text using GPT-2
                outputs = self.model.generate(inputs, max_length=500, num_return_sequences=1, no_repeat_ngram_size=2)
                # Decode the generated text and remove special tokens
                generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                # Append the generated text to the blog content
                blog_content += generated_text + "\n\n"
            except Exception as e:
                # Handle errors during content generation
                print(f"Error generating content: {e}")
                # Use fallback content if GPT-2 fails
                blog_content += f"<h2>{section['Heading']}</h2>\n<p>{section['Content']}</p>\n\n"
        return blog_content

# SEO Optimization Agent: Ensures content follows SEO best practices
class SEOOptimizationAgent:
    def optimize_content(self, content, keywords):
        # Optimize the blog content for SEO
        print("Optimizing content for SEO...")
        for keyword in keywords:
            # Add <strong> tags around keywords for SEO
            content = content.replace(keyword, f"<strong>{keyword}</strong>")
        
        # Ensure proper headings and subheadings
        content = content.replace("Trend 1", "<h2>Trend 1</h2>")
        content = content.replace("Trend 2", "<h2>Trend 2</h2>")
        
        return content

# Review Agent: Proofreads and improves content quality
class ReviewAgent:
    def __init__(self):
        # Ensure the required NLTK resources are downloaded
        nltk.download('punkt_tab')
        nltk.download('punkt')

    def proofread(self, content):
        # Proofread the content using NLTK
        print("Proofreading content...")
        # Split the content into sentences
        sentences = nltk.sent_tokenize(content)
        # Join the sentences back into a single string
        corrected_content = " ".join(sentences)
        return corrected_content

# Main System: Integrates all agents
class SEOBlogGenerator:
    def __init__(self):
        # Initialize all agents
        self.research_agent = ResearchAgent()
        self.planning_agent = ContentPlanningAgent()
        self.generation_agent = ContentGenerationAgent()
        self.seo_agent = SEOOptimizationAgent()
        self.review_agent = ReviewAgent()

    def generate_blog(self):
        # Step 1: Research trending topics
        print("Starting research...")
        topics = self.research_agent.search_trending_topics()
        if not topics:
            # If no topics are found, use a default topic
            print("No trending topics found. Using default topic: Remote Work")
            topics = ["Remote Work"]
        
        # Use the first topic for the blog post
        selected_topic = topics[0]
        print("Selected topic:", selected_topic)
        # Gather information about the selected topic
        research_data = self.research_agent.gather_information(selected_topic)
        
        # Step 2: Create an outline for the blog post
        print("Creating outline...")
        outline = self.planning_agent.create_outline(selected_topic, research_data)
        
        # Step 3: Generate the blog content
        print("Generating blog content...")
        blog_content = self.generation_agent.generate_content(outline)
        
        # Step 4: Optimize the content for SEO
        print("Optimizing content...")
        optimized_content = self.seo_agent.optimize_content(blog_content, ["HR trends", "2023"])
        
        # Step 5: Proofread the content
        print("Proofreading content...")
        final_content = self.review_agent.proofread(optimized_content)
        
        return final_content

# Run the System
if __name__ == "__main__":
    # Initialize the blog generator
    blog_generator = SEOBlogGenerator()
    
    # Generate the blog post
    print("Generating blog post...")
    blog_post = blog_generator.generate_blog()
    
    #  for Saving the blog post to a file with a hr_trends_blog.html
    output_file_name = "hr_trends_blog.html" 
    with open(output_file_name, "w", encoding="utf-8") as file:
        file.write(blog_post)
    
    print(f"Blog post generated and saved to '{output_file_name}'.")