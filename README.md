<h1>Well, Hello there!</h1>

I pity those of you who want to set the project up and running on your local env.

If you want to try still, you'll probably want to use Ubuntu with MongoDB.

That being said, the system is adapted to a very specific set of data which I cannot distribute for legal reasons. The reason I am sharing the code is because, well, maybe someone takes some good ideas from here one of these days!

<h4>So, what are the goals of this project?</h4>
<li>We want to create an online service that receives a GET petition with a username and returns a set of recommendations</li>
<li>The recommendations are structured by categories. We only send the top 3 categories (We'll how the relevance is determined later)</li>
<li>The recommendation is based on Collaborative Filtering (based on the activity of all our users)</li>
<li>We are going to infer what this patterns made by the user activity with a neural network and data extracted from a DB</li>

* In this particular case, the DB is a MongoDB.

<h4>So, how was it done?</h4>
<li>A Django server that listens to GET petitions and communicates with the recommender system</li>
<li>A Recommender System with a single-method API that responds to the server and trains the NN with info coming from DB</li>
<li>A 3-layer Fully Connected NN with 2 layers made out of RLU neurons and one sigmoid neuron in the output layer (so we can estimate the sigmoid range [0, 1] as the estimated rating of a given product</li>

<h4>The overall process</h4>
For each product we try to predict the rating that each user will give it and then pack them in categories sorted by predicted rating with a maximum of 10 elements.

To accomplish this, we generate training data taken from stored real ratings from users to products. We take as many transactions userXproduct --> rating as possible, then for each one we extract the logged rating as well as the characteristics of the user (gender, nationality, age and sex) and the product (average rating and category) and then send to the NN a training set of user_characteristicsXproduct_characteristics --> rating.

This results in our NN being trained and ready to make predictions. We can use it now to process the <i>holes</i> in the rating of our sparse rating matrix of usersXproducts. For this we just repeat the same process, taking combinations of {user, product} and calling the <i>predict()</i> method of the NN.

In order to answer to the server blazingly fast, we do the recommendation job before in a continuous batch process that does the thing that I just described and then stores for each user a list of categories with the recomendations. As mentioned before, each category holds 10 products of the category it represents. All categories are calculated but only three are stored as final and sent back to the server, those that have the highest rating summing up the top 10 individual product estimated ratings.

<h4>Side note</h4>
Interestingly, I noticed that the RLU learned much faster than other neuron models. My best guess is that this is because my inputs were not normalized between [0, 1]. Instead, I was sending values as <i>age</i> in a range of [14, 100] (and RLU does not have upper activation limit).

I observed that the NN was good at determining things like ageing being a good or a bad factor depending on the product category (say, good for books, bad for videogames) also making distinctions about gender, and giving almost always a big weight to the average rating.

It is quite impressing how a simple model like this one was capable of learning so much with a reduced set of data. It would be definitely worth it taking a look at what's going on in Spotify's recommender, for instance.
