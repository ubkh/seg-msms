# Music School Management System

## Objective
In this project, your team is tasked with developing a web application that serves as a Music School Management System.

The music school delivers one-to-one music lessons: i.e. each lesson involves one teacher and one student. These lessons may involve learning to play an instrument, music theory, music practice, and preparation for performances (though this is of limited importance for the system). The system you will be developing is primarily concerned with the administration of the lessons.

The school has a director, one or more administrators (sometimes they work only part-time), several teachers, and many students. Most of the students are children, and their parents book the lessons for them. The teachers are all musically trained but specialise in one or more instruments.

The music school employs the same academic calendar as the state school system in the UK. The school year starts at the beginning of September and ends in late July.  There are six terms in a school year.  For example, the terms for 2022/23 are as follows:

| Term | Start Date | End date |
| ------------- | ------------- | ------------- |
| 1 | 1/9/22 | 21/10/22 |
| 2 | 31/10/22 | 16/12/22 |
| 3 | 3/1/23 | 10/2/23 |
| 4 | 20/2/23 | 31/3/23 |
| 5 | 17/4/23 | 26/5/23 |
| 6 | 5/6/23 | 21/7/23 |

By the start of each half-term, lessons for most students are booked, and the students are invoiced for the duration of the half-term. In other words, students normally only cancel or change bookings after a half-term has ended. New students can join at any time during the year. If they join mid-term, lessons are normally booked for the remainder of the term.

**Note that the early epics describe a system that deviates from the normal process.  This is to simplify the requirements.**

## Epics

### Epic 1: Basics (highest priority)
This basic version of the system primarily aims at students and administrators and supports simple lesson administration.

Students can sign themselves up as (student) users of the system. Once they have signed up, they can log in using their email and password. After logging in, a student can request a set of lessons.  Such a request specifies the student's availability, the number of lessons, the interval between lessons (usually one lesson every 1 or 2 weeks), the duration of each lesson (usually 30, 45, or 60 minutes), and some further information (e.g. what the student wants to learn or the name of a teacher if they have one in mind).

Administrators have access to lists of fulfilled and unfulfilled requests for lessons. They fulfil a lesson request by booking the lessons.  Based on the student's request, the administrator specifies the day and time of the week of a lesson, the teacher, the start date, the duration of each lesson, the interval between lessons, and the number of lessons.  The system calculates a price for the lessons.

Students access the status of their requests.  Before the lessons are booked, they can only access their request, edit it, or delete it.  After the lessons are booked, the request can no longer be edited or deleted by the student.  At this time, the student can see a list of their lesson bookings, and they can access an invoice for their lessons.  If the student wishes to change their booking at this time, they need to contact a school administrator outside of the application.  Administrators can still edit lesson bookings or delete lessons.  Any changes they make to a booking are reflected in the associated invoice.

The system ensures each request is fulfilled only once.  However, it is not necessary to check whether the schedule of lessons is feasible (e.g. whether teachers are double booked).

Students can only pay via bank transfer.  The application is not used to take payments.  Each student has a unique reference number.  Each invoice also has a unique reference number that consists of the student reference number followed by a dash ("-") followed by the invoice number.  For example, invoice number 0129-002 is invoice number 002 for student number 0129. Students enter the invoice number as the reference for their bank transfer.  Administrators regularly check the school's bank account for incoming transfers.  All such transfers are recorded on the Music School Management System.

Administrators can check the balance for each student and their transactions (invoices and payments).  Students can check their balance with the music school and their own transactions (invoices and payments).

For security reasons, administrator accounts cannot be set up by signing up. Instead, they are created by the director, who has a super-administrator account. This means the director can do what an administrator can. In addition, the director can create, edit, and delete administrator accounts and assign super-administrator privileges to a regular administrator account.

### Epic 2.1: Children
The school primarily caters for children, with only a few adult learners. This epic addresses this.

Prospective clients can sign themselves up as regular users of the system. Once they have signed up, they can log in using their email and password. After logging in, clients can request a set of lessons for themselves.  They can also register any children they are the parent or guardian of and request lessons for these children.   A lesson request specifies the student's availability, the interval between lessons (usually one lesson every 1 or 2 weeks), the duration of each lesson (usually 30, 45, or 60 minutes), and some further information (e.g. what the student wants to learn or the name of a teacher if they have one in mind).

### Epic 2.2: School terms
The school only offers lessons during term time. This epic addresses this.

The school terms vary from school year to school year.  Any user with administrator privileges can create or edit terms.  The system must validate term dates, ensuring that terms do not overlap. 

Administrators have access to lists of fulfilled and unfulfilled requests for lessons. They fulfil a lesson request by booking the lessons.  Based on the client's request, the administrator specifies the day and time of the week of a lesson, the teacher, the duration of each lesson, the interval between lessons, and the number of lessons.  If the lessons start mid-term, the administrator specifies the date of the first lesson.  Otherwise, the administrator just specifies the term in which the lessons are booked.  If this is done close to the start of the upcoming term or during the break/holiday before the next term, the upcoming term is specified as the default value.  It is possible for the administrator to specify an end date.  If none is given (by default), the lesson booking is made for the entire term (or the remainder of the term).  Using the information that is entered, the system calculates a schedule of lessons for the duration of the term and the price.  Invoicing and payments are handled as in epic 1.  

The system ensures each request is fulfilled only once.  However, it is not necessary to check whether the schedule of lessons is feasible (e.g. whether teachers are double booked).

Clients can access the status of their requests.  Before the lessons are booked, they can only access their requests, edit them, or delete them.  After the lessons are booked, the request can no longer be edited or deleted by the client.  At this time, the client can see a list of their lesson bookings, and they can access an invoice for their lessons.  If the client wishes to change their booking at this time, they need to contact a school administrator outside of the application.  Administrators can still edit lesson bookings or delete lessons.  Any changes they make to a booking are reflected in the associated invoice.

Clients can access a schedule of lessons for each student associated with their account.  They can also access invoices as in epic 1.

### Epic 3.1: Repeat requests
Epics 1, 2.1, and 2.2 require students/clients to make fresh requests for each new set of lessons. However, many clients wish to retain the schedule from term to term.

After a lesson request has been fulfulled and the term is underway, a client may request a change in the lesson schedule for the next term. They can also request to stop the lessons at the end of the term. If a client wishes to continue with the bookings, they should not do anything.

Administrators can fulfil a request once per term. Normally, they do this booking a set of lessons just before each term. The system makes it easy to continue an existing booking into the next term, or make small changes.

The system ensures each request is fulfilled only once **per term**.  However, it is not necessary to check whether the schedule of lessons is feasible (e.g. whether teachers are double booked).

### Epic 3.2: Timetabling
Thus far, scheduling constraints have not yet been considered and need to be enforced manually. This is a major limitation.

When lessons are booked, the system ensures that a teacher is booked only once in a timeslot.

Music school teachers can now also log into the system and access their timetable.  Teacher accounts are created by the school's director in the same way as those of administrators.

### Epic 4: Multiple schools
The Music School Management System is so successful that other schools are interested in employing it as well. This epic addresses this.

The system now has a system administrator who can create new director accounts. A user with director privileges can create a new music school. After creating a music school on the system, they become a user with super-administrator privileges within that music school (see above). They can also edit information on the music school and delete the music school.

Clients, teachers, and administrator need sign themselves up to the system by submitting a sign up form. In other words, teacher and administrator user accounts are no longer created by a director. After logging into the system, any user can choose to become a client of any music school. A school director can grant teacher/administrator privileges to a user of the system.

Directors can ban clients from their school.

## More information
- [Project handbook](https://keats.kcl.ac.uk/mod/book/view.php?id=6368738)