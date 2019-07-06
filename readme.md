# Inventory Backend

The backend of an inventory manager built with Flask and MySQL.

## Architectural Overview

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
