# CS470
## Tweepy Crawler

### Environments Specification
1. Python v3.5 or higher
2. Java SDK and JVM in path
3. NodeJs


### Before Start
```
pip3 install tweepy
pip3 install konlpy
pip3 install sklearn
pip3 install flask
pip3 install flask_restful
pip3 install flask_cors
cd ~/cs470-ai/server
mkdir timelines
mkdir timelines/wtf
cd ~/cs470-ai/client
npm install
```

### Python file description in alphabetic order
* aggressive_words_extractor.py: Extract influential words referring frequent_words.txt and store into good_or_bad_words.txt
* combine_csv.py: combine tac_pairs csv files into one csv file
* constants.py: Access token, secret key for using tweepy and etc setting
* frequent_words_extractor.py: Extract words written more than 10 times and save in frequent_words.txt
* id_extractor.py: read raw json data(data_search.txt) and group by user id and extract/refine only required data
* real_good_extractor.py: extract real influential words from good_or_bad_words.txt and store into real_good_words.txt
* search.py: Using twitter api(tweepy), crawl raw json data and make data_search.txt.
* tac_extractor.py: extract tac pairs from data refering wtf folder

### Step
1. Crawl twitter raw json data
2. Refine raw json data
3. Extract tac pairs (user_id, text, retweet, favorite, hashtag, create time)
4. Extract features from tac pairs
5. Train tac pairs with features

### Running in server file
#### start crawling
```
// in server directory
./start_search.sh
```
#### refine data and extract tac pairs
```
// in server directory
./tac_extractor.sh
```
#### extact features of tac pairs
```
// in server directory
./features.sh
```
#### train models
```
// in server directory
python3 model_generator.py
```

#### Run server
```
// in server directory
python3 api.py
```
### Running in client file
#### Run client
```
// in client directory
npm start
```
