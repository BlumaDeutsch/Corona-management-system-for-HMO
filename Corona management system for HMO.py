import datetime

import pymongo
from flask import *
import json
from datetime import *
import dateutils


class Person:
    def __init__(self, name, last_name, id_number, date_of_birth, phone, city, street, number,
                 mobile_phone, date1, manufacturer1, date2, manufacturer2, date3,
                 manufacturer3, date4, manufacturer4, positive_result,
                 recovery_date):
        self.name = name
        self.last_name = last_name
        self.id_number = id_number
        self.date_of_birth = date_of_birth
        self.phone = phone
        self.city = city
        self.street = street
        self.number = number
        self.mobile_phone = mobile_phone
        if date1 != '':
            self.date1 = datetime.strptime(date1, '%Y-%m-%d')
        else:
            self.date1 = ''
        self.manufacturer1 = manufacturer1
        if date2 != '':
            self.date2 = datetime.strptime(date2, '%Y-%m-%d')
        else:
            self.date2 = ''
        self.manufacturer2 = manufacturer2
        if date3 != '':
            self.date3 = datetime.strptime(date3, '%Y-%m-%d')
        else:
            self.date3 = ''
        self.manufacturer3 = manufacturer3
        if date4 != '':
            self.date4 = datetime.strptime(date4, '%Y-%m-%d')
        else:
            self.date4 = ''
        self.manufacturer4 = manufacturer4
        if positive_result != '':
            self.positive_result = datetime.strptime(positive_result, '%Y-%m-%d')
        else:
            self.positive_result = ''
        if recovery_date != '':
            self.recovery_date = datetime.strptime(recovery_date, '%Y-%m-%d')
        else:
            self.recovery_date = ''

    def insert_person_to_db(self):
        collection.insert_one(
            Person.convert_data_to_json(self.name, self.last_name, self.id_number, self.date_of_birth, self.phone,
                                        self.city, self.street, self.number, self.mobile_phone, self.date1,
                                        self.manufacturer1, self.date2, self.manufacturer2, self.date3,
                                        self.manufacturer3, self.date4, self.manufacturer4, self.positive_result,
                                        self.recovery_date))

    @classmethod
    def find_person_by_id(cls, id_number):
        return collection.find({"id_number": id_number}, {"_id": 0, "positive_result": 0, "recovery_date": 0,
                                                          "date1": 0, "manufacturer1": 0, "date2": 0,
                                                          "manufacturer2": 0, "date3": 0, "manufacturer3": 0,
                                                          "date4": 0, "manufacturer4": 0}).next()

    @classmethod
    def convert_data_to_json(cls, name, last_name, id_number, date_of_birth, phone, city, street, number, mobile_phone,
                             date1, manufacturer1, date2, manufacturer2, date3, manufacturer3, date4, manufacturer4,
                             positive_result, recovery_date):
        return dict(name=name, last_name=last_name, id_number=id_number, date_of_birth=date_of_birth, phone=phone,
                    city=city, street=street, number=number, mobile_phone=mobile_phone, date1=date1,
                    manufacturer1=manufacturer1, date2=date2, manufacturer2=manufacturer2, date3=date3,
                    manufacturer3=manufacturer3, date4=date4, manufacturer4=manufacturer4,
                    positive_result=positive_result,
                    recovery_date=recovery_date)

    def data_update(self):
        pass


def convert_json_to_string(json_string):  # All json parameters must be strings
    ordered_str = json.dumps(json_string)
    ordered_str = ordered_str.replace('"', "")
    ordered_str = ordered_str.replace(', ', '\n')
    return ordered_str[1:-1]


# Returns an array of the number of active patients every day for a month
def active_patients_per_day():
    col = collection.find({}, {"positive_result": 1, "recovery_date": 1})
    active_patients = []
    for i in col:
        if not i['positive_result'] == '':
            active_patients += [(i['positive_result'], i['recovery_date'])]
    number_of_sick = []
    for day in range(30):
        number_of_sick += [0]
        for i in active_patients:
            if i[0] <= datetime.now() - dateutils.relativedelta(months=1) + dateutils.relativedelta(days=day):
                if i[1] == '':
                    number_of_sick[day] += 1
                elif i[1] >= datetime.now() - dateutils.relativedelta(months=1) + dateutils.relativedelta(days=day):
                    number_of_sick[day] += 1
    return number_of_sick


def not_vaccinated():
    col = collection.find({}, {"date1": 1})
    sum_of_people = 0
    sum_of_vaccinated = 0
    for i in col:
        if i["date1"] == '':
            sum_of_people += 1
        else:
            sum_of_people += 1
            sum_of_vaccinated += 1
    sum_of_vaccinated = sum_of_people - sum_of_vaccinated
    return sum_of_vaccinated, sum_of_vaccinated * 100 / sum_of_people


# Create database and collection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["HMOInformation"]
collection = db["PersonalInformation"]


not_vaccinated()


app = Flask(__name__)


# home page
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add_person')
def add_person():
    return render_template('add_person.html')


# Get data from a form, make a new person, add it to the database and return to the home page
@app.route('/create_person', methods=['POST', 'GET'])
def create_person():
    person = Person(request.form['name'], request.form['last_name'], request.form['id_number'],
                    request.form['date_of_birth'], request.form['phone'], request.form['city'],
                    request.form['street'], request.form['number'], request.form['mobile_phone'], request.form['date1'],
                    request.form['man1'], request.form['date2'], request.form['man2'], request.form['date3'],
                    request.form['man3'], request.form['date4'], request.form['man4'], request.form['positive'],
                    request.form['recovery'])
    person.insert_person_to_db()
    return redirect(url_for('home'))


# get an ID number and search it on the database, return the result, or error message
@app.route('/search_person')
def search_person():
    id_number = request.args.get('id_number')
    try:
        person = Person.find_person_by_id(id_number)
    except StopIteration:
        return render_template('find_person.html', person="The requested person is not found, Please try again")
    else:
        print(person)
        return render_template('find_person.html', person=convert_json_to_string(person))


@app.route('/find_person')
def find_person():
    return render_template('find_person.html')


# Sends an array of the number of active patients every day for a month to the html
@app.route('/chart')
def chart():
    return render_template('chart.html', sick_people=active_patients_per_day(), not_vaccinated=not_vaccinated()[0],
                           percent=not_vaccinated()[1])


app.run(debug=True)
