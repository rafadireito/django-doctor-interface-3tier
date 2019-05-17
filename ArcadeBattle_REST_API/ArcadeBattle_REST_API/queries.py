import random
import string
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail

from app.models import Person, Patient, Gesture, Game, GamePlayed


def get_user_by_cc_number (cc_number):
    p = Person.objects.get(nif=cc_number)
    return p.user



def get_user_type(username, request=None):
    if username == None:
        token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        user_id = Token.objects.get(key=token).user_id
        username = User.objects.get(id=user_id).username;

    if username == "admin" or User.objects.get(username=username).groups.all()[0].name  in ["admins_group"]:
        return 'admin'
    elif User.objects.get(username=username).groups.all()[0].name  in ["doctors_group"]:
        return 'doctor'
    elif User.objects.get(username=username).groups.all()[0].name in ["patients_group"]:
        return 'patient'
    else:
        return None

def username_from_token(auth_token):
    user_id = Token.objects.get(key=auth_token).user_id
    username = User.objects.get(id=user_id)

    return username

def all_people():
    people = Person.objects.all()
    people_data = []

    for p in people:
        dic = {}
        dic["username"] = p.user.username
        dic["user_type"] = get_user_type(p.user.username)
        dic["first_name"] = p.user.first_name
        dic["last_name"] = p.user.last_name
        dic["photo_b64"] = p.photo_b64
        dic["contact"] = p.contact
        dic["nif"] = p.nif
        dic["birth_date"] = p.birth_date.__str__()
        people_data.append(dic)

    return people_data


def all_admins():
    admins = [p for p in Person.objects.all() if p.user.groups.all()[0].name in ["admins_group"]]
    admins_data = []

    for a in admins:
        dic = {}
        dic["username"] = a.user.username
        dic["user_type"] = get_user_type(a.user.username)
        dic["first_name"] = a.user.first_name
        dic["last_name"] = a.user.last_name
        dic["photo_b64"] = a.photo_b64
        dic["contact"] = a.contact
        dic["nif"] = a.nif
        dic["birth_date"] = a.birth_date.__str__()
        admins_data.append(dic)

    return admins_data


def all_doctors():
    doctors = [p for p in Person.objects.all() if p.user.groups.all()[0].name in ["doctors_group"]]
    doctors_data = []

    for d in doctors:
        dic = {}
        dic["username"] = d.user.username
        dic["user_type"] = get_user_type(d.user.username)
        dic["first_name"] = d.user.first_name
        dic["last_name"] = d.user.last_name
        dic["photo_b64"] = d.photo_b64
        dic["contact"] = d.contact
        dic["nif"] = d.nif
        dic["birth_date"] = d.birth_date.__str__()
        doctors_data.append(dic)

    return doctors_data


def all_patients():
    patients = [p for p in Patient.objects.all() if p.person.user.groups.all()[0].name in ["patients_group"]]
    patients_data = []

    for p in patients:
        dic = {}
        dic["username"] = p.person.user.username
        dic["user_type"] = get_user_type(p.person.user.username)
        dic["first_name"] = p.person.user.first_name
        dic["last_name"] = p.person.user.last_name
        dic["photo_b64"] = p.person.photo_b64
        dic["contact"] = p.person.contact
        dic["nif"] = p.person.nif
        dic["notes"] = p.notes
        dic["birth_date"] = p.person.birth_date.__str__()
        patients_data.append(dic)

    return patients_data


def all_games():
    games_data = []
    for g in list(Game.objects.all()):
        dic = {}
        dic["name"] = g.name
        dic["photo_b64"] = g.photo_b64
        dic["preview_link"] = g.preview_link
        games_data.append(dic)

    return games_data


def user_profile(username):
    dic = {}

    # might be an admin
    if list(Person.objects.filter(user = User.objects.get(username=username))) == []:
        u = User.objects.get(username=username)
        dic["username"] = u.username
        dic["user_type"] = get_user_type(u.username)
        dic["first_name"] = u.first_name
        dic["last_name"] = u.last_name
    else:
        try:
            p =  Person.objects.get(user = User.objects.get(username=username))


            dic["username"] = p.user.username
            dic["user_type"] = get_user_type(p.user.username)
            dic["first_name"] = p.user.first_name
            dic["last_name"] = p.user.last_name
            dic["photo_b64"] = p.photo_b64
            dic["contact"] = p.contact
            dic["nif"] = p.nif
            dic["birth_date"] = p.birth_date.__str__()

            # if the user is a patient, he has medical notes
            if list(Patient.objects.filter(person=p)) != []:
                p = Patient.objects.get(person=Person.objects.get(user = User.objects.get(username=username)))
                dic["notes"] = p.notes
        except: return {}

    return dic


def delete_user(username):
    User.objects.get(username=username).delete()


def delete_gesture(username, gesture_name):
    gestures = list(Gesture.objects.all())
    g = [g for g in gestures if g.patient.person.user.username == username and g.name == gesture_name]

    if len(g) == 1:
        g = g[0]
        g.delete()



def update_notes(data):
    username = data.get("username")
    notes = data.get("notes")
    person = User.objects.get(username=username).person
    Patient.objects.filter(person=person).update(notes=notes)


def update_profile(username, data):

    try:
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        contact = data.get("contact")
        email = data.get("email")
        birth_date = data.get("birth_date")
        nif = data.get("nif")

        # get user and udate it
        u = User.objects.filter(username=email)
        u.update(first_name=first_name, last_name=last_name)

        # update password, if needed
        if 'password' in data:
            password = data.get("password")
            usr = User.objects.get(username=email)
            usr.set_password(password)
            usr.save()

        # get user and udate it
        p = Person.objects.filter(user=u[0])
        p.update(user=u[0], contact=contact, nif=nif, birth_date=birth_date)

        if 'photo_b64' in data:
            photo_b64 = data.get("photo_b64")
            p = p.update(photo_b64=photo_b64)

        return True
    except: return False

def add_game(data):

    try:
        name = data.get("name")
        preview_link = data.get("preview_link")
        photo_b64 = data.get("photo_b64")

        g = Game(name=name, preview_link=preview_link, photo_b64=photo_b64)
        g.save()

        state_message = "The game was added to database"
        return True, state_message

    except:
        state_message = "The game WASN'T added to database"
        return True, state_message


def game_gestures_stat(username):

    person = Person.objects.get(user=User.objects.get(username=username))
    patient = Patient.objects.get(person=person)
    gestures = Gesture.objects.filter(patient=patient)

    user_games_played = []

    for gest in gestures:
        # get played games for user
        for gp in GamePlayed.objects.filter(gesture=gest):
            user_games_played.append(gp)

    dic = {}

    games_played_names  = [g.game.name for g in user_games_played]
    for name in games_played_names:
        tmp = [g.gesture.name for g in user_games_played if g.game.name == name]

        total_quant = len(tmp)
        gest_count = {}

        for gest_name in tmp:
            if gest_name not in gest_count:
                gest_count[gest_name] = 1
            else:
                gest_count[gest_name] += 1

        dic[name] = (gest_count, total_quant)

    return dic

def add_user(data):

    username = data.get("username")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    contact = data.get("contact")
    username = data.get("username")
    birth_date = data.get("birth_date")
    nif = data.get("nif")
    photo_b64 = data.get("photo_b64")

    user_type = data.get("user_type")

    if list(User.objects.filter(username=username)) != []:
        error_message = "There is already a user with this email! The user WASN'T added to database!"
        return False, error_message
    elif list(Person.objects.filter(nif=nif)) != []:
        error_message = "There is already a user with this nif! The user min WASN'T added to database!"
        return False, error_message


    try:
        # generate pw and send email
        pw = send_email_pw(username)
        print("pw sent to mail!")
    except:
        pw = "pw"


    # create a user
    u = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=pw)
    u.save()

    # link the user to a person
    p = Person.objects.create(user=u, contact=contact, nif=nif, birth_date=birth_date, photo_b64=photo_b64)
    p.save()

    # add user to specific group
    if user_type == "admin":
        # check if the group admins exists, else create it
        # finally add admin to group
        admins_group = list(Group.objects.filter(name='admins_group'))

        if len(admins_group) == 0:
            admins_group = Group.objects.create(name='admins_group')
            admins_group.save()

        admins_group = Group.objects.get(name='admins_group')
        admins_group.user_set.add(u)

    elif user_type == "doctor":
        # check if the group docto exists, else create it
        # finally add docto to group
        doctors_group = list(Group.objects.filter(name='doctors_group'))

        if len(doctors_group) == 0:
            doctors_group = Group.objects.create(name='doctors_group')
            doctors_group.save()

        doctors_group = Group.objects.get(name='doctors_group')
        doctors_group.user_set.add(u)

    elif user_type == "patient":

        pat = Patient.objects.create(person=p, notes="")
        pat.save()

        # check if the group patients exists, else create it
        # finally add patient to group
        patients_group = list(Group.objects.filter(name='patients_group'))

        if len(patients_group) == 0:
            patients_group = Group.objects.create(name='patients_group')
            patients_group.save()

        patients_group = Group.objects.get(name='patients_group')
        patients_group.user_set.add(u)


    state_message = "The user was added to database. Check your email for the password"
    return True, state_message


def get_patient_gestures(username):

    # find patient
    person = User.objects.get(username=username).person
    p = Patient.objects.get(person=person)

    gestures =[]
    for g in Gesture.objects.filter(patient=p):
        dic = {}
        dic["username"] = username
        dic["id"] = g.id
        dic["name"] = g.name
        dic["image"] = g.image
        dic["repetitions"] = g.repetitions
        dic["default_difficulty"] = g.default_difficulty
        dic["patient_difficulty"] = g.patient_difficulty
        dic["decision_tree"] = g.decision_tree
        gestures.append(dic)

    return gestures


def send_email_pw(email):

    letters = string.ascii_lowercase
    pw = ''.join(random.choice(letters) for i in range(10))

    subject = "Arcade Battle - Account"
    message = "Welcome to arcade battle!" \
              "\n" \
              "\nYou have been granted access to our software. Here are your login credentials:" \
              "\n * Email: " + email + "" \
               "\n * Password: " + pw + "" \
                "\n" \
                "\n" \
                "\nWe strongly advise you to change the password you were give. To do this go to the Account tab." \
                "\n" \
                "\n" \
                "\nKind regards, " \
                "\nArcade Battle"

    x = send_mail(subject, message, "arcade.battle@outlook.com", [email], fail_silently=False)
    return pw



