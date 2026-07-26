const DraftDisplay = ({ title, draft, isRefined }) => {
  if (!draft) return null;

  return (
    <div className={`draft-card ${isRefined ? 'refined-styling' : ''}`}>
      <h3>{title}</h3>
      <div className="content-section">
        <p><strong>Explanation:</strong> {draft.explanation}</p>
      </div>
      
      <div className="mcq-section">
        <h4>Generated MCQs:</h4>
        <ul className="mcq-list">
          {draft.mcqs.map((mcq, idx) => (
            <li key={idx} className="mcq-item">
              <p className="question-text"><strong>Q{idx + 1}:</strong> {mcq.question}</p>
              <ul className="options-list">
                {mcq.options.map((opt, i) => (
                  <li key={i}>{opt}</li>
                ))}
              </ul>
              <p className="answer-text"><em>Correct Answer: {mcq.answer}</em></p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default DraftDisplay;