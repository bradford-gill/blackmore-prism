# blackmore-prism
Experimenting with web-scraping &amp; computer use to collect colorful data from the web 

## Required Reading
[Anthropic Computer Use Beta Docs](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/computer-use-tool#claude-4-models)

## Env Set Up

```bash
# Install uv (if needed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Set up environment and install dependencies (if needed)
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Add new dependencies
uv pip install <package_name> && uv pip freeze > requirements.txt

# Create .env with ANTHROPIC_API_KEY=...
# source needed env vars
export $(cat .env | xargs)
```