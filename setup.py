from setuptools import setup, find_packages

setup(
    name="ai_agent_zork",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langgraph>=0.0.15",
        "langchain>=0.0.267",
        "langchain-openai>=0.0.2",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "jericho": ["jericho>=3.0.0"],
    },
    python_requires=">=3.8",
    description="An AI agent that plays the classic text adventure game Zork",
    author="AI Agent Zork Team",
)
