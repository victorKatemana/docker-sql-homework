#Base Image
FROM python:3.12.8-slim

#set the working directory
WORKDIR /app

#copy requirements.txt and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

#copy the python script and data files
COPY load_data.py  .
COPY green_tripdata_2019-10.csv .
COPY taxi_zone_lookup.csv .

#run the python script
CMD [ "python", "load_data.py" ]