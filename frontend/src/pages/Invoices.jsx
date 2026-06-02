import { useEffect, useState } from 'react';
import axios from 'axios';
import { DollarSign, AlertTriangle, TrendingUp, Wallet } from 'lucide-react';

const API_BASE = 'https://2xshwaapwimchvrjacyfvpdboe0fjbbs.lambda-url.ap-south-1.on.aws/api/v1';

export default function Invoices() {
  const [billing, setBilling] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBilling = async () => {
      try {
        const response = await axios.get(`${API_BASE}/billing/summary`);
        setBilling(response.data);
      } catch (error) {
        console.error("Error fetching billing:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchBilling();
  }, []);

  if (loading) {
    return <div className="text-slate-400 p-8">Loading Billing Information...</div>;
  }

  if (!billing) {
    return <div className="text-red-400">Failed to load billing data.</div>;
  }

  const isOverBudget = billing.projected_bill > billing.budget_limit;
  const budgetPercentage = Math.min(100, (billing.projected_bill / billing.budget_limit) * 100);

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-slate-100">Billing & Invoices</h1>
        <p className="text-slate-400 mt-2">Manage your costs and budget</p>
      </header>

      {isOverBudget && (
        <div className="mb-8 bg-rose-500/10 border border-rose-500/20 rounded-xl p-4 flex items-start gap-4">
          <div className="bg-rose-500/20 p-2 rounded-lg mt-0.5">
            <AlertTriangle className="w-5 h-5 text-rose-400" />
          </div>
          <div>
            <h3 className="text-rose-400 font-medium text-lg">Budget Alert</h3>
            <p className="text-rose-300/80 mt-1">
              Your projected bill ({billing.currency} {billing.projected_bill.toFixed(2)}) is expected to exceed your set budget of {billing.currency} {billing.budget_limit.toFixed(2)}. Consider reducing usage on high-draw appliances.
            </p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-2xl p-6 shadow-lg">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-slate-400 font-medium mb-1">Current Balance</p>
              <h2 className="text-4xl font-bold text-slate-100">
                {billing.currency} {billing.current_balance.toFixed(2)}
              </h2>
            </div>
            <div className="bg-blue-500/20 p-3 rounded-xl text-blue-400">
              <Wallet className="w-6 h-6" />
            </div>
          </div>
          <div className="mt-6 pt-6 border-t border-slate-700/50 flex justify-between items-center text-sm">
            <span className="text-slate-400">Due in 14 days</span>
            <button className="text-blue-400 hover:text-blue-300 font-medium transition-colors">
              Pay Now
            </button>
          </div>
        </div>

        <div className="bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-2xl p-6 shadow-lg">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-slate-400 font-medium mb-1">Projected Bill</p>
              <h2 className="text-4xl font-bold text-slate-100">
                {billing.currency} {billing.projected_bill.toFixed(2)}
              </h2>
            </div>
            <div className="bg-emerald-500/20 p-3 rounded-xl text-emerald-400">
              <TrendingUp className="w-6 h-6" />
            </div>
          </div>
          <div className="mt-6 pt-6 border-t border-slate-700/50">
            <div className="flex justify-between text-sm mb-2">
              <span className="text-slate-400">Budget Limit</span>
              <span className="text-slate-300">{billing.currency} {billing.budget_limit.toFixed(2)}</span>
            </div>
            <div className="w-full bg-slate-700 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${isOverBudget ? 'bg-rose-500' : 'bg-blue-500'}`}
                style={{ width: `${budgetPercentage}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">
        <h3 className="text-xl font-semibold text-slate-200 mb-4">Recent Invoices</h3>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="flex items-center justify-between p-4 bg-slate-800/50 rounded-xl hover:bg-slate-800 transition-colors">
              <div className="flex items-center gap-4">
                <div className="bg-slate-700 p-2 rounded-lg text-slate-300">
                  <DollarSign className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-slate-200 font-medium">Invoice #INV-2026-0{i}</p>
                  <p className="text-slate-400 text-sm">May {i * 10}, 2026</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-slate-200 font-medium">$ {80 + (i * 15)}.00</p>
                <p className="text-emerald-400 text-sm">Paid</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
