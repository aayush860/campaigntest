import logging
import pytest

# Configure logging
logging.basicConfig(
    filename='test_log.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
pytest.mark.email_templates = pytest.mark.marker('tests related to email templates')

# pytest hook to log test outcome
def pytest_runtest_logreport(report):
    if report.when == 'call':
        if report.outcome == 'passed':
            logger.info(f"Test {report.nodeid} PASSED")
        elif report.outcome == 'failed':
            logger.error(f"Test {report.nodeid} FAILED")
        elif report.outcome == 'skipped':
            logger.warning(f"Test {report.nodeid} SKIPPED")

# pytest hook to add extra information to report
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="test", help="Environment to run tests against")

@pytest.fixture(scope='session')
def env(request):
    return request.config.getoption("--env")
