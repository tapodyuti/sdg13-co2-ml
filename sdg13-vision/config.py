# config.py

APPLIANCE_POWER = {
    "tv":              {"watts": 150,  "hours": 6,    "label": "Television"},
    "refrigerator":    {"watts": 250,  "hours": 24,   "label": "Refrigerator"},
    "microwave":       {"watts": 1200, "hours": 0.5,  "label": "Microwave"},
    "fan":             {"watts": 75,   "hours": 12,   "label": "Ceiling Fan"},
    "laptop":          {"watts": 65,   "hours": 6,    "label": "Laptop"},
    "cell phone":      {"watts": 10,   "hours": 2,    "label": "Phone Charger"},
    "oven":            {"watts": 2000, "hours": 0.5,  "label": "Oven/OTG"},
    "toaster":         {"watts": 800,  "hours": 0.25, "label": "Toaster"},
    "clock":           {"watts": 5,    "hours": 24,   "label": "Clock"},
    "washing machine": {"watts": 500,  "hours": 1,    "label": "Washing Machine"},
    "air conditioner": {"watts": 1500, "hours": 8,    "label": "Air Conditioner"},
    "water heater":    {"watts": 2000, "hours": 0.5,  "label": "Water Heater"},
    "plug_point": {"watts": 5, "hours": 24, "label": "Plug Point (Standby)"},
}

CO2_FACTOR = 0.82

TANGEDCO_SLABS = [
    (100,        0.00),
    (200,        1.50),
    (500,        3.00),
    (float("inf"), 5.00),
]
TANGEDCO_FIXED_CHARGE = 30

ROOM_TYPES = [
    "Living Room",
    "Bedroom",
    "Kitchen",
    "Bathroom",
    "Balcony",
    "Other",
]

YOLO_TO_APPLIANCE = {
    "tv":            "tv",
    "refrigerator":  "refrigerator",
    "microwave":     "microwave",
    "fan":           "fan",
    "laptop":        "laptop",
    "cell phone":    "cell phone",
    "oven":          "oven",
    "toaster":       "toaster",
    "clock":         "clock",
}

WHOLE_HOME_APPLIANCES = [
    "refrigerator",
    "washing machine",
    "water heater",
]
