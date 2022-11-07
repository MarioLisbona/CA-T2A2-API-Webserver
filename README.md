# **Coder Academy - Assignment T2A2 - API Webserver Project. By Mario Lisbona**

# **Table of contents**

## **R1 - Identification of the problem you are trying to solve by building this particular app.**

I'm building a forum API to create an online community with an environment that encourages open communication between like minded individuals. The forum will help facilitate this by providing a variety of channels where users can make posts that relate to that channel. Users can also post replies to help continue the conversation with meaningful input from the entire forum community.


Administrators will moderate all the interactions that happen on the platform. This will be vital in maintaining the platform's integrity as an environment where open communication can happen.


Administrators will be able to perform important moderation activities including deactivating/archiving posts that are inactive, deleting posts, issuing users warnings and deleting users who are violating the community guidelines.


## **R2 - Why is it a problem that needs solving?**

Open and honest communication is vital in creating a world where people from different backgrounds and ethnicities can appreciate and respect the way their fellow members of society interact and view the world we live in.

If an individual is seen to be communicating in an honest way then the person on the other end of that conversation will feel compelled to reciprocate. This kind of communication leads to a world where differences are celebrated rather than criticised. This fusion of different cultural idea and norms can be the catalyst for creativity and innovation in all societies.

Creating a virtual world where this communication can happen is a step towards it happening more often in the real world. [^1]

## **R3 - Why have you chosen this database system. What are the drawbacks compared to others?**

## **R4 - Identify and discuss the key functionalities and benefits of an ORM**

## **R5 - Document all endpoints for your API**

## **R6 - An ERD for your app**

## **R7 - Detail any third party services that your app will use**

## **R8 - Describe your projects models in terms of the relationships they have with each other**

## **R9 - Discuss the database relations to be implemented in your application**

## **R10 - Describe the way tasks are allocated and tracked in your project**

To manage all the tasks for this project is used a kanban board on Trello. I first created the users stories below that apply to the forum API. All the tasks that need to be completed in the project, including all the documentation, answers to assignment questions and the actual coding of different routes for the API are assigned to tickets and placed in the backlog column. I then assigned different coloured labels for different groups of tasks, green for R1, R2, R3  assignment rubrics, purple for assignment requirements to check, yellow for optional features after the minimum viable product was complete and orange for coding tasks. This allowed me to get a get a quick overview of of the project by showing where different tasks and groups of tasks where located in the cycle of the kanban board.

I then wrote all the user stories for the API. The user stories below are broken down into two classes of users that will be accessing the forum API, Administrator and user, and represent all the different routes to resources that the API will facilitate.

| User          	| Action                                                                                                 	|
|---------------	|--------------------------------------------------------------------------------------------------------	|
| Administrator 	| I want to view all user profiles                                                                       	|
| Administrator 	| I want to view a single user profile                                                                   	|
| Administrator 	| I want to delete any posts that violate community guidelines                                           	|
| Administrator 	| I want to delete any replies that violate community guidelines                                         	|
| Administrator 	| I want to deactivate a post that has had no activity for 3 months or has violated community guidelines 	|
| Administrator 	| I want to activate a post if the owner requests it                                                     	|
| Administrator 	| I want to view all archived/deactivated posts                                                          	|
| Administrator 	| I want to view all replies on the forum                                                                	|
| Administrator 	| I want to view all replies posted by a user                                                            	|
| Administrator 	| I want to issue a warning to a user                                                                    	|
| Administrator 	| I i want to a user to be automatically deleted on the next offence post third warning                     |
| Administrator 	| I want to grant admin rights to another user                                                           	|
| Administrator 	| I want to revoke admin rights from another user                                                        	|
| Administrator 	| I want to be able to view the forum statistics                                                         	|
| User          	| I want to register to use the forum                                                                    	|
| User          	| I want to login to participate in the forum                                                            	|
| User          	| I want to view my profile details                                                                      	|
| User          	| I want to update my profile details                                                                    	|
| User          	| I want to create a post in the forum                                                                   	|
| User          	| I want to edit a post i've posted to the forum                                                         	|
| User          	| I want to delete a post i posted to the forum                                                          	|
| User          	| I want to read all posts in the forum                                                                  	|
| User          	| I want to read a specific post in the forum                                                            	|
| User          	| I want to reply to a post in the forum                                                                 	|
| User          	| I want to update a reply iv already posted                                                             	|
| User          	| I want to delete a reply iv already posted                                                             	|
| User          	| I want to view all the replies to a specific post in the forum                                         	|
| User          	| I want to display all the posts in a forum channel                                                     	|
| User          	| I want to display all the posts from a particular user                                                 	|


I then created a kanban board with Trello to allocate and track tasks for the duration of the project. The kanban board is comprised of 5 columns, from left to right they are:
- Backlog
- To Do
- Doing
- Testing
- Done

<br>

<img src="./docs/kanban-columns.png" width='900' alt="kanban columns">

I set Work In Progress limits (WIP's) on the columns to track how many tasks where in each stage of the project. Once the kanban board was setup i would move tasks or tickets from the backlog column into the todo until that was full. At this stage i would give each ticket a date for the work to be completed by. Then i would take a task/tasks fro To Do and place it in the Doing column and then begin on the task. I added checklists for the more complicated tasks to keep track of each sub-task that would need to be completed before that ticket could be moved to the testing and Done columns.

If any completed features needed refactoring or their scope changed, then i would move the ticket back to the To Do column, adjust the checklists, date and the process would start again for that task.



You can become a member of my T2A2 Web API trello board [*here*](https://trello.com/invite/b/tgZAzcbl/ATTI8dca09e313c793fbac3a556003958f8aC962B77D/t2a2-api-webserver) to view all the tickets that were created.


## **References**

- [^1](#r2---why-is-it-a-problem-that-needs-solving) - John E Hind (2022) [*Why Is Being Open And Honest So Important?*](https://www.compass-resolution.com/2017/02/27/why-is-being-clear-open-and-honest-in-your-communications-so-important/), Compass Resolution website, accessed 07 November 2022.

** https://developer.mozilla.org/en-US/docs/Web/HTTP/Status**
https://regexr.com/38tvj
https://c4model.com/

https://vertabelo.com/blog/crow-s-foot-notation/
