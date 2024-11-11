import logging
import lightChecker

# logging
logging.basicConfig(level=logging.INFO, filename="../logs/light_checker_tests.log", format='%(asctime)s; %(levelname)s; %(message)s')

def test_lights_on():
    """
    on test
    :return:
    """
    status = lightChecker.should_turn_lights_on(50.930581, 5.780691)
    assert status == 'OFF', f"Waiting 'OFF', current:'{status}'"
    logging.info("[TEST] 'test_lights_on' SUCCESSFUL.")

def test_lights_off():
    """
    off test
    :return:
    """
    status = lightChecker.should_turn_lights_on(50.930581, 5.780691)
    assert status == 'OFF', f"Waiting 'OFF', current:'{status}'"
    logging.info("[TEST] 'test_lights_off' SUCCESSFUL.")

def test_api_failure():
    """
    bad api
    :return:
    """
    try:
        status = lightChecker.should_turn_lights_on(0, 0)  # wrong input
        # If no exception is raised, the test fails
        logging.error("[TEST] 'test_api_failure' FAILED. Expected an exception but none was raised.")
        assert False, "[FAILED] Expected an exception but none was raised."
    except Exception as e:
        # If an exception is raised, the test passes
        logging.info("[TEST] 'test_api_failure' SUCCESSFUL.")

if __name__ == '__main__':
    test_lights_on()
    test_lights_off()
    test_api_failure()
    print("[SUCCESS]")
