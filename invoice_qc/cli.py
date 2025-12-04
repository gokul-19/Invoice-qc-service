import argparse
import json
from .extractor import InvoiceExtractor
from .validator import InvoiceValidator
from .schemas import Invoice


def main():
    parser = argparse.ArgumentParser(description="Invoice QC CLI")
    sub = parser.add_subparsers(dest="command")

    # Extract
    p_extract = sub.add_parser("extract")
    p_extract.add_argument("--pdf-dir", required=True)
    p_extract.add_argument("--output", required=True)

    # Validate
    p_validate = sub.add_parser("validate")
    p_validate.add_argument("--input", required=True)
    p_validate.add_argument("--report", required=True)

    # Full run
    p_full = sub.add_parser("full-run")
    p_full.add_argument("--pdf-dir", required=True)
    p_full.add_argument("--report", required=True)

    args = parser.parse_args()

    # ----------------- Extract Only -----------------
    if args.command == "extract":
        extractor = InvoiceExtractor()
        invoices = extractor.extract_invoices(args.pdf_dir)

        with open(args.output, "w") as f:
            json.dump([inv.dict() for inv in invoices], f, indent=2)

        print(f"Extracted {len(invoices)} invoices")
        return

    # ----------------- Validate Only -----------------
    if args.command == "validate":
        data = json.load(open(args.input))

        invoices = [Invoice(**inv) for inv in data]
        validator = InvoiceValidator()
        results = validator.validate(invoices)

        with open(args.report, "w") as f:
            json.dump(results, f, indent=2)

        print("Validation Summary:")
        print(json.dumps(results["summary"], indent=2))
        return

    # ----------------- Full Run (Extract + Validate) -----------------
    if args.command == "full-run":
        extractor = InvoiceExtractor()
        invoices = extractor.extract_invoices(args.pdf_dir)

        validator = InvoiceValidator()
        results = validator.validate(invoices)

        with open(args.report, "w") as f:
            json.dump(results, f, indent=2)

        print("Validation Summary:")
        print(json.dumps(results["summary"], indent=2))
        return


if __name__ == "__main__":
    main()

