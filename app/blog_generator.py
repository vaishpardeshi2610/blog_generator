from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from config import Config

class BlogGenerator:
    def __init__(self):
        # Initialize the LLM
        self.llm = ChatGroq(
            temperature=Config.LLM_TEMPERATURE, 
            model=Config.LLM_MODEL
        )
        
        # Create the outline generation prompt
        self.outline_prompt = ChatPromptTemplate.from_template(
            """Create a detailed blog post outline for the topic: {topic}
            
            The outline should include:
            1. An engaging introduction.
            2. 1-2 main sections with relevant subsections.
            3. A strong conclusion.
            4. Keep it short, crisp and concise. Don't make it too large.
            
            Format the outline with clear hierarchical structure using proper numbering."""
        )
        
        # Create the content generation prompt
        self.content_prompt = ChatPromptTemplate.from_template(
            """Using the following outline, generate comprehensive blog content:
            
            {outline}
            
            Requirements:
            - Expand each section with detailed, well-researched information
            - Maintain a consistent and engaging writing style
            - Include relevant examples and explanations
            - Ensure smooth transitions between sections
            - Keep the content informative yet accessible"""
        )
        
        # Create the formatting prompt
        self.format_prompt = ChatPromptTemplate.from_template(
            """Format the following blog content using proper markdown styling:
            
            {content}
            
            Apply these formatting rules:
            - Use # for main title
            - Use ## for section headings
            - Use ### for subsection headings
            - Use **bold** for emphasis
            - Use *italic* for secondary emphasis
            - Use proper bullet points and numbered lists
            - Add block quotes where appropriate
            - Ensure proper paragraph spacing
            
            Make the content visually appealing and easy to read."""
        )
        
        # Set up the chain
        self.setup_chain()
    
    def setup_chain(self):
        # Create individual chains
        outline_chain = self.outline_prompt | self.llm | RunnableLambda(lambda x: x.content)
        content_chain = self.content_prompt | self.llm | RunnableLambda(lambda x: x.content)
        format_chain = self.format_prompt | self.llm | RunnableLambda(lambda x: x.content)
        
        # Create the main chain that processes everything sequentially
        self.main_chain = (
            RunnablePassthrough.assign(
                outline=lambda x: outline_chain.invoke({"topic": x["topic"]})
            )
            | RunnablePassthrough.assign(
                content=lambda x: content_chain.invoke({"outline": x["outline"]})
            )
            | RunnablePassthrough.assign(
                formatted_content=lambda x: format_chain.invoke({"content": x["content"]})
            )
        )
    
    def generate_blog(self, topic: str) -> dict:
        try:
            # Generate blog content using the chain
            result = self.main_chain.invoke({"topic": topic})
            
            return {
                "outline": result["outline"],
                "raw_content": result["content"],
                "formatted_content": result["formatted_content"]
            }
        except Exception as e:
            raise Exception(f"Blog generation failed: {str(e)}")