import pymongo
from flask import *
import json


class Person:
    def __init__(self, name, last_name, id_number, date_of_birth, phone, city=None, street=None, number=None,
                 mobile_phone=None, date1=None, manufacturer1=None, date2=None, manufacturer2=None, date3=None,
                 manufacturer3=None, date4=None, manufacturer4=None, positive_result=None, recovery_date=None):
        self.name = name
        self.last_name = last_name
        self.id_number = id_number
        self.date_of_birth = date_of_birth
        self.phone = phone
        self.city = city
        self.street = street
        self.number = number
        self.mobile_phone = mobile_phone
        self.date1 = date1
        self.manufacturer1 = manufacturer1
        self.date2 = date2
        self.manufacturer2 = manufacturer2
        self.date3 = date3
        self.manufacturer3 = manufacturer3
        self.date4 = date4
        self.manufacturer4 = manufacturer4
        self.positive_result = positive_result
        self.recovery_date = recovery_date

    def insert_person_to_db(self):
        collection.insert_one(
            Person.convert_data_to_json(self.name, self.last_name, self.id_number, self.date_of_birth, self.phone,
                                        self.city, self.street, self.number, self.mobile_phone, self.date1,
                                        self.manufacturer1, self.date2, self.manufacturer2, self.date3,
                                        self.manufacturer3, self.date4, self.manufacturer4, self.positive_result,
                                        self.recovery_date))

    @classmethod
    def find_person_by_id(cls, id_number):
        return collection.find({"id_number": id_number}, {"_id": 0}).next()

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


def convert_json_to_string(json_string):
    ordered_str = json.dumps(json_string)
    ordered_str = ordered_str.replace('"', "")
    ordered_str = ordered_str.replace(', ', '\n')
    return ordered_str[1:-1]


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["HMOInformation"]
collection = db["PersonalInformation"]

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/add_person')
def add_person():
    return render_template('add_person.html')


@app.route('/create_person', methods=['POST', 'GET'])
def create_person():
    person = Person(request.form['name'], request.form['last_name'], request.form['id_number'],
                    request.form['date_of_birth'], request.form['phone'], request.form['city'],
                    request.form['street'], request.form['number'], request.form['mobile_phone'], request.form['date1'],
                    request.form['man1'], request.form['date2'], request.form['man2'], request.form['date3'],
                    request.form['man3'], request.form['date4'], request.form['man4'], request.form['positive'],
                    request.form['recovery'])
    person.insert_person_to_db()
    return redirect(url_for('login'))


@app.route('/search_person')
def search_person():
    id_number = request.args.get('id_number')
    try:
        person = Person.find_person_by_id(id_number)
    except StopIteration:
        return render_template('find_person.html', person="The requested person is not found, Please try again")
    else:
        return render_template('find_person.html', person=convert_json_to_string(person))


@app.route('/find_person')
def find_person():
    return render_template('find_person.html')


app.run(debug=True)
