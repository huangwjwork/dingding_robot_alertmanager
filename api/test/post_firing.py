import requests
import json

api_url = 'http://localhost:8000'
json_data = {
    "receiver":
    "dev",
    "status":
    "firing",
    "alerts": [{
        "status":
        "firing",
        "labels": {
            "alertname": "InstanceDown",
            "instance": "test-exporter:10000",
            "job": "prometheus",
            "monitor": "codelab-monitor",
            "severity": "page"
        },
        "annotations": {
            "description":
            "test-exporter:10000 of job prometheus has been down for more than 5 minutes.",
            "summary": "Instance test-exporter:10000 down"
        },
        "startsAt":
        "2019-08-18T09:34:31.345816455Z",
        "endsAt":
        "0001-01-01T00:00:00Z",
        "generatorURL":
        "http://test-prometheus-58c75f5764-6rvjg:9090/graph?g0.expr=up+%3D%3D+0&g0.tab=1"
    }, {
        "status":
        "firing",
        "labels": {
            "alertname": "InstanceDown",
            "instance": "test-exporter:999",
            "job": "prometheus",
            "monitor": "codelab-monitor",
            "severity": "page"
        },
        "annotations": {
            "description":
            "test-exporter:999 of job prometheus has been down for more than 5 minutes.",
            "summary": "Instance test-exporter:999 down"
        },
        "startsAt":
        "2019-08-18T09:34:31.345816455Z",
        "endsAt":
        "0001-01-01T00:00:00Z",
        "generatorURL":
        "http://test-prometheus-58c75f5764-6rvjg:9090/graph?g0.expr=up+%3D%3D+0&g0.tab=1"
    }],
    "groupLabels": {
        "alertname": "InstanceDown"
    },
    "commonLabels": {
        "alertname": "InstanceDown",
        "instance": "test-exporter:10000",
        "job": "prometheus",
        "monitor": "codelab-monitor",
        "severity": "page"
    },
    "commonAnnotations": {
        "description":
        "test-exporter:10000 of job prometheus has been down for more than 5 minutes.",
        "summary": "Instance test-exporter:10000 down"
    },
    "externalURL":
    "http://test-prometheus-58c75f5764-6rvjg:9093",
    "version":
    "4",
    "groupKey":
    "{}/{severity=\"page\"}:{alertname=\"InstanceDown\"}"
}

headers = {'Content-Type': 'application/json'}
a = requests.post(url=api_url, data=json.dumps(json_data), headers=headers)
# print(m)
print(a.text)
print(a)
