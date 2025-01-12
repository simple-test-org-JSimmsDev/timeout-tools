import io
import sys
from app.hello_world import main

def test_main():
    captured_output = io.StringIO()
    sys.stdout = captured_output
    main()
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == "Hello, World!"
