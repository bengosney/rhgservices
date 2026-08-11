.PHONY: help clean install init python pip upgrade node cog css js assets watch-css watch-js dev bs _server infrastructure
.DEFAULT_GOAL := install
.PRECIOUS: requirements.%.in

REQS:=$(shell python3 -c 'import tomllib;[print(f"requirements.{k}.txt") for k in tomllib.load(open("pyproject.toml", "rb"))["project"]["optional-dependencies"].keys()]')

BINPATH=.venv

PYTHON_VERSION:=$(shell cat .python-version)
PIP_PATH:=$(BINPATH)/pip
UV_PATH:=$(shell command -v uv 2>/dev/null || echo "$$HOME/.local/bin/uv")
COG_CMD:=$(UV_PATH) tool run --from cogapp cog
PREK_CMD:=$(UV_PATH) tool run prek

COGABLE:=$(shell git ls-files | xargs grep -l "\[\[\[cog")
PYTHON_FILES:=$(shell git ls-files '*.py')

help: ## Display this help
	@grep -E '^[a-zA-Z0-9_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.gitignore:
	curl -q "https://www.toptal.com/developers/gitignore/api/visualstudiocode,python,direnv" > $@

.git: .gitignore
	git init

.pre-commit-config.yaml:
	curl https://gist.githubusercontent.com/bengosney/4b1f1ab7012380f7e9b9d1d668626143/raw/060fd68f4c7dec75e8481e5f5a4232296282779d/.pre-commit-config.yaml > $@
	$(PREK_CMD) autoupdate

requirements.%.txt: $(UV_PATH) pyproject.toml
	@echo "Building $@"
	$(UV_PATH) pip compile --generate-hashes --extra $* $(filter-out $<,$^) > $@

requirements.txt: $(UV_PATH) pyproject.toml
	@echo "Building $@"
	$(UV_PATH) pip compile --generate-hashes $(filter-out $<,$^) > $@

$(UV_PATH):
	@echo "Error: uv is not installed. Install it from https://github.com/astral-sh/uv" && false

.venv: | $(UV_PATH) .envrc
	$(UV_PATH) venv --managed-python --python $(PYTHON_VERSION)
	@touch $@

.git/hooks/pre-commit: $(UV_PATH) .pre-commit-config.yaml
	$(PREK_CMD) install

.envrc:
	@echo "Setting up .envrc then stopping"
	@echo 'if [ ! -d .venv ]; then' > $@
	@echo '    make .venv' >> $@
	@echo 'fi' >> $@
	@echo '' >> $@
	@echo 'PATH_add ".venv/bin"' >> $@
	@echo 'export VIRTUAL_ENV="$$PWD/.venv"' >> $@
	@echo 'export VIRTUAL_ENV_PROMPT="$$(basename $$PWD)"' >> $@
	@echo 'watch_file .venv' >> $@
	@touch -d '+1 minute' $@
	@false

$(PIP_PATH):
	@python -m ensurepip
	@python -m pip install --upgrade pip
	@touch $@

init: .envrc $(UV_PATH) .git .git/hooks/pre-commit requirements.dev.txt ## Initialise an environment

clean: ## Remove all build files
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache .testmondata .mypy_cache .hypothesis

package-lock.json: package.json
	npm install

node_modules: package.json package-lock.json
	npm install
	@touch $@

node: node_modules

python: $(UV_PATH) requirements.txt $(REQS)
	@echo "Installing $(filter-out $<,$^)"
	@$(UV_PATH) pip sync $(filter-out $<,$^)

pip: $(PIP_PATH) ## Update pip
	@python -m pip install --upgrade pip

install: python node ## Install development requirements (default)

upgrade: python
	@echo "Updating module paths"
	wagtail updatemodulepaths --ignore-dir .direnv
	@$(PREK_CMD) autoupdate || true
	$(PREK_CMD) run --all-files

cog: $(UV_PATH) $(COGABLE)
	@$(COG_CMD) -rc $(filter-out $<,$^)

# Requires HEROKU_APP to be set, e.g. `make db.sqlite3 HEROKU_APP=my-app`
db.sqlite3: ## Import database from heroku
	@echo "Importing database"
	@$(UV_PATH) tool run --from "db-to-sqlite[postgresql]" db-to-sqlite --all $(shell heroku config --app $(HEROKU_APP) | grep DATABASE_URL | tr -s " " | cut -f 2 -d " ") $@
	@echo "Clearing image renditions"
	@python manage.py clear_renditions

bs: ## Run browser-sync
	browser-sync start --proxy localhost:8000 --files "./rhgs/static/css/*.css" --files "./rhgs/static/js/*.js" --files "./**/*.html"

SCSS=$(shell find scss/ -name "*.scss")

rhgs/static/css/%.css: scss/%.scss $(SCSS)
	npx sass $< $@

rhgs/static/css/%.min.css: rhgs/static/css/%.css
	npx postcss $^ -o $@

css: rhgs/static/css/rhgs.min.css ## Build the css

JS_SRC = $(wildcard js/*.ts)
JS_LIB = $(JS_SRC:js/%.ts=rhgs/static/js/%.js)

rhgs/static/js/: $(JS_LIB)
rhgs/static/js/%.js: js/%.ts $(JS_SRC)
	@mkdir -p $(@D)
	npx parcel build $< --dist-dir $(@D)

js: rhgs/static/js/rhgs.js

watch-css: ## Watch and build the css
	@echo "Watching scss"
	$(MAKE) css
	@while inotifywait -qr -e close_write scss/; do \
		$(MAKE) css; \
	done

watch-js: ## Watch and build the js
	@echo "Watching js"
	$(MAKE) js
	@while inotifywait -qr -e close_write js/; do \
		$(MAKE) js; \
	done

assets: js css ## Build assets

cov.xml: $(PYTHON_FILES)
	python3 -m pytest --cov=. --cov-report xml:$@

coverage: $(PYTHON_FILES)
	python3 -m pytest --cov=. --cov-report html:$@

_server:
	python3 ./manage.py migrate
	python3 ./manage.py runserver

dev: _server watch-js watch-css bs ## Start the dev server, watch the css and js and start browsersync

infrastructure:
	git clone https://github.com/bengosney/tofu-wagtail.git $@
	cd $@ && $(MAKE) init
