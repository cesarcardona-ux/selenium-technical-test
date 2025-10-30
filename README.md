# Selenium Technical Test - FLYR Inc

Automated testing suite for nuxqa web application using Selenium WebDriver, Python, and pytest.

## Quick Start

### Prerequisites
- Python 3.9+
- Chrome, Edge, and Firefox browsers
- Git

### Setup

```bash
# Clone repository
git clone https://github.com/cesarcardona-ux/selenium-technical-test.git
cd selenium-technical-test

# Create virtual environment
python -m venv venv
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Running Tests

### Basic Execution

```bash
# Run all implemented tests
pytest tests/

# Run specific case with all combinations
pytest tests/nuxqa/test_language_change_Case4.py

# Generate Allure report
pytest tests/
allure serve reports/allure
```

### CLI Options

| Option          | Values                                     | Description                                   |
|-----------------|--------------------------------------------|-----------------------------------------------|
| `--browser`     | chrome, edge, firefox, all                 | Browser selection (default: all)              |
| `--language`    | Español, English, Français, Português, all | Language selection (default: all)             |
| `--env`         | qa4, qa5, all                              | Environment selection (default: all)          |
| `--screenshots` | none, on-failure, all                      | Screenshot capture mode (default: on-failure) |
| `--video`       | none, enabled                              | Video recording (default: none)               |

**Example with options:**
```bash
pytest tests/nuxqa/test_language_change_Case4.py --browser=chrome --language=English --env=qa5 --video=enabled --screenshots=all
```

**Parallel execution:**
```bash
pytest tests/ -n auto
```

## Test Cases Status

| Case   | Status       | Description               | Tests |
|--------|--------------|---------------------------|-----|
| Case 4 | ✅ Complete | Language Change Validation | 24 |
| Case 5 | ⏳ Pending  | POS Change Validation      | -  |
| Case 6 | ⏳ Pending  | Header Redirections        | -  |
| Case 7 | ⏳ Pending  | Footer Redirections        | -  |
| Case 3 | ⏳ Pending  | Login and Network Capture  | -  |
| Case 1 | ⏳ Pending  | One-way Booking            | -  |
| Case 2 | ⏳ Pending  | Round-trip Booking         | -  |

### Case 4: Language Change Validation ✅
- **Languages:** Spanish, English, French, Portuguese
- **Browsers:** Chrome, Edge, Firefox
- **Environments:** QA4, QA5
- **Total combinations:** 24 tests
- **File:** `tests/nuxqa/test_language_change_Case4.py`

## Technical Implementation

### Features
- ✅ Page Object Model (POM)
- ✅ Multi-browser support (Chrome, Edge, Firefox)
- ✅ Parametrized tests with pytest
- ✅ Allure reporting with screenshots and video
- ✅ SQLite database for results tracking
- ✅ Detailed logging
- ✅ Parallel execution (pytest-xdist)
- ✅ Video evidence (MP4 with OpenCV)

### Project Structure
```
├── pages/                  # Page Objects
├── tests/                  # Test cases
├── utils/                  # Database and utilities
├── Docs/                   # Additional documentation
├── conftest.py             # Pytest configuration
└── requirements.txt        # Dependencies
```

### Test Results

**Allure Report:**
```bash
allure serve reports/allure
```

**Database:** Test results are saved to `test_results.db`

**Logs:** Detailed execution logs in `reports/test_execution.log`

## Repository

https://github.com/cesarcardona-ux/selenium-technical-test

---

🤖 *Generated with Claude Code*
