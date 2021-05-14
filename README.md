# Covid19_TwitterSentimentAnalysis
Visualizations of tweets about Covid19 based on sentiment and geolocation.

Steps to run ->
1. Run Stream.py using 'Python3 Stream.py'
2. Enter the hastags you want searched
3. Run Spark.py on a separate terminal using 'Python3 Spark.py'
4. Data should be logged to your cluster on Elasticsearch as specified in the cloud_id
5. Create an Index pattern in Kibana to retreive data from Elasticsearch cluster
6. Use data to create the required visualizations

