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

### Driver Management

This project uses **Selenium Manager** (included in Selenium 4.6+) to automatically download and manage browser drivers.

**What does this mean?**
- No manual driver installation needed
- Works with any Chrome/Edge/Firefox version
- Automatically downloads the correct driver when you run tests

**Why Selenium Manager?**
During development, we found that Chrome updated to version 141, but external tools could only download drivers up to version 114. Selenium Manager solves this by always getting the correct driver version directly from the browser vendors.

**For evaluators:** You don't need to download or configure drivers manually. Just install the requirements and run the tests.

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

| Option            | Values                                                  | Description                                   |
|-------------------|---------------------------------------------------------|-----------------------------------------------|
| `--browser`       | chrome, edge, firefox, all                              | Browser selection (default: all)              |
| `--language`      | Español, English, Français, Português, all              | Language selection (default varies by case)   |
| `--pos`           | Chile, España, Otros países, all                        | POS selection (default: all)                  |
| `--header-link`   | ofertas-vuelos, credits, equipaje, all                  | Header link selection (default: all)          |
| `--footer-link`   | vuelos, noticias, aviancadirect, contactanos, all       | Footer link selection (default: all)          |
| `--env`           | qa4, qa5, uat1, all                                     | Environment selection (default: all)          |
| `--origin`        | BOG, MDE, CLO, MAD, etc. (IATA codes)                   | Origin airport (Case 3, default: BOG)         |
| `--destination`   | BOG, MDE, CLO, MAD, etc. (IATA codes)                   | Destination airport (Case 3, default: MDE)    |
| `--departure-days`| Integer (days from today)                               | Departure date offset (Case 3, default: 4)    |
| `--return-days`   | Integer (days from today)                               | Return date offset (Case 3, default: 5)       |
| `--screenshots`   | none, on-failure, all                                   | Screenshot capture mode (default: on-failure) |
| `--video`         | none, enabled                                           | Video recording (default: none)               |

**Note on `--language` parameter:**
- **Case 4**: Default is `all` (tests all 4 languages)
- **Cases 6 & 7**: Default is random language selection per test
  - Omit `--language` for random selection
  - Use `--language=English` (or other language) for specific language
  - Use `--language=all` to test all 4 languages

**Examples with options:**
```bash
# Case 4: Language change
pytest tests/nuxqa/test_language_change_Case4.py --browser=chrome --language=English --env=qa5 --video=enabled --screenshots=all

# Case 5: POS change
pytest tests/nuxqa/test_pos_change_Case5.py --browser=chrome --pos=Chile --env=qa5 --video=enabled --screenshots=all

# Case 6: Header redirections (random language)
pytest tests/nuxqa/test_header_redirections_Case6.py --browser=chrome --header-link=ofertas-vuelos --env=qa5 -v

# Case 6: Header redirections (specific language)
pytest tests/nuxqa/test_header_redirections_Case6.py --browser=chrome --header-link=ofertas-vuelos --env=qa5 --language=Français -v

# Case 6: Header redirections (all languages - generates 4 tests)
pytest tests/nuxqa/test_header_redirections_Case6.py --browser=chrome --header-link=ofertas-vuelos --env=qa5 --language=all -v

# Case 7: Footer redirections (random language)
pytest tests/nuxqa/test_footer_redirections_Case7.py --browser=chrome --footer-link=noticias --env=qa5 -v

# Case 7: Footer redirections (specific language)
pytest tests/nuxqa/test_footer_redirections_Case7.py --browser=chrome --footer-link=noticias --env=qa5 --language=English -v

# Case 3: Flight search and network capture (dynamic dates and cities)
pytest tests/nuxqa/test_login_network_Case3.py --browser=chrome --origin=BOG --destination=MDE --departure-days=4 --return-days=5 --env=uat1 -v

# Case 3: With video and Allure report
pytest tests/nuxqa/test_login_network_Case3.py --browser=chrome --origin=BOG --destination=MAD --departure-days=7 --return-days=10 --env=uat1 --video=enabled --screenshots=all --alluredir=reports/allure
```

**Parallel execution:**
```bash
pytest tests/ -n auto
```

## Test Cases Status

| Case   | Status       | Description                        | Tests |
|--------|--------------|-----------------------------------|-------|
| Case 3 | ✅ Complete | Flight Search & Network Capture    |   2  |
| Case 4 | ✅ Complete | Language Change Validation         |  24  |
| Case 5 | ✅ Complete | POS Change Validation              |  18  |
| Case 6 | ✅ Complete | Header Redirections                |  18  |
| Case 7 | ✅ Complete | Footer Redirections                |  24  |
| Case 1 | ⏳ Pending  | One-way Booking                    |  -   |
| Case 2 | ⏳ Pending  | Round-trip Booking                 |  -   |

### Case 3: Flight Search & Network Capture ✅
- **Environment:** UAT1 (nuxqa.avtest.ink)
- **Language/POS:** French, France
- **Flight Search:** Dynamic dates (TODAY + N days), parametrizable cities (IATA codes)
- **Flight Selection:** 4 clicks - Outbound FLEX, Return FLEX
- **Passengers:** 9 (3 adults + 3 teens + 3 children)
- **Network Capture:** Chrome DevTools Protocol (CDP) for Session JSON extraction
- **Extracted Fields:** origin, destination, std, productClass (4 fields from PDF requirements)
- **Browsers:** Chrome ✅, Edge ✅ (Chromium-based only - CDP limitation)
- **Total tests:** 2 (Chrome + Edge)
- **File:** `tests/nuxqa/test_login_network_Case3.py`
- **CLI Parameters:** `--origin`, `--destination`, `--departure-days`, `--return-days`

**Technical Highlights:**
- Real-time network capture using CDP (captures response bodies immediately)
- Dynamic date calculation to prevent test failures on future dates
- Complex flight selection with 25-30 second page loader handling
- Text-based filtering for return flights ("Choisir le tarif")
- Session JSON parsing from nested structure: `response.result.data.journeys[]`
- Dedicated Allure attachment for PDF-required fields
- 7 additional database fields for Case 3 tracking

**Browser Compatibility:**
- ✅ Chrome: Fully functional with CDP
- ✅ Edge: Fully functional with CDP
- ❌ Firefox: Not supported (CDP is Chromium-only)

### Case 4: Language Change Validation ✅
- **Languages:** Spanish, English, French, Portuguese
- **Browsers:** Chrome, Edge, Firefox
- **Environments:** QA4, QA5
- **Total combinations:** 24 tests
- **File:** `tests/nuxqa/test_language_change_Case4.py`

### Case 5: POS Change Validation ✅
- **POS:** Chile, España, Otros países
- **Browsers:** Chrome, Edge, Firefox
- **Environments:** QA4, QA5
- **Total combinations:** 18 tests
- **File:** `tests/nuxqa/test_pos_change_Case5.py`

### Case 6: Header Redirections with Language Validation ✅
- **Header Links:** Ofertas de vuelos, Avianca Credits, Equipaje
- **Language Validation:** Random selection (Español, English, Français, Português) with URL code verification
- **Browsers:** Chrome, Edge, Firefox
- **Environments:** QA4, QA5
- **Total combinations:** 18 tests (3 links × 3 browsers × 2 envs)
- **File:** `tests/nuxqa/test_header_redirections_Case6.py`

### Case 7: Footer Redirections with Language Validation ✅
- **Footer Links:** Vuelos baratos, Noticias corporativas, aviancadirect, Contáctanos
- **Language Validation:** Random selection (Español, English, Français, Português) with URL code verification
- **Browsers:** Chrome, Edge, Firefox
- **Environments:** QA4, QA5
- **Total combinations:** 24 tests (4 links × 3 browsers × 2 envs)
- **File:** `tests/nuxqa/test_footer_redirections_Case7.py`

## Technical Implementation

### Features
- ✅ Page Object Model (POM)
- ✅ Multi-browser support (Chrome, Edge, Firefox)
- ✅ Parametrized tests with pytest
- ✅ Allure reporting with rich visualizations
- ✅ Video recording (MP4 with OpenCV)
- ✅ Screenshot capture (configurable modes)
- ✅ SQLite database for results tracking
- ✅ Detailed logging
- ✅ Parallel execution (pytest-xdist)

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

### Database Schema

Test results are stored in SQLite with **30 comprehensive fields** for detailed tracking and analysis:

**General Fields (10):**
- `id`: Primary key
- `case_number`: Test case number (3, 4, 5, 6, 7) - positioned as 2nd column for easy filtering
- `test_name`: Unique test identifier
- `status`: Test result (PASSED, FAILED, SKIPPED)
- `execution_time`: Duration in seconds
- `error_message`: Error details if failed
- `timestamp`: Execution date/time
- `browser`: Browser used (chrome, edge, firefox)
- `url`: Final URL after test action
- `language`: Language used in test

**Tracking Fields (7):**
- `environment`: Test environment (qa4, qa5, uat1)
- `screenshots_mode`: Screenshot configuration (none, on-failure, all)
- `video_enabled`: Video recording status (enabled, none)
- `expected_value`: Expected validation value
- `actual_value`: Actual value retrieved
- `validation_result`: Validation outcome (PASSED, FAILED)
- `initial_url`: URL before test action

**Cases 4, 5, 6, 7 Specific Fields (6):**
- `pos`: Case 5 - POS selected (Chile, España, Otros países)
- `header_link`: Case 6 - Header link tested
- `footer_link`: Case 7 - Footer link tested
- `link_name`: Cases 6&7 - Descriptive link name
- `language_mode`: Cases 6&7 - Language selection mode (Random, Specific, All Languages)
- `validation_message`: Detailed validation message

**Case 3 Specific Fields (7):**
- `origin_city`: Origin airport IATA code (BOG, MDE, etc.)
- `destination_city`: Destination airport IATA code
- `departure_date`: Calculated departure date (TODAY + N days)
- `return_date`: Calculated return date (TODAY + N days)
- `passenger_count`: Total passengers (adults + teens + children)
- `session_journey_count`: Number of journeys extracted from Session JSON (should be 2)
- `session_data_json`: Complete Session JSON data with all extracted fields

**Benefits:**
- Advanced SQL queries for analysis
- Complete test traceability
- Easy debugging with expected vs actual values
- Configuration tracking per test
- Case-specific data properly structured

**Example queries:**
```sql
-- Filter by environment
SELECT * FROM test_executions WHERE environment = 'qa5';

-- Filter by case number
SELECT * FROM test_executions WHERE case_number = 3;

-- Filter by POS (Case 5)
SELECT * FROM test_executions WHERE pos = 'Chile';

-- Filter by language mode (Cases 6&7)
SELECT * FROM test_executions WHERE language_mode = 'Random';

-- Filter by origin/destination (Case 3)
SELECT * FROM test_executions WHERE origin_city = 'BOG' AND destination_city = 'MDE';

-- View Case 3 session data
SELECT test_name, session_journey_count, session_data_json FROM test_executions WHERE case_number = 3;
```

**Logs:** Detailed execution logs in `reports/test_execution.log`

## Repository

https://github.com/cesarcardona-ux/selenium-technical-test

---

🤖 *Generated with Claude Code*
