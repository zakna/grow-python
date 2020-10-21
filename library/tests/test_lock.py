import time


def test_pumps_are_mutually_exclusive(GPIO, smbus):
    from grow.pump import Pump, global_lock

    ch1 = Pump(channel=1)
    ch2 = Pump(channel=2)
    ch3 = Pump(channel=3)

    ch1.dose(speed=0.5, timeout=1.0, blocking=False)

    assert global_lock.locked() is True

    assert ch2.dose(speed=0.5) is False
    assert ch2.dose(speed=0.5, blocking=False) is False

    assert ch3.dose(speed=0.5) is False
    assert ch3.dose(speed=0.5, blocking=False) is False


def test_pumps_run_sequentially(GPIO, smbus):
    from grow.pump import Pump, global_lock

    ch1 = Pump(channel=1)
    ch2 = Pump(channel=2)
    ch3 = Pump(channel=3)

    assert ch1.dose(speed=0.5, timeout=0.1, blocking=False) is True
    assert global_lock.locked() is True
    time.sleep(0.3)
    assert ch2.dose(speed=0.5, timeout=0.1, blocking=False) is True
    assert global_lock.locked() is True
    time.sleep(0.3)
    assert ch3.dose(speed=0.5, timeout=0.1, blocking=False) is True
    assert global_lock.locked() is True
    time.sleep(0.3)
