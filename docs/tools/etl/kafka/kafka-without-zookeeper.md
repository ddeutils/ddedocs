# Without Zookeeper

!!! note

    **Kafka 3.3** introduced ==**KRaft**== for creating clusters without needing
    to create **Zookeeper**.[^1]

## Getting Started

### Why does Kafka depend on Zookeeper?

Kafka uses Zookeeper as a Service Discovery tool, meaning each Kafka node that
wants to find other nodes needs to discover their addresses and status through
service discovery.
Kafka also uses Zookeeper for other purposes such as Leader Election, Broker Discovery,
Configuration Management, and Health Monitoring.

### What is KRaft?

**KRaft** is a new algorithm developed by Kafka based on the Raft Consensus algorithm,
which is suitable for achieving consensus between trusted parties.
Kafka no longer needs Zookeeper because it can achieve its goals using the Raft
consensus algorithm

---

## Deploy with Docker Compose

```yaml title="docker-compose.yml"
version: '3'
services:

  kafka-1:
    image: 'bitnami/kafka:3.3.1'
    container_name: kafka-1
    environment:
      - KAFKA_ENABLE_KRAFT=yes
      - KAFKA_CFG_PROCESS_ROLES=broker,controller
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9094
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      - KAFKA_CFG_BROKER_ID=1
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=1@kafka-1:9094,2@kafka-2:9094,3@kafka-3:9094
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka-1:9092
      - ALLOW_PLAINTEXT_LISTENER=yes
      - KAFKA_KRAFT_CLUSTER_ID=r4zt_wrqTRuT7W2NJsB_GA
    ports:
      - 9192:9092

  kafka-2:
    image: 'bitnami/kafka:3.3.1'
    container_name: kafka-2
    environment:
      - KAFKA_ENABLE_KRAFT=yes
      - KAFKA_CFG_PROCESS_ROLES=broker,controller
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9094
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      - KAFKA_CFG_BROKER_ID=2
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=1@kafka-1:9094,2@kafka-2:9094,3@kafka-3:9094
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka-2:9092
      - ALLOW_PLAINTEXT_LISTENER=yes
      - KAFKA_KRAFT_CLUSTER_ID=r4zt_wrqTRuT7W2NJsB_GA
    ports:
      - 9292:9092

  kafka-3:
    image: 'bitnami/kafka:3.3.1'
    container_name: kafka-3
    environment:
      - KAFKA_ENABLE_KRAFT=yes
      - KAFKA_CFG_PROCESS_ROLES=broker,controller
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9094
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      - KAFKA_CFG_BROKER_ID=3
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=1@kafka-1:9094,2@kafka-2:9094,3@kafka-3:9094
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka-3:9092
      - ALLOW_PLAINTEXT_LISTENER=yes
      - KAFKA_KRAFT_CLUSTER_ID=r4zt_wrqTRuT7W2NJsB_GA
    ports:
      - 9392:9092

  kafka-ui:
    container_name: kafka-ui
    image: 'provectuslabs/kafka-ui:latest'
    ports:
      - "8080:8080"
    environment:
      - KAFKA_CLUSTERS_0_BOOTSTRAP_SERVERS=kafka-1:9092
      - KAFKA_CLUSTERS_0_NAME=r4zt_wrqTRuT7W2NJsB_GA
```

**Running Command**:

```shell
docker-compose -f docker-compose.yaml up -d
```

---

## Deploy using Helm Chart

```yaml title="helmfile.yaml"
repositories:
  - name: kafka-repo
    url: registry-1.docker.io/bitnamicharts
    oci: true

releases:
  - name: kafka
    namespace: test
    createNamespace: false
    chart: kafka-repo/kafka
    version: 26.8.3
    values:
      - ./values.yaml
```

**Running Command**:

```shell
$ helmfile apply -f helmfile.yaml
$ kubectl -n test get service
NAME                        TYPE        CLUSTER-IP        EXTERNAL-IP   PORT(S)                      AGE
kafka                       ClusterIP   10.43.54.217      <none>        9092/TCP                     3d4h
kafka-controller-headless   ClusterIP   None              <none>        9094/TCP,9092/TCP,9093/TCP   3d4h
```

!!! note

    You can use the following information within your application to connect to
    the Kafka cluster above:

    ```text
    spring.kafka.bootstrap-servers=kafka:9092
    spring.kafka.properties.security.protocol=SASL_PLAINTEXT
    spring.kafka.properties.sasl.mechanism=PLAIN
    spring.kafka.properties.sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="user1" password="xxxxxxx";
    ```

    you can find the password of user1 using the following command:

    ```shell
    kubectl -n test edit secrets kafka-user-passwords
    ```

    and here’s the password:

    ```text
    apiVersion: v1
    data:
      client-passwords: Nk5xWTRLNGJKWA==              <==== password of user1
      controller-password: TjRmeTRFRmlCcQ==
      inter-broker-password: OTJzZWx0SUYwSQ==
      system-user-password: Nk5xWTRLNGJKWA==
    kind: Secret
    ```

    decode using base64

    ```shell
    $ echo "Nk5xWTRLNGJKWA==" | base64 -d
    6NqY4K4bJX
    ```

[^1]: [Kafka cluster without Zookeeper](https://itnext.io/kafka-cluster-without-zookeeper-ca40d5f22304)
