-- 7 SELECT statements used to populate descriptions of the tables on each page
  -- get all columns and rows from Venues to populate the Existing Venues table on venues.html
  SELECT * FROM Venues;

  -- get primary_genre_description from Primary_Genres to populate the Genre List table performers.html
  SELECT * FROM Primary_Genres;

  -- get data for all columns from Attendees to populate the Attendees List table on Attendees.html
  SELECT * FROM Attendees;

  -- get data for all columns from Performers to populate the Performers List table on performers.html
  SELECT Performers.performer_id, Performers.performer_name, Performers.manager_email, Performers.standard_rate, Primary_Genres.primary_genre_description
  FROM Performers 
  LEFT JOIN Primary_Genres ON Performers.primary_genre_id = Primary_Genres.primary_genre_id;

  -- get data from Events to populate the Events List table on events.html
  SELECT event_id, event_name, event_date, age_restriction, general_ticket_price, member_ticket_price, Venues.venue_name
  FROM Events
  LEFT JOIN Venues ON Events.venue_id = Venues.venue_id;

  -- get data from Events and Performers via foreign keys in Events_has_Performers to populate the performance list table on performances.html
  SELECT events_has_performers_id, Events.event_name, Performers.performer_name
  FROM Events
  JOIN  Events_has_Performers ON Events.event_id = Events_has_Performers.event_id
  LEFT JOIN  Performers ON Events_has_Performers.performer_id = Performers.performer_id;

  -- get data from Events and Attendees via foreign keys in Events_has_Attendees to populate the attendance list table on attendances.html
  SELECT events_has_attendees_id, Events.event_name, CONCAT(Attendees.first_name, ' ', Attendees.last_name) AS attendee_name
  FROM Events
  JOIN  Events_has_Attendees ON Events.event_id = Events_has_Attendees.event_id
  LEFT JOIN  Attendees ON Events_has_Attendees.attendee_id = Attendees.attendee_id;


-- 7 INSERT statements used to add new rows to their respective tables
  -- add new row of data into Venues table
  INSERT INTO Venues (venue_name, capacity, address, city, state, zip)
  VALUES
  (:venue_name, :capacity, :address, :city, :state, :zip);

  -- add new row of data into Primary_Genres table
  INSERT INTO Primary_Genres (primary_genre_description)
  VALUES (:primary_genre_description);

  -- add new row of data into Attendees table
  INSERT INTO Attendees (first_name, last_name, birthday, is_member, attendee_email)
  VALUES (:first_name, :last_name, :birthday, :is_member, :attendee_email);

  -- add new row of data into Performers table
  INSERT INTO Performers (performer_name, manager_email, standard_rate, primary_genre_id)
  VALUES (:performer_name, :manager_email, :standard_rate, :primary_genre_id);

  -- add new row of data into Events table
  INSERT INTO Events (event_name, event_date, age_restriction, general_ticket_price, member_ticket_price, venue_id)
  VALUES (:event_name, :event_date, :age_restriction, :general_ticket_price, :member_ticket_price, :venue_id);

  -- add new performance into performance list table (:event_id and :performer_id selected by dropdowns)
  INSERT INTO Events_has_Performers (event_id, performer_id)
  VALUES (:event_id, :performer_id);
    
    -- populate dropdown used to pick values for INSERT statements involving a event_id as a FK
    SELECT * FROM Events;

    -- get names of performers to populate dropdown list used to pick values for INSERT statements ivolving performer_id as a FK
      SELECT * FROM Performers;
    
  -- add new attendance into attendances table
  INSERT INTO Events_has_Attendees (Events.event_id, Attendees.attendee_id)
  VALUES (:event_id, :attendee_id);

    -- get names of events to populate dropdown used to pick values for INSERT statement
    SELECT * FROM Events;

    -- get names of attendees to populate dropdown list used to pick values for INSERT statement
    SELECT attendee_id, CONCAT(first_name, ' ', last_name) AS attendee_name FROM Attendees;

-- 6 DELETE statements used to remove individual rows from thier respective tables on each page
  
  -- remove record from Venues
  DELETE FROM Venues WHERE venue_id = :venue_id;

  -- remove record from Primary_Genres, NULLable relationship will set the primary_genre_id FK in Performers table to NULL
  DELETE FROM Primary_Genres WHERE primary_genre_id = :primary_genre_id;

  -- remove record from Attendees
  DELETE FROM Attendees WHERE attendee_id = :attendee_id;

  -- remove record from Performers
  DELETE FROM Performers WHERE performer_id = :performer_id;

  -- remove record from Events
  DELETE FROM Events WHERE event_id = :event_id;
  
  -- remove record from Events_has_performers ()
  DELETE FROM Events_has_Performers WHERE events_has_performers_id = :events_has_performers_id;

  -- remove record from Events_has_attendees
  DELETE FROM Events_has_Attendees WHERE events_has_attendees_id = :events_has_attendees_id;

-- 9 Search statements to be used to populate the update form when updating/editing an entry or populate the dropdowns on insert forms
  
  -- populate the form for update attendee page
  SELECT * FROM Attendees WHERE attendee_id = :attendee_id

  -- populate peformer dropdown for update attendance
  SELECT attendee_id, CONCAT(first_name, ' ', last_name) AS attendee_name FROM Attendees;
  
  -- populate dropdown used to pick values for INSERT statements involving a event_id as a FK
  SELECT * FROM Events WHERE event_id = :event_id;

  -- populate the update form for update genre page
  SELECT * FROM Primary_Genres WHERE primary_genre_id = :primary_genre_id

  -- populate the update form for update event page
  SELECT event_id, event_name, event_date, age_restriction, general_ticket_price, member_ticket_price, Venues.venue_name, Events.venue_id FROM Events LEFT JOIN Venues ON Events.venue_id = Venues.venue_id WHERE event_id = :event_id;
  
  -- populate the update form for update attendance page
  SELECT events_has_attendees_id, Events_has_Attendees.event_id, Events_has_Attendees.attendee_id, Events.event_name, CONCAT(Attendees.first_name, ' ', Attendees.last_name) AS attendee_name FROM Events_has_Attendees JOIN Events ON Events_has_Attendees.event_id = Events.event_id JOIN Attendees ON Events_has_Attendees.attendee_id = Attendees.attendee_id WHERE events_has_attendees_id = :events_has_attendees_id;

  -- populate the update form for update performance page
  SELECT events_has_performers_id, Events_has_Performers.event_id, Events_has_Performers.performer_id, Events.event_name, Performers.performer_name FROM Events_has_Performers JOIN Events ON Events_has_Performers.event_id = Events.event_id JOIN Performers ON Events_has_Performers.performer_id = Performers.performer_id WHERE events_has_performers_id = :events_has_performers_id;

  -- populate the update form update venue page
  SELECT * FROM Venues WHERE venue_id = :venue_id

  -- get names of performers to populate dropdown list used to pick values for INSERT statements ivolving performer_id as a FK
  SELECT * FROM Performers WHERE performer_id = :performer_id;

  -- Return attendee info based on attendee_id for dropdowns
  SELECT first_name, last_name, birthday, is_member, email FROM Attendees WHERE attendee_id = :attendee_id;
-- 7 UPDATE statements
  -- edit a row in the Venues table
  UPDATE Venues 
  SET venue_name = :venue_name, capacity = :capacity, address = :address, city = :city, state = :state, zip = :zip 
  WHERE venue_id = :venue_id

  -- edit a row in the Primary_Genres table
  UPDATE Primary_Genres 
  SET primary_genre_description = :primary_genre_description 
  WHERE primary_genre_id = :primary_genre_id

  -- edit a row in the Attendees table
  UPDATE Attendees 
  SET first_name =:first_name, last_name = :last_name, birthday = :birthday, is_member = :is_member, attendee_email = :attendee_email 
  WHERE attendee_id = :attendee_id;

  -- edit a row in the Performers table
  UPDATE Performers
  SET performer_name = :performer_name, manager_email = :manager_email, standard_rate = :standard_rate, primary_genre_id = :primary_genre_id
  WHERE performer_id = :performer_id;

  --edit a row in the Events tables
  UPDATE Events
  SET event_name = :event_name, event_date = :event_date, age_restriction = :age_restriction, general_ticket_price = :general_ticket_price, member_ticket_price = :member_ticket_price, venue_id = :venue_id
  WHERE event_id = :event_id;

  -- 2 UPDATE statements for M:M tables
    -- edit a row on the intersection table between Events and Performers
    UPDATE Events_has_Performers
    SET event_id = :event_id, performer_id = :performer_id
    WHERE events_has_performers_id= :events_has_performers_id;

    -- edit a row on the intersection table between Events and Attendees
    UPDATE Events_has_Attendees
    SET event_id =:event_id, attendee_id = :performer_id
    WHERE events_has_attendees_id= :events_has_attendees_id;

-- 1 Search statement to be used for finding event attendees (probably will add others)
  -- Search Events_has_Attendees via the event_name to return name and emails of who attended a certain event
  SELECT Events.event_name, CONCAT(Attendees.first_name, ' ', Attendees.last_name) AS attendee_name, attendee_email FROM Events
  JOIN  Events_has_Attendees ON Events.event_id = Events_has_Attendees.event_id
  JOIN  Attendees ON Events_has_Attendees.attendee_id = Attendees.attendee_id
  AND Events.event_id = :event_id;