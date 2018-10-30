from flask import Flask, render_template, request, session, redirect, url_for, flash
import pymysql
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'C:\\Users\\Mary\\Documents\\1.PycharmProgams\\RestaurantWebsiteFlaskProject\\static\\image'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/additem', methods=['POST', 'GET'])
def additem():
    if request.method == 'POST':  # check if user posted something
        item = request.form['item']
        description = request.form['description']
        cost = request.form['cost']

        if item == "":
            # flash('Email is empty')
            return render_template('add-item.html', msg_email="*Item is empty")
        elif description == "":
            # flash('Name is empty')
            return render_template('add-item.html', msg_name="*Description is empty")
        elif cost == "":
            # flash('Message is empty')
            return render_template('add-item.html', msg_comment="*Cost is empty")
        else:
            # save the three items to db
            # establish db connection
            con = pymysql.connect("localhost", "root", "", "sampledb")
            # execute sql
            # create a cursor object, cursor executes sql
            cursor = con.cursor()
            sql = "INSERT INTO meals_tbl(`item`,`description`,`cost`) VALUES(%s,%s,%s)"  # use tick marks ( ` ) instead of single quotes
            try:
                cursor.execute(sql, (item, description, cost))
                con.commit()  # commit changes to the db
                return render_template('add-item.html', msg="Uploaded!")
            except:
                con.rollback()
                return render_template('add-item.html', msg="Failed!")
    else:
        return render_template('add-item.html')


@app.route('/meals')
def showMealsItems():

    # we are pulling all records here
    con = pymysql.connect("localhost", "root", "", "sampledb")
    # create cursor to execute sql
    cursor = con.cursor()
    sql = "SELECT * FROM `meals_tbl` ORDER BY `id`"
    # execute sql
    cursor.execute(sql)
    if cursor.rowcount < 1:
        return render_template('trialHomepage.html', msg="No items found!")
    else:
        rows = cursor.fetchall()
        # send the rows back to the presentation rows
        return render_template('trialHomepage.html', mealsdata=rows)


# ==============================================================================

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'img-file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['img-file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return render_template('upload-image.html')


from flask import send_from_directory
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/menuimages', methods=['GET', 'POST'])
def menuimages():
    return render_template('menu-images.html')


if __name__ == "__main__":
    app.run(debug=True)


