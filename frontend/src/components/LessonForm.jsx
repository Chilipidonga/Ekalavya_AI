const LessonForm = ({ grade, setGrade, topic, setTopic, generateLesson, loading }) => {
  return (
    <form onSubmit={generateLesson} className="lesson-form">
      <div className="input-group">
        <label>Grade Level:</label>
        <input 
          type="number" 
          min="1" max="12" 
          value={grade} 
          onChange={(e) => setGrade(e.target.value)} 
          required 
        />
      </div>
      <div className="input-group">
        <label>Topic:</label>
        <input 
          type="text" 
          value={topic} 
          onChange={(e) => setTopic(e.target.value)} 
          placeholder="e.g., The Water Cycle" 
          required 
        />
      </div>
      <button type="submit" disabled={loading}>
        {loading ? 'Agents Analyzing...' : 'Generate Content'}
      </button>
    </form>
  );
};

export default LessonForm;