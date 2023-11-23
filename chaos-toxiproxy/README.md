download redis

toxiproxy-server -config toxiproxy.json

toxiproxy-cli toxic update --toxicName latency_downstream -a latency=3000,jitter=800 redis-stack

toxiproxy-cli t remove --toxicName latency_downstream redis-stack

Пример гипотезы, что будет если увеличиваем таймауты
