import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


def check_password(password: str) -> list[str]:
    """
    :param password:
    :return: list of bad ideas
    """
    answer = list()

    if len(password) < 8:
        answer.append(f'Minimum length is 8, your length is {len(password)}')

    if not any([ch.isalpha() for ch in password]):
        answer.append('Add chars')
    else:
        if not any([ch.islower() for ch in password]):
            answer.append('Add lower chars')
        if not any([ch.isupper() for ch in password]):
            answer.append('Add upper chars')

    if not any([ch.isdigit() for ch in password]):
        answer.append('Add digits')
    if not any([not ch.isalnum() for ch in password]):
        answer.append('Add points')

    return answer


def check_email(email: str) -> bool:
    """

    :param email:
    :return: True if email is valid, else False
    """

    if re.fullmatch(regex, email):
        return True
    else:
        return False
