# doing necessary imports

from flask import Flask, render_template, request,jsonify
# from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pymongo
from flask_cors import CORS,cross_origin

app = Flask(__name__)  # initialising the flask app with the name 'app'

@app.route('/review',methods=['POST','GET'])
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/',methods=['POST','GET']) # route with allowed methods as POST and GET
@cross_origin()
def index():
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ","") # obtaining the search string entered in the form
        try:
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString # preparing the URL to search the product on flipkart
            uClient = uReq(flipkart_url) # requesting the webpage from the internet
            print('read')
            flipkartPage = uClient.read() # reading the webpage
            uClient.close() # closing the connection to the web server
            flipkart_html = bs(flipkartPage, "html.parser") # parsing the webpage as HTML
            bigboxes = flipkart_html.findAll("div", {"class": "cPHDOP col-12-12"}) # seacrhing for appropriate tag to redirect to the product link
            del bigboxes[0:3] # the first 3 members of the list do not contain relevant information, hence deleting them.
            box = bigboxes[0] #  taking the first iteration (for demo)
            productLink = "https://www.flipkart.com" + box.a['href'] # extracting the actual product link
            prodRes = requests.get(productLink) # getting the product page from server
            prod_html = bs(prodRes.text, "html.parser") # parsing the product page as HTML
            commentboxes = prod_html.find_all('div', {'class': "RcXBOT"}) # finding the HTML section containing the customer comments
            reviews = [] # initializing an empty list for reviews
            #  iterating over the comment section to get the details of customer and their comments
            for commentbox in commentboxes:
                try:
                    name = commentbox.find('p',{'class':'_2NsDsF AwS1CA'}).text

                except:
                    name = 'No Name'

                try:
                    rating = commentbox.find('div', {'class':'XQDdHH Ga3i8K'}).text

                except:
                    rating = 'No Rating'

                try:
                    commentHead = commentbox.find('p',{'class':'z9E0IG'}).text
                except:
                    commentHead = 'No Comment Heading'
                try:
                    # comtag = commentbox.div.div.find_all('div', {'class': ''})
                    custComment = commentbox.find('div', {'class':'ZmyHeo'}).div.div.text
                except:
                    custComment = 'No Customer Comment'
                #fw.write(searchString+","+name.replace(",", ":")+","+rating + "," + commentHead.replace(",", ":") + "," + custComment.replace(",", ":") + "\n")
                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment} # saving that detail to a dictionary

                reviews.append(mydict) #  appending the comments to the review list
            return render_template('results.html', reviews=reviews) # showing the review to the user
        except Exception as e:
            print(e)
            return 'something is wrong'
            #return render_template('results.html')
    else:
        return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True) # running the app on the local machine on port 8000
