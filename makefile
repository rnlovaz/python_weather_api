PYTHON := python3
# venv folder name
VENV := venv
# venv activation command
ACTIVATE := source $(VENV)/bin/activate

setup: venv pip-install git-hooks

# Create venv if it doesn't exist
venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo ">>> Creating virtual environment in $(VENV)"; \
		$(PYTHON) -m venv $(VENV); \
	fi

# Clean venv completely
clean-venv:
	rm -rf $(VENV)

# Install dependencies into venv
pip-install: venv
	$(ACTIVATE) && pip install --upgrade pip
	$(ACTIVATE) && pip install -r requirements.txt
	$(ACTIVATE) && pip install pre-commit

# Setup git hooks with pre-commit package
git-hooks: venv
	$(ACTIVATE) && pre-commit install

# Remove docker containers
down:
	docker compose down

# Spin up docker containers (also removes leftovers and forces recreation)
up:
	docker compose up -d --build --force-recreate --remove-orphans

# Run mypy on src files
type-check:
	mypy src

# Create a new Alembic migration with a custom message
# Usage: make make-migration MSG="your message here"
make-migration:
	@if [ -z "$(MSG)" ]; then \
		echo "Please provide a message: make make-migration MSG=\"your message\""; \
		exit 1; \
	fi
	timestamp=$$(date +%Y_%m_%d_%H_%M); \
	alembic revision --autogenerate -m "$${timestamp}_$(MSG)"

# Apply all migrations (upgrade to head)
migrate:
	alembic upgrade head
