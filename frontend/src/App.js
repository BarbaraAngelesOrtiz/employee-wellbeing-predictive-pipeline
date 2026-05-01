import React from 'react';
import StrategicDashboard from './components/StrategicDashboard';
import './index.css'; 

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-indigo-900 p-4 text-white shadow-lg">
        <div className="container mx-auto">
          <span className="text-xl font-bold tracking-tight">AI Wellbeing Insights</span>
        </div>
      </nav>
      
      <main className="container mx-auto py-8">
        {/* This calls your component */}
        <StrategicDashboard />
      </main>

      <footer className="mt-12 py-6 text-center text-gray-500 text-sm">
        Built for Women in AI Ireland - 2026
      </footer>
    </div>
  );
}

export default App;