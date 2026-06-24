from .device_agent import device_agent
from .energy_agent import energy_agent


def handle_query(user_query: str):

    query = user_query.lower()

    device_keywords = [
        "turn on",
        "turn off",
        "device",
        "status",
        "hvac",
        "heater",
        "refrigerator",
        "dishwasher",
        "light",
        "charger"
    ]

    energy_keywords = [
        "energy",
        "power",
        "consumption",
        "usage",
        "electricity",
        "bill",
        "saving",
        "cost"
    ]

    needs_device = any(
        keyword in query
        for keyword in device_keywords
    )

    needs_energy = any(
        keyword in query
        for keyword in energy_keywords
    )

    responses = []

    if needs_device:

        device_result = device_agent(user_query)

        if hasattr(device_result, "text"):
            responses.append(device_result.text)
        else:
            responses.append(str(device_result))

    if needs_energy:

        energy_result = energy_agent(user_query)

        if hasattr(energy_result, "text"):
            responses.append(energy_result.text)
        else:
            responses.append(str(energy_result))

    if not responses:

        device_result = device_agent(user_query)

        if hasattr(device_result, "text"):
            responses.append(device_result.text)
        else:
            responses.append(str(device_result))

    return "\n\n".join(responses)