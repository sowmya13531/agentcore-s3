import { useEffect, useState } from "react";
import axios from "axios";
import {
  Power,
  Thermometer,
  Lightbulb,
  Zap,
  Server,
} from "lucide-react";

const API_BASE = "http://127.0.0.1:8000/api/v1";

export default function SmartControl() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDevices();

    const interval = setInterval(() => {
      fetchDevices();
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const fetchDevices = async () => {
    try {
      const response = await axios.get(
        `${API_BASE}/devices`
      );

      setDevices(response.data);
    } catch (error) {
      console.error(
        "Error fetching devices:",
        error
      );
    } finally {
      setLoading(false);
    }
  };

  const toggleDevice = async (
    id,
    currentState
  ) => {
    try {
      setDevices((prev) =>
        prev.map((device) =>
          device.id === id
            ? {
                ...device,
                is_on: !currentState,
              }
            : device
        )
      );

      await axios.patch(
        `${API_BASE}/devices/${id}`,
        {
          is_on: !currentState,
        }
      );

      fetchDevices();
    } catch (error) {
      console.error(
        `Error toggling device ${id}:`,
        error
      );

      fetchDevices();
    }
  };

  const getDeviceIcon = (type) => {
    switch (type) {
      case "climate":
        return Thermometer;

      case "lighting":
        return Lightbulb;

      case "vehicle":
        return Zap;

      default:
        return Server;
    }
  };

  if (loading) {
    return (
      <div className="text-slate-400 p-8">
        Loading Smart Devices...
      </div>
    );
  }

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">

      <header className="mb-8 flex items-center justify-between">

        <div>
          <h1 className="text-3xl font-bold text-slate-100">
            Smart Control
          </h1>

          <p className="text-slate-400 mt-2">
            Manage your connected appliances
          </p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-lg px-4 py-2 flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>

          <span className="text-sm text-slate-300">
            {
              devices.filter(
                (device) => device.is_on
              ).length
            }{" "}
            Active
          </span>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

        {devices.map((device) => {
          const Icon = getDeviceIcon(
            device.type
          );

          return (
            <div
              key={device.id}
              className={`relative overflow-hidden border rounded-2xl p-6 transition-all duration-300 ${
                device.is_on
                  ? "bg-slate-800/80 border-blue-500/30 shadow-[0_0_30px_rgba(59,130,246,0.1)]"
                  : "bg-slate-900 border-slate-800 opacity-75 grayscale-[0.2]"
              }`}
            >
              <div className="flex justify-between items-start mb-6">

                <div
                  className={`p-3 rounded-xl ${
                    device.is_on
                      ? "bg-blue-500/20 text-blue-400"
                      : "bg-slate-800 text-slate-500"
                  }`}
                >
                  <Icon className="w-6 h-6" />
                </div>

                <button
                  onClick={() =>
                    toggleDevice(
                      device.id,
                      device.is_on
                    )
                  }
                  className={`w-14 h-8 rounded-full transition-colors relative flex items-center px-1 ${
                    device.is_on
                      ? "bg-blue-500"
                      : "bg-slate-700"
                  }`}
                >
                  <div
                    className={`w-6 h-6 rounded-full bg-white transition-transform duration-300 shadow-md ${
                      device.is_on
                        ? "translate-x-6"
                        : "translate-x-0"
                    }`}
                  />
                </button>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-slate-100 mb-1">
                  {device.name}
                </h3>

                <p className="text-slate-400 text-sm flex items-center gap-2">
                  <Power className="w-4 h-4" />
                  {device.power_draw_w} W
                </p>

                <p
                  className={`mt-3 text-sm font-medium ${
                    device.is_on
                      ? "text-emerald-400"
                      : "text-red-400"
                  }`}
                >
                  {device.is_on
                    ? "ON"
                    : "OFF"}
                </p>
              </div>

              {device.is_on && (
                <div className="absolute -bottom-4 -right-4 w-24 h-24 bg-blue-500 rounded-full blur-3xl opacity-20 pointer-events-none"></div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}