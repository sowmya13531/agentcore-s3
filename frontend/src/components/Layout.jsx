import { NavLink, Outlet } from "react-router-dom";
import { Activity, BarChart2, Cpu, FileText, Bot, Zap } from "lucide-react";

const navItems = [
  { path: "/", icon: Activity, label: "Dashboard" },
  { path: "/analytics", icon: BarChart2, label: "Analytics" },
  { path: "/devices", icon: Cpu, label: "Smart Control" },
  { path: "/billing", icon: FileText, label: "Billing" },
  { path: "/ai-chat", icon: Bot, label: "AI Copilot" },
];

export default function Layout() {
  return (
    <div className="flex h-screen bg-slate-950 text-slate-100">

      {/* SIDEBAR */}
      <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col">

        {/* LOGO */}
        <div className="p-6 border-b border-slate-800 flex items-center gap-3">
          <div className="bg-blue-500/20 p-2 rounded-lg">
            <Zap className="text-blue-400" />
          </div>
          <h1 className="text-blue-400 font-bold text-xl">VoltStream</h1>
        </div>

        {/* NAV */}
        <nav className="flex-1 p-4 space-y-2">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-xl transition ${
                  isActive
                    ? "bg-blue-600/20 text-blue-400"
                    : "text-slate-400 hover:bg-slate-800"
                }`
              }
            >
              <item.icon size={18} />
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="p-4 border-t border-slate-800 text-xs text-slate-500">
          AI Energy Platform
        </div>
      </aside>

      {/* MAIN */}
      <main className="flex-1 overflow-y-auto p-6">
        <Outlet />
      </main>
    </div>
  );
}