import logging
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Initialize PII detection engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# PII redactor function
def pii_redactor(record):
    """Detects and redacts PII in log messages."""
    results = analyzer.analyze(text=record.getMessage(), entities=["EMAIL_ADDRESS", "PHONE_NUMBER", "PERSON", "US_SSN"], language='en')
    if results:
        record.msg = anonymizer.anonymize(text=record.getMessage(), analyzer_results=results).text
    return True

class PiiFilter(logging.Filter):
    def filter(self, record):
        return pii_redactor(record)

# Configure root logger to always use the PII filter
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

root_logger = logging.getLogger()
handler = logging.FileHandler("app.log")
handler.addFilter(PiiFilter())

# Ensure filter applies to all loggers, including third-party libraries
for h in root_logger.handlers:
    h.addFilter(PiiFilter())

root_logger.addHandler(handler)

# Expose global logger
logger = root_logger
