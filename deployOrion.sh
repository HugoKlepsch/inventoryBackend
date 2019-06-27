#!/bin/bash

echo "Pushing db"

docker save inventorydb:latest | \
  bzip2 | \
  ssh hugo@blog.hugo-klepsch.tech 'bunzip2 | docker load'

echo "done"

echo "Pushing server"

docker save inventoryserver:latest | \
  bzip2 | \
  ssh hugo@blog.hugo-klepsch.tech 'bunzip2 | docker load'

echo "done"

echo "Push start.sh"
cat start.sh | \
  bzip2 | \
  ssh hugo@blog.hugo-klepsch.tech \
    'bunzip2 > /home/hugo/inventory/start.sh && chmod u+x /home/hugo/inventory/start.sh'

echo "done"

echo "Push stop.sh"
cat stop.sh | \
  bzip2 | \
  ssh hugo@blog.hugo-klepsch.tech \
    'bunzip2 > /home/hugo/inventory/stop.sh && chmod u+x /home/hugo/inventory/stop.sh'

echo "done"
