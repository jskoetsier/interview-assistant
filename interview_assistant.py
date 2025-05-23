#!/usr/bin/env python3
import sys
import json
import datetime
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QLineEdit, QPushButton,
                            QDateTimeEdit, QStackedWidget, QGroupBox,
                            QRadioButton, QCheckBox, QTextEdit, QMessageBox, QDialog)
from PyQt5.QtCore import Qt, QDateTime

class NetworkEngineerInterviewAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Engineer Interview Assistant")
        self.setGeometry(100, 100, 800, 600)

        # Initialize data structures
        self.selected_difficulties = ["easy"]  # Default to easy questions
        self.current_question_index = -1
        self.results = {"correct": 0, "partially": 0, "incorrect": 0}
        self.questions = self.load_questions()
        self.current_questions = []  # Will hold the mixed questions
        self.current_questions = []  # Will hold the mixed questions

        # Create the main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Create stacked widget for different screens
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Create the interview setup page
        self.setup_interview_setup_page()

        # Create the interview session page
        self.setup_interview_session_page()

        # Show the first page
        self.stacked_widget.setCurrentIndex(0)

    def setup_interview_setup_page(self):
        setup_page = QWidget()
        layout = QVBoxLayout(setup_page)

        # Title
        title = QLabel("Network Engineer Interview Assistant")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Interview details group
        details_group = QGroupBox("Interview Details")
        details_layout = QVBoxLayout(details_group)

        # Interviewee name
        name_layout = QHBoxLayout()
        name_label = QLabel("Interviewee Name:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        details_layout.addLayout(name_layout)

        # Interview date and time
        datetime_layout = QHBoxLayout()
        datetime_label = QLabel("Date & Time:")
        self.datetime_input = QDateTimeEdit()
        self.datetime_input.setDateTime(QDateTime.currentDateTime())
        self.datetime_input.setCalendarPopup(True)
        datetime_layout.addWidget(datetime_label)
        datetime_layout.addWidget(self.datetime_input)
        details_layout.addLayout(datetime_layout)

        # Start button
        self.start_button = QPushButton("Start Interview")
        self.start_button.clicked.connect(self.start_interview)
        details_layout.addWidget(self.start_button)

        layout.addWidget(details_group)
        self.stacked_widget.addWidget(setup_page)

    def setup_interview_session_page(self):
        session_page = QWidget()
        layout = QVBoxLayout(session_page)

        # Interview info section
        info_layout = QHBoxLayout()
        self.display_name_label = QLabel("Interviewee: ")
        self.display_datetime_label = QLabel("Date & Time: ")
        info_layout.addWidget(self.display_name_label)
        info_layout.addWidget(self.display_datetime_label)
        layout.addLayout(info_layout)

        # Question type and difficulty selector
        selector_group = QGroupBox("Question Selection")
        selector_layout = QVBoxLayout(selector_group)

        # Question type selection
        type_layout = QHBoxLayout()
        type_label = QLabel("Question Type:")
        self.technical_button = QRadioButton("Technical")
        self.tactical_button = QRadioButton("Tactical/Scenario")
        self.technical_button.setChecked(True)

        self.technical_button.clicked.connect(self.update_question_type)
        self.tactical_button.clicked.connect(self.update_question_type)

        type_layout.addWidget(type_label)
        type_layout.addWidget(self.technical_button)
        type_layout.addWidget(self.tactical_button)
        selector_layout.addLayout(type_layout)

        # Difficulty selector (only for technical questions)
        self.difficulty_layout = QHBoxLayout()
        difficulty_label = QLabel("Difficulty Levels:")
        self.easy_checkbox = QCheckBox("Easy")
        self.medium_checkbox = QCheckBox("Medium")
        self.hard_checkbox = QCheckBox("Hard")
        self.mix_button = QPushButton("Mix Selected Difficulties")

        self.easy_checkbox.setChecked(True)

        self.easy_checkbox.clicked.connect(self.update_difficulty_selection)
        self.medium_checkbox.clicked.connect(self.update_difficulty_selection)
        self.hard_checkbox.clicked.connect(self.update_difficulty_selection)
        self.mix_button.clicked.connect(self.mix_questions)

        self.difficulty_layout.addWidget(difficulty_label)
        self.difficulty_layout.addWidget(self.easy_checkbox)
        self.difficulty_layout.addWidget(self.medium_checkbox)
        self.difficulty_layout.addWidget(self.hard_checkbox)
        self.difficulty_layout.addWidget(self.mix_button)
        self.mix_button.clicked.connect(self.mix_questions)

        self.difficulty_layout.addWidget(difficulty_label)
        self.difficulty_layout.addWidget(self.easy_checkbox)
        self.difficulty_layout.addWidget(self.medium_checkbox)
        self.difficulty_layout.addWidget(self.hard_checkbox)
        self.difficulty_layout.addWidget(self.mix_button)
        selector_layout.addLayout(self.difficulty_layout)

        layout.addWidget(selector_group)

        # Question section
        question_group = QGroupBox("Question")
        question_layout = QVBoxLayout(question_group)

        self.question_label = QLabel("Click 'Next Question' to begin")
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("font-size: 16px;")
        question_layout.addWidget(self.question_label)

        # Answer section
        self.show_answer_button = QPushButton("Show Answer")
        self.show_answer_button.clicked.connect(self.toggle_answer)
        question_layout.addWidget(self.show_answer_button)

        self.answer_text = QTextEdit()
        self.answer_text.setReadOnly(True)
        self.answer_text.setVisible(False)
        question_layout.addWidget(self.answer_text)

        # Evaluation section
        eval_group = QGroupBox("Evaluation")
        eval_layout = QHBoxLayout(eval_group)

        eval_label = QLabel("Did the candidate answer correctly?")
        self.correct_button = QPushButton("Correct")
        self.partially_button = QPushButton("Partially Correct")
        self.incorrect_button = QPushButton("Incorrect")

        self.correct_button.clicked.connect(lambda: self.evaluate_answer("correct"))
        self.partially_button.clicked.connect(lambda: self.evaluate_answer("partially"))
        self.incorrect_button.clicked.connect(lambda: self.evaluate_answer("incorrect"))

        eval_layout.addWidget(eval_label)
        eval_layout.addWidget(self.correct_button)
        eval_layout.addWidget(self.partially_button)
        eval_layout.addWidget(self.incorrect_button)
        question_layout.addWidget(eval_group)

        layout.addWidget(question_group)

        # Next question button
        self.next_question_button = QPushButton("Next Question")
        self.next_question_button.clicked.connect(self.next_question)
        layout.addWidget(self.next_question_button)

        # Results section
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout(results_group)

        self.results_label = QLabel("Correct: 0 | Partially Correct: 0 | Incorrect: 0")
        results_layout.addWidget(self.results_label)

        self.finish_button = QPushButton("Finish Interview")
        self.finish_button.clicked.connect(self.finish_interview)
        results_layout.addWidget(self.finish_button)

        layout.addWidget(results_group)

        self.stacked_widget.addWidget(session_page)

    def load_questions(self):
        """Load questions from the JSON file or return default questions if file not found."""
        json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'network_questions.json')

        try:
            with open(json_file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading questions file: {e}")
            QMessageBox.warning(
                self,
                "Questions File Error",
                f"Could not load questions from {json_file_path}. Using default questions instead."
            )

            # Return a minimal set of default questions as fallback
            return {
                "easy": [
                    {
                        "question": "What is the purpose of a subnet mask?",
                        "answer": "A subnet mask is used to divide an IP address into network and host portions."
                    }
                ],
                "medium": [
                    {
                        "question": "Explain the difference between TCP and UDP protocols.",
                        "answer": "TCP is connection-oriented and reliable, while UDP is connectionless and faster but unreliable."
                    }
                ],
                "hard": [
                    {
                        "question": "Explain BGP path selection process.",
                        "answer": "BGP selects paths based on attributes like weight, local preference, AS path length, origin, MED, and others in a specific order."
                    }
                ],
                "tactical": [
                    {
                        "question": "You receive a call from a user who can't access the company intranet but can browse external websites. How would you troubleshoot this issue?",
                        "answer": "1. Verify the user's network connectivity\n2. Check if the user can ping the intranet server\n3. Check DNS settings\n4. Verify proxy settings\n5. Check VPN requirements\n6. Verify firewall rules"
                    }
                ]
            }

    def start_interview(self):
        # Validate inputs
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Input Error", "Please enter the interviewee's name.")
            return

        # Update display labels
        self.display_name_label.setText(f"Interviewee: {self.name_input.text()}")
        self.display_datetime_label.setText(f"Date & Time: {self.datetime_input.dateTime().toString('yyyy-MM-dd hh:mm')}")

        # Switch to interview session page
        self.stacked_widget.setCurrentIndex(1)

    def update_question_type(self):
        if self.tactical_button.isChecked():
            # Hide difficulty options for tactical questions
            self.easy_checkbox.setEnabled(False)
            self.medium_checkbox.setEnabled(False)
            self.hard_checkbox.setEnabled(False)
            self.mix_button.setEnabled(False)

            # Set to tactical questions
            self.selected_difficulties = ["tactical"]
            self.mix_questions()
        else:
            # Re-enable difficulty options for technical questions
            self.easy_checkbox.setEnabled(True)
            self.medium_checkbox.setEnabled(True)
            self.hard_checkbox.setEnabled(True)
            self.mix_button.setEnabled(True)

            # Update selected difficulties based on checkboxes
            self.update_difficulty_selection()

        # Reset question index when type changes
        self.current_question_index = -1
        self.answer_text.setVisible(False)
        self.question_label.setText("Click 'Next Question' to begin")

    def update_difficulty_selection(self):
        """Update the list of selected difficulties based on checkbox states"""
        if not self.tactical_button.isChecked():  # Only update if in technical mode
            self.selected_difficulties = []

            if self.easy_checkbox.isChecked():
                self.selected_difficulties.append("easy")
            if self.medium_checkbox.isChecked():
                self.selected_difficulties.append("medium")
            if self.hard_checkbox.isChecked():
                self.selected_difficulties.append("hard")

            # Ensure at least one difficulty is selected
            if not self.selected_difficulties:
                self.easy_checkbox.setChecked(True)
                self.selected_difficulties = ["easy"]

    def mix_questions(self):
        """Mix questions from all selected difficulty levels"""
        self.current_questions = []

        # Get questions from each selected difficulty
        for difficulty in self.selected_difficulties:
            if difficulty in self.questions:
                # Add difficulty level to each question for display
                for question in self.questions[difficulty]:
                    q_copy = question.copy()
                    q_copy["difficulty"] = difficulty
                    self.current_questions.append(q_copy)

        # Shuffle the questions
        import random
        random.shuffle(self.current_questions)

        # Reset question index
        self.current_question_index = -1
        self.answer_text.setVisible(False)
        self.question_label.setText("Click 'Next Question' to begin")

        # Show confirmation
        difficulty_str = ", ".join(d.capitalize() for d in self.selected_difficulties)
        QMessageBox.information(self, "Questions Mixed",
                               f"Questions from {difficulty_str} difficulty levels have been mixed.\n\n"
                               f"Total questions in mix: {len(self.current_questions)}")

    def next_question(self):
        if not self.current_questions:
            # If current_questions is empty, mix questions first
            self.mix_questions()

        if not self.current_questions:
            QMessageBox.warning(self, "No Questions Available",
                               "No questions are available. Please select at least one difficulty level.")
            return

        # Move to next question or cycle back to beginning
        self.current_question_index = (self.current_question_index + 1) % len(self.current_questions)

        # Display the question
        current_question = self.current_questions[self.current_question_index]

        # Show difficulty level in the question display
        difficulty_display = ""
        if "difficulty" in current_question:
            difficulty_display = f"[{current_question['difficulty'].upper()}] "

        self.question_label.setText(f"{difficulty_display}{current_question['question']}")
        self.answer_text.setText(current_question["answer"])
        self.answer_text.setVisible(False)
        self.show_answer_button.setText("Show Answer")

    def toggle_answer(self):
        if self.answer_text.isVisible():
            self.answer_text.setVisible(False)
            self.show_answer_button.setText("Show Answer")
        else:
            self.answer_text.setVisible(True)
            self.show_answer_button.setText("Hide Answer")

    def evaluate_answer(self, result):
        self.results[result] += 1
        self.update_results_display()

        # Automatically move to next question
        self.next_question()

    def update_results_display(self):
        self.results_label.setText(
            f"Correct: {self.results['correct']} | "
            f"Partially Correct: {self.results['partially']} | "
            f"Incorrect: {self.results['incorrect']}"
        )

    def finish_interview(self):
        # Calculate statistics
        total = sum(self.results.values())
        if total == 0:
            QMessageBox.warning(self, "No Questions Answered",
                               "No questions have been answered yet. Please conduct the interview before finishing.")
            return

        correct_percentage = (self.results['correct'] / total) * 100
        partially_percentage = (self.results['partially'] / total) * 100
        incorrect_percentage = (self.results['incorrect'] / total) * 100
        weighted_score = (self.results['correct'] + (self.results['partially'] * 0.5)) / total * 100

        # Create dialog for notes
        notes_dialog = QDialog(self)
        notes_dialog.setWindowTitle("Interview Notes")
        notes_dialog.setMinimumWidth(600)
        notes_dialog.setMinimumHeight(500)

        layout = QVBoxLayout(notes_dialog)

        # Add performance summary at the top
        summary_label = QLabel(
            f"<b>Performance Summary:</b><br>"
            f"Total Questions: {total}<br>"
            f"Correct: {self.results['correct']} ({correct_percentage:.1f}%)<br>"
            f"Partially Correct: {self.results['partially']} ({partially_percentage:.1f}%)<br>"
            f"Incorrect: {self.results['incorrect']} ({incorrect_percentage:.1f}%)<br>"
            f"Overall Score: {weighted_score:.1f}%"
        )
        layout.addWidget(summary_label)

        # Technical knowledge notes
        tech_group = QGroupBox("Technical Knowledge Notes")
        tech_layout = QVBoxLayout(tech_group)
        tech_notes = QTextEdit()
        tech_notes.setPlaceholderText("Enter notes about the candidate's technical knowledge...")
        tech_layout.addWidget(tech_notes)
        layout.addWidget(tech_group)

        # Problem-solving notes
        problem_group = QGroupBox("Problem-Solving Skills Notes")
        problem_layout = QVBoxLayout(problem_group)
        problem_notes = QTextEdit()
        problem_notes.setPlaceholderText("Enter notes about the candidate's problem-solving abilities...")
        problem_layout.addWidget(problem_notes)
        layout.addWidget(problem_group)

        # Communication notes
        comm_group = QGroupBox("Communication Skills Notes")
        comm_layout = QVBoxLayout(comm_group)
        comm_notes = QTextEdit()
        comm_notes.setPlaceholderText("Enter notes about the candidate's communication skills...")
        comm_layout.addWidget(comm_notes)
        layout.addWidget(comm_group)

        # Recommendation
        rec_group = QGroupBox("Hiring Recommendation")
        rec_layout = QVBoxLayout(rec_group)
        rec_notes = QTextEdit()
        rec_notes.setPlaceholderText("Enter your hiring recommendation...")
        rec_layout.addWidget(rec_notes)
        layout.addWidget(rec_group)

        # Additional notes
        add_group = QGroupBox("Additional Notes")
        add_layout = QVBoxLayout(add_group)
        add_notes = QTextEdit()
        add_notes.setPlaceholderText("Enter any additional notes or observations...")
        add_layout.addWidget(add_notes)
        layout.addWidget(add_group)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save Report")
        cancel_button = QPushButton("Cancel")

        save_button.clicked.connect(notes_dialog.accept)
        cancel_button.clicked.connect(notes_dialog.reject)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        # Show dialog and process result
        result = notes_dialog.exec_()

        if result == QDialog.Accepted:
            # Create a detailed report
            report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      f"interview_report_{self.name_input.text().replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

            try:
                with open(report_path, 'w') as report_file:
                    report_file.write(f"NETWORK ENGINEER INTERVIEW REPORT\n")
                    report_file.write(f"==============================\n\n")
                    report_file.write(f"Interviewee: {self.display_name_label.text()[12:]}\n")
                    report_file.write(f"Date & Time: {self.display_datetime_label.text()[11:]}\n\n")
                    report_file.write(f"PERFORMANCE SUMMARY\n")
                    report_file.write(f"------------------\n")
                    report_file.write(f"Total Questions Answered: {total}\n")
                    report_file.write(f"Correct Answers: {self.results['correct']} ({correct_percentage:.1f}%)\n")
                    report_file.write(f"Partially Correct Answers: {self.results['partially']} ({partially_percentage:.1f}%)\n")
                    report_file.write(f"Incorrect Answers: {self.results['incorrect']} ({incorrect_percentage:.1f}%)\n\n")
                    report_file.write(f"Overall Score: {weighted_score:.1f}%\n\n")
                    report_file.write(f"EVALUATION NOTES\n")
                    report_file.write(f"--------------\n")
                    report_file.write(f"Technical Knowledge:\n{tech_notes.toPlainText() or '[No notes provided]'}\n\n")
                    report_file.write(f"Problem-Solving Skills:\n{problem_notes.toPlainText() or '[No notes provided]'}\n\n")
                    report_file.write(f"Communication Skills:\n{comm_notes.toPlainText() or '[No notes provided]'}\n\n")
                    report_file.write(f"RECOMMENDATION\n")
                    report_file.write(f"-------------\n")
                    report_file.write(f"{rec_notes.toPlainText() or '[No recommendation provided]'}\n\n")

                    if add_notes.toPlainText():
                        report_file.write(f"ADDITIONAL NOTES\n")
                        report_file.write(f"---------------\n")
                        report_file.write(f"{add_notes.toPlainText()}\n")

                summary = (
                    f"Interview Summary for {self.display_name_label.text()[12:]}\n\n"
                    f"Total Questions: {total}\n"
                    f"Correct: {self.results['correct']} ({correct_percentage:.1f}%)\n"
                    f"Partially Correct: {self.results['partially']} ({partially_percentage:.1f}%)\n"
                    f"Incorrect: {self.results['incorrect']} ({incorrect_percentage:.1f}%)\n\n"
                    f"Overall Score: {weighted_score:.1f}%\n\n"
                    f"Interview conducted on: {self.display_datetime_label.text()[11:]}\n\n"
                    f"Detailed report saved to:\n{report_path}"
                )

                QMessageBox.information(self, "Interview Complete", summary)

                # Reset and go back to setup page
                self.name_input.clear()
                self.datetime_input.setDateTime(QDateTime.currentDateTime())
                self.results = {"correct": 0, "partially": 0, "incorrect": 0}
                self.current_question_index = -1
                self.update_results_display()
                self.stacked_widget.setCurrentIndex(0)

            except Exception as e:
                QMessageBox.critical(self, "Error Saving Report", f"Failed to save detailed report: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = NetworkEngineerInterviewAssistant()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
