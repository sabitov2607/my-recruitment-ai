import React, { useEffect, useState } from "react";

const STORAGE_KEY = "candidates";

function App() {
  const [file, setFile] = useState(null);
  const [vacancy, setVacancy] = useState("");
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Load candidates from localStorage
  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      setCandidates(JSON.parse(stored));
    }
  }, []);

  // Save to localStorage
  const saveCandidates = (list) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
    setCandidates(list);
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please select a CV file");
      return;
    }
    if (!vacancy) {
      setError("Please enter vacancy");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("vacancy", vacancy);

      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Analyze failed");
      }

      const data = await res.json();

      const newCandidate = {
        id: Date.now(),
        name: data.filename,
        vacancy,
        match_score: data.match_score,
        skills: data.skills,
      };

      const updated = [...candidates, newCandidate]
        .sort((a, b) => b.match_score - a.match_score);

      saveCandidates(updated);
    } catch (e) {
      console.error(e);
      setError("Server error");
    } finally {
      setLoading(false);
    }
  };

  const clearAll = () => {
    localStorage.removeItem(STORAGE_KEY);
    setCandidates([]);
  };

  return (
    <div className="container">
      <h1>AI Recruitment System</h1>

      <div className="card">
        <input
          type="text"
          placeholder="Vacancy (e.g. ML Engineer)"
          value={vacancy}
          onChange={(e) => setVacancy(e.target.value)}
        />

        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button onClick={handleAnalyze} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze CV"}
        </button>

        {error && <p className="error">{error}</p>}
      </div>

      {candidates.length > 0 && (
        <>
          <div className="header">
            <h2>Top Candidates</h2>
            <button className="danger" onClick={clearAll}>
              Clear
            </button>
          </div>

          <div className="grid">
            {candidates.map((c) => (
              <div key={c.id} className="candidate">
                <h3>{c.name}</h3>
                <p><strong>Vacancy:</strong> {c.vacancy}</p>
                <p>
                  <strong>Match:</strong>{" "}
                  <span className="score">
                    {(c.match_score).toFixed(1)}%
                  </span>
                </p>
                <p className="skills">
                  {c.skills.join(", ")}
                </p>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default App;
