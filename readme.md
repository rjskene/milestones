I would like to build a web app that allows the user to select a series of payment milestones and displays the timing between those milestones for the user, in a form similar to a gantt chart.

Requirements:

- the user can create custom Payment Milestone structures from an input form. the Payment Milestone structures should input:
    + a name, the percentage of payment due
    + the net terms for payment after the due date
    + the number of days after the prior milestone that the current milestone is reached (if the milestone is the first milestone, then the days after commencement of the project which is defaulted to 0)
- the user can then create Equipment Sales structures from an input form. the Equipment Sales structure should take a name, a vendor (optional), the quantity to be sold, and a total dollar amount for the sale, and a Payment Milestone structure (previously created by the user)
- the user can then create a Milestone Schedule for the equipment sale. this schedule should be displayed similar to a gantt chart, with the horizontal axis incremented in days, and the vertical access showing rows corresponding to the different payment structures, with the chart filled in with color for the period between when the prior milestone ends and the current milestone ends.
- a database should be used to store the schema for the different objects used
- we need unit tests for business logic and e2e tests for core user journies
- use git and pnpm, use descriptive commits

Design:

- highly minimal and very basic; complicated UX is not required

Frontend:
- use vuejs with composition api and the vite build tool

Backend:
- SQLite
- Django ORM



Check off items in teh plan as we accomplish them as a todo list. If you have open questions that require my input, add those in the plan as well.