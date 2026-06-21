# Agentic AI Personal Finance Assistant

## Overview

Agentic AI Personal Finance Assistant is an intelligent financial management application that helps users track expenses, analyze spending patterns, and receive personalized financial recommendations. By leveraging Large Language Models (LLMs), the system acts as an AI agent that can understand financial data, generate insights, and assist users in making better financial decisions.

The application provides an interactive dashboard where users can monitor their spending habits, compare expenses against budgets, and receive actionable suggestions to improve their financial health.

---

## Features

### Expense Tracking

* Record and categorize financial transactions.
* Monitor daily, weekly, and monthly expenses.
* Maintain a structured view of spending history.

### Budget Analysis

* Compare actual spending against planned budgets.
* Identify overspending categories.
* Track financial goals effectively.

### AI-Powered Insights

* Analyze spending behavior using AI.
* Generate personalized financial recommendations.
* Suggest cost-saving opportunities and budgeting strategies.

### Data Visualization

* Interactive charts and graphs for financial analysis.
* Visual representation of spending trends.
* Easy-to-understand financial reports.

### Agentic Decision Support

* Understand user financial data.
* Reason about spending patterns.
* Provide intelligent recommendations and next-step actions.

---

## System Architecture

1. **Data Collection Layer**

   * Collects transaction and budget information.

2. **Data Processing Layer**

   * Cleans and organizes financial data using Pandas.

3. **AI Reasoning Layer**

   * Uses a Large Language Model through the Groq API to analyze financial information and generate insights.

4. **Visualization Layer**

   * Displays reports, charts, and recommendations using Streamlit and Plotly.

---

## Tech Stack

* Python
* Streamlit
* Pandas
* Plotly
* Groq API
* NumPy

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/KotiSai-Sankar/Agentic-Ai-Personal-Finance-Assistant.git
cd Agentic-Ai-Personal-Finance-Assistant
```

### Create a Virtual Environment

```bash
python -m venv .venv
```

### Activate the Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### macOS/Linux

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
streamlit run app.py
```

The application will launch in your browser at:

```text
http://localhost:8501
```

---

## Project Workflow

1. User provides financial transaction data.
2. Data is processed and categorized.
3. AI agent analyzes spending behavior.
4. Budget comparisons are performed.
5. Personalized recommendations are generated.
6. Insights are displayed through interactive dashboards.

---

## Future Enhancements

* Multi-user authentication
* Real-time bank transaction integration
* Investment tracking module
* Savings goal prediction
* Voice-enabled financial assistant
* Multi-agent financial planning system

---

## Learning Outcomes

Through this project, I gained experience in:

* Agentic AI concepts
* Large Language Model integration
* Financial data analysis
* Data visualization
* Prompt engineering
* Streamlit application development
* API integration
* End-to-end AI project deployment

---

## Author

**Uddandi Koti Sai Sankar**

GitHub: https://github.com/KotiSai-Sankar

---

## License

This project is developed for educational and learning purposes.
