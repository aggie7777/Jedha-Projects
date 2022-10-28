Instant Machine Learning Web Application with Streamlit and FastAPI

The goal of this project is to build complete end-to-end Regression ML model, Backend RestAPI to serve this model and front end UI so end user can interact and use it through web browser. Complete implementation is done Python language. 
![archiBMW](https://user-images.githubusercontent.com/59807046/198572006-40b97c78-15ca-47de-b454-1b35607a3a93.png)

1. Build ML Model (In my case I did regression model)
2. Develop REST API as Backend ( I use FastAPI framework in python)
3. Develop Front End UI (I use Streamlit an open-source app framework as web applications)

These two services can then be deployed in two Docker containers and orchestrated using Docker Compose.
To wire the containers together I used docker-compose.yml 
Each service requires its own Dockerfile to assemble the Docker images. A Docker Compose YAML file is required to define and share both container applications. 
