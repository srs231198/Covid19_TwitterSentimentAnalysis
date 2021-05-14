# Covid19_TwitterSentimentAnalysis
Visualizations of tweets about Covid19 based on sentiment and geolocation.

Steps to run ->
1. Run Stream.py using 'Python3 Stream.py'
2. Enter the hastags you want searched
3. Run Spark.py on a separate terminal using 'Python3 Spark.py'
4. Data should be logged to your cluster on Elasticsearch as specified in the cloud_id
5. Create an Index pattern in Kibana to retreive data from Elasticsearch cluster
6. Use data to create the required visualizations

Heatmap based on Tweet locations in the US
![image](https://user-images.githubusercontent.com/28936137/118322057-2444a400-b4c4-11eb-9b9a-d6ce0093a414.png)

Heatmap based on locations of Negative tweets in India
![image](https://user-images.githubusercontent.com/28936137/118322360-9ddc9200-b4c4-11eb-8694-6e0e35ab2a55.png)

Top locations for tweets in the US
![image](https://user-images.githubusercontent.com/28936137/118322712-31ae5e00-b4c5-11eb-8b47-5af2fa8ad78f.png)

Top 40 states by tweets
![image](https://user-images.githubusercontent.com/28936137/118322846-63bfc000-b4c5-11eb-9c37-546c0abd02c0.png)

Top 100 Cities
![image](https://user-images.githubusercontent.com/28936137/118322947-85b94280-b4c5-11eb-8420-8d465149c32d.png)
