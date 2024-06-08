# AI News - Jugend Forscht project (website)
In this repo you can find the website code for my AI news research project for the german science competition Jugend Forscht. The website is used to showcase AI generated and human made articles and collect user feedback.

## The project

This repo is a part of my project for the german science competition Jugend Forscht about the question "how well can ai be used to create news articles that are objective and have no halluzinations in it?". The project consists of a fined-tuned version of Mistral-7b to write news articles,a classification modell to categorize the articles, a system to collect halluzinations (based on GPT-3.5) and a website to collect user reviews.
#### Links:
- The scripts for analysing the collected data and create the articles: [News-creator](https://github.com/L-S-2020/News-creator)
- The project on the official site of Jugend Forscht: [Jugend Forscht BW](https://www.jugend-forscht-bw.de/projekt/journalismus-in-zeiten-kuenstlicher-intelligenz/) 
- News articles about the project: [GSG Waldkirch](https://www.gsg-waldkirch.de/aktuelles/jugend-forscht-leonard-stegle-gewinnt-1-preis-beim-regionalwettbewerb.html) [Badische Zeitung](https://www.badische-zeitung.de/waldkircher-gewinnt-regional-entscheid-mit-projekt-zu-kuenstlicher-intelligenz)


## Features

- **Main page**: On the main page you can see the latest articles uploaded.
![mainpage](https://raw.githubusercontent.com/L-S-2020/News-server/master/images/mainpage.png)
- **Category page**: Page to view the articles of a spezific categorie.
![category](https://raw.githubusercontent.com/L-S-2020/News-server/master/images/categorie.png)
- **Article page**: Shows the selected article.
![article](https://raw.githubusercontent.com/L-S-2020/News-server/master/images/article.png)
- **Review function**: Users can review the articles and give atip, if they think the article is made by ai or not.
![review](https://raw.githubusercontent.com/L-S-2020/News-server/master/images/review.png)
- **Data collection mode**: To collect as much data as possible, the data collection mode lets users quickly navigate through the articles and review them. (Used to collect article reviews from my teachers and class mates.)
![data collection](https://raw.githubusercontent.com/L-S-2020/News-server/master/images/datacollection.png)
- **Dashboard**: View the average reviews in realtime. 
![data collection](https://raw.githubusercontent.com/L-S-2020/News-server/master/images/dashboard.png)
## Setup

1. Clone the repository to your local machine.
2. Install the required Python packages using pip: `pip install -r requirements.txt`
4. Create the database (I would recommend to use a Postgresql database in production): `python manage.py migrate`
5. Create a superuser to access the admin panel: `python manage.py createsuperuser`
6. Start the server (In production you should use NGINX to host the site): `python manage.py runserver`

## Technologies Used

- Python
- Django
- HTML + Bootstrap CSS

## Urls

- `/` : Main page to view the latest upload articles
- `/article/'category'` : Display the articles belonging to the given categorie
- `/article/'category'/'article_id'` : Display the article with the given article_id
- `/admin`: Django admin panel
- `/welcome` : Welcome page to enter the data collection mode
- `/dashboard` : Dashboard to view the average reviews in realtime
- `/neuerArtikel/'alt_id'` : Get the next article (for the data collection mode)
- `/api/checkNumber` : Endpoint to check if an article already exists
- `/api/uploadArticle` : Endpoint to upload a new article
- `/api/aktualisieren` : Endpoint to get the latest data for the dashboard (uses a caching system)
- `/api/getbewertungen` : Endpoint to export all reviews as json