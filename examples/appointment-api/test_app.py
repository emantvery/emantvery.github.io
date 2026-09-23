"""Runnable contract tests for the intentionally simplified demo API."""

from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import pytest
import requests

from app import AppointmentServer

TIMEOUT = 2


@pytest.fixture
def base_url():
    server = AppointmentServer(("127.0.0.1", 0))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=TIMEOUT)


def post(base_url, payload):
    return requests.post(f"{base_url}/appointments", json=payload, timeout=TIMEOUT)


def payload(request_id="req-1", slot_id="slot-01", patient_id="patient-01"):
    return {"patientId": patient_id, "slotId": slot_id, "requestId": request_id}


def test_create_appointment_updates_slot_and_can_be_queried(base_url):
    response = post(base_url, payload())
    assert response.status_code == 201
    appointment_id = response.json()["appointmentId"]
    assert response.json()["status"] == "reserved"

    saved = requests.get(f"{base_url}/appointments/{appointment_id}", timeout=TIMEOUT)
    slot = requests.get(f"{base_url}/slots/slot-01", timeout=TIMEOUT)
    assert saved.status_code == 200
    assert saved.json() == response.json()
    assert slot.json()["remaining"] == 0


@pytest.mark.parametrize("field", ["patientId", "slotId", "requestId"])
def test_missing_required_field_does_not_take_slot(base_url, field):
    invalid = payload()
    del invalid[field]
    response = post(base_url, invalid)
    assert response.status_code == 400
    assert response.json()["error"] == "missing_or_invalid_field"
    slot = requests.get(f"{base_url}/slots/slot-01", timeout=TIMEOUT)
    assert slot.json()["remaining"] == 1


def test_same_request_id_returns_original_appointment(base_url):
    first = post(base_url, payload())
    second = post(base_url, payload())
    assert first.status_code == 201
    assert second.status_code == 200
    assert second.json()["appointmentId"] == first.json()["appointmentId"]
    slot = requests.get(f"{base_url}/slots/slot-01", timeout=TIMEOUT)
    assert slot.json()["remaining"] == 0


def test_reused_request_id_with_changed_body_is_rejected(base_url):
    assert post(base_url, payload()).status_code == 201
    changed = post(base_url, payload(patient_id="patient-02"))
    assert changed.status_code == 409
    assert changed.json()["error"] == "request_id_conflict"


def test_exhausted_slot_is_rejected(base_url):
    response = post(base_url, payload(slot_id="slot-02"))
    assert response.status_code == 409
    assert response.json()["error"] == "slot_unavailable"


def test_concurrent_requests_cannot_overbook_one_slot(base_url):
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda i: post(base_url, payload(request_id=f"req-{i}")), (1, 2)))
    assert sorted(result.status_code for result in results) == [201, 409]
    slot = requests.get(f"{base_url}/slots/slot-01", timeout=TIMEOUT)
    assert slot.json()["remaining"] == 0
