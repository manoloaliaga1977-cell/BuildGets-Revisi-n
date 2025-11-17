"""
Simple test script to verify BC3 parser
"""
import sys
sys.path.insert(0, '/home/user/BuildGets-Revisi-n/backend')

from app.parsers.bc3_parser import BC3Parser
from app.generators.pdf_generator import PDFGenerator

# Test with example file
bc3_file = '/home/user/BuildGets-Revisi-n/examples/ejemplo_basico.bc3'

print("Testing BC3 Parser...")
print(f"Reading file: {bc3_file}")

try:
    parser = BC3Parser()
    budget = parser.parse_file(bc3_file)

    print(f"\n✅ Parsing successful!")
    print(f"Title: {budget.metadata.title}")
    print(f"Total chapters: {len(budget.chapters)}")
    print(f"Total: {float(budget.total):.2f} EUR")

    print(f"\nChapters:")
    for chapter in budget.chapters:
        print(f"  - {chapter.code}: {chapter.title} ({len(chapter.items)} items, Total: {float(chapter.total):.2f})")
        for item in chapter.items[:2]:  # Show first 2 items
            print(f"    * {item.code}: {item.description} - {float(item.total):.2f}")

    # Test PDF generation
    print(f"\nTesting PDF generation...")
    pdf_gen = PDFGenerator()
    output_path = '/tmp/test_output.pdf'
    pdf_gen.generate_file(budget, output_path)
    print(f"✅ PDF generated at: {output_path}")

except Exception as e:
    import traceback
    print(f"\n❌ Error: {e}")
    print(traceback.format_exc())
