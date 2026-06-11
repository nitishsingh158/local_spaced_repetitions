.PHONY: dev test

dev:
	cd frontend && npm install
	npx concurrently \
		"uv run uvicorn backend.main:app --reload" \
		"cd frontend && npm run dev"

test:
	uv run pytest backend/tests/ -v
