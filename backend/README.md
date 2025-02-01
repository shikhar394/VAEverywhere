# Backend

## Setup
Download uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install dependencies
```bash
uv sync
```

Run the server
```bash
uv run uvicorn main:app --reload
```

