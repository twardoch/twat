#!/usr/bin/env python
# pyright: strict
"""
this_file: phiagentic.py

A simple web agent using phi.agent with GPT-4 and DuckDuckGo search.
"""

# uv pip install --upgrade --target="/Users/adam/Library/Application Support/FontLab/FontLab 8/python/3.11/site-packages" --python-version 3.11 --python-platform x86_64-apple-darwin --python cpython-3.11.11-macos-x86_64-none phidata openai duckduckgo-search

#!/usr/bin/env python
# pyright: strict
"""
this_file: phiagentic.py

A simple web agent using phi.agent with GPT-4 and DuckDuckGo search.
"""

import os

os.environ["OPENAI_API_KEY"] = ""

from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo

web_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGo()],
    instructions=["search in site:fontlabcom.github.io/fontlab-python-docs/"],
    show_tool_calls=True,
    markdown=True,
)
web_agent.print_response(
    "Write Python code that will create a simple PythonQt dialog box", stream=True
)
