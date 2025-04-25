# parse_json_brief

# usage : 

## install requirements : 
    pip install -r requirements.txt

## to display data in terminal : 

    py app.py 
        can take a filename argument, /files/employes_data_test.json used by default
        json file should be put in /files


## to use streamlit : 

    streamlit run app_stream.py
        you can upload any JSON file 
        the downloaded files are put in /files

## to generate fake data:

    py utils/gen_fake.py
        generate a file named data_faker.json
        by default, generate 5 subsidiary, with between 10 and 20 employees
        else you can pass 3 params :
            number of subsidiary
            lower bound for number of employees in each subsidiary
            higher bound for number of employees in each subsidiary