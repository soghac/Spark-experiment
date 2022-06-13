import datetime
import os
import re
import time

containers_name = [
    "bitnami-docker-spark_spark-master_1",
    "bitnami-docker-spark_spark-worker-1_1",
    "bitnami-docker-spark_spark-worker-2_1",
    "bitnami-docker-spark_spark-worker-3_1",
    "bitnami-docker-spark_spark-worker-4_1"
]


def toBytes(transform):
    r = re.compile("([-+]?\d*\.\d+|\d+)([a-zA-Z]+)")
    match = r.match(transform)

    if match:
        value = match.group(1)
        unit = match.group(2)
        unit = unit.lower()
        if value is None:
            return 0
        if unit == "kb":
            return float(value) * 1000
        if unit == "mb":
            return float(value) * 1000000
        if unit == "gb":
            return float(value) * 1000000
        if unit == 'b':
            return float(value)
    else:
        raise Exception("error formation %s", transform)


with open('stats2.csv', 'w') as f:
    f.write('user_count,name,time,cpu_percent,memory_percent,net_i,net_o,block_i,block_o\n')
    while True:
        time.sleep(10)
        user_count = '0'
        with open('user_count.txt', 'r') as user_count_file:
            user_count = user_count_file.read()
        with os.popen("docker stats --no-stream") as docker_stats:
            for s in docker_stats.readlines()[1:]:
                ss = s.split()
                if len(ss) >= 3 and ('worker' in ss[1] or 'master' in ss[1]):
                    data = dict()
                    data['user_count'] = user_count
                    name = ss[1]
                    data["name"] = name
                    data["time"] = str(datetime.datetime.now().time()).split('.')[0]
                    cpu = round(float(ss[2].replace("%", "")), 2)
                    data['cpu_percent'] = str(cpu)
                    mem = round(float(ss[6].replace("%", "")), 2)
                    data["memory_percent"] = str(mem)
                    net_i = toBytes(ss[7])
                    net_o = toBytes(ss[9])
                    data['net_o'] = str(net_o)
                    data['net_i'] = str(net_i)
                    block_i = toBytes(ss[10])
                    block_o = toBytes(ss[12])
                    data['block_o'] = str(block_o)
                    data['block_i'] = str(block_i)
                    print(
                        "INFO: container %s: cpu %.2f%%, mem %.2f%%, net_i %d B, net_o %d B, block_i %d B, block_o %d B" % (
                            name, cpu, mem, net_i, net_o, block_i, block_o
                        )
                    )
                    f.write(str(','.join(data.values())) + '\n')
                    f.flush()
