.PHONY := install, help, init, pre-init, css, pip
.DEFAULT_GOAL := install

HOOKS=$(.git/hooks/pre-commit)
INS=$(wildcard requirements.*.in)
REQS=$(subst in,txt,$(INS))

SCSS_PARTIALS=$(wildcard scss/_*.scss)
SCSS=$(filter-out scss/_%.scss,$(wildcard scss/*.scss))
CSS=rhgs/static/$(subst scss,css,$(SCSS))

BINPATH=$(shell which python | xargs dirname | xargs realpath --relative-to=".")
DBTOSQLPATH="$(BINPATH)/db-to-sqlite"

HEROKU_APP_NAME=rhgs

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

node_modules: package-lock.json ## Install node modules
	npm install
	touch $@

rhgs/static/css/%.css: scss/%.scss $(SCSS_PARTIALS)
	sass $< $@

css: ## Build the css
	npx gulp css

watch-css:
	inotifywait -m -r -e modify,create,delete ./scss/ | while read NEWFILE; do $(MAKE) css; done

.envrc: runtime.txt
	@echo layout python $(shell cat $^ | tr -d "-" | egrep -o "python[0-9]\.[0-9]+") > $@
	@echo export DATABASE_URL="postgres://$(DB_USER):$(DB_PASS)@localhost:5432/$(DB_NAME)" >> $@
	@echo "Created .envrc, run make again"
	@touch requirements.in
	@touch $(INS)
	direnv exec . make init
	@false

requirements.%.txt: requirements.%.in requirements.txt
	@echo "Builing $@"
	@python -m piptools compile -q -o $@ $<
	@touch $@

requirements.txt: requirements.in
	@echo "Builing $@"
	@python -m piptools compile -q $^

pip: requirements.txt $(REQS) ## Install development requirements
	@echo "Installing $^"
	@python -m piptools sync $^

_update: requirements.in
	@echo "Updating $^"
	@python -m piptools compile --upgrade $^

update: _update pip

install: pip node_modules

$(HOOKS):
	pre-commit install

pre-init:
	pip install --upgrade pip
	pip install wheel pip-tools

init: .envrc pre-init install $(HOOKS) ## Initalise a dev enviroment
	@which direnv > /dev/null || echo "direnv not found but recommended"
	@echo "Read to dev"

latest.dump:
	@echo "Dumping database"
	heroku pg:backups:capture --app $(HEROKU_APP_NAME)
	heroku pg:backups:download --app $(HEROKU_APP_NAME)

restoredb:
	rm -f db.sqlite3
	$(MAKE) db.sqlite3

$(DBTOSQLPATH):
	pip install 'db-to-sqlite[postgresql]'

db.sqlite3: $(DBTOSQLPATH)
	db-to-sqlite $(shell heroku config | grep DATABASE_URL | tr -s " " | cut -d " " -f 2) $@ --all -p

clean:
	rm -f latest.dump
	rm -rf css/*
