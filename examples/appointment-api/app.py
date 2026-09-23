"""A tiny in-memory appointment API for the blog article, not a production service."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock
from urllib.parse import urlparse


class AppointmentServer(ThreadingHTTPServer):
    def __init__(self, server_address):
        super().__init__(server_address, AppointmentHandler)
        self.lock = Lock()
        self.slots = {"slot-01": 1, "slot-02": 0}
        self.appointments = {}
        self.request_ids = {}


class AppointmentHandler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def respond(self, status, body):
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlparse(self.path).path
        if path.startswith("/slots/"):
            slot_id = path.removeprefix("/slots/")
            with self.server.lock:
                remaining = self.server.slots.get(slot_id)
            if remaining is None:
                return self.respond(404, {"error": "slot_not_found"})
            return self.respond(200, {"slotId": slot_id, "remaining": remaining})
        if path.startswith("/appointments/"):
            appointment_id = path.removeprefix("/appointments/")
            with self.server.lock:
                appointment = self.server.appointments.get(appointment_id)
            if appointment is None:
                return self.respond(404, {"error": "appointment_not_found"})
            return self.respond(200, appointment)
        return self.respond(404, {"error": "not_found"})

    def do_POST(self):
        if urlparse(self.path).path != "/appointments":
            return self.respond(404, {"error": "not_found"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 4096 or length <= 0:
                return self.respond(400, {"error": "invalid_body"})
            body = json.loads(self.rfile.read(length))
        except (ValueError, UnicodeDecodeError):
            return self.respond(400, {"error": "invalid_json"})
        if not isinstance(body, dict):
            return self.respond(400, {"error": "invalid_body"})
        fields = ("patientId", "slotId", "requestId")
        if any(not isinstance(body.get(key), str) or not body[key].strip() for key in fields):
            return self.respond(400, {"error": "missing_or_invalid_field"})

        fingerprint = (body["patientId"], body["slotId"])
        with self.server.lock:
            existing = self.server.request_ids.get(body["requestId"])
            if existing:
                old_fingerprint, appointment_id = existing
                if old_fingerprint != fingerprint:
                    return self.respond(409, {"error": "request_id_conflict"})
                return self.respond(200, self.server.appointments[appointment_id])
            remaining = self.server.slots.get(body["slotId"])
            if remaining is None:
                return self.respond(404, {"error": "slot_not_found"})
            if remaining == 0:
                return self.respond(409, {"error": "slot_unavailable"})
            appointment_id = f"appointment-{len(self.server.appointments) + 1:03d}"
            appointment = {
                "appointmentId": appointment_id,
                "patientId": body["patientId"],
                "slotId": body["slotId"],
                "status": "reserved",
            }
            self.server.appointments[appointment_id] = appointment
            self.server.request_ids[body["requestId"]] = (fingerprint, appointment_id)
            self.server.slots[body["slotId"]] -= 1
        return self.respond(201, appointment)


if __name__ == "__main__":
    server = AppointmentServer(("127.0.0.1", 8000))
    print("Demo API: http://127.0.0.1:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
