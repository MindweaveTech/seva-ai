import React from 'react';

function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="text-center max-w-2xl">
        <h1 className="text-5xl font-bold text-primary-500 mb-4">
          Smart AI
        </h1>
        <h2 className="text-2xl font-semibold text-gray-700 mb-6">
          Admin Dashboard
        </h2>
        <p className="text-lg text-gray-600">
          Caregiver monitoring and patient management portal
        </p>
        <div className="mt-8 flex gap-4 justify-center">
          <button className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-3 rounded-lg font-medium transition-colors">
            Get Started
          </button>
          <button className="bg-white hover:bg-gray-100 text-primary-500 border-2 border-primary-500 px-6 py-3 rounded-lg font-medium transition-colors">
            Learn More
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
