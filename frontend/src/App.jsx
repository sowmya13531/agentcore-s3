import { Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";

import LiveDashboard from "./pages/LiveDashboard";
import UsageHistory from "./pages/UsageHistory";
import SmartControl from "./pages/SmartControl";
import Invoices from "./pages/Invoices";
import AIChat from "./pages/AIChat";
import NotFound from "./pages/NotFound";

export default function App() {
  return (
    <Routes>
      
      {/* MAIN LAYOUT ROUTE */}
      <Route path="/" element={<Layout />}>

        {/* DEFAULT DASHBOARD */}
        <Route index element={<LiveDashboard />} />

        {/* CORE PAGES */}
        <Route path="analytics" element={<UsageHistory />} />
        <Route path="devices" element={<SmartControl />} />
        <Route path="billing" element={<Invoices />} />

        {/* AI COPILOT PAGE */}
        <Route path="ai-chat" element={<AIChat />} />

        {/* 404 INSIDE LAYOUT */}
        <Route path="*" element={<NotFound />} />

      </Route>

    </Routes>
  );
}