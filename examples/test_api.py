"""
Script de ejemplo para probar la API de Budget Converter
"""
import requests
import json
from pathlib import Path

API_BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("🏥 Testing health endpoint...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_bc3_to_json():
    """Test BC3 to JSON conversion"""
    print("📄 Testing BC3 to JSON conversion...")

    bc3_file = Path("ejemplo_basico.bc3")
    if not bc3_file.exists():
        print("❌ File ejemplo_basico.bc3 not found")
        return

    with open(bc3_file, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f"{API_BASE_URL}/convert/bc3-to-json",
            files=files
        )

    if response.status_code == 200:
        print("✅ Conversion successful")
        budget = response.json()
        print(f"Title: {budget['metadata']['title']}")
        print(f"Total chapters: {len(budget['chapters'])}")
        print(f"Total: {budget.get('total', 'N/A')}")

        # Save JSON
        with open('output_budget.json', 'w', encoding='utf-8') as f:
            json.dump(budget, f, indent=2, ensure_ascii=False)
        print("💾 Saved to output_budget.json")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
    print()


def test_bc3_to_pdf():
    """Test BC3 to PDF conversion"""
    print("📊 Testing BC3 to PDF conversion...")

    bc3_file = Path("ejemplo_basico.bc3")
    if not bc3_file.exists():
        print("❌ File ejemplo_basico.bc3 not found")
        return

    with open(bc3_file, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f"{API_BASE_URL}/convert/bc3-to-pdf",
            files=files
        )

    if response.status_code == 200:
        print("✅ Conversion successful")
        with open('output_budget.pdf', 'wb') as f:
            f.write(response.content)
        print("💾 Saved to output_budget.pdf")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
    print()


def test_validate_budget():
    """Test budget validation"""
    print("🔍 Testing budget validation...")

    json_file = Path("output_budget.json")
    if not json_file.exists():
        print("❌ File output_budget.json not found. Run test_bc3_to_json first.")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        budget_data = json.load(f)

    response = requests.post(
        f"{API_BASE_URL}/ai/validate-budget",
        json=budget_data
    )

    if response.status_code == 200:
        print("✅ Validation successful")
        result = response.json()
        print(f"Valid: {result.get('is_valid')}")

        if result.get('errors'):
            print(f"Errors: {result['errors']}")
        if result.get('warnings'):
            print(f"Warnings: {result['warnings']}")
        if result.get('suggestions'):
            print(f"Suggestions: {result['suggestions']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
    print()


def test_enhance_budget():
    """Test budget enhancement"""
    print("✨ Testing budget enhancement...")

    bc3_file = Path("ejemplo_basico.bc3")
    if not bc3_file.exists():
        print("❌ File ejemplo_basico.bc3 not found")
        return

    with open(bc3_file, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f"{API_BASE_URL}/ai/enhance-bc3",
            files=files
        )

    if response.status_code == 200:
        print("✅ Enhancement successful")
        enhanced_budget = response.json()

        # Save enhanced budget
        with open('enhanced_budget.json', 'w', encoding='utf-8') as f:
            json.dump(enhanced_budget, f, indent=2, ensure_ascii=False)
        print("💾 Saved to enhanced_budget.json")

        # Show some enhanced descriptions
        if enhanced_budget.get('chapters'):
            print("\n📝 Sample enhanced descriptions:")
            for chapter in enhanced_budget['chapters'][:1]:
                for item in chapter.get('items', [])[:2]:
                    print(f"  - {item['code']}: {item['description']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("Budget Converter API - Test Suite")
    print("=" * 60)
    print()

    try:
        # Run tests
        test_health()
        test_bc3_to_json()
        test_bc3_to_pdf()

        # AI tests (only if API key is configured)
        print("🤖 AI-powered tests (requires API key):")
        try:
            test_validate_budget()
            test_enhance_budget()
        except Exception as e:
            print(f"⚠️  AI tests skipped: {e}")

        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API")
        print("Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
