
## greet
* greet 
  - action_greet_user

## Form Happy Path
* start_training
  - stage0_form
  - form{"name": "stage0_form"} 
  - form{"name": null}
  
## Form Sad Path
* start_training
  - stage0_form
  - form{"name": "stage0_form"} 
* stop_training
  - action_deactivate_form
  - form{"name": null}
  
## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
  
## Some questions for faq
* faq
  - respond_faq
 
