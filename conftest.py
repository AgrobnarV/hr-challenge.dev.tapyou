import pytest


def pytest_addoption(parser):
    parser.addoption("--generate_report", action="store_true", help="Generate HTML report")


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if config.getoption("--generate_report"):
        config.option.htmlpath = "report.html"