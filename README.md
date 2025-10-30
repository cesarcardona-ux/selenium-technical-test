# Selenium Technical Test - FLYR Inc

Automated testing suite for nuxqa web application using Selenium WebDriver, Python, and pytest.

---------------------------------------

## Requirements

- Python 3.9+
- Google Chrome browser
- Microsoft Edge browser
- Mozilla Firefox browser
- Git

---------------------------------------

## Setup Instructions

### Windows

1. **Clone the repository**
   ```bash
   git clone https://github.com/cesarcardona-ux/selenium-technical-test.git
   cd selenium-technical-test
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### MacOS / Linux

1. **Clone the repository**
   ```bash
   git clone https://github.com/cesarcardona-ux/selenium-technical-test.git
   cd selenium-technical-test
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---------------------------------------

## Running Tests

### CLI Options

This test suite supports flexible execution with custom CLI options:

**--browser**: Choose browser (default: all)
- `chrome` - Run tests only in Chrome
- `edge` - Run tests only in Edge
- `firefox` - Run tests only in Firefox
- `all` - Run tests in all browsers

**--language**: Choose language (default: all)
- `Español`, `English`, `Français`, `Português` - Specific language
- `all` - Test all languages

**--env**: Choose environment (default: all)
- `qa4` - Run tests only on QA4 environment
- `qa5` - Run tests only on QA5 environment
- `all` - Run tests on both environments

**--screenshots**: Screenshot capture mode (default: on-failure)
- `none` - No screenshots
- `on-failure` - Capture screenshots only when tests fail
- `all` - Capture screenshots at every test step

**--video**: Video recording mode (default: none)
- `none` - No video recording
- `enabled` - Record full test execution video (MP4 format)

### Examples

**Run all tests (all browsers, all languages, all environments)**
```bash
pytest tests/
```

**Run specific test case with all combinations**
```bash
pytest tests/nuxqa/test_language_change_Case4.py --browser=all --language=all --env=all -v
```

**Run tests in Chrome only with English on QA4**
```bash
pytest tests/nuxqa/test_language_change_Case4.py --browser=chrome --language=English --env=qa4 -v
```

**Run tests in Firefox with all languages on QA5**
```bash
pytest tests/nuxqa/test_language_change_Case4.py --browser=firefox --language=all --env=qa5 -v
```

**Run tests in parallel (all browsers)**
```bash
pytest tests/ -n auto
```

**Run tests with video recording and full screenshots**
```bash
pytest tests/nuxqa/test_language_change_Case4.py --video=enabled --screenshots=all --alluredir=reports/allure
```

**Run tests with video but no screenshots**
```bash
pytest tests/nuxqa/test_language_change_Case4.py --video=enabled --screenshots=none
```

**Generate and view Allure report**
```bash
pytest tests/
allure serve reports/allure
```

---------------------------------------

## Implemented Test Cases

### ✅ Case 4: Language Change Validation (5 pts)
- **Description:** Validates language switching functionality
- **Languages tested:** Spanish, English, French, Portuguese
- **Browsers:** Chrome, Edge, Firefox
- **Environments:** QA4 and QA5
- **Total tests:** 24 (4 languages × 2 environments × 3 browsers)
- **File:** `tests/nuxqa/test_language_change_Case4.py`

**Run this case:**
```bash
pytest tests/nuxqa/test_language_change_Case4.py --browser=all --language=all --env=all -v
```

---------------------------------------

## Pending Test Cases

- ⏳ Case 5: POS Change Validation (5 pts)
- ⏳ Case 6: Header Redirections (5 pts)
- ⏳ Case 7: Footer Redirections (5 pts)
- ⏳ Case 3: Login and Network Capture (10 pts)
- ⏳ Case 1: One-way Booking (15 pts)
- ⏳ Case 2: Round-trip Booking (15 pts)

---------------------------------------

## Technical Requirements Compliance

- ✅ Allure Reports (10 pts)
- ✅ Detailed Logging (5 pts)
- ✅ SQLite Database (5 pts)
- ✅ QA4 and QA5 Environments (5 pts)
- ✅ Parallel Execution with xdist (5 pts)
- ✅ Clear Assertions (5 pts)
- ✅ Page Object Model (POM)
- ✅ Multiple Browsers (Chrome, Edge, Firefox)
- ✅ Video Evidence (15 pts - Optional) - MP4 recording with OpenCV

---------------------------------------

## Project Structure

```
├── pages/              # Page Objects (POM)
│   └── nuxqa/
│       └── home_page.py
├── tests/              # Test cases
│   └── nuxqa/
│       └── test_language_change_Case4.py
├── utils/              # Utilities
│   └── database.py     # SQLite integration
├── Docs/               # Documentation
├── reports/            # Test reports (not in repo)
├── conftest.py         # Pytest configuration
├── pytest.ini          # Pytest settings
└── requirements.txt    # Dependencies
```

---------------------------------------

## View Test Results

### Allure Report
After running tests, view the interactive HTML report:
```bash
allure serve reports/allure
```

### SQLite Database
Test results are saved to `test_results.db` (not in repo).

### Logs
Detailed execution logs are saved to `reports/test_execution.log`.

---------------------------------------

## Notes

- Virtual environment (`venv/`) is excluded from repository
- Test reports (`reports/`) are excluded from repository
- Database files (`*.db`) are excluded from repository
- Browser drivers are automatically managed:
  - ChromeDriver via webdriver-manager
  - EdgeDriver via Selenium Manager (built-in)
  - GeckoDriver via webdriver-manager

---------------------------------------

## Repository

https://github.com/cesarcardona-ux/selenium-technical-test

---------------------------------------

🤖 *Generated with Claude Code*
