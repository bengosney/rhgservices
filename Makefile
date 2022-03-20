.PHONY := install, help, init, pre-init, css
.DEFAULT_GOAL := install

HOOKS=$(.git/hooks/pre-commit)
INS=$(wildcard requirements.*.in)
REQS=$(subst in,txt,$(INS))

SCSS_PARTIALS=$(wildcard scss/_*.scss)
SCSS=$(filter-out scss/_%.scss,$(wildcard scss/*.scss))
CSS=$(subst scss,css,$(SCSS))

HEROKU_APP_NAME=rhgs
DB_USER=rhgs
DB_PASS=rhgs
DB_NAME=rhgs
DB_CONTAINER_NAME=rhgs-postgres

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

node_modules: package-lock.json ## Install node modules
	npm install
	touch $@

static/css/%.css: scss/%.scss $(SCSS_PARTIALS)
	sass $< $@

css: ##$(CSS)
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
	@pip-compile --generate-hashes -q -o $@ $<
	@touch $@

requirements.txt: requirements.in
	@echo "Builing $@"
	@pip-compile --generate-hashes -q $^

install: requirements.txt $(REQS) ## Install development requirements
	@echo "Installing $^"
	@pip-sync $^

$(HOOKS):
	pre-commit install

pre-init:
	pip install --upgrade pip
	pip install wheel pip-tools

init: .envrc pre-init install $(HOOKS) ## Initalise a dev enviroment
	@which direnv > /dev/null || echo "direnv not found but recommended"
	@echo "Read to dev"

postgres-down:
	@echo "Stopping any excisting postgres containers"
	@docker stop $(DB_CONTAINER_NAME) || true
	@docker rm $(DB_CONTAINER_NAME) || true

postgres: postgres-down
	docker run --name $(DB_CONTAINER_NAME) -p 5432:5432 -e POSTGRES_PASSWORD=$(DB_PASS) -e POSTGRES_USER=$(DB_USER) -d postgres

latest.dump:
	@echo "Dumping database"
	heroku pg:backups:capture --app $(HEROKU_APP_NAME)
	heroku pg:backups:download --app $(HEROKU_APP_NAME)

restoredb: latest.dump
	@echo "Restoring database"
	docker exec -i $(DB_CONTAINER_NAME) /bin/bash -c "pg_restore --verbose --clean --no-acl --no-owner -h localhost -U $(DB_USER) -d $(DB_NAME)" < $?

clean:
	rm -f latest.dump
	rm -rf css/*
