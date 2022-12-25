# Cleaning Planner
## Video Demo: https://youtu.be/zZ2-EO6yflQ
## Description:

###### Explanation of the web application:

The Cleaning Planner application can be used to plan cleaning sessions for a group of people within a property.
A potential use case would be within a residential building or business. Each time a cleaning of a specific room
in a buiding needs to be cleaned for example, a user could create a job for this and assign it to another user.
The user can then see all jobs that have been assigned to him, and can update the job if the work has been executed.
All users also have an overview of all the jobs that were created and their current status.

The application works as following:

As a user of the platform you need to create an account which allows you to log in on the platform. On the dashboard,
which is visible for everyone that has an account, you can see all cleaning jobs that have been created. For each job
you can see when it was created, who created it, to who it was assigned, the status of the job, and a description of
the job. Cleaning jobs can either have the status "Open", "Progress", or "Finisehd". The status "Open" means that a job
has been created, but no one is currently working on the job. The status "Progress" means that a user is currently
working on a job, and "Finisehd" means that the job was executed.

Everyone is able to create a job from the dashboard page, and assign it to a specific user. The job will then appear on
the personal page of the user under the section "My Jobs" in the navigation bar of the webpage. On the my jobs page,
you can navigate to "All", to see an overview of all the jobs that were assigned to you, independent of their status.
With the "Open", "Progress", and "Finished", you can view the jobs assigned to you that have that specific status. You
can change the status of each job by selecting the "Change Status" dropdown list, and then clicking the "Change Status"
button. It is also possible to delete a job, by selecting the "Delete Job" option in the dropdown list and clicking on
"Change Status".

###### A more in depth explanation of the software

The application is build using the flask framework. The front end is made with HTMS, CSS, and Javascript. For the most
part bootstrap is used to style the page, but there is a little custom CSS added to finalize the styling. The same layout
is re-used with a layout page and JINGA syntax to add the HTML, and Javascript for the different pages. The back-end
is written in Python and uses an SQL database.

If a person navigates to the application's URL and there is no active session running for the user, he is redirected to
the login page with a get request. If a user has a username and password created, he can log in and with a post request
his credentials are passed to the post route in Python on the back end. It is then checked if there is a match between
the username and password and the user table in the database by doing a request to the user table of the SQL database.
The user table in SQL consists of an id, username, and a hash as password. If a person gives in a username that does't
exist in the database or a wrong password, he will be redirected to the apology page and get a message of whatnwent wrong.
If there was a succesful match with the user database, he will be redirected to the index page. In the case that the
user already has an active session with the page, he will directly be navigated to the index page when he enter the
URL.

A user can be created using the "Register" link on the navigation bar, which redirects to the create page using the get
route in Python. On the creation page, a person can chose a username and repeat his password two times. After creating
his account with the create account button, he is redirected to the login page using the post option on the create page.
Throughout the session, the username and password are remembered, so that the user can be linked to specific jobs within
the application. For this feature, parts of the code from the finance project were re-used.

By navigating to the index page with a get request, the user get's an overview from all the jobs that have been
created, independent ofnwho created to the job or to who it was assigned. All jobs in the jobs database consist
of a job_id, creator_id, date, descripton,ncreation_time, and worker_id. The creator_id and the worker_id are both
foreign keys from the user table. The creator_id is the user that has created the job, while the worker_id is the
user that the job was assigned to. By clicking "Create Jobs" on this page, a post request redirects the user to the
create page. Here the user can create a new job with a date, user the job will be assigned to, and a description of
the job. By clicking the "Create Job" button on the create page, a post request is done and the  information is passed
to the back end. The post route in Python then adds the job to the database.

From the navigation bar page, the user can navigate to the jobs page with a get request to get an overview of all jobs that
have been specifically assigned to him. This is done by passing the entire jobs table from the back end to a dictionary array
in Javascript in the front end. Each time a user switches the view of the jobs (All, Open, Progress, or Finished), all
rows that are currently on the page are deleted, based on the filter selected, a new dictionary is created that only
contains the jobs that match with the selected status, and all the rows are recreated. There are therefore no calls to
the database, and all manipulation of the data happens in javascript on the jobs page. A dropdown menu to change the status
of the job and a button to confirm this is also dynamically generated for each job that is added to the table. By selecting
the desired status and clicking the "Change Job" button next to the job for which the status needs to be changed, a post request
is done on the /changeJobStatus route in Python. The status of the specific job is then updated in the SQL database and the user
all jobs assigned to the user are displayed again. If the user selects the option delete, that specific job will be deleted from
the database.

###### Limitations of the application

The application could already have practical use as it is, but ther are some limitations. The fact that there is no
distinction between roles, makes that everyone can create a job and assing it to any other person. A job can also be
deleted by any user. The application is best suitable for a single team, as the only way to distinguish different jobs
is through the description. There are no options to recover a password in case it is lost, and there is no link with a
user's e-mail address to confirm his account. Finally, the layout and styling of the page is very basic and makes use
of out-of-the-box bootstrap, this could be more customized.

###### Options to expand the application

A possibility to expand the application would be to make a distinction between cleaners and managers. That way only
a manager could enter a job and assign it to a cleaner, while a cleaner would not be able to create jobs, but could
only accept or reject them. Another additon would be to also introduce buildings. That way it would be easier to
distinguish jobs not only based on their description, but also on the building they are assigned to. Managers as
well as cleaners could then be assigned to one or multiple buildings, and when creating a job, you would need to
select a building first. There could also be more information added to each job, and there could be a possiblity
to upload attachments that specify how the job should be executed.

An even further expansion would be to introduce some kind of rating system to the application. After each job,
the manager could come and inspect if the job was executed according to pre-set standards, based on that a cleaner
could get a rating. The average rating of the cleaner could then be displayed in the application. If cleaners are
working on a contract basis, the rating could be used to decide whether to assign the job to a specific cleaner. In
the case that cleaners are working for a company that uses the application internally, the rating could be used to
determine possible promotions or salary increases.

Finally, a payment system could be added in the application that would allow for managers to pay the cleaners after
a job or on a set moment.