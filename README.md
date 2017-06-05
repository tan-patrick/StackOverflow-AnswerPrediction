# UCLA 17S CS 249 Final Project 

## Overall Framework 

1. Feature Extraction
2. Learning-to-Rank

## Implemented Features

* User Features
    * user_age [1 numerical features]
    * user_badge [categorical features]
    * user_reputation [1 numerical features]
    * user_views [1 numerical features]
    * user_votes [1 numerical features]
* User-User Features
    * user-user interactions [1 numerical features]
* Post Features
    * comment_cnt [1 numerical feature]

## Instructions

### Preprocessing
```bash
cd src/preprocess
./preprocess.py [name of dataset]
```

* Convert the format from XML to JSON
* Convert HTML-like contents into plaintext
* Link each question to the corresponding answers
    * See _data/[name of dataset]/question_answer_mapping.json_ after preprocessing
* Split the whole set into training and testing sets
    * See _data/[name of dataset]/train.\*_ and  _data/[name of dataset]/test.\*_
    * Questions without the best answer (ground truth) and with less than two answers are removed 


### Example of Feature Extraction
**Extract user_age features**
```bash
cd src/feature_extraction
./user_age.py [name of dataset]
```


## Directory Descriptions

Here some descriptions briefly show the purpose of each directory.

* __raw/__: The directory for the raw data (i.e., *Posts.xml*, *Users.xml*, etc) 
    * __raw/[name of dataset]/__: the corresponding raw data for a certain dataset (e.g., *StackOverflow*)
    * Note that the file names should not be modified.
* __data/__: The directory for the preprocessed data
    * __data/[name of dataset]/__: the corresponding preprocessed data for a certain dataset (e.g., *StackOverflow*)
* __src/__: The directory for all source codes
    * __src/preprocess/__: Codes for preprocessing raw data
* __model/__: The directory for some trained model on large English corpus