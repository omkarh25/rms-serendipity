import React from 'react';

export default function Home() {
  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="bg-white shadow rounded-lg p-6">
        <h1 className="text-3xl font-bold text-gray-900">Welcome to RMS</h1>
        <p className="mt-2 text-gray-600">
          Rating Management System for content creation based on Mathu-Kathe principles
        </p>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900">Active Projects</h3>
          <p className="mt-2 text-3xl font-bold text-indigo-600">12</p>
        </div>
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900">Total Ratings</h3>
          <p className="mt-2 text-3xl font-bold text-indigo-600">248</p>
        </div>
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900">Avg Rating</h3>
          <p className="mt-2 text-3xl font-bold text-indigo-600">4.8</p>
        </div>
      </div>

      {/* Recent Projects */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Projects</h2>
        <div className="space-y-4">
          {[1, 2, 3].map((project) => (
            <div key={project} className="border-b pb-4 last:border-b-0 last:pb-0">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-medium text-gray-900">Project Title {project}</h3>
                  <p className="text-sm text-gray-500">Last updated: 2 hours ago</p>
                </div>
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                  Active
                </span>
              </div>
              <div className="mt-2 text-sm text-gray-600">
                Project description goes here. This is a brief overview of what the project is about.
              </div>
              <div className="mt-3 flex space-x-4">
                <button className="text-sm text-indigo-600 hover:text-indigo-900">View Details</button>
                <button className="text-sm text-indigo-600 hover:text-indigo-900">Add Rating</button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Navarasa Overview */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Navarasa Distribution</h2>
        <div className="grid grid-cols-3 md:grid-cols-9 gap-4">
          {[
            'Shringara', 'Hasya', 'Karuna',
            'Veera', 'Bhayanaka', 'Adbhuta',
            'Shanta', 'Bibhatsa', 'Raudra'
          ].map((rasa) => (
            <div key={rasa} className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-indigo-100 text-indigo-600">
                {rasa.charAt(0)}
              </div>
              <p className="mt-2 text-sm font-medium text-gray-600">{rasa}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
            Create New Project
          </button>
          <button className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700">
            Add New Rating
          </button>
          <button className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700">
            View Analytics
          </button>
        </div>
      </div>
    </div>
  );
}
