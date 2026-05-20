from pydantic import BaseModel
from typing import List, Optional

class LivePowerStatus(BaseModel):
    grid_draw_kw: float
    solar_generation_kw: float
    net_usage_kw: float

class EnergyDataPoint(BaseModel):
    timestamp: str
    usage_kwh: float
    generation_kwh: float

class DeviceResponse(BaseModel):
    id: str
    name: str
    type: str
    power_draw_w: float
    is_on: bool

class DeviceUpdate(BaseModel):
    is_on: bool

class BillingSummary(BaseModel):
    current_balance: float
    projected_bill: float
    budget_limit: float
    currency: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
