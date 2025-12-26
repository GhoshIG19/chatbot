
from markdownify import markdownify as md
html = "<h1>Hello World</h1><a href='google.com'>Link</a>"

# Add heading_style="ATX" to get hashtags instead of underlines
print(md(html, heading_style="ATX"))