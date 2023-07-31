import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import re
import json
from pprint import pprint


BASE_URL = 'https://spb.hh.ru'
URL = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
# f'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={page}'
# for page in range(0,40)
parsed_data = []


def get_headers():
    return Headers(browser="firefox", os="win").generate()


hh_main_html = requests.get(URL, headers=get_headers()).text

hh_main_soup = BeautifulSoup(hh_main_html, 'lxml')
# Нахождение ссылки и названия вакансии
# список всех вакансий
vacancies_list = hh_main_soup.find_all('div', class_='serp-item')
# tag_all_vacancies_div = hh_main_soup.find('div', class_='serp-item')


# print(vacancies_list)
# вывод всех вакансий в списке
for vacancy in vacancies_list:
    tag_all_h3 = vacancy.find('h3')
    tag_a = tag_all_h3.find('a')
    link = tag_a['href']
    # print(tag_a)
    # print('----' * 8)
    # pprint(link)
    url2 = link

    vacancies_html = requests.get(url2, headers=get_headers()).text

    vacancies_soup = BeautifulSoup(vacancies_html, 'lxml')


    # получение названия компании
    tag_div_company_name = vacancies_soup.find('div', class_='vacancy-company-details')
    tag_span_company_name = tag_div_company_name.find('span', class_='vacancy-company-name')
    company_name = tag_span_company_name.find('span').text
    # print(company_name)

    # Получение города вакансии
    tag_div_company_city = vacancies_soup.find('div', class_='vacancy-company-redesigned')
    if tag_div_company_city.find('p') is None:
        company_blok = tag_div_company_city.find('span', class_='vacancy-company-name')
        link_tag_a = tag_div_company_city.find('a')
        company_page = BASE_URL + link_tag_a['href']
        company_html = requests.get(company_page, headers=get_headers()).text
        company_soup = BeautifulSoup(company_html, 'lxml')
        if company_soup.find('div', class_='employer-sidebar-block') is None:
            city = 'Ссылка на карту'
        else:
            city = company_soup.find('div', class_='employer-sidebar-block').text
    else:
        city = tag_div_company_city.find('p').text
    # print(city)

    tag_div_salary = vacancies_soup.find('div', class_='vacancy-title')
    if tag_div_salary.find('span') is None:
        salary = 'Не указана'
    else:
        salary = tag_div_salary.find('span').text
    # print(salary)
    #Описание вакансии
    if vacancies_soup.find('div', class_='vacancy-branded-user-content') is None:
        vacancies_description = vacancies_soup.find('div', class_='g-user-content').text
    else:
        vacancies_description = vacancies_soup.find('div', class_='vacancy-branded-user-content').text
    # print(vacancies_description)

    # print(link)

    flask_pattern = re.findall('Flask', vacancies_description)
    django_pattern = re.findall('Flask', vacancies_description)
    sql_pattern = re.findall('[SQL|sql]{3}', vacancies_description)

    # print(dict)

    if (flask_pattern and django_pattern) or sql_pattern:
        dict = {
            'Link': f'{link}',
            'Company_name': f'{company_name}',
            'Salary': f'{salary}',
            'City': f'{city}'
        }
        parsed_data.append(dict)
    # pprint(dict)



# pprint(parsed_data)

# for vacancy_info in parsed_data:
with open ('parsed_data.json', 'w', encoding='utf-8') as file:
    json.dump(parsed_data, file, ensure_ascii=False)


pprint(')')
