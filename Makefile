# Makefile for building resume artifacts from RESUME.md

.PHONY: all html pdf clean help

# Default target: build both HTML and PDF
all: html pdf

# Build HTML version only
html: resume.html

# Build PDF version only
pdf: resume.pdf

resume.html: RESUME.md build_resume.py
	uv run python build_resume.py

resume.pdf: RESUME.md build_resume.py
	uv run python build_resume.py --pdf-only

# Build both HTML and PDF in one pass
both: RESUME.md build_resume.py
	uv run python build_resume.py --pdf

# Clean generated files
clean:
	rm -f resume.html resume.pdf

# Help
help:
	@echo "Available targets:"
	@echo "  all   - Build both HTML and PDF (default)"
	@echo "  html  - Build resume.html only"
	@echo "  pdf   - Build resume.pdf only"
	@echo "  both  - Build both in a single run"
	@echo "  clean - Remove generated files"
	@echo "  help  - Show this help message"
