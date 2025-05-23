# Network Engineer Interview Assistant

A desktop application to assist with conducting network engineering job interviews. This tool helps interviewers manage interview sessions, ask relevant technical questions, and track candidate performance.

## Features

- Record interviewee details (name, date, and time)
- Generate questions for network engineers:
  - Technical questions at different difficulty levels (Easy, Medium, Hard)
  - Mix questions from multiple difficulty levels for varied challenge
  - Tactical/scenario-based questions for assessing problem-solving skills
- Show/hide answers for reference
- Track candidate performance (correct, partially correct, incorrect answers)
- View detailed interview summary with performance statistics and percentages
- Generate comprehensive interview reports saved as text files
- Add custom notes and remarks before generating reports

## Requirements

- Python 3.6 or higher
- PyQt5

## Installation

1. Make sure you have Python installed on your system. If not, download and install it from [python.org](https://www.python.org/downloads/).

2. Install PyQt5 using pip:

```bash
pip install PyQt5
```

## Running the Application

Navigate to the project directory and run:

```bash
python interview_assistant.py
```

## Usage Instructions

1. **Start Screen**:
   - Enter the interviewee's name
   - Set the date and time of the interview
   - Click "Start Interview"

2. **Interview Session**:
   - **Question Type Selection**:
     - Choose between "Technical" or "Tactical/Scenario" questions

   - **For Technical Questions**:
     - Select one or more difficulty levels using the checkboxes (Easy, Medium, Hard)
     - Click "Mix Selected Difficulties" to combine and shuffle questions from selected levels
     - Questions will display their difficulty level (e.g., [EASY], [MEDIUM], [HARD])

   - **Question Navigation**:
     - Click "Next Question" to display a question
     - Use "Show Answer" to view the reference answer
     - Evaluate the candidate's response using the "Correct", "Partially Correct", or "Incorrect" buttons
     - Track results in real-time

   - **Finishing the Interview**:
     - Click "Finish Interview" when done
     - Add notes about technical knowledge, problem-solving skills, communication skills, and recommendations
     - Save the report to generate a comprehensive evaluation document

## Customizing Questions

The application currently includes built-in questions for network engineers. To customize or add more questions, you can modify the `load_questions()` method in the `interview_assistant.py` file.

Each question should follow this format:

```python
{
    "question": "Your question text here",
    "answer": "The reference answer here"
}
```

## About the Questions

The application includes questions specifically designed for network engineers:

### Technical Questions
Organized by difficulty level:
- **Easy**: Fundamental networking concepts (subnet masks, basic devices, DNS)
- **Medium**: Intermediate topics (TCP/UDP, routing protocols, VLANs)
- **Hard**: Advanced concepts (BGP, MPLS, IPsec VPN, SDN, EVPN-VXLAN)

You can select any combination of these difficulty levels to create a customized question mix that suits your interview needs.

### Tactical/Scenario Questions
Real-world scenarios that assess problem-solving skills:
- Troubleshooting network issues
- Network design considerations
- Incident response
- Performance optimization
- Security incident handling

## Interview Reports

The application automatically generates detailed interview reports that include:
- Interviewee information and interview date/time
- Performance statistics (number and percentage of correct/partially correct/incorrect answers)
- Overall weighted score
- Custom notes and evaluations:
  - Technical knowledge assessment
  - Problem-solving skills evaluation
  - Communication skills observations
  - Hiring recommendation
  - Additional notes and remarks

Reports are saved as text files in the application directory with filenames that include the candidate's name and interview timestamp.

## Future Enhancements

- Import/export question banks
- Add timing features for interview segments
- Include more specialized question categories
- Add support for custom scoring algorithms
- Enable report customization
