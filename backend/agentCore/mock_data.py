from models import (
    LivePowerStatus,
    EnergyDataPoint,
    DeviceResponse,
    BillingSummary
)

# Mock Data Storage

MOCK_DASHBOARD_LIVE = LivePowerStatus(
    grid_draw_kw=2.5,
    solar_generation_kw=1.8,
    net_usage_kw=0.7
)

MOCK_ANALYTICS_HISTORY = {
    "daily": [
        {"timestamp": "00:00", "usage_kwh": 0.5, "generation_kwh": 0.0},
        {"timestamp": "04:00", "usage_kwh": 0.4, "generation_kwh": 0.0},
        {"timestamp": "08:00", "usage_kwh": 1.2, "generation_kwh": 2.5},
        {"timestamp": "12:00", "usage_kwh": 1.5, "generation_kwh": 5.0},
        {"timestamp": "16:00", "usage_kwh": 2.0, "generation_kwh": 3.2},
        {"timestamp": "20:00", "usage_kwh": 2.8, "generation_kwh": 0.0},
    ],
    "weekly": [
        {"timestamp": "Mon", "usage_kwh": 15.2, "generation_kwh": 12.0},
        {"timestamp": "Tue", "usage_kwh": 14.8, "generation_kwh": 18.5},
        {"timestamp": "Wed", "usage_kwh": 16.5, "generation_kwh": 9.2},
        {"timestamp": "Thu", "usage_kwh": 13.0, "generation_kwh": 15.0},
        {"timestamp": "Fri", "usage_kwh": 18.2, "generation_kwh": 14.2},
        {"timestamp": "Sat", "usage_kwh": 22.0, "generation_kwh": 16.0},
        {"timestamp": "Sun", "usage_kwh": 20.5, "generation_kwh": 17.5},
    ],
    "monthly": [
        {"timestamp": "Week 1", "usage_kwh": 120.5, "generation_kwh": 95.2},
        {"timestamp": "Week 2", "usage_kwh": 115.0, "generation_kwh": 110.5},
        {"timestamp": "Week 3", "usage_kwh": 130.2, "generation_kwh": 85.0},
        {"timestamp": "Week 4", "usage_kwh": 125.8, "generation_kwh": 105.4},
    ]
}

MOCK_DEVICES = [
    DeviceResponse(
        id="dev-1",
        name="HVAC System",
        type="climate",
        power_draw_w=3500,
        is_on=True
    ),
    DeviceResponse(
        id="dev-2",
        name="Water Heater",
        type="appliance",
        power_draw_w=4500,
        is_on=False
    ),
    DeviceResponse(
        id="dev-3",
        name="Pool Pump",
        type="appliance",
        power_draw_w=1500,
        is_on=True
    ),
    DeviceResponse(
        id="dev-4",
        name="EV Charger",
        type="vehicle",
        power_draw_w=7200,
        is_on=False
    ),
    DeviceResponse(
        id="dev-5",
        name="Living Room Lights",
        type="lighting",
        power_draw_w=150,
        is_on=True
    ),
    DeviceResponse(
        id="dev-6",
        name="Refrigerator",
        type="appliance",
        power_draw_w=800,
        is_on=True
    ),
    DeviceResponse(
        id="dev-7",
        name="Dishwasher",
        type="appliance",
        power_draw_w=1200,
        is_on=True
    )
]

MOCK_BILLING_SUMMARY = BillingSummary(
    current_balance=45.50,
    projected_bill=112.75,
    budget_limit=100.00,
    currency="USD"
)