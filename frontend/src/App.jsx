import { Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";

import LiveDashboard from "./pages/LiveDashboard";
import UsageHistory from "./pages/UsageHistory";
import SmartControl from "./pages/SmartControl";
import Invoices from "./pages/Invoices";
import AIChat from "./pages/AIChat";
import NotFound from "./pages/NotFound";

import AIWidget from "./components/AIWidget";

export default function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<LiveDashboard />} />
          <Route path="analytics" element={<UsageHistory />} />
          <Route path="devices" element={<SmartControl />} />
          <Route path="billing" element={<Invoices />} />
          <Route path="ai-chat" element={<AIChat />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>

      <AIWidget />
    </>
  );
}