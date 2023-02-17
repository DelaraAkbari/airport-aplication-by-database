from databse import render_template,request,flash,redirect,make_response,app,Users,db
import os

flight_numbers=["1112","4565","7845","3212"]
flight_time=["12:30","13:15","16:45","18:00"]

db.create_all()
avatar_path='./static/avatar/'
@app.route('/',methods=['GET','POST'])
def home():
        return render_template("index_2.html",flight_number=flight_numbers,flight_time=flight_time,items=len(flight_numbers))

@app.route('/panel')
def panel():
    if request.cookies.get("user"):
        return render_template("panel_2.html",user=request.cookies.get("user"),avatar=avatar_path)
    else:
        flash("you most login first", "danger")
        return redirect('/login')
@app.route('/about')
def about():
        return render_template("about_2.html")

@app.route('/contact')
def contact():
        return render_template("contact.html")
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        found=False
        for user in Users.query.all():
            if request.form.get('username') == user.username and request.form.get('password') == user.password:
        # for i in range(len(username_list)):
        #     if request.form.get('username')==username_list[i] and request.form.get('password')==password_list[i]:
                found=True
                flash("login successfully","success")
                flash("wellcome dear user", "info")
                flash("nice to see you again", "warning")
                response=make_response(redirect('/panel'))
                response.set_cookie("user",request.form.get('username'))
                return response
        if found==False:
            flash("username or password invalid","danger")
            return redirect('/login')
    else:
        return render_template("login_2.html")
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        if request.form.get('password')==request.form.get('re_password'):
            found=False
            for user in Users.query.all():
                if request.form.get('username')==user.username:
                    found=True
                    flash("the username is exist,please select an other one", "warning")
                    return redirect('/register')
        if found==False:
            # username_list.append(request.form.get('username'))
            # password_list.append(request.form.get('password'))
            user = Users(username=request.form.get('username'),password=request.form.get('password'))
            db.session.add(user)
            db.session.commit()
            flash("the user registered successfully", "success")
            return redirect('/login')
    else:
        return render_template("register_2.html")
@app.route('/add',methods=['GET','POST'])
def add():
    if request.method=='POST':
        found=False
        for i in range(len(flight_numbers)):
                if request.form.get('flight_number')==flight_numbers[i]:
                    found=True
                    flash("the flight number is exist", "warning")
                    return redirect('/add')
        if found==False:
            flight_numbers.append(request.form.get('flight_number'))
            flight_time.append(request.form.get('flight_time'))
            flash("flight added successfully", "info")
            return redirect('/')
    else:
        return render_template("add_2.html")

@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method=='POST':
        found=False
        for i in range(len(flight_numbers)):
                if request.form.get('flight_number')==flight_numbers[i]:
                    found=True
                    flight_numbers.remove(request.form.get('flight_number'))
                    flight_time.remove(request.form.get('flight_time'))
                    flash("flight deleted successfully", "info")
                    return redirect('/delete')
                    break
        if found==False:
            flash("invalid flight number", "warning")
            return redirect('/delete')
    else:
        return render_template("delete.html")
@app.route('/logout')
def logout():
        response=make_response(redirect('/login'))
        response.delete_cookie('user')
        return response

@app.route('/profile',methods=["get","post"])
def profile():
    if request.cookies.get('user'):
        if request.method=='POST':
            response = make_response(redirect('/panel'))
            if request.form.get('new_username'):
                for user in Users.query.all():
                    if user.username==request.cookies.get('user'):
                        user.username=request.form.get('new_username')
                        flash("username changes successfuly","success")
                        response.delete_cookie('user')
                        response.set_cookie("user", request.form.get('new_username'))
                        avatar_name=request.form.get('new_username')
            else:
                avatar_name = request.cookies.get('user')
            if request.files.get("avatar"):
                avatar = request.files.get('avatar')
                avatar.save(os.path.join(avatar_path, avatar_name+".jpg"))
            return response
        else:
            return render_template('profile.html',user=request.cookies.get('user'))


    else:
        return redirect('/login')


if __name__=='__main__':
    app.run(host="0.0.0.0",port=1111,debug=True)