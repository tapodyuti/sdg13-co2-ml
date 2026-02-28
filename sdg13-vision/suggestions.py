# suggestions.py


def generate_suggestions(total_inventory: dict, total_kwh: float) -> list:
    suggestions = []

    ac    = total_inventory.get("air conditioner", 0)
    fan   = total_inventory.get("fan", 0)
    fridge = total_inventory.get("refrigerator", 0)
    wh    = total_inventory.get("water heater", 0)
    tv    = total_inventory.get("tv", 0)
    laptop = total_inventory.get("laptop", 0)

    # ── AC ───────────────────────────────────────────
    if ac > 0:
        suggestions.append({
            "priority": "🔴 HIGH",
            "icon": "❄️",
            "action": "Set AC to 24°C instead of 18-20°C",
            "reason": "Each 1°C increase saves 6% energy",
            "kwh_saved": round(ac * 54, 1),
            "co2_saved": round(ac * 44.3, 1),
            "bill_saved": round(ac * 378, 1),
        })
        suggestions.append({
            "priority": "🔴 HIGH",
            "icon": "⭐",
            "action": f"Upgrade {ac} AC(s) to 5-star BEE rating",
            "reason": "5-star uses 30% less power than 3-star",
            "kwh_saved": round(ac * 108, 1),
            "co2_saved": round(ac * 88.6, 1),
            "bill_saved": round(ac * 756, 1),
        })

    # ── Solar ────────────────────────────────────────
    if total_kwh > 300:
        suggestions.append({
            "priority": "🔴 HIGH",
            "icon": "☀️",
            "action": "Install 2-3 kW rooftop solar panels",
            "reason": f"Your usage ({total_kwh} kWh/month) gives excellent ROI",
            "kwh_saved": round(total_kwh * 0.7, 1),
            "co2_saved": round(total_kwh * 0.7 * 0.82, 1),
            "bill_saved": round(total_kwh * 0.7 * 7, 1),
        })

    # ── Water Heater ─────────────────────────────────
    if wh > 0:
        suggestions.append({
            "priority": "🔴 HIGH",
            "icon": "🚿",
            "action": "Replace geyser with solar water heater",
            "reason": "Eliminates 90% of water heating electricity",
            "kwh_saved": 54.0,
            "co2_saved": 44.3,
            "bill_saved": 378.0,
        })

    # ── Fans ─────────────────────────────────────────
    if fan > 0:
        suggestions.append({
            "priority": "🟡 MEDIUM",
            "icon": "🌀",
            "action": f"Replace {fan} fan(s) with BLDC fans",
            "reason": "BLDC fans use 50% less power than regular fans",
            "kwh_saved": round(fan * 13.5, 1),
            "co2_saved": round(fan * 11.1, 1),
            "bill_saved": round(fan * 94.5, 1),
        })

    # ── Fridge ───────────────────────────────────────
    if fridge > 0:
        suggestions.append({
            "priority": "🟡 MEDIUM",
            "icon": "🧊",
            "action": "Clean refrigerator coils every month",
            "reason": "Dirty coils increase consumption by 15%",
            "kwh_saved": 9.0,
            "co2_saved": 7.4,
            "bill_saved": 63.0,
        })
        suggestions.append({
            "priority": "🟡 MEDIUM",
            "icon": "🌡️",
            "action": "Set fridge to 3-4°C and freezer to -15°C",
            "reason": "Optimal temperature reduces unnecessary cooling",
            "kwh_saved": 7.5,
            "co2_saved": 6.2,
            "bill_saved": 52.5,
        })

    # ── TV ───────────────────────────────────────────
    if tv > 0:
        suggestions.append({
            "priority": "🟡 MEDIUM",
            "icon": "📺",
            "action": "Enable auto power-off on TV when idle",
            "reason": "Standby mode wastes 10W continuously",
            "kwh_saved": round(tv * 4.5, 1),
            "co2_saved": round(tv * 3.7, 1),
            "bill_saved": round(tv * 31.5, 1),
        })

    # ── Laptop ───────────────────────────────────────
    if laptop > 0:
        suggestions.append({
            "priority": "🟢 LOW",
            "icon": "💻",
            "action": "Enable sleep mode after 10 mins idle",
            "reason": "Sleep uses 90% less power than active mode",
            "kwh_saved": round(laptop * 3.5, 1),
            "co2_saved": round(laptop * 2.9, 1),
            "bill_saved": round(laptop * 24.5, 1),
        })

    # ── General ──────────────────────────────────────
    suggestions.append({
        "priority": "🟢 LOW",
        "icon": "🔌",
        "action": "Use smart power strips to kill standby power",
        "reason": "Standby power wastes 5-10% of total usage",
        "kwh_saved": round(total_kwh * 0.05, 1),
        "co2_saved": round(total_kwh * 0.05 * 0.82, 1),
        "bill_saved": round(total_kwh * 0.05 * 7, 1),
    })

    # ── Sort by priority ─────────────────────────────────────────────
    order = {"🔴 HIGH": 0, "🟡 MEDIUM": 1, "🟢 LOW": 2}
    suggestions.sort(key=lambda x: order.get(x["priority"], 3))

    # ── Scale ALL individual suggestions proportionally ───────────────
    total_suggested = sum(s["kwh_saved"] for s in suggestions)

    if total_suggested > total_kwh * 0.80:
        scale_factor = (total_kwh * 0.80) / total_suggested
        for s in suggestions:
            s["kwh_saved"] = round(s["kwh_saved"] * scale_factor, 1)
            s["co2_saved"] = round(s["co2_saved"] * scale_factor, 1)

    # ── Recalculate bill savings from scaled kWh AFTER scaling ────────
    # Using TANGEDCO approximate rate ₹2/kWh (slab-aware estimate)
    EFFECTIVE_BILL_RATE = 2.0
    for s in suggestions:
        s["bill_saved"] = round(s["kwh_saved"] * EFFECTIVE_BILL_RATE, 1)

    return suggestions

