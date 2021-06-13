# Advisor Network App(Python/Django) #
Advisor network is a simple web application built using django and rest framework where users can come and book an advisor for a call

## API's ##

### *Admin* ###
#### 1. API: Add an advisor
Admin can add new Advisors into the advisor network 
1. Method: POST
2. Endpoint: /admin
3. Request:
   * Advisor name
   * Advisor Photo URL
4. Response:
   * Body:List of Advisors
   * Status:
      * 200_OK if the request is successful
      * 400_BAD_REQUEST if any of the above fields are missing


### *User* ###
#### 1. API: Signup ####
User can an create account
1. Method: POST
2. Endpoint: /user/register/
3. Request:
   * Name
   * Email
   * Password
4. Response:
   * Body: List of Advisors
   * Status:
      * 200_OK if the request is successful
      * 400_BAD_REQUEST if any of the above fields are missing

#### 2. API: Can log in as a user ####
If a user already has a user account, then they can signin
1. Method: POST
2. Endpoint: /user/login/
3. Request:
   * Email
   * Password
4. Response:
   * Body: List of Advisors
   * Status:
      * 200_OK if the request is successful
      * 400_BAD_REQUEST if any of the above fields are missing

#### 3. API:List of Advisor ####
1. Method: GET
2. Endpoint: /user/`<user-id>`/advisor
3. Request:
   * Email
   * Password
4. Response:
   * Body: List of Advisors
   * Status:
      * 200_OK if the request is successful
      * 400_BAD_REQUEST if any of the above fields are missing
 
#### 4. API: Book an Advisor for a call ####
1. Method: POST
2. Endpoint: /user/`<user-id>`/advisor/`<advisor-id>`
3. Request: Booking time
4. Response:
   * Body: List of Advisors
   * Status:
      * 200_OK if the request is successful

#### 5. API: Get all the booked calls ####
1. Method: GET
2. Endpoint: /user/`<user-id>`/advisor/booking/
3. Request: None
4. Response:
   * Body: All booking of User
   * Status:
      * 200_OK if the request is successful

 




