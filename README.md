# genpark-agentic-shipment-delivery-rescheduler-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Skill-blue.svg)](https://genpark.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0%20(Pure%20Stdlib)-brightgreen.svg)](requirements.txt)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-purple.svg)](mcp_server.py)

Autonomous Shipment Exception Detection & Delivery Rescheduler. Ingests FedEx, UPS, DHL, and SF Express tracking webhooks, detects failed delivery attempts and customs delays, auto-negotiates delivery windows, locker hold orders, and neighbor safe-drop instructions.

---

## 🌟 Key Features

- **100% Zero External Dependencies**: Runs entirely on the Python 3.9+ standard library.
- **Model Context Protocol (MCP) Standard**: Native support for JSON-RPC 2.0 `initialize`, `tools/list`, and `tools/call`.
- **Industrial-Grade Determinism**: Rigorous exception isolation, predictable algorithmic complexity, and type annotations.
- **Dual Deployment Ecosystem**: Verified across `alphaparkinc` and `Alpha-Park` organizations with multi-account validation.

---

## 🚀 Quick Start

### 1. Direct Python SDK Usage

```python
"""Example usage for AgenticShipmentDeliveryRescheduler."""
import sys
import json
from client import AgenticShipmentDeliveryRescheduler

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== Agentic Commerce Shipment Delivery Rescheduler Demo ===")
    rescheduler = AgenticShipmentDeliveryRescheduler()

    # 1. Parse carrier webhook indicating missed delivery
    print("\n--- 1. Ingesting Carrier Webhook with Delivery Exception ---")
    event = rescheduler.parse_carrier_event(
        carrier="FEDEX",
        tracking_number="789456123999",
        raw_status="Attempted delivery - business closed / customer not available",
        location="Austin Distribution Hub, TX"
    )
    print(f"Exception Detected: {event['has_exception']} (Code: {event['exception_code']})")

    # 2. Compute dynamic recovery delivery windows & pickup locker alternatives
    print("\n--- 2. Computing Autonomous Rescheduling Options ---")
    options = rescheduler.compute_reschedule_options(
        tracking_number="789456123999",
        preferred_windows=["Tomorrow 18:00 - 21:00 (After Work)"]
    )
    print(json.dumps(options, indent=2))

    # 3. Dispatch automated carrier instruction
    print("\n--- 3. Dispatching Carrier Safe-Drop Instruction ---")
    result = rescheduler.dispatch_reschedule_request(
        tracking_number="789456123999",
        selected_option_id="opt_carrier_pickup_point",
        safe_drop_instructions="Deposit into Parcel Locker Box #12. Recipient code verified."
    )
    print(f"Carrier Response: {result['status']}, Token: {result['confirmation_token']}")

if __name__ == "__main__":
    main()

```

### 2. Run as Model Context Protocol (MCP) Server

Start standard JSON-RPC 2.0 server over `stdio`:

```bash
python mcp_server.py
```

Execute embedded test harness:

```bash
python mcp_server.py --test
```

---

## 🛠️ MCP Tool Specification

Inspect [`skill.json`](skill.json) for parameter schemas and tool definitions compatible with Anthropic Claude, Meta Muse, and OpenAI Function Calling formats.

---

## 📜 License

Licensed under the [MIT License](LICENSE). Copyright © 2026 GenPark AI.
