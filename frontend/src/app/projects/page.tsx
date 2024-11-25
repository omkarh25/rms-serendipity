/**
 * Projects page component for RMS.
 * Displays a list of projects and provides functionality to create new projects.
 */
'use client';

import React, { useState, useEffect } from 'react';

interface Project {
  id: number;
  title: string;
  description: string;
  expected_rasa: string;
  created_at: string;
}

const ProjectsPage = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newProject, setNewProject] = useState({
    title: '',
    description: '',
    expected_rasa: 'SHRINGARA'
  });

  // Navarasa options for the dropdown
  const rasaOptions = [
    { value: 'SHRINGARA', label: 'Shringara (Aesthetic Pleasure)' },
    { value: 'HASYA', label: 'Hasya (Joy)' },
    { value: 'KARUNA', label: 'Karuna (Empathy)' },
    { value: 'VEERA', label: 'Veera (Heroic)' },
    { value: 'BHAYANAKA', label: 'Bhayanaka (Horrific)' },
    { value: 'ADBHUTA', label: 'Adbhuta (Wonder)' },
    { value: 'SHANTA', label: 'Shanta (Serene)' },
    { value: 'BIBHATSA', label: 'Bibhatsa (Disgust)' },
    { value: 'RAUDRA', label: 'Raudra (Fiery)' }
  ];

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/projects/');
      if (!response.ok) throw new Error('Failed to fetch projects');
      const data = await response.json();
      setProjects(data);
      setLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setLoading(false);
    }
  };

  const handleCreateProject = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/v1/projects/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newProject),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create project');
      }

      await fetchProjects();
      setShowCreateForm(false);
      setNewProject({ title: '', description: '', expected_rasa: 'SHRINGARA' });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create project');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">Error!</strong>
          <span className="block sm:inline"> {error}</span>
          <button
            className="absolute top-0 right-0 px-4 py-3"
            onClick={() => setError(null)}
          >
            <span className="sr-only">Close</span>
            <span className="text-2xl">&times;</span>
          </button>
        </div>
      )}

      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Projects</h1>
        <button
          onClick={() => setShowCreateForm(true)}
          className="btn btn-primary"
        >
          Create New Project
        </button>
      </div>

      {/* Create Project Form */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Create New Project</h2>
            <form onSubmit={handleCreateProject} className="space-y-4">
              <div>
                <label className="form-label" htmlFor="title">Title</label>
                <input
                  type="text"
                  id="title"
                  className="form-input"
                  value={newProject.title}
                  onChange={(e) => setNewProject({ ...newProject, title: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="form-label" htmlFor="description">Description</label>
                <textarea
                  id="description"
                  className="form-input"
                  value={newProject.description}
                  onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
                  rows={3}
                />
              </div>
              <div>
                <label className="form-label" htmlFor="expected_rasa">Expected Rasa</label>
                <select
                  id="expected_rasa"
                  className="form-input"
                  value={newProject.expected_rasa}
                  onChange={(e) => setNewProject({ ...newProject, expected_rasa: e.target.value })}
                >
                  {rasaOptions.map((rasa) => (
                    <option key={rasa.value} value={rasa.value}>{rasa.label}</option>
                  ))}
                </select>
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowCreateForm(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Create Project
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Projects List */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {projects.map((project) => (
          <div key={project.id} className="card hover-scale">
            <h3 className="text-lg font-semibold text-gray-900">{project.title}</h3>
            <p className="text-sm text-gray-500 mt-1">
              Created: {new Date(project.created_at).toLocaleDateString()}
            </p>
            <p className="mt-2 text-gray-600">{project.description}</p>
            <div className={`mt-3 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium rasa-${project.expected_rasa.toLowerCase()}`}>
              {project.expected_rasa}
            </div>
            <div className="mt-4 flex justify-end space-x-3">
              <button className="text-sm text-indigo-600 hover:text-indigo-900">View Details</button>
              <button className="text-sm text-indigo-600 hover:text-indigo-900">Add Rating</button>
            </div>
          </div>
        ))}
      </div>

      {projects.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500">No projects found. Create your first project!</p>
        </div>
      )}
    </div>
  );
};

export default ProjectsPage;
