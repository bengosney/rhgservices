.PHONY: help clean test install all init dev css watch DBTOSQLPATH assets js node
.DEFAULT_GOAL := install
.PRECIOUS: requirements.%.in

MAKEFLAGS += -j4

HOOKS=$(.git/hooks/pre-commit)
REQS=$(shell python -c 'import tomllib;[print(f"requirements.{k}.txt") for k in tomllib.load(open("pyproject.toml", "rb"))["project"]["optional-dependencies"].keys()]')

BINPATH=$(shell which python | xargs dirname | xargs realpath --relative-to=".")

PYTHON_VERSION:=$(shell cat .python-version)
PIP_PATH:=$(BINPATH)/pip
WHEEL_PATH:=$(BINPATH)/wheel
UV_PATH:=$(BINPATH)/uv
PRE_COMMIT_PATH:=$(BINPATH)/pre-commit
DBTOSQLPATH:=$(BINPATH)/db-to-sqlite

PYTHON_FILES:=$(wildcard ./**/*.py ./**/tests/*.py)

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.gitignore:
	curl -q "https://www.toptal.com/developers/gitignore/api/visualstudiocode,python,direnv" > $@

.git: .gitignore
	git init

.pre-commit-config.yaml:
	curl https://gist.githubusercontent.com/bengosney/4b1f1ab7012380f7e9b9d1d668626143/raw/060fd68f4c7dec75e8481e5f5a4232296282779d/.pre-commit-config.yaml > $@
	python -m pip install pre-commit
	pre-commit autoupdate

requirements.%.txt: $(UV_PATH) pyproject.toml
	@echo "Builing $@"
	python -m uv pip compile --generate-hashes --extra $* $(filter-out $<,$^) > $@

requirements.txt: $(UV_PATH) pyproject.toml
	@echo "Builing $@"
	python -m uv pip compile --generate-hashes $(filter-out $<,$^) > $@

.direnv: .envrc
	python -m pip install --upgrade pip
	python -m pip install wheel pip-tools
	@touch $@ $^

.git/hooks/pre-commit: $(PRE_COMMIT_PATH) .pre-commit-config.yaml
	pre-commit install

.envrc: .python-version
	@echo "Setting up .envrc then stopping"
	@echo "layout python python$(PYTHON_VERSION)" > $@
	@touch -d '+1 minute' $@
	@false

$(PIP_PATH):
	@python -m ensurepip
	@python -m pip install --upgrade pip
	@touch $@

$(WHEEL_PATH): $(PIP_PATH)
	python -m pip install wheel
	@touch $@

$(PIP_SYNC_PATH): $(PIP_PATH) $(WHEEL_PATH)
	python -m pip install pip-tools
	@touch $@

$(PRE_COMMIT_PATH): $(PIP_PATH) $(WHEEL_PATH)
	python -m pip install pre-commit
	@touch $@

$(UV_PATH): $(PIP_PATH) $(WHEEL_PATH)
	python -m pip install uv
	@touch $@

init: .direnv $(UV_PATH) .git .git/hooks/pre-commit requirements.dev.txt ## Initalise a enviroment

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
	@python -m uv pip sync $(filter-out $<,$^)

pip: $(PIP_PATH) ## Update pip
	@python -m pip install --upgrade pip

install: python node ## Install development requirements (default)

upgrade: python
	@echo "Updateing module paths"
	wagtail updatemodulepaths --ignore-dir .direnv
	@python -m pre_commit autoupdate
	python -m pre_commit run --all

$(DBTOSQLPATH):
	pip install git+https://github.com/bengosney/db-to-sqlite.git

db.sqlite3: $(DBTOSQLPATH)
	db-to-sqlite --all $(shell heroku config | grep DATABASE_URL | tr -s " " | cut -f 2 -d " ") $@
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
