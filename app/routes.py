from app import app

# Landing Page
@app.route('/', methods=['GET', 'POST'])
def index():
    '''Main landing page'''
    # if flask.request.method == POST
    #    handleUserPost(flask.request.values.get('postText'))
    #
    #  This would just handle when users want to submit things to the board?
    return "Hello, Index!"

# Categories (can split if need be later on)
@app.route('/categories/', defaults={'category': None}, methods=['GET'])
@app.route('/categories/<category>/', methods=['GET'])
def categories(category):
    '''Categories page'''
    if category == None:
        return "Select a category"
    elif category != "":
        return f"welcome to the category {category}"
    
# Main profile page - maybe use cookies?? Need a sign in page probs /profile/signin?
@app.route('/profile', methods=['GET'])
def profile():
    '''Profile page'''
    # if signedInProfile == None:
    #    return redirect("https://www.127.0.0.1:5000/profile/signin")??? Maybe idk
    return "welcome to your profile!"

@app.route('search/<searchedFor>', methods=['GET'])
def search():
    '''Search Bar Functionality'''
    # Handle what ever it is that the search bar needs to handle - string matching etc.


    