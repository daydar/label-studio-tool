# Label Studio
A Python package for creating images from the pages of a pdf and for cropping images based on label coordinates.

Label Studio is also used as a container to generate the coordinates for the cropping.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (installed automatically by `make setup`)
- Docker (for containerized deployment and local dependencies)


### Local Development
```bash
# Install uv and dependencies
make setup

# Start label studio
make docker-compose-up

# Stop label studio
make docker-compose-down

# Create pages from all pdf in pdfs/ and save the pages in pages_images/
make create-pages

# Crop pages based on the 'file_upload' field from the generated json export from label studio web interface.
# Be aware that the uploaded page should therefore have the same name as the generated page so that the script can match them.
make crop-pages

# Run service
make run
```

### Workflow

1. The requested pdf are first used to generate the pages with the create script.
2. The generated pages are then uploaded to label studio.
3. The pages are then labeled in label studio and exported.
4. The exported json is then placed in the coordinates folder.
5. The crop script is then run with the exported json.
6. The generated results are then placed in the crops folder.
