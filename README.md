# CryptoVision
--- 

CryptoVision is a crypto currency research and portfolio management solution. The primary purpose of this app is to beta demo Python and Django interactions. This project is based on an automated spreadsheet used to manage cryptocurrency research, price monitoring, and portfolio management over a six year period from 2016 to 2022. 

## Technologies Used: 
--- 

- HTML
- CSS
- Python
- Django
- [Environs] (https://github.com/sloria/environs)
- [Materialize] (https://materializecss.com/)
- [Heroku] (https://www.heroku.com/)
- [Bit.io] (https://bit.io/)
- [CoinGecko API] (https://www.coingecko.com/en/api)

## Screenshot(s):
--- 
CryptoVision Main Page:
Pages to be added...
<!-- ![Login](images/login_screen.png) -->

## Getting Started: 
--- 

A live version of this app is hosted on Heroku. To use the app, please visit the following link: [CryptoVision] (https://cryptovision.herokuapp.com/)

### Features:
--- 
- [X] Authentication
  - [X] Login/Logout
  - [X] Sign Up
- [X] Authorization
  - [X] Restricted access to app functions until user is logged in
  - [X] User coin list and holdings tied to user account
- [X] Multiple Models
  - [X] Coin - Global Coin Information
    - [X] User ability to add, edit, and delete coins
  - [X] User Coin - User Specific Coin Information
    - [X] User ability to add, edit, and delete User Coins
  - [X] Holdings - User Specific Holding Information, Sub of User Coin
    - [X] User ability to add, edit, and delete Holding Items
  - [X] Recommendation - User Specific Recommendation Information
    - [X] User ability to add, edit, and delete Recommendations
  - [ ] Notes - Field for information over time
    - [ ] User ability to add, edit, and delete notes
- [X] Add a Coin from CoinGecko API
  - [X] Search CoinGecko API for Coin
  - [X] Display Currency Name, Symbol, CoinGeck ID
  
- [X] Admin View
  - [X] Ability to add, edit, and delete coins
  - [X] Ability to add, edit, and delete user coins
  - [X] Ability to add, edit, and delete holding items

### Future Enhancements:
- [ ] Scheduled API query to CoinGecko for Updates
- [ ] Exchange Model for Coins
- [ ] Influencer Tracking Model for Coins
- [ ] Reporting and Analytics
  - [ ] Pie Chart of Holdings
  - [ ] Heatmap of Holdings (% change)
  - [ ] Profitability of Holdings
  - [ ] Portfolio Performance

## Project MVP Description and Rubric
--- 

- [X] Be a full-stack Django application.
- [X] Persist data in PostreSQL.
- [X] Have two models Minimum.
- [X] Authenticate users using Django's built-in authentication.
- [X] Implement authorization by restricting access to the Creation, Updating & Deletion of resources.
- [X] Be deployed online using Heroku.
- [X] Have Professional Styling utilizing a CSS framework/library like Materialize or Bootstrap. (Should not be an exact replica of the catcollector app)

