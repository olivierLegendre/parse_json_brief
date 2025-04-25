from faker import Faker
import random as r
import json


def create_subsidiary_name(nb_subsidiary: int) -> list:
    """_summary_
    create a list of fake company name
    Args:
        nb_subsidiary (int): number of subsidiary to create

    Returns:
        list: list of fake company name
    """
    fake_company_name_list = list()
    fake_sub_name = Faker()
    for _ in range(nb_subsidiary):
        fake_company_name_list.append(fake_sub_name.company())
    return fake_company_name_list


def create_fake_employee(nb_employee: int) -> list:
    """_summary_
    create a list of fake employees
    Args:
        nb_employee (int): number of employee to generate

    Returns:
        list: list of fake employee
    """
    fake_employee_list = list()
    fake = Faker()
    for _ in range(nb_employee):
        fake_name = fake.name()
        fake_job = fake.job()
        fake_hourly_rate = r.randrange(25, 75)
        fake_contract_hours = r.randrange(15, 50)
        fake_weekly_hours_worked = r.randrange(20, 50)
        fake_employee = dict({"name": fake_name, "job": fake_job, "hourly_rate": fake_hourly_rate, "weekly_hours_worked": fake_weekly_hours_worked,"contract_hours": fake_contract_hours})
        fake_employee_list.append(fake_employee)
        
    return fake_employee_list


def create_fake_json(nb_subsidiary: int , min_employee: int, max_employee: int) -> dict:
    """_summary_
    create a fake json to test our app
    Args:
        nb_subsidiary (int): the number of subsidiary to create
        min_employee (int): the number of employee to generate will be between
        max_employee (int): min_employee and max_employee
    Returns:
        dict: the dict to export 
    """
    json_data = dict()
    fake_company_name_list = create_subsidiary_name(nb_subsidiary)
    for fake_name in fake_company_name_list:
        nb_employees_subsidiary = r.randrange(min_employee, max_employee)
        json_data[fake_name] = create_fake_employee(nb_employees_subsidiary)
    return json_data


def create_json_file(data: dict, origin_files, filename="data_faker.json") -> None:
    """_summary_
    export data to
    Args:
        data (dict): _the data to export
        filename (str, optional): the file nampe to export "data_faker.json".
    """
    json_object = json.dumps(data, indent=4)
    with open(origin_files+filename, "w") as outfile:
        outfile.write(json_object)


def main():
    fake_json = create_fake_json(5, 10, 20)
    origin_files = "../files/"
    create_json_file(fake_json, origin_files)
    # print(fake_json)


if __name__ == "__main__":
    main()