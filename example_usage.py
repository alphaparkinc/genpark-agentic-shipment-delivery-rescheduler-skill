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
