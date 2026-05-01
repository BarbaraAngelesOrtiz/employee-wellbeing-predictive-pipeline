import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { modelWeights, modelIntercept, syntheticProfiles } from '../constants/modelData';

const StrategicDashboard = () => {
  const [inputs, setInputs] = useState(syntheticProfiles[0].inputs);

  const calculateComfort = () => {
    let z = modelIntercept;
    Object.keys(modelWeights).forEach((key) => {
      z += modelWeights[key] * (inputs[key] || 0);
    });
    
    const prob = 1 / (1 + Math.exp(-z));
    return (prob * 100).toFixed(1);
  };

  
  const chartData = Object.entries(modelWeights)
    .map(([name, value]) => ({ name, value: parseFloat(value.toFixed(3)) }))
    .sort((a, b) => Math.abs(b.value) - Math.abs(a.value)); // Ordenar por impacto

  const comfortScore = calculateComfort();

  return (
    <div className="p-8 bg-gray-100 min-h-screen font-sans text-gray-800">
      <header className="mb-10">
        <h1 className="text-4xl font-extrabold text-indigo-900">Strategic Wellbeing Insights</h1>
        <p className="text-gray-600 mt-2">Data-driven simulation based on Logistic Regression and Clustering.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* --- SECCIÓN 1: WHAT-IF SIMULATOR --- */}
        <section className="bg-white p-6 rounded-2xl shadow-xl border-t-4 border-indigo-500">
          <h2 className="text-2xl font-bold mb-4 flex items-center">
            <span className="mr-2">🎮</span> What-If Simulator
          </h2>
          <div className="mb-8 text-center bg-indigo-50 p-6 rounded-xl">
            <p className="text-sm uppercase tracking-widest text-indigo-400 font-semibold">Predicted Comfort Probability</p>
            <p className={`text-6xl font-black ${comfortScore > 50 ? 'text-green-500' : 'text-red-500'}`}>
              {comfortScore}%
            </p>
          </div>

          <div className="space-y-4 max-h-96 overflow-y-auto pr-2">
            {Object.keys(modelWeights).map((key) => (
              <div key={key} className="flex flex-col">
                <div className="flex justify-between text-sm mb-1">
                  <span className="capitalize font-medium">{key.replace(/_/g, ' ')}</span>
                  <span className="font-mono text-indigo-600">{(inputs[key] || 0).toFixed(2)}</span>
                </div>
                <input
                  type="range"
                  min="0" max="1" step="0.01"
                  value={inputs[key] || 0}
                  onChange={(e) => setInputs({ ...inputs, [key]: parseFloat(e.target.value) })}
                  className="w-full h-2 bg-indigo-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                />
              </div>
            ))}
          </div>
        </section>

        <div className="space-y-8">
          {/* --- SECCIÓN 2: DRIVER RADAR --- */}
          <section className="bg-white p-6 rounded-2xl shadow-xl">
            <h2 className="text-2xl font-bold mb-4 flex items-center">
              <span className="mr-2">📊</span> Key Risk Drivers
            </h2>
        {/* Cambiamos h-64 por un estilo fijo de 300px */}
        <div style={{ height: '300px', width: '100%' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} layout="vertical">
              <XAxis type="number" hide />
              <YAxis dataKey="name" type="category" width={150} fontSize={12} />
              <Tooltip />
              <Bar dataKey="value">
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.value > 0 ? '#10B981' : '#EF4444'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
            <p className="text-xs text-gray-400 mt-4 italic">
              *Green indicates a positive impact on comfort, Red indicates an inhibitor.
            </p>
          </section>

          {/* --- SECCIÓN 3: PERSONA QUICK SELECT --- */}
          <section className="bg-white p-6 rounded-2xl shadow-xl">
            <h2 className="text-2xl font-bold mb-4">Synthetic Personas</h2>
            <div className="flex gap-4">
              {syntheticProfiles.map((profile) => (
                <button
                  key={profile.id}
                  onClick={() => setInputs(profile.inputs)}
                  className="flex-1 p-3 border-2 border-indigo-100 rounded-xl hover:border-indigo-500 hover:bg-indigo-50 transition-all text-sm font-semibold"
                >
                  {profile.name}
                </button>
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default StrategicDashboard;