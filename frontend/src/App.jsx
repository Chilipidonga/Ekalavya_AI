import { useState } from 'react';
import axios from 'axios';
import LessonForm from './components/LessonForm.jsx';
import DraftDisplay from './components/DraftDisplay.jsx';
import FeedbackAlert from './components/FeedbackAlert.jsx';
function App() {
  const [grade, setGrade] = useState(4);
  const [topic, setTopic] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const generateLesson = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/api/generate-lesson', {
        grade: parseInt(grade),
        topic: topic
      });
      setResult(response.data);
    } catch (err) {
      setError('Pipeline execution failed. Please check the backend server.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>AI Agent Educational Pipeline</h1>
        <p>Built with FastAPI, React, and Llama-3</p>
      </header>
      
      <LessonForm 
        grade={grade} 
        setGrade={setGrade} 
        topic={topic} 
        setTopic={setTopic} 
        generateLesson={generateLesson} 
        loading={loading} 
      />

      {error && <div className="error-banner">{error}</div>}

      {result && (
        <div className="pipeline-results">
          <DraftDisplay 
            title="1. Initial Generator Draft" 
            draft={result.initial_draft} 
            isRefined={false} 
          />
          
          <FeedbackAlert 
            status={result.status} 
            feedback={result.feedback} 
          />

          {result.final_draft && (
            <DraftDisplay 
              title="3. Refined Output (After Feedback)" 
              draft={result.final_draft} 
              isRefined={true} 
            />
          )}
        </div>
      )}
    </div>
  );
}

export default App;