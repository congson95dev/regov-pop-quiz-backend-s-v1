# regov-pop-quiz-backend-s-v1

## Design for the quiz:

## Database design:
### student
	email
	first_name
	last_name
	username
	password
	birth_date
	phone
	
### admin
	email
	first_name
	last_name
	username
	password

### course
	title
	capacity
	
### course_enroll
	course_id FK course
	student_id FK course
	created_date
	deleted_date


## API Flow:

### student -> 
	view list course -> /courses GET
	enroll course if avaiable -> /courses/enroll POST
	drop course enroll if they are in that course, then capa auto update -> /courses/enroll PUT

### admin ->
	create course + set max capa -> /courses POST
	view list course + number of student inside -> /courses GET
	view course detail + view student list inside -> /courses/{id} GET