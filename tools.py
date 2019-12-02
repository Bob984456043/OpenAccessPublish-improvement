from routes import *


class Table:
    def __init__(self):
        self.name = ''
        self.thead = []
        self.items = []


class CommentTable(Table):
    def __init__(self):
        super().__init__()
        self.name = 'comment'
        self.thead.append('ID')
        self.thead.append("email")
        self.thead.append('target')
        self.thead.append('content')
        self.thead.append("date")
        self.thead.append('voteup')
        self.thead.append('votedown')
        comments = Comment.query.all()
        for c in comments:
            row = []
            row.append(c.id)
            row.append(c.email)
            row.append(c.target)
            row.append(c.content)
            row.append(c.date)
            row.append(c.voteup)
            row.append(c.votedown)
            self.items.append(row)


class ArticleTable(Table):
    def __init__(self):
        super().__init__()
        self.name = 'article'
        self.thead.append('ID')
        self.thead.append('Title')
        self.thead.append('Author')
        self.thead.append('Highlight')
        self.thead.append('Subject')
        self.thead.append('Email')
        self.thead.append('Date')
        self.thead.append('Pdf')
        self.thead.append('voteup')
        self.thead.append('votedown')
        articles = Article.query.all()
        for a in articles:
            row = []
            row.append(a.id)
            row.append(a.title)
            row.append(a.author)
            row.append(a.highlight)
            row.append(a.subject)
            row.append(a.email)
            row.append(a.date)
            row.append(a.pdf)
            row.append(a.voteup)
            row.append(a.votedown)
            self.items.append(row)


class BadWordTable(Table):
    def __init__(self):
        super().__init__()
        self.name = 'bad word'
        self.thead.append('id')
        self.thead.append('word')
        bad_words = BadWord.query.all()
        for b in bad_words:
            row = []
            row.append(b.id)
            row.append(b.word)
            self.items.append(row)


def remove_captcha():
    for file in os.listdir(os.path.join(app.root_path, 'static', 'captcha')):
        os.unlink(os.path.join(app.root_path, "static", "captcha", file))


def remove_article(id):
    a = Article.query.filter_by(id=id).first()
    if a is not None:
        os.unlink(os.path.join(app.root_path, 'static', 'pdf', a.pdf))  # remove files
        vote = VoteArticle.query.filter_by(target_id=a.id).all()
        for v in vote:  # remove related votes
            db.session.delete(v)
        comments = Comment.query.filter_by(target=a.id).all()
        for c in comments:  # remove related comments
            db.session.delete(c)
        db.session.delete(a)
        db.session.commit()
        return True
    return False


def showhide_article(id, action):
    if action == 'hide':
        Article.query.filter_by(id=id).update({'is_hide': 'yes'})
    else:
        Article.query.filter_by(id=id).update({'is_hide': 'no'})
    db.session.commit()


def remove_comment(id):
    c = Comment.query.filter_by(id=id).first()
    if c is not None:
        vote = VoteComment.query.filter_by(target_id=c.id).all()
        for v in vote:
            db.session.delete(v)
        db.session.delete(c)
        db.session.commit()
        return True
    return False


@app.route('/admin/<action>')
@app.route('/admin')
def administrator(action=None):
    if action is None:
        return render_template("admin.html", title="Admin", table=None)
    elif action == 'captcha':
        remove_captcha()
        return "yes"
    elif action == 'articles':
        a = ArticleTable()
        return render_template("admin.html", title="Admin", table=a)

    elif action == 'comments':
        c = CommentTable()
        return render_template("admin.html", title="Admin", table=c)
    elif action == 'badword':
        b = BadWordTable()
        return render_template('admin.html', title="admin bad words", table=b)
    abort(404)


# future work:add permission check
@app.route('/admin/<action>/<int:id>/<type>')
def admin_remove(action, id, type):
    if action == 'delete':
        if type == 'article':
            if remove_article(id):
                return "yes"
        elif type == 'comment':
            if remove_comment(id):
                return "yes"
    elif action == 'hide' or action == 'show':
        showhide_article(id, action)
        return "yes"
    abort(404)


from forms import *


class SubjectForm(FlaskForm):
    formname = "subject"
    name = StringField("Name", validators=[DataRequired()])
    father = StringField("Father", validators=[DataRequired()])
    depth = StringField("Depth", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/admin/subject/add', methods=['GET', 'POST'])
def add_subject():
    form = SubjectForm()
    if request.method == 'POST' and form.validate_on_submit():
        s = Subject()
        s.name = form.name.data
        ts = Subject.query.filter_by(name=form.father.data).first()
        s.super_subject = 0
        if ts is not None:
            s.super_subject = int(ts.id)
        s.depth = form.depth.data
        db.session.add(s)
        db.session.commit()
        return redirect('/admin/subject/add')
    return render_template("admin.html", title="add subject", form=form)


'''
Physical Sciences
    Physics
        Astronomy
	Quantum Mechanics
    Chemistry
    Environmental Sciences
Social Sciences
    Anthropology
    Sustainability Science
Biological Sciences
    Cell Biology
    Genetics
    Neuroscience **
    Plant Biology
    Developmental Biology
    System Biology
    Biochemistry
    Biophysics and Computational Biology
Computer Sciences
    Machine Learning
    Computational Biology
    Computational Complexity
    Computational Linguistics
Statistics
    Applied Statistics
    Mathematical Statistics
Mathematics
    Graphy Theory
    Number Theory
Medical Sciences
    Breast Cancer
    Ebola Virus
    Epidemics
    Dermatology General
    Immunity
    Obesity
    Neuroscience **
    
    INSERT INTO subject (id, depth, name, super_subject) VALUES (1, 0, 'Physical Sciences', '0');
INSERT INTO subject (id, depth, name, super_subject) VALUES (2, 1, 'Physics', '1');
INSERT INTO subject (id, depth, name, super_subject) VALUES (3, 2, 'Astronomy', '2');
INSERT INTO subject (id, depth, name, super_subject) VALUES (4, 1, 'Quantum Mechanics', '1');
INSERT INTO subject (id, depth, name, super_subject) VALUES (5, 1, 'Chemistry', '1');
INSERT INTO subject (id, depth, name, super_subject) VALUES (6, 1, 'Environmental Sciences', '1');
INSERT INTO subject (id, depth, name, super_subject) VALUES (7, 0, 'Social Sciences', '0');
INSERT INTO subject (id, depth, name, super_subject) VALUES (8, 1, 'Anthropology', '7');
INSERT INTO subject (id, depth, name, super_subject) VALUES (9, 1, 'Sustainability Science', '7');
INSERT INTO subject (id, depth, name, super_subject) VALUES (10, 0, 'Biological Sciences', '0');
INSERT INTO subject (id, depth, name, super_subject) VALUES (12, 1, 'Plant Biology', '10');
INSERT INTO subject (id, depth, name, super_subject) VALUES (13, 1, 'Developmental Biology', '10');
INSERT INTO subject (id, depth, name, super_subject) VALUES (14, 1, 'System Biology', '10');
INSERT INTO subject (id, depth, name, super_subject) VALUES (15, 1, 'Biochemistry', '10');
INSERT INTO subject (id, depth, name, super_subject) VALUES (16, 1, 'Biophysics and Computational Biology', '10');
INSERT INTO subject (id, depth, name, super_subject) VALUES (17, 0, 'Computer Sciences', '0');
INSERT INTO subject (id, depth, name, super_subject) VALUES (18, 1, 'Machine Larning', '17');
INSERT INTO subject (id, depth, name, super_subject) VALUES (19, 1, 'Computational Biology', '17');
INSERT INTO subject (id, depth, name, super_subject) VALUES (20, 1, 'Computational Complexity', '17');
INSERT INTO subject (id, depth, name, super_subject) VALUES (21, 1, 'Computational Linguistics', '17');
INSERT INTO subject (id, depth, name, super_subject) VALUES (22, 0, 'Statistics', '0');
INSERT INTO subject (id, depth, name, super_subject) VALUES (23, 1, 'Applied Statistics', '22');
INSERT INTO subject (id, depth, name, super_subject) VALUES (24, 1, 'Mathematical Statistics', '22');
INSERT INTO subject (id, depth, name, super_subject) VALUES (25, 0, 'Mathematics', '0');
INSERT INTO subject (id, depth, name, super_subject) VALUES (26, 1, 'Graphy Theory', '25');
INSERT INTO subject (id, depth, name, super_subject) VALUES (27, 1, 'Number Theory', '25');
INSERT INTO subject (id, depth, name, super_subject) VALUES (28, 0, 'Medical Sciences', '0');
INSERT INTO subject (id, depth, name, super_subject) VALUES (29, 1, 'Breast Cancer', '28');
INSERT INTO subject (id, depth, name, super_subject) VALUES (30, 1, 'Ebola Virus', '28');
INSERT INTO subject (id, depth, name, super_subject) VALUES (31, 1, 'Epidemics', '28');
INSERT INTO subject (id, depth, name, super_subject) VALUES (32, 1, 'Dermatology General', '28');
INSERT INTO subject (id, depth, name, super_subject) VALUES (33, 1, 'Immunity', '28');
INSERT INTO subject (id, depth, name, super_subject) VALUES (34, 1, 'Obesity', '28');
INSERT INTO subject (id, depth, name, super_subject) VALUES (35, 1, 'Neuroscience', '28');
'''
