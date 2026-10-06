"""MCP Server for Agentic Shipment Delivery Rescheduler."""
import sys
import json
import time
from client import AgenticShipmentDeliveryRescheduler

rescheduler = AgenticShipmentDeliveryRescheduler()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "reschedule_shipment_delivery":
        raise ValueError(f"Unknown tool: {name}")

    action = args.get("action", "compute_reschedule_options")
    if action == "parse_carrier_event":
        return rescheduler.parse_carrier_event(
            carrier=args.get("carrier", "FEDEX"),
            tracking_number=args.get("tracking_number", "123456"),
            raw_status=args.get("raw_status", "In transit"),
            location=args.get("location")
        )
    elif action == "diagnose_exception":
        event = rescheduler.parse_carrier_event(
            carrier=args.get("carrier", "FEDEX"),
            tracking_number=args.get("tracking_number", "123456"),
            raw_status=args.get("raw_status", "Attempted delivery - customer not available")
        )
        return {"has_exception": event["has_exception"], "exception_code": event["exception_code"]}
    elif action == "compute_reschedule_options":
        return rescheduler.compute_reschedule_options(
            tracking_number=args.get("tracking_number", "123456"),
            preferred_windows=args.get("preferred_windows")
        )
    elif action == "dispatch_reschedule_request":
        return rescheduler.dispatch_reschedule_request(
            tracking_number=args.get("tracking_number", "123456"),
            selected_option_id=args.get("selected_option_id", "opt_window_morning"),
            safe_drop_instructions=args.get("safe_drop_instructions")
        )
    else:
        raise ValueError(f"Invalid action: {action}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running self-test...")
        event = rescheduler.parse_carrier_event("UPS", "1Z999999999", "Attempted delivery - customer not available")
        assert event["has_exception"] is True
        assert event["exception_code"] == "FAILED_ATTEMPT_RETRY_NEEDED"
        opts = rescheduler.compute_reschedule_options("1Z999999999")
        assert len(opts["available_options"]) > 0
        disp = rescheduler.dispatch_reschedule_request("1Z999999999", "opt_carrier_pickup_point", "Deliver to locker 402")
        assert disp["status"] == "RESCHEDULE_ACCEPTED"
        print("Self-test PASSED!")
        sys.exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            msg_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "AgenticShipmentDeliveryRescheduler", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "reschedule_shipment_delivery",
                            "description": "Parse carrier tracking events, diagnose delivery exceptions, generate optimal reschedule windows, or dispatch safe-drop instructions.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["parse_carrier_event", "diagnose_exception", "compute_reschedule_options", "dispatch_reschedule_request"]},
                                    "carrier": {"type": "string"},
                                    "tracking_number": {"type": "string"},
                                    "raw_status": {"type": "string"},
                                    "preferred_windows": {"type": "array"},
                                    "safe_drop_instructions": {"type": "string"}
                                },
                                "required": ["action"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
