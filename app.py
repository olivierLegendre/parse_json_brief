import json
import csv
import sys


def get_json_file_as_dict(file_name: str) -> dict:
    """
    parse a json file into a dict
    parameters:
        file_name (string): the file to parse
    Returns:
        (dict) : a dictionnary with data from the JSON file
    """
    try:
        with open(file_name) as file_open:
            return json.load(file_open)
    except OSError as error:
        print(f"{error}")

        
def check_data_integrity(data: dict) -> bool:
    """_summary_
    check JSON conformity 
    Args:
        data (dict): initial datas
    Returns:
        bool: return True if the JSON is valid, False otherwise
    """
    data_check_ok = True
    for sub in data:
        if not isinstance(sub, str):
            print(f"type error on subsidiary {sub}")
            data_check_ok = False
        if not isinstance(data[sub], list):
            print(f"type error on content subsidiary {sub}")
            data_check_ok = False
        for employee in data[sub]:
            if not isinstance(employee, dict):
                print(f"type error on employee  -> {sub} : {employee}")
                data_check_ok = False
            if not isinstance(employee["name"], str):
                print(f"type error on employee name -> {sub} : {employee["name"]}")
                data_check_ok = False
            if not isinstance(employee["job"], str):
                print(f"type error on employee job -> {sub} : {employee["job"]}")
                data_check_ok = False
            if not isinstance(employee["hourly_rate"], int):
                print(f"type error on employee hourly_rate -> {sub} : {employee["hourly_rate"]}")
                data_check_ok = False
            if not isinstance(employee["weekly_hours_worked"], int):
                print(f"type error on employee weekly_hours_worked -> {sub} : {employee["weekly_hours_worked"]}")
                data_check_ok = False
            if not isinstance(employee["contract_hours"], int):
                print(f"type error on employee contract_hours -> {sub} : {employee["contract_hours"]}")
                data_check_ok = False

        return data_check_ok


def change_structure_data(data_dict: dict) -> None:
    """
    we change the structure of the data to put all employees data into data_dict[subsidiary]["employees"]
    and statistics into data_dict[subsidiary]["statistics"]
    parameters:
        data_dict (dict) : the dictonnary with all corporate date
    Returns:
        nothing : the data_dict is modified
    """
    for subsidiary in list(data_dict.keys()):
        employees_and_statistics_by_subsidiary = dict()
        employees_and_statistics_by_subsidiary['employees'] = data_dict[subsidiary]
        employees_and_statistics_by_subsidiary['statistics'] = dict()
        data_dict[subsidiary] = employees_and_statistics_by_subsidiary
        
    data_dict["GLOBAL"] = dict()
    data_dict["GLOBAL"]["statistics"] = dict()


def get_subsidiary_name(data_dict: dict, global_sub=False) -> list:
    """
    we retrieve the names of all subsidiary, excluding global
    parameters:
        data_dict (dict) : the dictonnary with all corporate date
        global_sub (bool) : indicate if we want the global value to be returned
    Returns:
        sub_names (list) : the list with all subsidiary
    """
    if data_dict.keys() is not False:
        sub_names = list(data_dict.keys())
        if ('GLOBAL' in sub_names and global_sub is False):
            sub_names.remove('GLOBAL')
        return list(sub_names)
    else:
        print("there is no subisidary in your data file")
        quit()


def check_data_is_numeric(*should_be_numeric: int | float) -> None:
    """
    check if specific data is numeric
    parameters:
        any number of int of float : should be numeric data given in the json
    Returns;
        None : quit the script if the tested input is not numeric
    """
    for input_to_test in should_be_numeric:
        if isinstance(input_to_test, int) or isinstance(input_to_test, float):
            pass
        else: 
            quit(f"this input should be a number {input_to_test}")


def add_salary_to_each_employee_by_subsidiary(data_dict: dict, subsidiary: int) -> None:
    """
    we add 'salary' data to each employee
    parameters:
        data_dict (dict) : the dictonnary with all corporate date
    Returns:
        nothing : the data_dict is modified
    """
    for employee in data_dict[subsidiary]["employees"]:
        salary = total_salary_for_one_employee( employee['hourly_rate'], 
                                                employee['weekly_hours_worked'], 
                                                employee['contract_hours'])
        employee['salary'] = salary


def add_statistics_by_subsidiary(data_dict: dict, subsidiary: int) -> None:
    """
    we add 'average_salary', 'highest_salary' and 'lowest_salary' to data_dict[subsidiary][statistics]
    parameters:
        data_dict (dict) : the dictonnary with all corporate date
    Returns:
        nothing : the data_dict is modified
    """
    temp_salary_list = []
    for employe in data_dict[subsidiary]["employees"]:
        temp_salary_list.append(employe['salary'])
    nb_employees = len(temp_salary_list)
    sum_salary = sum(temp_salary_list)
    data_dict[subsidiary]["statistics"]["average_salary"] = sum_salary / nb_employees
    data_dict[subsidiary]["statistics"]["highest_salary"] = max(temp_salary_list)
    data_dict[subsidiary]["statistics"]["lowest_salary"] = min(temp_salary_list)
    

def total_salary_for_one_employee(hourly_rate: int, weekly_hours_worked: int, contract_hours: int) -> int:
    """
    calculate salary for each employee
    parameters:
        hourly_rate (int): pay in € by hour
        weekly_hours_worked (int): total number of hour worked
        contract_hours (int) : number of hours before overtime
    Returns:
        total_salary(intdict) : the salary as calculated by the formula
    """
    check_data_is_numeric(hourly_rate, weekly_hours_worked, contract_hours)
    majored_hours = weekly_hours_worked - contract_hours if weekly_hours_worked > contract_hours  else 0
    base_hours = weekly_hours_worked if weekly_hours_worked <= contract_hours else contract_hours
    base_salary_weekly = base_hours * hourly_rate 
    majored_salary_weekly = majored_hours * hourly_rate * 1.5
    total_salary_weekly = base_salary_weekly + majored_salary_weekly
    monthly_salary = total_salary_weekly * 4
    return monthly_salary


def add_global_statistics(data_dict: dict) -> None:
    """
    add a new ["GLOBAL"] in subsidiary for the overall stats
    parameters:
        data(dict):  the full data
    Returns:
        none
    """
    subsidiary_names = get_subsidiary_name(data_dict)
    nb_subsidiary = len(subsidiary_names)
    
    temp_sum_list = []
    temp_max_list = []
    temp_min_list = []
    for subsidiary in subsidiary_names:
        temp_sum_list.append(data_dict[subsidiary]["statistics"]["average_salary"])
        temp_max_list.append(data_dict[subsidiary]["statistics"]["highest_salary"])
        temp_min_list.append(data_dict[subsidiary]["statistics"]["lowest_salary"])
    
    sum_salary = sum(temp_sum_list)
        
    data_dict["GLOBAL"]["statistics"]["average_salary"] = sum_salary / nb_subsidiary
    data_dict["GLOBAL"]["statistics"]["highest_salary"] = max(temp_max_list)
    data_dict["GLOBAL"]["statistics"]["lowest_salary"] = min(temp_min_list)


def generate_enriched_data(data_dict: dict) -> dict:
    """
    create a new dictionnary with enriched data
    parameters:
        data(dict):  the initials datas
    Returns:
        dict : dictionnary enriched 
    """
    corporate_data = data_dict
    if corporate_data is None: 
        quit("no data loaded")
    subsidiary_names = get_subsidiary_name(corporate_data)
    
    change_structure_data(corporate_data)
    
    for subsidiary in subsidiary_names:
        add_salary_to_each_employee_by_subsidiary(corporate_data, subsidiary)
        add_statistics_by_subsidiary(corporate_data, subsidiary)
    
    add_global_statistics(corporate_data)
        
    return corporate_data


def export_corporate_data_to_json(data: dict, origin_file, file_name="employees_data_complete.json") -> None:
    """
    export the data in a new json file with added value
    parameters:
        data(dict):  the full data
    Returns:
        none : 
    """
    json_object = json.dumps(data, indent=4)
    with open(origin_file+file_name, "w") as outfile:
        outfile.write(json_object)


def export_corporate_data_to_csv(data: dict, origin_file, file_name="employees_data_complete.csv") -> None:
    """
    export the statistics data in a csv file
    parameters:
        data(dict):  the full data
    Returns:
        none : 
    """
    fieldnames = ['subsidiary_name', 'average_salary', 'highest_salary', 'lowest_salary']
    rows = []
    for sub in get_subsidiary_name(data, True):
        row = { 'subsidiary_name' : sub, 
                'average_salary' : data[sub]["statistics"]["average_salary"],
                'highest_salary' : data[sub]["statistics"]["highest_salary"],
                'lowest_salary' : data[sub]["statistics"]["lowest_salary"]
                }
        rows.append(row)
    
    with open(origin_file+file_name, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def display_in_terminal(data: dict) -> None:
    """
    display the result in terminal
    parameters:
        data(dict):  the full data
    Returns:
        none : display in the terminal
    """
    for subsidary in get_subsidiary_name(data):
        print(f"Entreprise : {subsidary}")
        print("\n")
        for employee in data[subsidary]["employees"]:
            print(f"{employee['name']:<10}   |  {employee['job']:<20}   |   salaire mensuel : {employee['salary']:.2f}€")
            
        print("\n")
        print("=======================================================================")
        print(f"Statistic des salaires pour l'entreprises {subsidary}")
        print(f"Salaire moyen :  {data[subsidary]["statistics"]["average_salary"]:.2f}€")
        print(f"Salaire le plus élevé :  {data[subsidary]["statistics"]["highest_salary"]:.2f}€")
        print(f"Salaire le plus bas :  {data[subsidary]["statistics"]["lowest_salary"]:.2f}€")
        print("\n")
        print("***********************************************************************")
    

    print("=======================================================================")
    print("=======================================================================")
    
    print(f"Statistic des salaires pour l'ensemble de l'entreprise")
    print(f"Salaire moyen :  {data["GLOBAL"]["statistics"]["average_salary"]:.2f}€")
    print(f"Salaire le plus élevé :  {data["GLOBAL"]["statistics"]["highest_salary"]:.2f}€")
    print(f"Salaire le plus bas :  {data["GLOBAL"]["statistics"]["lowest_salary"]:.2f}€")
    
    print("***********************************************************************")
    print("***********************************************************************")


def main():
    """
    we run the script to enrich the data with statistics on the salaries of the employees
    and we display it on the terminal
    parameters:
        none
    Returns:
        none : 
    """
    arg_name = ""
    if len(sys.argv) > 1:
        arg_name = sys.argv[1]
    file_name = arg_name if arg_name != "" else 'employes_data_test.json'
    #if we want to use faker as the source for testing
    #faker_file_name = 'data_faker.json'
    origin_file = "files/"
    json_file_name = origin_file+file_name
    base_data = get_json_file_as_dict(json_file_name)
    
    if ({check_data_integrity(base_data)}):
        corporate_data = generate_enriched_data(base_data)

        display_in_terminal(corporate_data)
        export_corporate_data_to_json(corporate_data, origin_file)
        export_corporate_data_to_csv(corporate_data, origin_file)
    else:
        print("error on json")


if __name__ == "__main__":
    main()