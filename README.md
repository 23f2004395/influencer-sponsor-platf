# Project Report: Influencer Engagement and Sponsorship Coordination Platform

## Problem Statement:
The project, Influencer Engagement and Sponsorship Coordination Platform is aimed to develop a web-based application that allows sponsors and influencers to create and manage advertising campaigns. The application required features such as user authentication, campaign and ad request management, and search functionalities for sponsors and influencers.
## My solution:
**1. Initial Setup:** The development began by setting up a basic web application using Flask and HTML. Flask was chosen for its simplicity and flexibility in building web applications. The initial setup included creating the basic structure of the application, including setting up routes and templates for different web pages.<br>
**2. Progressive Feature Integration:** After the basic structure was in place, I added features and built out the application:<br>
<ul>
  <li>Page Development: I started by creating the necessary web pages, each with its own route and corresponding HTML template.</li>
  <li>Database Integration: To handle data storage and retrieval, I integrated a database into the application through SQLAlchemy. This was done through a models.py file, which defined the necessary models for the application, such as users, influencers, sponsor, campaigns and ad requests.</li>
  <li>Controllers Setup: To manage the application's logic and handle redirects and template rendering, I created a controllers file. This file played a crucial role in managing the flow of the application, ensuring that the correct data was passed to the appropriate templates and that users were redirected to the correct pages based on their actions.</li>
</ul>

**3. User Authentication:** Before moving on to more complex features, I implemented a user authentication system. This included a login and registration system, allowing sponsors and influencers to create accounts, login, and access their dashboards.<br>
**4. Dashboard Development:** <br> With the authentication system in place, I proceeded to develop individual dashboards for sponsors and influencers. The key features included:
<ul>
  <li>Creating Ad Requests: Users could create new ad requests, specifying details such as the Influencer name, requirements, and payment amount.</li>
  <li>Creating Campaigns: Users could create new campaigns by specifying description, start date, end date, goals, budget, visibility and manage their Ad Requests.</li>
  <li>Updating Ad Requests and Campaigns: The application included features for users to update their ad requests and campaigns as needed.</li>
</ul>

**5. Search Functionality:** To enhance usability, I added search features for both influencers and sponsors. These search functions allowed users to easily find sponsors and influencers based on their search.<br>
## Frameworks and Technologies Used: 
The development of this application utilized the following frameworks and technologies:
<ul>
  <li>Flask</li>
  <li>SQLAlchemy</li>
  <li>HTML/CSS</li>
  <li>Bootstrap</li>
  <li>Chart.JS</li>
  <li>SQLite</li>
  <li>Jinja</li>
</ul>

## ER DIAGRAM 
