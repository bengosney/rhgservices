.PHONY: help clean test install all init dev css watch
.DEFAULT_GOAL := install
.PRECIOUS: requirements.%.in

HOOKS=$(.git/hooks/pre-commit)
INS=$(wildcard requirements.*.in)
REQS=$(subst in,txt,$(INS))

BINPATH=$(shell which python | xargs dirname | xargs realpath --relative-to=".")

PYTHON_VERSION:=$(shell python --version | cut -d " " -f 2)
PIP_PATH:=$(BINPATH)/pip
WHEEL_PATH:=$(BINPATH)/wheel
PIP_SYNC_PATH:=$(BINPATH)/pip-sync
PRE_COMMIT_PATH:=$(BINPATH)/pre-commit

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

requirements.%.in:
	echo "-c requirements.txt" > $@

requirements.in:
	@touch $@

requirements.%.txt: $(PIP_SYNC_PATH) requirements.%.in requirements.txt
	@echo "Builing $@"
	@python -m piptools compile -q -o $@ $(filter-out $<,$^)

requirements.txt: $(PIP_SYNC_PATH) requirements.in
	@echo "Builing $@"
	@python -m piptools compile -q $(filter-out $<,$^)

.direnv: .envrc
	python -m pip install --upgrade pip
	python -m pip install wheel pip-tools
	@touch $@ $^

.git/hooks/pre-commit: $(PRE_COMMIT_PATH) .pre-commit-config.yaml
	pre-commit install

.envrc:
	@echo "Setting up .envrc then stopping"
	@echo "layout python python3.10" > $@
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

init: .direnv $(PIP_SYNC_PATH) .git .git/hooks/pre-commit requirements.dev.txt ## Initalise a enviroment

clean: ## Remove all build files
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache
	rm -f .testmondata
	rm -rf .mypy_cache
	rm -rf .hypothesis

package-lock.json: package.json
	npm install

node_modules: package.json package-lock.json
	npm install
	@touch $@

node: node_modules

python: $(PIP_SYNC_PATH) requirements.txt $(REQS)
	@echo "Installing $(filter-out $<,$^)"
	@python -m piptools sync $(filter-out $<,$^)

install: python node ## Install development requirements (default)

_upgrade: requirements.in
	@echo "Upgrading pip packages"
	@python -m pip install --upgrade pip
	@python -m piptools compile -q --upgrade requirements.in

upgrade: _upgrade python
	@echo "Updateing module paths"
	wagtail updatemodulepaths --ignore-dir .direnv
	@python -m pre_commit autoupdate
	python -m pre_commit run --all

requirements.db.in:
	echo "-c requirements.txt\n-c $(REQS)\ndb-to-sqlite\npsycopg2" > requirements.db.in
	$(MAKE) python

db.sqlite3:	requirements.db.txt
	db-to-sqlite --all $(shell heroku config | grep DATABASE_URL | tr -s " " | cut -f 2 -d " ") $@

watch: ## Watch and build the css
	@echo "Watching scss"
	@while inotifywait -qr -e close_write scss/; do \
		$(MAKE) css; \
	done

bs: ## Run browser-sync
	browser-sync start --proxy localhost:8000 --files "./**/*.css" --files "./**/*.js" --files "./**/*.html"

css: ## Build the css
	npx gulp css

watch-css:
	inotifywait -m -r -e modify,create,delete ./scss/ | while read NEWFILE; do $(MAKE) css; done
