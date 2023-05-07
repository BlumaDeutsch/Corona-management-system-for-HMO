import pymongo
import flask


class Person:
    def __init__(self, name, last_name, id_number, city=None, street=None, number=None, date_of_birth=None, phone=None,
                 mobile_phone=None, date1=None, manufacturer1=None, date2=None, manufacturer2=None, date3=None,
                 manufacturer3=None, date4=None, manufacturer4=None, positive_result=None, recovery_date=None):
        self.name = name
        self.last_name = last_name
        self.id_number = id_number
        self.city = city
        self.street = street
        self.number = number
        self.date_of_birth = date_of_birth
        self.phone = phone
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
        collection.insert_one({"name": self.name, "last_name": self.last_name, "id_number": self.id_number})

    @classmethod
    def find_person_by_id(cls, id_number):
        return collection.find({"id_number": id_number}, {"_id": 0, "id_number": 0}).next()

    def corona_data_update(self):
        pass


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["HMOInformation"]
collection = db["PersonalInformation"]


app = flask.Flask(__name__)


@app.route('/add_person')
def add_person():
    person = Person(flask.request.args.get('name'), flask.request.args.get('last_name'), flask.request.args.get('id_number'))
    person.insert_person_to_db()
    return '%s is added to the data base!' % flask.request.args.get('name')


@app.route('/find_person')
def find_person():
    id_number = flask.request.args.get('id_number')
    return Person.find_person_by_id(id_number)


@app.route('/update_corona_data')
def update():
    return 'done'


app.run(debug=True)
