# build_check.ps1
# PowerShell script to run the full development integrity check (Python equivalent of 'mvn install')

# -----------------------------------------------------------------------------
# Configuration and Setup
# -----------------------------------------------------------------------------
$ErrorActionPreference = "Stop" # Stop the script immediately if any command fails (non-zero exit code)
Write-Host "--- Running Python Integrity Checks ---" -ForegroundColor Yellow

# Ensure the Poetry virtual environment is active for the current session
# We don't use 'poetry run' here because we want the commands to be shorter 
# and the whole script to run in the activated context.
poetry shell

# -----------------------------------------------------------------------------
# 1. Clean (Optional)
# -----------------------------------------------------------------------------
# Uncomment this if you need to clean up distribution files (like .whl)
# Write-Host "1/4. Cleaning build artifacts..." -ForegroundColor Cyan
# poetry run python -m build --clean 

# -----------------------------------------------------------------------------
# 2. Linting and Formatting Check
# -----------------------------------------------------------------------------
Write-Host "1/4. Running Black (Code Formatting Check)..." -ForegroundColor Green
# Check only: ensure code matches Black's style without modifying files
poetry run black --check .

Write-Host "2/4. Running iSort (Import Sorting Check)..." -ForegroundColor Green
# Check only: ensure imports are correctly grouped/sorted
poetry run isort --check .

# -----------------------------------------------------------------------------
# 3. Static Type Checking (The "Compiler" Check)
# -----------------------------------------------------------------------------
Write-Host "3/4. Running MyPy (Type Safety Check)..." -ForegroundColor Green
# Checks for type errors, missing methods, etc.
poetry run mypy .

# -----------------------------------------------------------------------------
# 4. Testing
# -----------------------------------------------------------------------------
Write-Host "4/4. Running Pytest (Unit and Integration Tests)..." -ForegroundColor Green
# Executes all test files in the 'tests/' directory
poetry run pytest

# -----------------------------------------------------------------------------
# Conclusion
# -----------------------------------------------------------------------------
Write-Host "--- SUCCESS: All Checks Passed! The code is validated and ready to run. ---" -ForegroundColor Cyan
Write-Host "To start the application, run: poetry run uvicorn app.main:app --reload" -ForegroundColor Green