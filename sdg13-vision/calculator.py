# calculator.py

from config import (
    APPLIANCE_POWER,
    CO2_FACTOR,
    TANGEDCO_SLABS,
    TANGEDCO_FIXED_CHARGE,
)


def calculate_monthly_kwh(appliance: str, count: int = 1) -> float:
    if appliance not in APPLIANCE_POWER:
        return 0.0
    data = APPLIANCE_POWER[appliance]
    kwh = (data["watts"] * data["hours"] * 30 * count) / 1000
    return round(kwh, 2)


def calculate_room_kwh(room_inventory: dict) -> float:
    total = 0.0
    for appliance, count in room_inventory.items():
        total += calculate_monthly_kwh(appliance, count)
    return round(total, 2)


def calculate_co2(kwh: float) -> float:
    return round(kwh * CO2_FACTOR, 2)


def calculate_tangedco_bill(units: float) -> float:
    bill = 0.0
    previous_limit = 0

    for limit, rate in TANGEDCO_SLABS:
        if units <= previous_limit:
            break
        taxable = min(units, limit) - previous_limit
        bill += taxable * rate
        previous_limit = limit

    bill += TANGEDCO_FIXED_CHARGE
    return round(bill, 2)


def get_full_report(assembled_rooms: dict) -> dict:
    report = {}
    total_kwh = 0.0

    for room, inventory in assembled_rooms.items():
        room_kwh = calculate_room_kwh(inventory)
        room_co2 = calculate_co2(room_kwh)
        room_bill = calculate_tangedco_bill(room_kwh)

        breakdown = {}
        for appliance, count in inventory.items():
            kwh = calculate_monthly_kwh(appliance, count)
            breakdown[appliance] = {
                "count": count,
                "kwh": kwh,
                "co2": calculate_co2(kwh),
            }

        report[room] = {
            "inventory": inventory,
            "breakdown": breakdown,
            "total_kwh": room_kwh,
            "total_co2": room_co2,
            "bill": room_bill,
        }
        total_kwh += room_kwh

    report["__totals__"] = {
        "total_kwh": round(total_kwh, 2),
        "total_co2": round(calculate_co2(total_kwh), 2),
        "total_bill": round(calculate_tangedco_bill(total_kwh), 2),
    }

    return report
