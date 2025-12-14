# Mentor Me
## My crowdfunding_back_end project
By Maria Bodero

- [Mentor Me](#mentor-me)
  - [My crowdfunding\_back\_end project](#my-crowdfunding_back_end-project)
  - [Planning:](#planning)
    - [Concept/Name](#conceptname)
    - [Intended Audience/User Stories](#intended-audienceuser-stories)
    - [Project Overview](#project-overview)
    - [Front End Pages/Functionality](#front-end-pagesfunctionality)
    - [API Spec](#api-spec)
    - [DB Schema](#db-schema)

## Planning:
### Concept/Name
My website aims to provide a simple, free and accessible mentorship platform where mentors can donate time, and mentees can learn new skills without financial constraints.
As a result, make skill-building accessible for everyone and encourage a culture of giving back.

### Intended Audience/User Stories
My website will have two different type of users:

1. **Mentors**: people willing to volunteer time to teach or guide others. They can be: professionals, skilled hobbyists, students with advanced knowledge, retirees and anyone with a skill they can safely and ethically share.
2. **Mentees**: Anyone who wants to learn a new skill, improve existing knowledge, or gain confidence.

### Project Overview

This platform allows users to register as either mentor or mentee. Mentors can create fundraisers and offer booking time slots for their mentees. While mentees can pledge to mentor fundraisers and book available slots.

Key features include:

* Secure API with authentification
* Role-based access control (mentors vs mentees)
* Creating booking time slots with auto-calculated end times
* Preventing overlapping slots and restricting slot modifications if already pledged
* Viewing or editing user profiles with restrictions

### Front End Pages/Functionality

**1. User Page**
  - Anyone can create an user
  - Super user can create an account without specifying user_type
  - All other users must specify user_type which is a selection between Mentor or Mentee
  - Passwords are stored securely and write-only
  - Login required to received a token for API authentication

**2. User Profile**
  - Only authenticated users can view profiles
  - Users can view their own profile
  - Mentor's profile can be viewed by anyone authenticated
  - Mentees cannot view other mentee's profiles
  - Mentors can only view mentees who have pledge to them
  - Users can only edit their own profile

**3. Fundraiser Page**
  - Only mentors can create a fundraiser
  - Each fundraiser is represented as a skill profile and the mentor needs to provide different information about the skill provided. E.g, background, experience, etc.
  - Fundraisers are divided in categories and Mentor must specify it when creating it.
  - Mentors can create as many fundraiser as they wish.
  - Fundraisers profiles are public, so anyone can view.
  - Only owners can edit fundraisers.
  - Mentors are not allowed to delete fundraisers, only deactivate it.

**4. Pledge Page**
  - Only mentees can pledge to a fundraiser's booking slot
  - Mentee needs to specify the slot they want to pledge for
  - Mentees can view all pledges
  - Mentors can see pledges made to their fundraisers
  - Mentees can edit or delete their own pledge only

**4. Booking Slots Page**
  - Only mentors can create booking slots for their fundraisers.
  - Each booking slot ID belongs to a specific fundraiser. 
  - Mentors can only post a slot in their fundraisers.
  - Mentors can only edit or delete their fundraiser's slot.
  - The session end time is calculated automatically based on the session length and the start time.
  - Authentication is required to view bookings.
  - Mentor and Mentees are allowed to view all bookings.
  - If a booking slot is created and overlaps with another existing one, a bad request response will appear. Preventing overlapping slots.
  - Mentor can't delete a slot that has a pledge.
  - Booked slots can't be modified.

### API Spec

**Base URL:** [https://my-fundraiser-7be3066dd2ea.herokuapp.com]
[API Test Evidence](./API_Tests.pdf)


| URL                 | HTTP Method | Purpose                    | Request Body           | Success Response Code | Authentication / Auth |
| ------------------ | ----------- | -------------------------- | ---------------------- | --------------------- | ----------------------- |
| /api-token-auth/   | POST        | Obtain auth token          | username, password     | 200 OK                | Public                  |
| /users/            | GET         | List users (role-filtered) | None                   | 200 OK                | Authenticated           |
| /users/            | POST        | Create user account        | User fields            | 201 Created           | Public                  |
| /users/{id}/       | GET         | View user profile          | None                   | 200 OK                | Authenticated (role rules apply)|
| /users/{id}/       | PUT         | Update own profile         | User fields            | 200 OK                | Owner only              |
| /fundraisers/      | GET         | List fundraisers           | None                   | 200 OK                | Public                  |
| /fundraisers/      | POST        | Create fundraiser          | Fundraiser fields      | 201 Created           | Mentor only             |
| /fundraisers/{id}/ | GET         | View fundraiser details    | None                   | 200 OK                | Public                  |
| /fundraisers/{id}/ | PUT         | Update fundraiser          | Fundraiser fields      | 200 OK                | Owner mentor only       |
| /fundraisers/{id}/ | DELETE      | Deactivate fundraiser      | None                   | 200 OK                | Owner mentor only       |
| /Bookings/         | GET         | List booking slots         | None                   | 200 OK                | Authenticated           |
| /Bookings/         | POST        | Create booking slot        | start_time, fundraiser | 201 Created           | Owner mentor only       |
| /Bookings/{id}/    | GET         | View booking slot          | None                   | 200 OK                | Authenticated           |
| /Bookings/{id}/    | PUT         | Update booking slot        | Slot fields            | 200 OK                | Owner mentor only       |
| /Bookings/{id}/    | DELETE      | Delete unbooked slot       | None                   | 204 No Content        | Owner mentor only       |
| /pledges/          | GET         | List pledges               | None                   | 200 OK                | Authenticated           |
| /pledges/          | POST        | Create pledge              | slot, notes            | 201 Created           | Mentee only             |
| /pledges/{id}/     | GET         | View pledge                | None                   | 200 OK                | Authenticated           |
| /pledges/{id}/     | PUT         | Update pledge              | Pledges field          | 200 OK                | Mentee owner only       |
| /pledges/{id}/     | DELETE      | Cancel pledge              | None                   | 204 No Content        | Mentee owner only       |


### DB Schema

The database is designed around four core entities:
  - **CustomUser**: represents mentors and mentees
  - **Fundraiser**: created by mentors to offer mentoring sessions
  - **BookingTime**: individual time slots for a fundraiser
  - **Pledge**: a booking made by a mentee for a specific time slot
  
<ins>**Entity Relationships**</ins>
  - A User (mentor) can own many Fundraisers
  - A Fundraiser can have many BookingTime slots
  - A BookingTime can have at most one Pledge
  - A User (mentee) can create many Pledges
  - A Pledge links:
    * one mentee
    * one booking slot
    * one fundraiser (derived from the slot)

<ins>**Tables and Fields**</ins>
**CustomUser**
  * id (PK)
  * email
  * password
  * user_type (mentor or mentee)
  * first_name
  * last_name
Other Django auth fields

**Fundraiser**
  * id (PK)
  * owner (FK → CustomUser)
  * title
  * category
  * background
  * years_experience
  * profile_url
  * session_length
  * is_active
  * date_created
    
  **Relationships**
One-to-many with BookingTime
One-to-many with Pledge

**BookingTime**
  * id (PK)
  * fundraiser (FK → Fundraiser)
  * start_time
  * end_time (auto-calculated from session length)

  **Relationships**
One-to-one with Pledge

**Pledge**
  * id (PK)
  * slot (OneToOne → BookingTime)
  * fundraiser (FK → Fundraiser)
  * mentee (FK → CustomUser)
  * notes
  * date_created
    
**Relationship Rules**
- Only mentors can create fundraisers and booking slots
- Booking slots cannot overlap for the same fundraiser
- A booking slot cannot be edited or deleted once pledged
- Mentees can only pledge to available (unbooked) slots
- Fundraiser ownership is enforced at the API level
