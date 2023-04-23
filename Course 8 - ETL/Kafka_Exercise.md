# get kafka
wget https://archive.apache.org/dist/kafka/2.8.0/kafka_2.12-2.8.0.tgz
tar -xzf kafka_2.12-2.8.0.tgz

# start zookeeper
cd kafka_2.12-2.8.0
bin/zookeeper-server-start.sh config/zookeeper.properties

# start broker service
cd kafka_2.12-2.8.0
bin/kafka-server-start.sh config/server.properties

#create topics
cd kafka_2.12-2.8.0
bin/kafka-topics.sh --create --topic news --bootstrap-server localhost:9092

# start producer on a topic and send messages
bin/kafka-console-producer.sh --topic news --bootstrap-server localhost:9092

# on '>'
Good morning
Good day
Enjoy the Kafka lab

# start consumer from the beginning, for a topic
cd kafka_2.12-2.8.0
bin/kafka-console-consumer.sh --topic news --from-beginning --bootstrap-server localhost:9092

# start with partitions
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic bankbranch  --partitions 2

# list all topics
bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

# describe a topic
bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic bankbranch

# start a producer for the partitioned topic
bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic bankbranch

# submit message after '>'
{"atmid": 1, "transid": 100}
{"atmid": 1, "transid": 101}
{"atmid": 2, "transid": 200}
{"atmid": 1, "transid": 102}
{"atmid": 2, "transid": 201}

# start consumer on partitioned topic
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bankbranch --from-beginning

# create keys to distinguish partitions
# --property parse.key=true to make the producer parse message keys
# --property key.separator=: define the key separator to be the : character,
bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic bankbranch --property parse.key=true --property key.separator=:

# submit a key-value pair-like message
1:{"atmid": 1, "transid": 100}
1:{"atmid": 1, "transid": 101}
2:{"atmid": 2, "transid": 200}
1:{"atmid": 1, "transid": 102}
1:{"atmid": 2, "transid": 201}

# start the consumer with key-value pair config
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bankbranch --from-beginning --property print.key=true --property key.separator=:

### OFFSET MODULE ###

# Start consumer groups
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bankbranch --group atm-app

# describe a group 
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group atm-app

# send a keyvalue
1:{"atmid": 1, "transid": 105}
2:{"atmid": 2, "transid": 204}

# start a consumer 
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bankbranch --group atm-app #notice the log-end and current offset

# reset offset
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092  --topic bankbranch --group atm-app --reset-offsets --to-earliest --execute

# start at 0, reconsume all consumed topics
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bankbranch --group atm-app

# start at a specific offset, Shift the offset to left by 2 using
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092  --topic bankbranch --group atm-app --reset-offsets --shift-by -2 --execute

# notice the difference
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bankbranch --group atm-app
