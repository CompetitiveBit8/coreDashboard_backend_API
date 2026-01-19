            ------------HTTP Methods and Routes-----------
This is my firt major FastAPI project where I tested some http methods.

This is a simple password protected memo app. The app has 11 routers which include:
1. GET  --  / or Root
2. POST  --  /Signup
3. POST  --  /Signin and Access token router
4. POST  --  (Access point) /Refresh router
5. PATCH  --  /details  -  User Detail Completion
6. GET  --  /getDetails - Gets User Details
7. GET  --  /getMemo/{user_name} 
8. POST  --  /inputMemo
9. GET  --  /getAllMemo
10. DELETE  --  /deleteMemo
11. GET  --  /decode

         -------------Brief Explanation of what the App Does------------
The user gets to signup and login before he can input any memo or complete the user details. He can get all the memos at once and can get them individually by title.

Here I used the GET, POST, PATCH and DELETE methods extensively. 

          --------------Authentication anad Authorisation------
I also worked on Authentication and Authorization which worked well. This also worked to prevent unauthorised access to protected routes which include the following
- Patch for User Detail Completion
- Get (user) Details
- Get (individual) memos (by title)
- Input Memo
- Get All Memo
- Delete Memo
- Get Current User

             ------------Database Management------------
I Practiced the use of Two tables containing two different categories of data: User information and 
Memo table. I was able to input, retrieve, update and delete data from these tables


           ------------Python Basics Refreshers--------------
In the course of this project, I practiced some python basics like loops and Data structures 
such as List and Dictionary


           -------------Enviroment settings and configuration-----------
I also learnt how to configure the environment variables using the environment and the config files before importing them for use in the program
