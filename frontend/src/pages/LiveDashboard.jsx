import { useEffect, useState } from 'react';
import axios from 'axios';
import { Zap, Sun, Activity } from 'lucide-react';

const API_BASE = 'https://2xshwaapwimchvrjacyfvpdboe0fjbbs.lambda-url.ap-south-1.on.aws/api/v1';

export default function LiveDashboard() {
  const [powerStatus, setPowerStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLiveStatus = async () => {
      try {
        const response = await axios.get(`${API_BASE}/dashboard/live`);
        setPowerStatus(response.data);
      } catch (error) {
        console.error("Error fetching live power status:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchLiveStatus();
    // In a real app, we'd poll this or use WebSockets, but for pre-boarding mock it once is fine, or poll every 5s.
    const intervalId = setInterval(fetchLiveStatus, 5000);
    return () => clearInterval(intervalId);
  }, []);

  if (loading) {
    return <div className="flex h-full items-center justify-center text-blue-400">Loading Power Data...</div>;
  }

  if (!powerStatus) {
    return <div className="text-red-400">Failed to load dashboard data. Ensure backend is running.</div>;
  }

  return (
    <div className="animate-in fade-in zoom-in-95 duration-500">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-slate-100">Live Dashboard</h1>
        <p className="text-slate-400 mt-2">Real-time energy generation and consumption</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <GaugeCard 
          title="Grid Draw" 
          value={powerStatus.grid_draw_kw} 
          unit="kW" 
          icon={Zap} 
          colorClass="text-rose-400"
          bgClass="from-rose-500/20 to-transparent"
        />
        <GaugeCard 
          title="Solar Generation" 
          value={powerStatus.solar_generation_kw} 
          unit="kW" 
          icon={Sun} 
          colorClass="text-amber-400"
          bgClass="from-amber-500/20 to-transparent"
        />
        <GaugeCard 
          title="Net Usage" 
          value={powerStatus.net_usage_kw} 
          unit="kW" 
          icon={Activity} 
          colorClass={powerStatus.net_usage_kw > 0 ? "text-blue-400" : "text-emerald-400"}
          bgClass={powerStatus.net_usage_kw > 0 ? "from-blue-500/20 to-transparent" : "from-emerald-500/20 to-transparent"}
        />
      </div>

      <div className="mt-8 bg-slate-900/50 border border-slate-800 rounded-2xl p-6 backdrop-blur-sm">
        <h3 className="text-lg font-medium text-slate-300 mb-4">System Status</h3>
        <div className="flex items-center gap-4">
          <div className="flex h-3 w-3 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
          </div>
          <span className="text-slate-400">All systems optimal. Connection to inverter is stable.</span>
        </div>
      </div>
    </div>
  );
}

function GaugeCard({ title, value, unit, icon: Icon, colorClass, bgClass }) {
  return (
    <div className={`relative overflow-hidden bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg group hover:border-slate-700 transition-colors`}>
      <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl ${bgClass} rounded-full blur-2xl -mr-10 -mt-10 opacity-50 group-hover:opacity-100 transition-opacity`}></div>
      <div className="relative z-10">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-slate-400 font-medium">{title}</h3>
          <div className="bg-slate-800 p-2 rounded-lg">
            <Icon className={`w-5 h-5 ${colorClass}`} />
          </div>
        </div>
        <div className="flex items-end gap-2 mt-4">
          <span className="text-4xl font-bold text-slate-100">{value.toFixed(2)}</span>
          <span className="text-slate-500 mb-1">{unit}</span>
        </div>
      </div>
    </div>
  );
}
