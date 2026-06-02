import { NavLink, Outlet } from 'react-router-dom';
import { Activity, BarChart2, Cpu, FileText, Zap } from 'lucide-react';
import AIChat from '../pages/AIChat';


const navItems = [
  { path: '/', icon: Activity, label: 'Dashboard' },
  { path: '/analytics', icon: BarChart2, label: 'Analytics' },
  { path: '/devices', icon: Cpu, label: 'Smart Control' },
  { path: '/billing', icon: FileText, label: 'Billing' },
];

export default function Layout() {
  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col transition-all duration-300">
        <div className="p-6 flex items-center gap-3 border-b border-slate-800">
          <div className="bg-blue-500/20 p-2 rounded-lg">
            <Zap className="w-6 h-6 text-blue-400" />
          </div>
          <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-teal-400 bg-clip-text text-transparent">
            VoltStream
          </span>
        </div>
        
        <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                  isActive
                    ? 'bg-blue-500/10 text-blue-400 shadow-[0_0_15px_rgba(59,130,246,0.1)]'
                    : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
                }`
              }
            >
              <item.icon className="w-5 h-5" />
              <span className="font-medium">{item.label}</span>
            </NavLink>
          ))}
        </nav>
        
        <div className="p-4 border-t border-slate-800 text-xs text-slate-500 text-center">
          Prosumer AI Copilot
        </div>
      </aside>

      {/* Main Content */}
            <main className="flex-1 overflow-y-auto p-8 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-slate-900 via-slate-950 to-slate-950">
        <div className="max-w-6xl mx-auto">
          <Outlet />
        </div>
      </main>

      <AIChat />

    </div>
    );
}
