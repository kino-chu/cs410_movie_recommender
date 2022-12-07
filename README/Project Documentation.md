Movie Recommender Documentation 

Project Overview 

   The moive recommender is an simple but powerful application that recommends similar movies based on moive description similarity between users' favourite moive and recommended ones. The application incorproates over 8,800 movie from Netflix and specifically, it requests the user to select one movie as their favourite from those 8,800 ones and then it will recommend the top 5 similar movies based on description similarity. In addition to similar movie recommendation, it offers quick look up of basic movie information including type, director, cast, country, release year, rating, duration, and description. 
    
Library and models 
   
   The application leverages dash to enable the back end, front end and call back functions to return results based on user inputs. 'rank_bm25' is the main package used to calculate and derive the similarity between two movie descriptions. 'pandas' data frame is used to take in the data and store basic movie information. 
    
Code Structure 

   The following diagram describes the high-level code structure for implementing the application. 
   
![image](https://user-images.githubusercontent.com/101125363/206075239-327df9a6-19a8-4bb7-8d05-3a3562b9ce3b.png)

Instruction to run the code 

   Download 'netflix_title.csv' and 'MovieRecommenderApp.py' locally into the same folder and run the MovieRecommenderApp.py file in terminal. The following message will display with a link to the application: http://127.0.0.1:8050/. Click the link to go to the application. Potential dependencies in case user hasn't installed required packages, they could run: 
                 
         pip install pandas 
         pip install dash 
         pip install rank_bm25 
   
   ![image](https://user-images.githubusercontent.com/101125363/206076729-2bd8688f-0c65-421e-8c1f-6246675153e6.png)



  
