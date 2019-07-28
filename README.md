# Inventory

An inventory manager built with Flask, MySQL, and Vue.js.

## Contents

- [Developing](#developing)
- [Brainstorm](#brainstorm)
- [Please Note](#please-note)



## Developing

There are a couple of ways you can build the project for development and testing;

- The Vue Dev Server. Quick, but you can only test the front-end, Flask is not serving the API.
- Docker containers. Slow and not automatic. But you can test front-end and API interactions.
- Docker and Python Server. A mix of both solutions. DB is in Docker, Python Server serves Flask and Vue.

### The Vue Dev Server

If you want to quickly see a stylistic change or you want to test a Vue component, navigate to server/ and run the command `npm run serve`. This starts Vue-CLI's hot-reloading dev server on localhost:8080. As mentioned above, **interactions with the API will fail as Flask is not running.**

### Docker Containers

There are two containers at the moment, one for the python server, and one for the database.

To build the containers, run:

    ./buildContainers.sh

To start containers

    ./start.sh

To restart just the server instead of restarting the server and the db

    ./restartServer.sh

To check logs:

    docker logs inventoryserver
    or
    docker logs inventorydb

If you want to access the db container from the server container, use the url

    inventorydb.inventory

If you want to access the server container from the db container, use the url

    inventoryserver.inventory

To install docker on Ubuntu:

    sudo apt-get update
    sudo apt-get install docker-ce
    sudo gpasswd -a <your user name here> docker

To access web server:

- Build and start the containers
- The web server should be accessible at localhost:1221
- The db should be accessible at localhost:3301

### Docker and Python Server

Workflow to come


## Brainstorm

<details>

As a user, after I login I want to see:

- dashboard of items
  - items sold,
  - items not sold yet (in inventory)
- link to "my items page" (paginated), sort by price
- "Add new items" button, opens modal(?) or page
  - also attach pictures


</details>


## Please Note

### package(-lock).json

`package.json` and `package-lock.json` are set to read-only and should only be committed while in read-only mode. If adding an npm package,

- Add the write bit to `package.json` using the command `chmod 644 package.json`
- Install your package with `npm install <package_name>`
- Return `package.json` to read-only with the command `chmod 444 package.json`

