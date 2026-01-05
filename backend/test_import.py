try:
    import streamlit_keyup

    print("SUCCESS: streamlit_keyup imported")
    print(streamlit_keyup.__file__)
except ImportError as e:
    print(f"FAILURE: {e}")
except Exception as e:
    print(f"ERROR: {e}")
