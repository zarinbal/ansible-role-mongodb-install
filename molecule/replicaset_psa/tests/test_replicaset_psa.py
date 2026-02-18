import json
import time


def _get_rs_status(host, retries=20, delay=3):
    for _ in range(retries):
        result = host.run('mongosh --quiet --eval "JSON.stringify(rs.status())"')
        if result.rc == 0 and result.stdout.strip():
            try:
                return json.loads(result.stdout.strip())
            except json.JSONDecodeError:
                pass
        time.sleep(delay)
    raise AssertionError("replica set status did not become available in time")


def test_psa_cluster_shape(host):
    status = _get_rs_status(host)
    assert status["set"] == "rs0"

    members = status.get("members", [])
    names = sorted(member["name"] for member in members)
    assert names == ["mongo1:27017", "mongo2:27017", "mongo3:27017"]
    assert sum(1 for member in members if member.get("arbiterOnly", False)) == 1


def test_psa_has_primary_secondary_arbiter(host):
    status = _get_rs_status(host)
    members = status.get("members", [])
    states = [member.get("stateStr") for member in members]
    assert "PRIMARY" in states
    assert "SECONDARY" in states
    assert "ARBITER" in states
