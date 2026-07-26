const FeedbackAlert = ({ status, feedback }) => {
  const isPass = status === 'pass';
  
  return (
    <div className={`feedback-card ${isPass ? 'status-pass' : 'status-fail'}`}>
      <h3>2. Reviewer Agent Evaluation</h3>
      <div className="status-badge">
        <strong>Status:</strong> {status.toUpperCase()}
      </div>
      
      {isPass ? (
        <p className="success-text">✓ Content passed all criteria successfully. No feedback required.</p>
      ) : (
        <div className="error-list">
          <p><strong>Issues Identified:</strong></p>
          <ul>
            {feedback.map((fb, idx) => (
              <li key={idx}>{fb}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FeedbackAlert;