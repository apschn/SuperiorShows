from flask import Flask, render_template, request, redirect, json
from flask_mysqldb import MySQL
import os



app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_schneada'
app.config['MYSQL_PASSWORD'] = '6618'
app.config['MYSQL_DB'] = 'cs340_schneada'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

states = ( 
    ('AL','Alabama'),
    ('AK','Alaska'),
    ('AS','American Samoa'),
    ('AZ','Arizona'),
    ('AR','Arkansas'),
    ('CA','California'),
    ('CO','Colorado'),
    ('CT','Connecticut'),
    ('DE','Delaware'),
    ('DC','District of Columbia'),
    ('FL','Florida'),
    ('GA','Georgia'),
    ('GU','Guam'),
    ('HI','Hawaii'),
    ('ID','Idaho'),
    ('IL','Illinois'),
    ('IN','Indiana'),
    ('IA','Iowa'),
    ('KS','Kansas'),
    ('KY','Kentucky'),
    ('LA','Louisiana'),
    ('ME','Maine'),
    ('MD','Maryland'),
    ('MA','Massachusetts'),
    ('MI','Michigan'),
    ('MN','Minnesota'),
    ('MS','Mississippi'),
    ('MO','Missouri'),
    ('MT','Montana'),
    ('NE','Nebraska'),
    ('NV','Nevada'),
    ('NH','New Hampshire'),
    ('NJ','New Jersey'),
    ('NM','New Mexico'),
    ('NY','New York'),
    ('NC','North Carolina'),
    ('ND','North Dakota'),
    ('MP','Northern Mariana Islands'),
    ('OH','Ohio'),
    ('OK','Oklahoma'),
    ('OR','Oregon'),
    ('PA','Pennsylvania'),
    ('PR','Puerto Rico'),
    ('RI','Rhode Island'),
    ('SC','South Carolina'),
    ('SD','South Dakota'),
    ('TN','Tennessee'),
    ('TX','Texas'),
    ('UT','Utah'),
    ('VT','Vermont'),
    ('VI','Virgin Islands'),
    ('VA','Virginia'),
    ('WA','Washington'),
    ('WV','West Virginia'),
    ('WI','Wisconsin'),
    ('WY','Wyoming')                 
)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/attendees', methods=('GET', 'POST'))
def attendees():
    # Read functionality for attendees Entity
    if request.method == "GET":
        query = "SELECT attendee_id, first_name, last_name, DATE_FORMAT(birthday, '%m/%d/%Y') birthday, attendee_email, is_member FROM Attendees;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        attendees_from_app_py = cur.fetchall()

        return render_template('attendees.html', attendees=attendees_from_app_py)
    
    # Create functionality for Attendees entity
    if request.method == "POST":

        fname = request.form["attendee-fname"]
        lname = request.form["attendee-lname"]
        email = request.form["attendee-email"]
        birthday = request.form["attendee-birthday"]
        ismember = request.form["attendee-is-member"]
        if email =='':
            email = None
        
        query = "INSERT INTO Attendees (first_name, last_name, birthday, is_member, attendee_email) VALUES (%s,%s,%s,%s,%s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (fname, lname, birthday, ismember, email))
        mysql.connection.commit()

        return redirect("/attendees")


@app.route('/events', methods=('GET', 'POST'))
def events():            
    # Read functionality for Events entity
    if request.method == "GET":
        # Query to populate the Events table
        query = "SELECT event_id, event_name, event_date, age_restriction, general_ticket_price, member_ticket_price, Venues.venue_name FROM Events LEFT JOIN Venues ON Events.venue_id = Venues.venue_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        events_data = cur.fetchall()
        # Query to populate the Venues dropdown on add event form
        query2 = "SELECT * FROM Venues;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        venues_data = cur.fetchall()

        return render_template('events.html', events=events_data, venues=venues_data)
    
    # Create functionality for Events entity
    if request.method == "POST":
        name = request.form["event-name"]
        date = request.form["event-date"]
        mem_price = request.form["event-price-mem"]
        reg_price = request.form["event-price"]
        age_min = request.form["event-min-age"]
        venue = request.form["event-venue"]     
        if age_min == "":
            age_min = None
         
        query = "INSERT INTO Events (event_name, event_date, age_restriction, general_ticket_price, member_ticket_price, venue_id) VALUES (%s,%s,%s,%s,%s,%s);"
        cur = mysql.connection.cursor()
        cur.execute(query, (name, date, age_min, reg_price, mem_price, venue))
        mysql.connection.commit()
    
        return redirect("/events")


@app.route('/performers_genres', methods=('GET', 'POST'))
def performers(): 
    # Read functionality for Performers and Genres entities
    if request.method == "GET":
        # Query to populate the Performers table
        query1 = "SELECT Performers.performer_id, Performers.performer_name, Performers.manager_email, Performers.standard_rate, Primary_Genres.primary_genre_description FROM Performers LEFT JOIN Primary_Genres ON Performers.primary_genre_id = Primary_Genres.primary_genre_id;"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        performers_from_app_py = cur.fetchall()

        # Query to populate the Genres table and dropdown for add Performer
        query2 = "SELECT * FROM Primary_Genres;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        primary_genres_from_app_py = cur.fetchall()

        return render_template('performers_genres.html', performers=performers_from_app_py, genres=primary_genres_from_app_py)

@app.route('/add_performer', methods=('GET','POST'))
def add_performer():   
    if request.method == "POST":
        name = request.form["performer-name"]
        genre = request.form["performer-genre"]
        email = request.form["performer-email"]
        rate = request.form["performer-rate"]
        if genre == '':
            genre = None
        if rate == '':
            rate = None

        query = "INSERT INTO Performers (performer_name, manager_email, standard_rate, primary_genre_id) VALUES (%s,%s,%s,%s);"
        cur = mysql.connection.cursor()
        cur.execute(query, (name, email, rate, genre,))
        
        mysql.connection.commit()

        return redirect("/performers_genres")


@app.route('/add_genre', methods=('GET','POST'))
def add_genre():
    if request.method == "POST":
        genre_description = request.form["genre-name"]

        query = "INSERT INTO Primary_Genres (primary_genre_description) VALUES (%s);"
        cur = mysql.connection.cursor()
        cur.execute(query, (genre_description,))
        mysql.connection.commit()

        return redirect("/performers_genres")


@app.route('/venues', methods=('GET', 'POST'))
def venues():
    # Read functionality for Venues entity
    if request.method == "GET":
        query = "SELECT * FROM Venues;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        venues_from_app_py = cur.fetchall()

        return render_template('venues.html', venues=venues_from_app_py, states=states) 
    
    # Create functionality for Venues entity
    if request.method == "POST":
        venue_name = request.form["venue-name"]
        capacity = request.form["venue-capacity"]
        address = request.form["venue-address"]
        city = request.form["venue-city"]
        state = request.form["venue-state"]
        zip = str(request.form["venue-zip"])

        query = "INSERT INTO Venues (venue_name, capacity, address, city, state, zip) VALUES (%s,%s,%s,%s,%s,%s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (venue_name, capacity, address, city, state, zip))
        mysql.connection.commit()

        return redirect("/venues")


@app.route("/performances", methods=('GET', 'POST'))
def performances():
    if request.method == "GET":
        # Query to populate the Performances table
        query1 = "SELECT events_has_performers_id, Events.event_name, Performers.performer_name FROM Events JOIN  Events_has_Performers ON Events.event_id = Events_has_Performers.event_id LEFT JOIN Performers ON Events_has_Performers.performer_id = Performers.performer_id;"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        performances_data = cur.fetchall()

        # Query to populate the Events dropdown in Add Performance form
        query2 = "SELECT * FROM Events;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        events_data = cur.fetchall()
        
        # Query to populate the Performer dropdown in Add Performance form
        query3 = "SELECT * FROM Performers;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        performers_data = cur.fetchall()

        return render_template('performances.html', performances=performances_data, events=events_data, performers=performers_data)
    
    # Create functionality for Performances entity
    if request.method == "POST":
        event = request.form["performance-event"]
        performer = request.form["performance-performer"]
        
        query = "INSERT INTO Events_has_Performers (event_id, performer_id) VALUES (%s,%s);"
        cur = mysql.connection.cursor()
        cur.execute(query, (event, performer))
        mysql.connection.commit()
        
        return redirect("/performances")


@app.route("/attendances", methods=('GET', 'POST'))
def attendances():
    if request.method == "GET":
        # Query to populate the Performances table
        query1 = "SELECT events_has_attendees_id, Events.event_name, CONCAT(Attendees.first_name, ' ', Attendees.last_name) AS attendee_name FROM Events JOIN  Events_has_Attendees ON Events.event_id = Events_has_Attendees.event_id LEFT JOIN  Attendees ON Events_has_Attendees.attendee_id = Attendees.attendee_id;"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        attendances_data = cur.fetchall()

        # Query to populate the Events dropdown in Add Performance form
        query2 = "SELECT * FROM Events;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        events_data = cur.fetchall()
        
        # Query to populate the Attendees dropdown in Add Performance form
        query3 = "SELECT attendee_id, CONCAT(first_name, ' ', last_name) AS attendee_name FROM Attendees;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        attendees_data = cur.fetchall()

        return render_template('attendances.html', attendances=attendances_data, events=events_data, attendees=attendees_data)
    
    # Create functionality for Attendances entity
    if request.method == "POST":
        event = request.form["attendance-event"]
        attendee = request.form["attendance-attendee"]
        
        query = "INSERT INTO Events_has_Attendees (event_id, attendee_id) VALUES (%s,%s);"
        cur = mysql.connection.cursor()
        cur.execute(query, (event, attendee))
        mysql.connection.commit()
        
        return redirect("/attendances")

@app.route("/update_attendee/<int:attendee_id>", methods=["POST", "GET"])
@app.route("/update_attendee", methods=["POST", "GET"])
def update_attendee(attendee_id=None):
    if request.method == "GET":
        query = "SELECT * FROM Attendees WHERE attendee_id = %s" % (attendee_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()        
        return render_template("update_attendee.html", data=data)

    if request.method == "POST":
        
        attendee_id = request.form["attendee-id"]
        fname = request.form["attendee-fname"]
        lname = request.form["attendee-lname"]
        email = request.form["attendee-email"]
        birthday = request.form["attendee-birthday"]
        ismember = request.form["attendee-is-member"]
        if email == '':
            email = None
        
        query = "UPDATE Attendees SET first_name = %s, last_name = %s, birthday = %s, is_member = %s, attendee_email = %s WHERE attendee_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (fname, lname, birthday, ismember, email, attendee_id))
        mysql.connection.commit()

        return redirect("/attendees")

@app.route("/delete_attendee/<int:attendee_id>", methods=["GET", "POST"])
def delete_attendee(attendee_id):
    if request.method == 'POST':
        query1 = "DELETE FROM Attendees WHERE attendee_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query1, (attendee_id,))
        mysql.connection.commit()
        return redirect('/attendees')
    query2 = "SELECT first_name, last_name FROM Attendees WHERE attendee_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query2, (attendee_id,))
    first_name_data = (cur.fetchall())[0]
    first_name = list(first_name_data.values())
    
    query3 = "SELECT last_name FROM Attendees WHERE attendee_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query3, (attendee_id,))
    last_name_data = (cur.fetchall())[0]
    last_name = list(last_name_data.values())
    
    full_name = first_name[0] + " " + last_name[0]
    return render_template('delete_confirm.html', return_link = '/attendees', entity_name=full_name, delete_type="Attendee")


@app.route("/update_event/<int:event_id>", methods=["POST", "GET"])
@app.route("/update_event", methods=["POST", "GET"])
def update_event(event_id=None):
    if request.method == "GET":
        # to populate fields with existing data
        query1 = "SELECT event_id, event_name, event_date, age_restriction, general_ticket_price, member_ticket_price, Venues.venue_name, Events.venue_id FROM Events LEFT JOIN Venues ON Events.venue_id = Venues.venue_id WHERE event_id = %s" % (event_id)
        cur = mysql.connection.cursor()
        cur.execute(query1)
        data = cur.fetchall()
        
        # for populating venues dropdown
        query2 = "SELECT * FROM Venues;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        venues = cur.fetchall()

        return render_template("update_event.html", data=data, venues=venues)

    if request.method == "POST":
        
        event_id = request.form["event-id"]
        name = request.form["event-name"]
        date = request.form["event-date"]
        mem_price = request.form["event-price-mem"]
        reg_price = request.form["event-price"]
        age_min = request.form["event-min-age"]
        venue = request.form["event-venue"]
        if age_min =="":
            age_min = None

        query = "UPDATE Events SET event_name = %s, event_date = %s, age_restriction = %s, general_ticket_price = %s, member_ticket_price = %s, venue_id = %s WHERE event_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (name, date, age_min, reg_price, mem_price, venue, event_id))
        mysql.connection.commit()
        return redirect("/events")

@app.route("/delete_event/<int:event_id>", methods=["GET", "POST"])
def delete_event(event_id):
    if request.method == 'POST':
        query1 = "DELETE FROM Events WHERE event_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query1, (event_id,))
        mysql.connection.commit()
        return redirect('/events')
    query2 = "SELECT event_name FROM Events WHERE event_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query2, (event_id,))
    event_data = (cur.fetchall())[0]
    event_name = "the " + list(event_data.values())[0]
    mysql.connection.commit()    
    return render_template('delete_confirm.html', return_link = '/events', entity_name=event_name, delete_type="Event" )


@app.route("/update_genre/<int:primary_genre_id>", methods=["POST", "GET"])
@app.route("/update_genre", methods=["POST", "GET"])
def update_genre(primary_genre_id=None):
    if request.method == "GET":
        query = "SELECT * FROM Primary_Genres WHERE primary_genre_id = %s" % (primary_genre_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
        return render_template("update_genre.html", data=data)

    if request.method == "POST":
        
        primary_genre_id = request.form["genre-id"]
        primary_genre_description = request.form["genre-name"]
        
        query = "UPDATE Primary_Genres SET primary_genre_description = %s WHERE primary_genre_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (primary_genre_description, primary_genre_id))
        mysql.connection.commit()

        return redirect("/performers_genres")


@app.route("/delete_genre/<int:primary_genre_id>", methods=["GET", "POST"])
def delete_genre(primary_genre_id):
    if request.method == 'POST':
        query1 = "DELETE FROM Primary_Genres WHERE primary_genre_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query1, (primary_genre_id,))
        mysql.connection.commit()
        return redirect('/performers_genres')
    query2 = "SELECT primary_genre_description FROM Primary_Genres WHERE primary_genre_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query2, (primary_genre_id,))
    genre_data = (cur.fetchall())[0]
    genre_name = list(genre_data.values())[0]
    mysql.connection.commit()
    return render_template('delete_confirm.html', return_link = '/performers_genres', entity_name = genre_name, delete_type="Genre" )


@app.route("/update_performer/<int:performer_id>", methods=["POST", "GET"])
@app.route("/update_performer", methods=["POST", "GET"])
def update_performer(performer_id=None):
    if request.method == "GET":
        # to populate fields with existing data
        query = "SELECT Performers.performer_id, Performers.performer_name, Performers.manager_email, Performers.standard_rate, Primary_Genres.primary_genre_description FROM Performers LEFT JOIN Primary_Genres ON Performers.primary_genre_id = Primary_Genres.primary_genre_id WHERE performer_id = %s" % (performer_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
        # for populating genre dropdown
        query2 = "SELECT * FROM Primary_Genres;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        genres = cur.fetchall()

        return render_template("update_performer.html", data=data, genres=genres)

    if request.method == "POST":
        
        performer_id = request.form["performer-id"]
        name = request.form["performer-name"]
        genre = request.form["performer-genre"]
        email = request.form["performer-email"]
        rate = request.form["performer-rate"]
        if rate == '':
            rate = None
        if genre == '':
            genre = None
        
        query = "UPDATE Performers SET performer_name = %s, manager_email = %s, standard_rate = %s, primary_genre_id = %s WHERE performer_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (name, email, rate, genre, performer_id))
        mysql.connection.commit()


        return redirect("/performers_genres")


@app.route("/delete_performer/<int:performer_id>", methods=["GET", "POST"])
def delete_performer(performer_id):
    if request.method == 'POST':
        query1 = "DELETE FROM Performers WHERE performer_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query1, (performer_id,))
        mysql.connection.commit()
        return redirect('/performers_genres')
    query2 = "SELECT performer_name FROM Performers WHERE performer_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query2, (performer_id,))
    performer_data = (cur.fetchall())[0]
    performer_name = list(performer_data.values())[0]
    mysql.connection.commit()
    return render_template('delete_confirm.html', return_link = '/performers_genres', entity_name=performer_name, delete_type = "Performer" )


@app.route("/update_venue/<int:venue_id>", methods=["POST", "GET"])
@app.route("/update_venue", methods=["POST", "GET"])
def update_venue(venue_id=None):
    if request.method == "GET":
        query = "SELECT * FROM Venues WHERE venue_id = %s" % (venue_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()     
        return render_template("update_venue.html", data=data, states=states)

    if request.method == "POST":
        
        venue_id = request.form["venue-id"]
        venue_name = request.form["venue-name"]
        capacity = request.form["venue-capacity"]
        address = request.form["venue-address"]
        city = request.form["venue-city"]
        state = request.form["venue-state"]
        zip = request.form["venue-zip"]
        
        query = "UPDATE Venues SET venue_name = %s, capacity = %s, address = %s, city = %s, state = %s, zip = %s WHERE venue_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (venue_name, capacity, address, city, state, zip, venue_id))
        mysql.connection.commit()

        return redirect("/venues")


@app.route("/delete_venue/<int:venue_id>", methods=["GET", "POST"])
def delete_venue(venue_id):
    if request.method == 'POST':        
        query1 = "DELETE FROM Venues WHERE venue_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query1, (venue_id,))
        mysql.connection.commit()
        return redirect('/venues')
    query2 = "SELECT venue_name FROM Venues WHERE venue_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query2, (venue_id,))
    venue_data = (cur.fetchall())[0]
    venue_name = "the " + list(venue_data.values())[0]
    mysql.connection.commit()
    return render_template('delete_confirm.html', return_link = '/venues', entity_name=venue_name, delete_type = "Venue" )

@app.route("/update_performance/<int:events_has_performers_id>", methods=["POST", "GET"])
@app.route("/update_performance", methods=["POST", "GET"])
def update_performance(events_has_performers_id=None):
    if request.method == "GET":
        # to populate fields with existing data
        query1 = "SELECT events_has_performers_id, Events_has_Performers.event_id, Events_has_Performers.performer_id, Events.event_name, Performers.performer_name FROM Events_has_Performers JOIN Events ON Events_has_Performers.event_id = Events.event_id JOIN Performers ON Events_has_Performers.performer_id = Performers.performer_id WHERE events_has_performers_id = %s" % (events_has_performers_id)
        cur = mysql.connection.cursor()
        cur.execute(query1)
        data = cur.fetchall()
        
        # for populating events dropdown
        query2 = "SELECT * FROM Events;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        events = cur.fetchall()

        # for populating performer dropdown
        query3 = "SELECT * FROM Performers;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        performers = cur.fetchall()

        return render_template("update_performance.html", data=data, events=events, performers=performers)

    if request.method == "POST":
        
        performance_id = request.form["performance-id"]
        event_id = request.form["performance-event"]
        performer_id = request.form["performance-performer"]
        
        query = "UPDATE Events_has_Performers SET event_id = %s, performer_id = %s WHERE events_has_performers_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (event_id, performer_id, performance_id))
        mysql.connection.commit()

        return redirect("/performances")


@app.route("/delete_performance/<int:events_has_performers_id>", methods=["GET", "POST"])
def delete_performance(events_has_performers_id):
    args=request.args
    performer = args.get("performer")
    event = args.get("event")
    performance_name = performer + " at " + event
    if request.method == 'POST':
        query = "DELETE FROM Events_has_Performers WHERE events_has_performers_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (events_has_performers_id,))
        mysql.connection.commit()
        return redirect('/performances')
    return render_template('delete_confirm.html', return_link = '/performances', entity_name = performance_name, delete_type="Performance")


@app.route("/update_attendance/<int:events_has_attendees_id>", methods=["POST", "GET"])
@app.route("/update_attendance", methods=["POST", "GET"])
def update_attendance(events_has_attendees_id=None):
    if request.method == "GET":
        # to populate fields with existing data
        query1 = "SELECT events_has_attendees_id, Events_has_Attendees.event_id, Events_has_Attendees.attendee_id, Events.event_name, CONCAT(Attendees.first_name, ' ', Attendees.last_name) AS attendee_name FROM Events_has_Attendees JOIN Events ON Events_has_Attendees.event_id = Events.event_id JOIN Attendees ON Events_has_Attendees.attendee_id = Attendees.attendee_id WHERE events_has_attendees_id = %s" % (events_has_attendees_id)
        cur = mysql.connection.cursor()
        cur.execute(query1)
        data = cur.fetchall()
        
        # for populating events dropdown
        query2 = "SELECT * FROM Events;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        events = cur.fetchall()

        # for populating performer dropdown
        query3 = "SELECT attendee_id, CONCAT(first_name, ' ', last_name) AS attendee_name FROM Attendees;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        attendees = cur.fetchall()

        return render_template("update_attendance.html", data=data, events=events, attendees=attendees)

    if request.method == "POST":
        
        attendance_id = request.form["attendance-id"]
        event_id = request.form["attendance-event"]
        attendee_id = request.form["attendance-attendee"]

        query = "UPDATE Events_has_Attendees SET Events_has_Attendees.event_id = %s, Events_has_Attendees.attendee_id = %s WHERE events_has_attendees_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (event_id, attendee_id, attendance_id))
        mysql.connection.commit()

        return redirect("/attendances")


@app.route("/filter_attendance", methods=["POST", "GET"])
def filter_attendance():
    if request.method == "POST":
        event_id = request.form["attendance-event"]
        query1 = "SELECT event_name FROM Events WHERE event_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query1, (event_id,))
        event_name = cur.fetchall()
        
        query2 = "SELECT Events.event_name, CONCAT(Attendees.first_name, ' ', Attendees.last_name) AS attendee_name, attendee_email FROM Events JOIN  Events_has_Attendees ON Events.event_id = Events_has_Attendees.event_id JOIN  Attendees ON Events_has_Attendees.attendee_id = Attendees.attendee_id AND Events.event_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query2, (event_id,))
        results = cur.fetchall()
        
        
        return render_template("filter_attendance.html", results=results, event=event_name)

@app.route("/delete_attendance/<int:events_has_attendees_id>", methods=["GET", "POST"])
def delete_attendance(events_has_attendees_id):
    args=request.args
    attendee = args.get("attendee")
    event = args.get("event")
    attendance_name = attendee + " at " + event
    if request.method == 'POST':
        query = "DELETE FROM Events_has_Attendees WHERE events_has_attendees_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (events_has_attendees_id,))
        mysql.connection.commit()
        return redirect('/attendances')
    return render_template('delete_confirm.html', return_link = '/attendances',  entity_name = attendance_name, delete_type="Attendance")


if __name__ == '__main__':
    app.run(port=54529)