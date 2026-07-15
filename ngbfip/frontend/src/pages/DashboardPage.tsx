import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { dashboardService } from '../services/apiClient';
import { AlertCircle, TrendingUp, Activity, Shield, Bell } from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const { user, logout } = useAuth();
  const [overview, setOverview] = useState<any>(null);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [overviewRes, statsRes] = await Promise.all([
          dashboardService.getOverview(),
          dashboardService.getStatistics(),
        ]);
        setOverview(overviewRes.data);
        setStats(statsRes.data);
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-4 border-blue-500 border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Navigation */}
      <nav className="backdrop-blur-xl bg-white/5 border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-white">NG-BIFP Dashboard</h1>
          <div className="flex items-center gap-4">
            <span className="text-slate-300">{user?.email}</span>
            <button
              onClick={logout}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Total Transactions */}
          <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-xl p-6 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">Total Transactions</p>
                <p className="text-3xl font-bold text-white mt-2">{stats?.transactions?.total || 0}</p>
              </div>
              <Activity size={40} className="text-blue-400 opacity-50" />
            </div>
          </div>

          {/* Flagged Transactions */}
          <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-xl p-6 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">Flagged</p>
                <p className="text-3xl font-bold text-red-400 mt-2">{stats?.transactions?.flagged || 0}</p>
              </div>
              <AlertCircle size={40} className="text-red-400 opacity-50" />
            </div>
          </div>

          {/* Risk Score */}
          <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-xl p-6 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">Avg Risk Score</p>
                <p className="text-3xl font-bold text-yellow-400 mt-2">{overview?.average_risk_score?.toFixed(2) || '0.00'}</p>
              </div>
              <TrendingUp size={40} className="text-yellow-400 opacity-50" />
            </div>
          </div>

          {/* Trusted Devices */}
          <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-xl p-6 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">Trusted Devices</p>
                <p className="text-3xl font-bold text-green-400 mt-2">{stats?.devices?.trusted || 0}</p>
              </div>
              <Shield size={40} className="text-green-400 opacity-50" />
            </div>
          </div>
        </div>

        {/* Risk Distribution */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Risk Levels */}
          <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-xl p-6 shadow-lg">
            <h3 className="text-white font-semibold mb-4">Risk Distribution</h3>
            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-400">Low Risk</span>
                  <span className="text-green-400 font-semibold">{stats?.risk?.low || 0}</span>
                </div>
                <div className="w-full bg-slate-700/50 rounded-full h-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{ width: '80%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-400">Medium Risk</span>
                  <span className="text-yellow-400 font-semibold">{stats?.risk?.medium || 0}</span>
                </div>
                <div className="w-full bg-slate-700/50 rounded-full h-2">
                  <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '15%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-400">High Risk</span>
                  <span className="text-red-400 font-semibold">{stats?.risk?.high || 0}</span>
                </div>
                <div className="w-full bg-slate-700/50 rounded-full h-2">
                  <div className="bg-red-500 h-2 rounded-full" style={{ width: '5%' }}></div>
                </div>
              </div>
            </div>
          </div>

          {/* Alerts */}
          <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-xl p-6 shadow-lg">
            <h3 className="text-white font-semibold mb-4 flex items-center gap-2">
              <Bell size={20} /> Alerts
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center text-sm">
                <span className="text-slate-400">Open Alerts</span>
                <span className="px-3 py-1 bg-red-500/20 text-red-400 rounded-full font-semibold">
                  {stats?.alerts?.open || 0}
                </span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-slate-400">Resolved</span>
                <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full font-semibold">
                  {stats?.alerts?.resolved || 0}
                </span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-slate-400">Dismissed</span>
                <span className="px-3 py-1 bg-slate-500/20 text-slate-400 rounded-full font-semibold">
                  {stats?.alerts?.dismissed || 0}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
