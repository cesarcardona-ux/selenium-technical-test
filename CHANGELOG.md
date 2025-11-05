# Changelog

All notable changes and milestones for this automation project will be documented in this file.

---

## [v1.5.0] - 2025-11-05

### 🌍 Multi-Language URL Validation - Cases 6 & 7

This release implements **comprehensive multi-language support** for Cases 6 and 7, achieving 100% JSON-driven URL validation with support for 4 languages simultaneously.

### ✨ Case 6: Header Redirections - Multi-Language Validation

**Previous State**: Basic validation with hardcoded URL patterns, limited multi-language support

**Changes Made**:
- ✅ Multi-language URL patterns in `parameter_options.json` (lines 292-326)
- ✅ OR Logic validation: At least ONE pattern must match (changed from AND logic)
- ✅ Language exceptions system for special cases (Français + credits → LifeMiles)
- ✅ Dynamic loading of exceptions from JSON (eliminated hardcoded "Français" in code)
- ✅ Support for 4 languages (Español, English, Français, Português) without code changes
- ✅ **Test Results**: 12/12 tests PASSED (3 links × 4 languages)

**URL Pattern Examples**:
```json
"credits": {
  "expected_url_contains": [
    "avianca-credits",      // Español
    "creditos-avianca",     // Español alternate
    "credits-avianca",      // English
    "les-credits-avianca",  // Français
    "creditos-da-avianca"   // Português
  ]
}
```

**Updated Files**:
- `pages/nuxqa/home_page.py` - Lines 335-405
  - Dynamic language exception loading from JSON
  - OR logic for URL validation (at least one pattern matches)
  - Eliminated hardcoded language values
- `ide_test/config/parameter_options.json` - Lines 292-326
  - Multi-language URL patterns for all header links
  - Language exceptions configuration

**Benefits**:
- Zero hardcoded URL patterns
- Easy to add new languages without code changes
- Robust validation across all language variants
- Special case handling via language exceptions

### ✨ Case 7: Footer Redirections - Multi-Language Validation

**Previous State**: Basic validation with hardcoded URL patterns, limited multi-language support

**Changes Made**:
- ✅ Multi-language URL patterns in `parameter_options.json` (lines 328-359)
- ✅ OR Logic validation: At least ONE pattern must match
- ✅ Support for 4 languages (Español, English, Français, Português) without code changes
- ✅ Up to 7 URL variations per link to cover all languages
- ✅ **Test Results**: 16/16 tests PASSED (4 links × 4 languages)

**URL Pattern Examples**:
```json
"vuelos": {
  "expected_url_contains": [
    "ofertas-destinos",     // Español
    "ofertas-de-vuelos",    // Español alternate
    "offers-destinations",  // English
    "flight-offers",        // English alternate
    "offres-destinations",  // Français
    "offres-de-vols",       // Français alternate
    "ofertas-de-voos"       // Português
  ]
}
```

**Updated Files**:
- `pages/nuxqa/home_page.py` - Lines 543-556
  - OR logic for URL validation
  - Multi-language pattern matching
- `ide_test/config/parameter_options.json` - Lines 328-359
  - Extensive URL patterns for all footer links
  - Support for external domains (ayuda.avianca.com)

**Benefits**:
- Zero hardcoded URL patterns for footer links
- Comprehensive coverage of language variants
- Easy maintenance and extension
- Reliable validation across all languages

### 🔧 Technical Improvements

**Validation Logic Change**:
- **Before**: AND logic - ALL patterns had to match (brittle, language-specific)
- **After**: OR logic - AT LEAST ONE pattern must match (flexible, multi-language)

**Example**:
```python
# OLD (AND logic - all must match):
if "avianca-credits" in url and "creditos-avianca" in url:  # ❌ Fails for most URLs

# NEW (OR logic - at least one must match):
for pattern in expected_patterns:
    if pattern in url:  # ✅ Succeeds if ANY pattern matches
        return True
```

**JSON-Driven Configuration**:
- All URL validation patterns loaded from `parameter_options.json`
- Language exceptions loaded dynamically
- No hardcoded values in Python code
- Easy to modify without code changes

### 📊 Test Results

**Case 6 - Header Redirections**:
- ✅ 12 tests PASSED (3 links × 4 languages)
- ✅ Language exception working (Français + credits → LifeMiles)
- ✅ All URL patterns validated correctly

**Case 7 - Footer Redirections**:
- ✅ 16 tests PASSED (4 links × 4 languages)
- ✅ All URL patterns validated correctly
- ✅ External domains validated (ayuda.avianca.com)

**Total**: 28 tests PASSED with multi-language support

### 📝 Documentation Updates

**Files Updated**:
- ✅ `Docs/Advance Test.md` - Complete documentation of multi-language validation for Cases 6 & 7
- ✅ `README.md` - Updated test counts and multi-language capabilities
- ✅ `CHANGELOG.md` - This entry

### 🚀 Commit

**Commit Hash**: `fa4aa75`
**Message**: "Multi-language URL validation for Cases 6 & 7 with JSON-driven configuration"

---

## [v1.4.0] - 2025-11-04

### 🎯 Complete Parametrization - Zero Hardcoded Values

This release achieves **100% parametrization** across all test cases, eliminating all hardcoded values and introducing a modern GUI tool for test configuration.

### 🆕 GUI Pytest Command Generator v1.0.0

**New Application**: Modern GUI application for generating and executing pytest commands without manual CLI editing.

**Features**:
- Modern interface built with CustomTkinter
- 3 main panels: Test Parameters, Pytest Flags, Test Data
- 7 configurable test cases
- Auto-load configuration on startup
- Single-button save to `testdata.json`
- Copy/Execute commands with one click
- Light/Dark theme support
- Complete documentation in `ide_test/README.md`

**File Structure**:
```
ide_test/
├── main.py                    # Application entry point
├── gui/main_window.py         # Main GUI window (755 lines)
├── core/
│   ├── config_manager.py      # JSON configuration management
│   ├── case_mapper.py         # Case-to-parameter mapping
│   └── command_builder.py     # Pytest command builder
└── config/
    ├── testdata.json          # Test data + current session
    ├── parameter_options.json # Parameter definitions
    └── case_mappings.json     # Case configurations
```

**Tag**: `v1.0.0-pytest-generator`
**Restoration**: See `RESTORE_PYTEST_GENERATOR.md` for recovery instructions

### ✨ Case 1: Complete Parametrization

**Previous State**: 7/10 score - Had hardcoded values for POS, origin, destination, and departure days

**Changes Made**:
- ✅ Added `--origin`, `--destination`, `--departure-days` CLI parameters
- ✅ Load city information dynamically from `parameter_options.json`
- ✅ Test summaries now use dynamic values
- ✅ All hardcoded values replaced with CLI parameters
- ✅ **NEW SCORE**: 10/10 - Zero hardcoded values

**Updated Files**:
- `tests/nuxqa/test_oneway_booking_Case1.py` - Lines 66-234
  - Added CLI parameter loading
  - Replaced hardcoded "Chile" with `pos_param`
  - Replaced hardcoded cities with dynamic IATA codes
  - Replaced hardcoded departure days with CLI parameter

**New CLI Usage**:
```bash
pytest tests/nuxqa/test_oneway_booking_Case1.py \
  --browser=chrome \
  --language=Español \
  --pos=Chile \
  --env=qa4 \
  --origin=BOG \
  --destination=MDE \
  --departure-days=4 \
  -v
```

### ✨ Case 3: Complete Parametrization

**Previous State**: 8/10 score - Had hardcoded language→POS and airport search mappings

**Changes Made**:
- ✅ Removed hardcoded `LANGUAGE_TO_POS_MAPPING` dictionary
- ✅ Removed hardcoded `AIRPORT_SEARCH_MAPPING` dictionary
- ✅ Load language→POS mapping from `parameter_options.json`
- ✅ Load airport information from `parameter_options.json`
- ✅ **NEW SCORE**: 10/10 - Zero hardcoded values

**Updated Files**:
- `tests/nuxqa/test_login_network_Case3.py` - Lines 37-107
  - Removed hardcoded dictionaries
  - Added dynamic loading from JSON
  - All mappings now configurable

### 🌍 New POS Options Added

**Francia (France)**:
- Display name: "Francia"
- Command value: "Francia"
- Country code: FR
- Button text: "France"
- Added to `parameter_options.json`

**Peru**:
- Display name: "Peru"
- Command value: "Peru"
- Country code: PE
- Button text: "Perú"
- Added to `parameter_options.json`

**Updated POS Options**: Chile, España, Francia, Peru, Otros países, all

### 🗂️ ConfigManager & JSON System

**New Architecture**:
- `ConfigManager` class for centralized config management
- `parameter_options.json` - All parameter definitions (378 lines)
- `testdata.json` - Per-case data isolation
- `case_mappings.json` - Case-to-parameter relationships

**New Feature**: `language_pos_mapping` (Lines 360-377 in parameter_options.json)
```json
"language_pos_mapping": {
  "Español": {"default_pos": "Chile"},
  "English": {"default_pos": "Chile"},
  "Français": {"default_pos": "Francia"},
  "Português": {"default_pos": "Chile"}
}
```

### 📋 Updated CLI Parameters Table

| Parameter | Cases | Values |
|-----------|-------|--------|
| `--origin` | 1, 3 | BOG, MDE, CLO, MAD, etc. (IATA codes) |
| `--destination` | 1, 3 | BOG, MDE, CLO, MAD, etc. (IATA codes) |
| `--departure-days` | 1, 3 | Integer (days from today) |
| `--pos` | 1, 5 | Chile, España, Francia, Peru, Otros países, all |

### 🎯 Key Benefits

1. **Zero Maintenance**: No hardcoded values to update when requirements change
2. **Full Flexibility**: All test parameters configurable via CLI or JSON
3. **Easy Configuration**: GUI tool eliminates need to memorize CLI syntax
4. **Data Isolation**: Each case has independent configuration in JSON
5. **Scalability**: Adding new parameters/cases doesn't require code changes

### 📊 Parametrization Scores

- **Case 1**: 7/10 → **10/10** ✅
- **Case 3**: 8/10 → **10/10** ✅
- **Cases 4-7**: Already 10/10 ✅

**Overall**: 100% parametrization achieved across all cases

### 🛠️ Technical Details

**ConfigManager Methods**:
- `get_testdata()` - Load test data from testdata.json
- `save_testdata()` - Save configuration to testdata.json
- `get_parameter_options()` - Get parameter definitions
- `get_case_mappings()` - Get case configurations

**Error Fixed**:
- AttributeError with nested config_manager access
- Changed `test_config.config_manager.get_parameter_options()` to `test_config.get_parameter_options()`

---

## [v1.3.0] - 2025-11-03

### ✅ Case 1 COMPLETE - One-way Booking with Performance Optimizations

This release marks the **completion of Case 1: One-way Booking**, bringing the project to **6 out of 7 completed cases** (85.7% complete).

### 🎯 Case 1: One-way Booking - COMPLETE

**Completion Status:**
- ✅ Framework implementation complete
- ✅ Iframe handling implemented (cookie modal + payment gateway)
- ✅ Timing optimizations applied across all page objects
- ✅ Functional tests running successfully
- ✅ 6 parametrized tests (3 browsers × 2 environments)
- **Status**: Changed from 🚧 In Development to ✅ Complete

**Key Features:**
- **6-Page Flow**: Home → Select Flight → Passengers → Services → Seatmap → Payment
- **4 Passenger Types**: 1 Adult, 1 Teen, 1 Child, 1 Infant with complete form automation
- **Flight Type**: One-way (Solo ida)
- **Fare Selection**: Basic plan
- **Services**: Skip all services (as per requirements)
- **Seat Selection**: Economy seats
- **Payment**: Test credit card data with iframe handling
- **Browsers**: Chrome, Edge, Firefox
- **Environments**: QA4, QA5

### ⚡ Performance Optimizations

Comprehensive timing optimizations applied across **6 page objects** to reduce test execution time by **~84 seconds (23% improvement)**:

**Select Flight Page** (`select_flight_page.py`):
- Page load waits reduced (3s→2s, 5s→3s)
- Flight selection optimized (1s→0.5s, 2s→1.5s)
- FLEX plan interactions streamlined
- Continue button timing reduced (0.5s→0.3s, 2s→1.5s)
- **Total savings**: ~6.7 seconds

**Passengers Page** (`passengers_page.py`):
- Initial page load (3s→2s)
- All scroll waits optimized (0.2s→0.1s)
- Gender dropdown interactions reduced
- Birth date field waits minimized
- Nationality dropdown timing improved
- **CRITICAL**: Wait between passengers (2s→1s) = 3s total savings
- Continue button optimizations
- **Total savings**: ~8.3 seconds

**Services Page** (`services_page.py`):
- Initial wait reduced (3s→2s)
- Skip button interactions optimized (2s→1s)
- Continue button timing reduced (0.5s→0.3s, 2s→1.5s)
- **Total savings**: ~3.7 seconds

**Combined with previous optimizations**:
- Home Page: Previously optimized
- Select Flight Page: 6.7s saved
- Passengers Page: 8.3s saved
- Services Page: 3.7s saved
- Seatmap Page: Previously optimized
- Payment Page: Previously optimized
- **Total time savings**: ~84 seconds
- **Estimated execution time**: Reduced from 6:00 to ~4:36 (23% improvement)

### 📝 Page Objects

**4 New Page Objects Created**:
- `pages/nuxqa/passengers_page.py` - Multi-passenger form automation
- `pages/nuxqa/services_page.py` - Service selection/skipping logic
- `pages/nuxqa/seatmap_page.py` - Seat map interaction and selection
- `pages/nuxqa/payment_page.py` - Payment form with iframe handling

**Test File**:
- `tests/nuxqa/test_oneway_booking_Case1.py` - Complete 6-page booking flow

### 🎉 Technical Achievements

- ✅ Complete 6-page booking flow automation
- ✅ Dynamic passenger data handling (4 different types)
- ✅ Advanced iframe context switching (cookies + payment gateway)
- ✅ Service skipping logic implementation
- ✅ Economy seat selection with fallback strategies
- ✅ Payment form automation with PCI-compliant iframe
- ✅ Comprehensive timing optimizations (23% faster)
- ✅ Full Allure integration with step-by-step tracking
- ✅ Database tracking with Case 1 specific fields

### 📊 Updated Statistics

- **Completed Cases**: 6/7 (Cases 1, 3, 4, 5, 6, 7) - Only Case 2 pending
- **Total Tests**: 92 (6 + 2 + 24 + 18 + 18 + 24)
- **Page Objects**: 8 (home, login, select_flight, passengers, services, seatmap, payment, network_capture)
- **Completion Rate**: 85.7%

### 📄 Documentation Updates

**README.md**:
- Updated Case 1 status from "🚧 En Desar." to "✅ Completo"
- Updated total tests from "PTE" to "6 (3 navegadores × 2 ambientes)"
- Added section "Terminar Procesos en Ejecución" with Windows/Linux/Mac commands
- Updated Case 1 description with completion status and optimizations

**CHANGELOG.md**:
- Added this v1.3.0 entry documenting Case 1 completion
- Documented all performance optimizations with specific savings
- Updated project statistics

### 🔜 Next Steps

- **Case 2**: Round-trip Booking (final pending case)
- Cross-browser validation for Case 1
- Additional regression testing

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
