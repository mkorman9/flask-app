def pytest_configure(config):
    print('before all')


def pytest_unconfigure(config):
    print('after all')
