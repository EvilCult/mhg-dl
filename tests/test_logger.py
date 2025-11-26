import pytest
from mhg_dl.logger import Logger

@pytest.fixture
def logger():
    return Logger()

def test_logger_default_mode(logger, capsys):
    """Test logger in default (non-verbose) mode."""
    logger.set_verbose(False)
    
    # Test info
    logger.info("Hello World")
    captured = capsys.readouterr()
    assert captured.out == "Hello World\n"
    
    # Test progress (should use carriage return)
    logger.progress("Downloading...")
    captured = capsys.readouterr()
    # Expecting clear line sequence and carriage return
    assert "\033[K" in captured.out
    assert "Downloading..." in captured.out
    assert captured.out.endswith("\r")
    
    # Test info after progress (should print newline first)
    logger.info("Done")
    captured = capsys.readouterr()
    assert captured.out == "\nDone\n"

def test_logger_verbose_mode(logger, capsys):
    """Test logger in verbose mode."""
    logger.set_verbose(True)
    
    # Test info
    logger.info("Hello World")
    captured = capsys.readouterr()
    assert captured.out == "Hello World\n"
    
    # Test progress (should just print with newline)
    logger.progress("Downloading...")
    captured = capsys.readouterr()
    assert captured.out == "Downloading...\n"
    
    # Test info after progress (no extra newline needed)
    logger.info("Done")
    captured = capsys.readouterr()
    assert captured.out == "Done\n"

def test_logger_error(logger, capsys):
    """Test error logging."""
    logger.error("Something went wrong")
    captured = capsys.readouterr()
    assert captured.out == "Error: Something went wrong\n"

def test_logger_mixed_interaction(logger, capsys):
    """Test interaction between progress and error in default mode."""
    logger.set_verbose(False)
    
    logger.progress("Step 1")
    captured = capsys.readouterr()
    
    # Error should clear the progress line first
    logger.error("Failed")
    captured = capsys.readouterr()
    assert captured.out.startswith("\n")
    assert "Error: Failed" in captured.out
