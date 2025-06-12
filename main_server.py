from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import util
import util_D
import util_Ch
import util_mum

app = Flask(__name__)
app.secret_key = "supersecretkey"  

VALID_USER = {
    "email": "test@example.com",
    "password": "password123",
    # "email": 'ram_yeet1108@gmail.com',      
    # "password": 'yeet'
}




@app.route("/")
def home():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))
    return render_template("city_price_prediction.html")  

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if email == VALID_USER["email"] and password == VALID_USER["password"]:
        session["user"] = email  
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


@app.route("/get_location_names")
def get_location_names():
    city = request.args.get("city")  
    if city == "Delhi":
        locations = util_D.get_location_names_delhi()
    elif city == "Chennai":
        locations = util_Ch.get_location_names_chennai()
    elif city == "Mumbai":
        locations = util_mum.get_location_names_mumbai()
    else:
        locations = util.get_location_names()
    
    response = jsonify({"locations": locations})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/predict_home_price", methods=["POST"])
def predict_home_price():
    if "user" not in session:  
        return jsonify({"message": "Unauthorized"}), 403

    city = request.form.get("city")  # Get city from form data
    total_sqft = float(request.form["total_sqft"])
    location = request.form["location"]
    bhk = int(request.form["bhk"])
    bath = int(request.form["bath"])

    
    if city == "Delhi":
        estimated_price = util_D.get_price_delhi(location, total_sqft, bhk, bath)
    elif city == "Chennai":
        estimated_price = util_Ch.get_price_chennai(location, total_sqft, bhk, bath)
    elif city == "Mumbai":
        estimated_price = util_mum.get_price_mumbai(location, total_sqft, bhk, bath)
    else:
        estimated_price = util.get_price(location, total_sqft, bhk, bath)

    response = jsonify({"estimated_price": estimated_price})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    util.load_artifacts()
    util_D.load_artifacts_delhi()
    util_Ch.load_artifacts_chennai() 
    util_mum.load_artifacts_mumbai()
    app.run(debug=True)
