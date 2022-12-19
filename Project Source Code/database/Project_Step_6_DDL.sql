SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

CREATE OR REPLACE TABLE Venues(
  venue_id INT NOT NULL AUTO_INCREMENT,
  venue_name VARCHAR(255) NOT NULL,
  capacity INT NOT NULL,
  address VARCHAR(255) NOT NULL,
  city VARCHAR(255) NOT NULL,
  state VARCHAR(2) NOT NULL,
  zip VARCHAR(10) NOT NULL,
  PRIMARY KEY (venue_id)
  );


CREATE OR REPLACE TABLE Events(
  event_id INT NOT NULL AUTO_INCREMENT,
  event_name VARCHAR(255) NOT NULL,
  event_date DATE NOT NULL,
  age_restriction INT NULL,
  general_ticket_price DECIMAL(9,2) NOT NULL,
  member_ticket_price DECIMAL(9,2) NOT NULL,
  venue_id INT NOT NULL,
  PRIMARY KEY (event_id),
  FOREIGN KEY (venue_id) REFERENCES Venues(venue_id) ON DELETE CASCADE
  );


CREATE OR REPLACE TABLE Primary_Genres(
  primary_genre_id INT NOT NULL AUTO_INCREMENT,
  primary_genre_description VARCHAR(255) NOT NULL,
  PRIMARY KEY (primary_genre_id)
  );


CREATE OR REPLACE TABLE Performers(
  performer_id INT NOT NULL AUTO_INCREMENT,
  performer_name VARCHAR(255) NOT NULL,
  manager_email VARCHAR(255) NOT NULL,
  standard_rate DECIMAL(10, 2) NULL,
  primary_genre_id INT,
  PRIMARY KEY (performer_id),
  FOREIGN KEY (primary_genre_id) REFERENCES Primary_Genres(primary_genre_id) ON DELETE SET NULL
  );


CREATE OR REPLACE TABLE Attendees(
  attendee_id INT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  birthday DATE NOT NULL,
  is_member VARCHAR(1) NOT NULL,
  attendee_email VARCHAR(255),
  PRIMARY KEY (attendee_id)
  );


CREATE OR REPLACE TABLE Events_has_Attendees(
  events_has_attendees_id INT NOT NULL AUTO_INCREMENT,
  attendee_id INT NOT NULL,
  event_id INT NOT NULL,
  PRIMARY KEY (events_has_attendees_id),
  FOREIGN KEY (attendee_id) REFERENCES Attendees(attendee_id) ON DELETE CASCADE,
  FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE
  );


CREATE OR REPLACE TABLE Events_has_Performers(
  events_has_performers_id INT NOT NULL AUTO_INCREMENT,
  event_id INT NOT NULL,
  performer_id INT NOT NULL,
  PRIMARY KEY (events_has_performers_id),
  FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE,
  FOREIGN KEY (performer_id) REFERENCES Performers(performer_id) ON DELETE CASCADE
);

INSERT INTO Attendees (first_name, last_name, birthday, attendee_email, is_member)
VALUES  ('Quinn', 'Smith', '2009-03-16', NULL, 'I'),
        ('Destiny', 'Jones', '2000-07-07', 'destiny_j@cs340.com', 'A'),
        ('Amar', 'Patil', '1985-12-04', 'amar.patil@cs340.com', 'I'),
        ('Natalia', 'Moreno', '1972-05-23', 'natalia.r.moreno@cs340.com', 'A' );

INSERT INTO Venues (venue_name, capacity, address, city, state, zip)
VALUES  ('Gun Flint Tavern', 100, '111 Wisconsin St', 'Grand Marais', 'MN', '55604'),
        ('Bayfront Festival Park', 400, '350 Harbor Drive', 'Duluth', 'MN', '55802'),
        ('Madeline Island Chamber Music', 250, '666 Mandamin Trail', 'La Pointe', 'WI', '54850'),
        ('Breakers Roadhouse', 50, '149 W Baraga Ave', 'Marquette', 'MI','49855');

INSERT INTO Primary_Genres(primary_genre_description)
VALUES ('Comedy'),('Music'),('Poetry'), ('Theater');

INSERT INTO Events(event_name, event_date, age_restriction, general_ticket_price, member_ticket_price, venue_id)
VALUES  ( 'Poetry Slam', '2022-08-14', NULL, 10.25, 8.25, 
          (SELECT venue_id from Venues where venue_name = 'Madeline Island Chamber Music')),
        ( 'Drag Show', '2021-01-01', 18, 16.50, 14.99, 
          (SELECT venue_id from Venues where venue_name = 'Breakers Roadhouse')),
        ( 'Lakefront Concert', '2020-07-03', 21, 56.00, 43.75, 
          (SELECT venue_id from Venues where venue_name = 'Bayfront Festival Park')),
        ( 'Comedy Show', '2021-02-14', 21, 5.00, 0.00, 
          (SELECT venue_id from Venues where venue_name = 'Gun Flint Tavern'));

INSERT INTO Performers(performer_name, manager_email, standard_rate, primary_genre_id)
VALUES  ( 'The New Salty Dogs', 'bookings@lokituesday.com', 1200.00, 
          (SELECT primary_genre_id from Primary_Genres where primary_genre_description = 'Music')),
        ( 'Tig Notaro', 'contact@tignotaro.com', 2700.00, 
          (SELECT primary_genre_id from Primary_Genres where primary_genre_description = 'Comedy')),
        ( 'Trampled by Turtles', 'mgmt.contact@trampledbyturtles.com', 6000.00,
          (SELECT primary_genre_id from Primary_Genres where primary_genre_description = 'Music')),
        ( 'Zenith City Horror', 'zenithcithhorror@duluthstuff.com', 900.00,
          (SELECT primary_genre_id from Primary_Genres where primary_genre_description = 'Theater'));


INSERT INTO Events_has_Performers(event_id, performer_id)
VALUES  ( (SELECT event_id FROM Events WHERE event_name = 'Lakefront Concert'),
          (SELECT performer_id FROM Performers WHERE performer_name = 'The New Salty Dogs')),
        ( (SELECT event_id FROM Events WHERE event_name = 'Lakefront Concert'),
          (SELECT performer_id FROM Performers WHERE performer_name = 'Tig Notaro')),
        ( (SELECT event_id FROM Events WHERE event_name = 'Lakefront Concert'),
          (SELECT performer_id FROM Performers WHERE performer_name = 'Trampled by Turtles')),
        ( (SELECT event_id FROM Events WHERE event_name = 'Comedy Show'),
          (SELECT performer_id FROM Performers WHERE performer_name = 'Zenith City Horror'));


INSERT INTO Events_has_Attendees(attendee_id, event_id)
VALUES  ( (SELECT event_id from Events where event_name = 'Drag Show'),
          (SELECT attendee_id from Attendees where first_name = 'Quinn' and last_name = 'Smith')),
        ( (SELECT event_id from Events where event_name = 'Lakefront Concert'),
          (SELECT attendee_id from Attendees where first_name = 'Quinn' and last_name = 'Smith')),
        ( (SELECT event_id from Events where event_name = 'Lakefront Concert'),
          (SELECT attendee_id from Attendees where first_name = 'Natalia' and last_name = 'Moreno')),
        ( (SELECT event_id from Events where event_name = 'Lakefront Concert'),
          (SELECT attendee_id from Attendees where first_name = 'Destiny' and last_name = 'Jones')),
        ( (SELECT event_id from Events where event_name = 'Comedy Show'),
          (SELECT attendee_id from Attendees where first_name = 'Natalia' and last_name = 'Moreno')),
        ( (SELECT event_id from Events where event_name = 'Comedy Show'),
          (SELECT attendee_id from Attendees where first_name = 'Amar' and last_name = 'Patil'));

SET FOREIGN_KEY_CHECKS=1;
COMMIT;