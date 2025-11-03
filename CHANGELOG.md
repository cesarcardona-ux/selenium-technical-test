# Changelog

All notable changes and milestones for this automation project will be documented in this file.

---

## [v1.2.1-dev] - 2025-11-03

### 🐛 Critical Fix: Payment Page Iframe Handling

This release implements **critical iframe handling** for the Payment page in Case 1, resolving cookie modal and payment gateway iframe issues.

### 🔧 Payment Page Iframe Implementation

#### Problem Discovery
During Case 1 testing, two critical issues were identified on the Payment page:

1. **Cookie Consent Modal Blocking Forms**:
   - OneTrust cookie consent modal appeared as overlay with dark background
   - Modal prevented interaction with payment form fields
   - Button `#onetrust-accept-btn-handler` was in separate iframe or main DOM

2. **Payment Form Fields Not Found**:
   - After accepting cookies, card form fields (Holder, Card Number, CVV, Expiration) were not detectable
   - Critical discovery: Fields are NOT in main Payment page DOM
   - Fields hosted in external payment gateway iframe: `api-pay.avtest.ink`
   - Iframe class: `payment-forms-layout_iframe`
   - Implemented for PCI compliance (secure credit card data handling)

#### Solution Implemented

**1. Dual-Strategy Cookie Modal Detection**:
- **Strategy 1**: Search for button in main DOM
- **Strategy 2**: If not found, search in OneTrust iframe and switch context
- Proper context switching: Main DOM → Cookie Iframe → Click → Return to Main DOM
- Modal completely disappears before proceeding

**2. Payment Gateway Iframe Context Switching**:
```
Main DOM → Accept Cookies → Return to Main DOM →
Wait 15s for Angular to inject iframe →
Switch to Payment Iframe → Fill Card Fields →
Return to Main DOM → Fill Billing Fields
```

**3. Implementation Details**:
- Added 15-second wait for Angular to inject payment iframe into DOM
- Detect iframe using `By.CLASS_NAME, "payment-forms-layout_iframe"`
- Wait for iframe presence with `WebDriverWait(30)`
- Switch to iframe context with `driver.switch_to.frame(payment_iframe)`
- Fill card fields with explicit waits inside iframe
- Switch back to main DOM with `driver.switch_to.default_content()`
- Fill billing fields (email, address, city, country) in main DOM
- All context switches properly logged for debugging

#### Files Modified

**pages/nuxqa/payment_page.py** (lines 97-352):
- Added 15s Angular wait before iframe detection
- Implemented dual-strategy cookie modal detection (lines 102-196)
- Added payment iframe detection and context switching (lines 214-257)
- Modified `fill_credit_card_info()` to work inside iframe (lines 248-334)
- Updated `fill_billing_info()` documentation for main DOM (lines 336-352)

**README.md**:
- Updated Case 1 section with "Critical Payment Page Implementation"
- Documented cookie modal handling strategy
- Documented payment gateway iframe discovery
- Added context switching flow diagram
- Explained why iframe handling is necessary

#### Technical Achievements

- ✅ Cookie modal successfully detected and clicked in both contexts
- ✅ Payment iframe correctly identified and context switched
- ✅ Card fields successfully filled inside iframe
- ✅ Billing fields successfully filled in main DOM
- ✅ Complete test flow executes end-to-end
- ✅ Comprehensive logging for debugging iframe issues

#### Testing Status

- **First successful execution**: Test completed with exit code 0
- **Full flow verified**: Home → Select Flight → Passengers → Seatmap → Payment (form filled)
- **Pending**: Full end-to-end validation with payment submission

### 📝 Key Learnings

**Why This Was Critical**:
- Using `driver.find_element()` directly on Payment page will NOT find card fields
- Must explicitly detect and switch to payment gateway iframe
- Cookie modals may be in separate iframe (OneTrust framework)
- Context switching must be properly managed (switch to iframe → action → switch back)
- Angular applications may inject iframes dynamically (require wait time)

**For Future Implementations**:
- Always check if elements are inside iframes when not found in main DOM
- Payment gateways commonly use iframes for PCI compliance
- Cookie consent frameworks (OneTrust, CookieBot) often use separate iframes
- Use dual-strategy detection for elements that may be in multiple contexts

---

## [v1.2.0-dev] - 2025-10-31

### 🎯 Case 1 Framework Implementation - One-way Booking

This release adds the **complete framework for Case 1: One-way Booking**, bringing the project closer to full completion.

### ✅ Case 1 Implementation (In Development)

#### One-way Booking - Complete Flow
- **Flow**: 6 pages (Home → Select Flight → Passengers → Services → Seatmap → Payment)
- **Browsers**: Chrome, Edge, Firefox (to be tested)
- **Environments**: QA4, QA5
- **Total tests**: TBD (pending parametrization testing)
- **Status**: 🚧 Framework complete, pending first execution and adjustments

**Key Features:**
- **Complete 6-Page Flow**: Full booking automation from search to payment
- **4 Passenger Types**: Adult, Teen, Child, Infant (1 of each)
- **Flight Type**: One-way (Solo ida)
- **Fare Selection**: Basic (lowest tier)
- **Services**: Skip all services (as per Case 1 requirements)
- **Seat Selection**: Economy seat
- **Payment**: Fake credit card data (rejection is acceptable)

**New Page Objects Created (4 total):**
- `pages/nuxqa/passengers_page.py` (315 lines) - Passenger information handling
- `pages/nuxqa/services_page.py` (280 lines) - Services selection/skipping
- `pages/nuxqa/seatmap_page.py` (290 lines) - Seat map and seat selection
- `pages/nuxqa/payment_page.py` (360 lines) - Payment form filling

**New Test File:**
- `tests/nuxqa/test_oneway_booking_Case1.py` (550+ lines) - Complete one-way booking flow

**Technical Achievements:**
- **Passenger Data Handling**: Dynamic forms for 4 different passenger types
- **Service Skipping Logic**: Intelligent detection of skip buttons vs continue
- **Seat Map Interaction**: Economy seat selection with fallback strategies
- **Payment Form Automation**: Credit card and billing information filling
- **Comprehensive Logging**: Detailed logs for each page and action
- **Allure Integration**: 7-step flow with attachments for each page
- **Database Tracking**: Reuses existing 30-field schema

**Pending Work:**
- First test execution
- Selector adjustments based on actual page structure
- Flight search methods implementation in HomePage
- Basic fare selection method in SelectFlightPage
- Cross-browser testing
- Parametrization testing

### 📊 Updated Statistics

- **Completed Cases**: 5/7 (Cases 3, 4, 5, 6, 7 complete; Case 1 in development)
- **Total Page Objects**: 8 (home, login, select_flight, passengers, services, seatmap, payment, network_capture)
- **Total Test Files**: 6 (1 in development + 5 complete)
- **Lines of Code Added**: ~1,800 (4 page objects + 1 test file)

### 🔜 Next Steps

- Execute Case 1 for first time
- Adjust selectors based on actual page behavior
- Complete HomePage search methods
- Complete SelectFlightPage Basic fare selection
- Cross-browser validation
- Move Case 1 from 🚧 to ✅

---

## [v1.1.0] - 2025-10-31

### 🎯 Case 3 Complete - Flight Search & Network Capture

This release adds **Case 3: Flight Search and Network Capture** to the automation suite, bringing the total completed cases to **5 out of 7**.

### ✅ Case 3 Implementation

#### Flight Search & Network Session Capture
- **Environment**: UAT1 (nuxqa.avtest.ink)
- **Language/POS**: French, France
- **Browsers**: Chrome ✅, Edge ✅ (CDP-compatible only)
- **Total tests**: 2 combinations
- **Status**: ✅ 100% PASSED

**Key Features:**
- **Dynamic Date Calculation**: Dates relative to TODAY (TODAY + N days) to prevent test failures
- **Parametrizable Cities**: IATA codes via CLI (--origin, --destination)
- **Complex Flight Selection**: 4-click workflow with FLEX plan selection
  1. Select outbound flight
  2. Select FLEX plan for outbound
  3. Select return flight (with 25-30s page loader wait)
  4. Select FLEX plan for return
- **Chrome DevTools Protocol (CDP)**: Real-time network traffic capture
- **Session JSON Extraction**: 4 PDF-required fields from nested JSON structure
  - `origin`
  - `destination`
  - `std` (Standard Departure Time)
  - `productClass`

**Technical Achievements:**
- **Network Capture**: Real-time response body capture using CDP to avoid Chrome cache issues
- **Text-based Filtering**: Reliable return flight selection using "Choisir le tarif" text
- **Page Loader Handling**: Automatic detection and waiting for 25-30 second airplane animation
- **JSON Parsing**: Navigates nested structure `response.result.data.journeys[]`
- **Dedicated Allure Attachment**: Clear PDF fields section in report
- **Database Extension**: 7 new fields for Case 3 tracking (total: 30 fields)

**New CLI Parameters:**
```bash
--origin          # Origin airport IATA code (default: BOG)
--destination     # Destination airport IATA code (default: MDE)
--departure-days  # Days from today for departure (default: 4)
--return-days     # Days from today for return (default: 5)
```

**Example Execution:**
```bash
pytest tests/nuxqa/test_login_network_Case3.py \
  --browser=chrome \
  --origin=BOG \
  --destination=MDE \
  --departure-days=4 \
  --return-days=5 \
  --env=uat1 -v
```

**Browser Compatibility:**
- ✅ Chrome: Fully functional (142s execution time)
- ✅ Edge: Fully functional (142s execution time)
- ❌ Firefox: Not supported (CDP is Chromium-only - expected limitation)

**Files Added:**
- `tests/nuxqa/test_login_network_Case3.py` (550+ lines)
- `pages/nuxqa/login_page.py` (361 lines)
- `pages/nuxqa/select_flight_page.py` (315 lines)
- `utils/network_capture.py` (465 lines)

**Files Modified:**
- `utils/database.py` - Added 7 Case 3 fields
- `conftest.py` - Added 4 CLI parameters for Case 3

### 📊 Updated Statistics

- **Completed Cases**: 5/7 (Cases 3, 4, 5, 6, 7)
- **Total Tests**: 86 (2 + 24 + 18 + 18 + 24)
- **Database Fields**: 30 (increased from 23)
- **Page Objects**: 4 (home_page, login_page, select_flight_page, network_capture)
- **Test Files**: 5 complete test cases

### 🔧 Technical Improvements

**Database Schema:**
- Extended from 23 to 30 fields
- Added Case 3 specific fields:
  - `origin_city`, `destination_city`
  - `departure_date`, `return_date`
  - `passenger_count`
  - `session_journey_count`
  - `session_data_json`

**Allure Reporting:**
- Dedicated attachment for PDF-required fields
- Clear separation from debug information
- Enhanced configuration summary
- Dynamic test metadata

**Code Quality:**
- Comprehensive documentation in all files
- Clear method comments explaining complex logic
- Proper error handling and logging
- Page loader detection and handling
- Element visibility strategies (JavaScript forcing)

### 🔜 Pending Implementation

- **Case 1**: One-way Booking (complete flow)
- **Case 2**: Round-trip Booking (complete flow)

### 📝 Commits in This Release

- `c9bc246` - Implement Case 3: Flight Search & Network Session Capture (COMPLETE)
- `57afd43` - Add dedicated PDF fields attachment to Allure report
- `e4ec631` - ✅ Case 3 COMPLETO Y VALIDADO - Flight Search & Network Capture

---

## [v1.0.0-stable] - 2025-10-30

### 🎯 STABLE MILESTONE - Reference Point

This release marks a **stable, fully tested, and validated** state of the technical test automation suite.

### ✅ Completed Test Cases (4/7)

#### Case 4: Language Change Validation
- **Languages**: 4 (Español, English, Français, Português)
- **Browsers**: 3 (Chrome, Edge, Firefox)
- **Environments**: 2 (QA4, QA5)
- **Total tests**: 24 combinations
- **Status**: ✅ 100% PASSED

#### Case 5: POS Change Validation
- **POS**: 3 (Chile, España, Otros países)
- **Browsers**: 3 (Chrome, Edge, Firefox)
- **Environments**: 2 (QA4, QA5)
- **Total tests**: 18 combinations
- **Status**: ✅ 100% PASSED

#### Case 6: Header Redirections with Language Validation
- **Header Links**: 3 (ofertas-vuelos, credits, equipaje)
- **Language Modes**: Random (default), Specific, All (4 languages)
- **Browsers**: 3 (Chrome, Edge, Firefox)
- **Environments**: 2 (QA4, QA5)
- **Total tests**: 18-72 combinations (depending on language mode)
- **Status**: ✅ 100% PASSED

#### Case 7: Footer Redirections with Language Validation
- **Footer Links**: 4 (vuelos, noticias, aviancadirect, contactanos)
- **Language Modes**: Random (default), Specific, All (4 languages)
- **Browsers**: 3 (Chrome, Edge, Firefox)
- **Environments**: 2 (QA4, QA5)
- **Total tests**: 24-96 combinations (depending on language mode)
- **Status**: ✅ 100% PASSED

### 🎉 Validation Status

- ✅ **Exhaustive testing completed** - All 4 cases executed successfully
- ✅ **Database storage verified** - 23 comprehensive fields working correctly
- ✅ **Allure reports enhanced** - Detailed information for all cases
- ✅ **Documentation updated** - README and Docs fully synchronized
- ✅ **Code quality verified** - No critical, major, or minor issues found
- ✅ **Stability confirmed** - 100% test pass rate across all combinations

### 📊 Technical Achievements

- **23-field database schema** with case-specific tracking
- **Configurable language parameter** for Cases 6 & 7 (random, specific, all modes)
- **Enhanced Allure reporting** with detailed attachments and validation details
- **Video recording capability** (MP4 format with OpenCV)
- **Screenshot management** (none, on-failure, all modes)
- **Multi-browser support** via Selenium Manager (Chrome, Edge, Firefox)
- **Comprehensive CLI options** (8 custom parameters)
- **Page Object Model** properly implemented

### 🔧 How to Use This Reference Point

#### View Stable State
```bash
# View tag information
git show v1.0.0-stable

# Checkout to this stable point
git checkout v1.0.0-stable
```

#### Create Branch from Stable Point
```bash
# For implementing new cases (1, 2, 3) from stable point
git checkout v1.0.0-stable
git checkout -b feature/case-3-login

# Or from main
git checkout main
git checkout -b feature/case-1-booking
```

#### Rollback if Needed
```bash
# If new changes cause problems, return to stable state
git reset --hard v1.0.0-stable

# Or create backup branch
git checkout -b backup-stable v1.0.0-stable
```

#### Compare Changes
```bash
# See what changed since stable point
git diff v1.0.0-stable

# View commits since stable point
git log v1.0.0-stable..HEAD --oneline
```

#### Manager Review
```bash
# Review stable state specifically
git checkout v1.0.0-stable

# Or view release on GitHub
# https://github.com/cesarcardona-ux/selenium-technical-test/releases/tag/v1.0.0-stable
```

### 🔜 Pending Implementation

- **Case 1**: One-way Booking (complete flow)
- **Case 2**: Round-trip Booking (complete flow)

**Note**: Case 3 was completed in v1.1.0 (2025-10-31)

### 📝 Commit Reference

**Commit**: `b95488b` - 🎯 MILESTONE: Stable Release - Cases 4, 5, 6, 7 Complete and Validated
**Tag**: `v1.0.0-stable`
**Date**: 2025-10-30

---

## Previous Changes

### [fa8140d] - 2025-10-30
**Document comprehensive database schema with 23 fields**
- Added detailed Database Schema section to README.md
- Documented all 23 fields (10 general + 7 tracking + 6 case-specific)
- Included SQL query examples for common use cases

### [f99b70f] - 2025-10-30
**Enhance database schema with 13 comprehensive tracking fields**
- Migrated from 10 to 23 database fields
- Added environment, screenshots_mode, video_enabled
- Added expected_value, actual_value, validation_result, initial_url
- Added case-specific fields: pos, header_link, footer_link, link_name, language_mode, validation_message
- Updated all test files to save complete data

### [ca2eebf] - 2025-10-30
**Enhance Allure reports for Cases 4 & 5 with validation details**
- Added detailed attachments (Expected/Actual/Validation Details)
- Enhanced test organization and readability

### [b2147ff] - 2025-10-30
**Enhance Allure reports with detailed language information**
- Added language mode information for Cases 6 & 7
- Added dynamic tags for filtering
- Enhanced configuration visibility in reports

### [ce69c4c] - 2025-10-30
**Fix Case 4 language dropdown issue**
- Resolved NoSuchElementException caused by double-clicking dropdown
- Simplified language selection to single method call

### [9f334f6] - 2025-10-30
**Add configurable language parameter to Cases 6 & 7**
- Implemented three language modes: random (default), specific, all
- Updated conftest.py with conditional parametrization logic
- Modified home_page.py to accept optional language parameter

---

## Repository

https://github.com/cesarcardona-ux/selenium-technical-test

---

**Note**: This changelog follows [Keep a Changelog](https://keepachangelog.com/) principles.
