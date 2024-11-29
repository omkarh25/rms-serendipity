/**
 * Ratings page component for RMS.
 * Handles rating creation and display for projects based on the Navarasa model.
 */
'use client';

import React, { useState, useEffect } from 'react';

interface Rating {
  id: number;
  project_id: number;
  rasa: string;
  rating_value: number;
  feedback: string;
  created_at: string;
}

interface Project {
  id: number;
  title: string;
  expected_rasa: string;
}

const RatingsPage = () => {
  const [ratings, setRatings] = useState<Rating[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showRatingForm, setShowRatingForm] = useState(false);
  const [newRating, setNewRating] = useState({
    project_id: '',
    rasa: 'SHRINGARA',
    rating_value: 5,
    feedback: ''
  });

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
    Promise.all([
      fetchRatings(),
      fetchProjects()
    ]).then(() => setLoading(false))
      .catch(err => {
        setError(err instanceof Error ? err.message : 'An error occurred');
        setLoading(false);
      });
  }, []);

  const fetchRatings = async () => {
    try {
      const response = await fetch('https://rms-docs.theserendipity.org/api/v1/ratings');
      if (!response.ok) throw new Error('Failed to fetch ratings');
      const data = await response.json();
      setRatings(data);
    } catch (err) {
      throw err;
    }
  };

  const fetchProjects = async () => {
    try {
      const response = await fetch('https://rms-docs.theserendipity.org/api/v1/projects');
      if (!response.ok) throw new Error('Failed to fetch projects');
      const data = await response.json();
      setProjects(data);
    } catch (err) {
      throw err;
    }
  };

  const handleCreateRating = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('https://rms-docs.theserendipity.org/api/v1/ratings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...newRating,
          project_id: parseInt(newRating.project_id),
          rating_value: parseInt(String(newRating.rating_value))
        }),
      });

      if (!response.ok) throw new Error('Failed to create rating');

      await fetchRatings();
      setShowRatingForm(false);
      setNewRating({
        project_id: '',
        rasa: 'SHRINGARA',
        rating_value: 5,
        feedback: ''
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create rating');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="spinner"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong className="font-bold">Error!</strong>
        <span className="block sm:inline"> {error}</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Ratings</h1>
        <button
          onClick={() => setShowRatingForm(true)}
          className="btn btn-primary"
        >
          Add New Rating
        </button>
      </div>

      {/* Rating Form */}
      {showRatingForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Add New Rating</h2>
            <form onSubmit={handleCreateRating} className="space-y-4">
              <div>
                <label className="form-label" htmlFor="project">Project</label>
                <select
                  id="project"
                  className="form-input"
                  value={newRating.project_id}
                  onChange={(e) => setNewRating({ ...newRating, project_id: e.target.value })}
                  required
                >
                  <option value="">Select a project</option>
                  {projects.map((project) => (
                    <option key={project.id} value={project.id}>{project.title}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="form-label" htmlFor="rasa">Rasa (Emotional Essence)</label>
                <select
                  id="rasa"
                  className="form-input"
                  value={newRating.rasa}
                  onChange={(e) => setNewRating({ ...newRating, rasa: e.target.value })}
                >
                  {rasaOptions.map((rasa) => (
                    <option key={rasa.value} value={rasa.value}>{rasa.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="form-label" htmlFor="rating">Rating (1-10)</label>
                <input
                  type="range"
                  id="rating"
                  min="1"
                  max="10"
                  className="w-full"
                  value={newRating.rating_value}
                  onChange={(e) => setNewRating({ ...newRating, rating_value: parseInt(e.target.value) })}
                />
                <div className="text-center">{newRating.rating_value}</div>
              </div>
              <div>
                <label className="form-label" htmlFor="feedback">Feedback</label>
                <textarea
                  id="feedback"
                  className="form-input"
                  value={newRating.feedback}
                  onChange={(e) => setNewRating({ ...newRating, feedback: e.target.value })}
                  rows={3}
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowRatingForm(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Submit Rating
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Ratings List */}
      <div className="space-y-4">
        {ratings.map((rating) => {
          const project = projects.find(p => p.id === rating.project_id);
          return (
            <div key={rating.id} className="card">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {project?.title || 'Unknown Project'}
                  </h3>
                  <p className="text-sm text-gray-500">
                    {new Date(rating.created_at).toLocaleDateString()}
                  </p>
                </div>
                <div className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium rasa-${rating.rasa.toLowerCase()}`}>
                  {rating.rasa}
                </div>
              </div>
              <div className="mt-2">
                <div className="flex items-center">
                  <div className="text-2xl font-bold text-indigo-600">{rating.rating_value}</div>
                  <div className="ml-2 text-sm text-gray-500">/ 10</div>
                </div>
                {rating.feedback && (
                  <p className="mt-2 text-gray-600">{rating.feedback}</p>
                )}
              </div>
            </div>
          );
        })}

        {ratings.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">No ratings found. Add your first rating!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default RatingsPage;
