from fake_useragent import UserAgent, FakeUserAgentError
from tools.logger import logger


def get_random_ua():
    count = 0
    try:
        ua = UserAgent(verify_ssl=False)
        return ua.random
    except FakeUserAgentError as e:
        count += 1
        if count < 5:
            get_random_ua()
        else:
            logger.warning(e)


if __name__ == '__main__':
    logger.info(get_random_ua())