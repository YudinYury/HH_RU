'''Find Python developer vacancy with HH API
result save to *.csv file
https://hh.ru/search/vacancy?text=Python+developer&specialization=1&area=1&salary=&currency_code=RUR&
experience=noExperience&employment=full&employment=part&employment=project&employment=volunteer&employment=probation&
order_by=salary_desc&search_period=&items_on_page=100&no_magic=true
'''

import json
import requests
import re

from config import HH_ACCESS_TOKEN, hh_user_id, hh_email

HH_URL = 'https://api.hh.ru/'
USER_AGENT = 'User-Agent: api-test-agent'


def make_hh_params(**kwargs):
    params = {
        'user_id': hh_user_id,
        'access_token': HH_ACCESS_TOKEN
    }
    params.update(kwargs)
    return params


def check_name_vacancy(name):
    name = name.upper()
    if 'PHP' in name:
        return False
    elif 'RUBY' in name:
        return False
    elif 'C++' in name:
        return False
    else:
        return True


def check_requirement_vacancy(requirement):
    requirement = requirement.lower()
    if 'высшее техническое образование' in requirement:
        return False
    elif 'высокий средний балл в дипломе' in requirement:
        return False
    elif 'Crrrrrrr' in requirement:
        return False
    else:
        return True

def del_html_tags(text):
    text = re.sub(r'<\w+>', '', text)
    text = re.sub(r'</\w+>', '', text)
    return text


def get_vacancies(params, ):
    list_of_vacancies = []
    response = requests.get(HH_URL + 'vacancies', params=params)
    response_json = response.json()
    for item in response_json['items']:
        # print(item)
        # if 'ython' in item['snippet']['requirement']:
        requirement = del_html_tags(item['snippet']['requirement'])
        if check_name_vacancy(item['name']) and check_requirement_vacancy(requirement):
            vacancy = {
                'name': item['name'],
                'id': item['id'],
                'url': item['alternate_url'],
                'employer': item['employer']['name'],
                'requirement': requirement,
                'experience': params['experience']
                }
            list_of_vacancies.append(vacancy)
    return list_of_vacancies


if __name__ == '__main__':
    list_of_vacancies = []
    params = make_hh_params(text='Python', area='1', specialization='1.221', experience='noExperience')  # noExperience  between1And3
    list_of_vacancies.extend(get_vacancies(params=params))

    params = make_hh_params(text='Python', area='1', specialization='1.221', experience='between1And3')
    list_of_vacancies.extend(get_vacancies(params=params))

    for item in list_of_vacancies:
        print('*** {} (id: {}) для  "{}"'.format(item['name'], item['id'], item['employer']))
        print('requirement: {} '.format(item['requirement']))
        print('experience: {} '.format(item['experience']))
        print(item['url'])


