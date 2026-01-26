install-uv: ## Install uv package manager
	@command -v uv >/dev/null 2>&1 || { echo "Installing uv..."; curl -LsSf https://astral.sh/uv/install.sh | sh; }

setup: install-uv ## Set up local development environment
	@uv sync --all-extras

docker-compose-up:
	docker compose up -d

docker-compose-down:
	docker compose down

create-pages:
	uv run python create_page_image_from_pdf.py

crop-pages:
	uv run python crop_images_by_label_coordinates.py

create-and-crop-pages:
	uv run python create_page_image_from_pdf.py
	uv run python crop_images_by_label_coordinates.py