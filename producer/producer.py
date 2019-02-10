import random
import time

import confluent_kafka
import scipy.stats

num_clusters = 2
means = [[3, 3], [-3, -3]]

p = confluent_kafka.Producer({"bootstrap.servers": "localhost:9092"})

while True:
    component = random.randrange(num_clusters)
    obs = scipy.stats.multivariate_normal(means[component]).rvs()
    p.produce("datastream", obs.tobytes())
    p.flush()
    time.sleep(5)
