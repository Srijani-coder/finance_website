import os,re,secrets, time

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import jsonify, abort
from functools import wraps
from flask import Flask,render_template,request,redirect,url_for,flash,Response
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import text, inspect
from werkzeug.middleware.proxy_fix import ProxyFix
from models import db,Admin,Client,SiteSetting,Post,Gallery,Service,Testimonial

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
app=Flask(__name__, static_folder=os.path.join(BASE_DIR,'static'), template_folder=os.path.join(BASE_DIR,'templates')); app.config['SECRET_KEY']=os.getenv('SECRET_KEY','local-demo-secret-change-before-deploy')
app.config['MAX_CONTENT_LENGTH']=8*1024*1024
app.wsgi_app=ProxyFix(app.wsgi_app,x_proto=1,x_host=1)
app.config['SESSION_COOKIE_HTTPONLY']=True
app.config['SESSION_COOKIE_SAMESITE']='Lax'
app.config['SESSION_COOKIE_SECURE']=os.getenv('RENDER','').lower()=='true' or os.getenv('FORCE_HTTPS','').lower()=='true'
dburl=os.getenv('DATABASE_URL','sqlite:///'+os.path.join(BASE_DIR,'site.db').replace('\\','/'))
if dburl.startswith('postgres://'): dburl='postgresql://'+dburl[len('postgres://'):]
if dburl.startswith('postgresql://') and 'sslmode=' not in dburl:
 dburl += ('&' if '?' in dburl else '?')+'sslmode=require'
app.config['SQLALCHEMY_DATABASE_URI']=dburl; app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app); login=LoginManager(app); login.login_view='client_login'
@login.user_loader
def load_user(uid):
 try: return db.session.get(Admin if uid.startswith('admin:') else Client,int(uid.split(':')[-1]))
 except (ValueError,IndexError): return None

def slugify(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def settings(): return SiteSetting.query.first()
def client_required(fn):
 @wraps(fn)
 def protected(*args,**kwargs):
  if not current_user.is_authenticated or not isinstance(current_user,Client): return redirect(url_for('client_login',next=request.path))
  return fn(*args,**kwargs)
 return protected

def upload_image(file):
 if not file or not file.filename:return None
 if not file.mimetype.startswith('image/') or file.mimetype not in ('image/jpeg','image/png','image/webp','image/gif'): return None
 try:
  import cloudinary,cloudinary.uploader
  if os.getenv('CLOUDINARY_CLOUD_NAME'):
   cloudinary.config(cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),api_key=os.getenv('CLOUDINARY_API_KEY'),api_secret=os.getenv('CLOUDINARY_API_SECRET'),secure=True)
   return cloudinary.uploader.upload(file,folder='finance-site')['secure_url']
 except Exception: pass
 if os.getenv('RENDER','').lower()=='true':
  raise RuntimeError('Configure Cloudinary before uploading images on Render (ephemeral filesystem).')
 upload_dir=os.path.join(BASE_DIR,'static','uploads'); os.makedirs(upload_dir,exist_ok=True); fn=secrets.token_hex(10)+'_'+secure_filename(file.filename); path=os.path.join(upload_dir,fn); file.save(path); return '/static/uploads/'+fn
@app.context_processor
def inject(): return dict(site=settings(),site_url=os.getenv('SITE_URL',request.url_root.rstrip('/')))
def initialize_database():
 with app.app_context():
  db.create_all()
  for col in ['twitter','profile_image','chatbot_intro','chatbot_plan','certifications']:
   try:
    if db.engine.dialect.name=='sqlite':
     existing=[x[1] for x in db.session.execute(text('PRAGMA table_info(site_setting)'))]
     if col not in existing: db.session.execute(text('ALTER TABLE site_setting ADD COLUMN '+col+' TEXT'))
   except Exception: db.session.rollback()
  if 'username' not in [c['name'] for c in inspect(db.engine).get_columns('admin')]:
   db.session.execute(text('ALTER TABLE admin ADD COLUMN username VARCHAR(80)'))
   db.session.commit()
  for existing_admin in Admin.query.all():
   if not existing_admin.username: existing_admin.username=('admin' if existing_admin.id==1 else 'admin'+str(existing_admin.id))
  if not SiteSetting.query.first(): db.session.add(SiteSetting(name='Debabrata Chakrabarti',tagline='Smart Finance, Strategic Growth',hero_title='Your money should be protected and should touch your goal',hero_text='35 years in financial services. Helping clients work towards financial freedom.',phone='9434193509',email='cdebabrata67@yahoo.com',address='KC Dutta Road, Uttar Ghosh Para, Chakdaha, Nadia',about='Meet Debabrata Chakrabarti, a financial services professional with 35 years of industry experience. Our vision is financial freedom through thoughtful planning and long-term relationships.'))
  if not Admin.query.first():
   initial_password=os.getenv('ADMIN_PASSWORD')
   if not initial_password:
    if os.getenv('RENDER','').lower()=='true': raise RuntimeError('Set ADMIN_PASSWORD in Render environment variables before deployment.')
    initial_password='pass'
   db.session.add(Admin(username=os.getenv('ADMIN_USERNAME','admin'),email=os.getenv('ADMIN_EMAIL','admin@example.com'),password_hash=generate_password_hash(initial_password)))
  if Service.query.count()==0:
   for a,b,c in [('Financial Distribution','Guidance and service support across suitable financial distribution offerings.','◈'),('Client Relationship','Relationship-led assistance, documentation coordination and ongoing service.','◎'),('Market Insights','Educational market updates and financial awareness content for clients.','↗')]: db.session.add(Service(title=a,description=b,icon=c))
  db.session.commit()
@app.route('/')
def home(): return render_template('home.html',posts=Post.query.filter_by(published=True).order_by(Post.created_at.desc()).all(),gallery=Gallery.query.order_by(Gallery.created_at.desc()).all(),services=Service.query.all(),testimonials=Testimonial.query.filter_by(approved=True).all())
@app.route('/signup',methods=['GET','POST'])
def signup():
 if request.method=='POST':
  name=request.form.get('name','').strip()[:120]; email=request.form.get('email','').strip().lower()[:160]; password=request.form.get('password','')
  if not name or not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+',email) or len(password)<12: flash('Enter your name, valid email and password of at least 12 characters.','bad')
  elif Client.query.filter_by(email=email).first(): flash('This email is already registered. Please sign in.','bad')
  else:
   c=Client(name=name,email=email,password_hash=generate_password_hash(password));db.session.add(c);db.session.commit();login_user(c);return redirect(url_for('home'))
 return render_template('client_auth.html',mode='signup')
@app.route('/login',methods=['GET','POST'])
def client_login():
 if request.method=='POST':
  c=Client.query.filter_by(email=request.form.get('email','').strip().lower()).first()
  if c and check_password_hash(c.password_hash,request.form.get('password','')):
   login_user(c); dest=request.args.get('next','/')
   return redirect(dest if dest.startswith('/') and not dest.startswith('//') else '/')
  flash('Invalid email or password.','bad')
 return render_template('client_auth.html',mode='login')
@app.route('/logout')
def client_logout(): logout_user();return redirect(url_for('home'))
@app.route('/about')
@client_required
def about(): return render_template('page.html',title='About Us',content=settings().about)
@app.route('/services')
@client_required
def services(): return render_template('services.html',services=Service.query.all())
@app.route('/gallery')
@client_required
def gallery(): return render_template('gallery.html',gallery=Gallery.query.order_by(Gallery.created_at.desc()).all())
@app.route('/blog')
@client_required
def blog(): return render_template('blog.html',posts=Post.query.filter_by(published=True).order_by(Post.created_at.desc()).all())
@app.route('/blog/<slug>')
@client_required
def post(slug): return render_template('post.html',post=Post.query.filter_by(slug=slug,published=True).first_or_404())
@app.route('/contact',methods=['GET','POST'])
@client_required
def contact():
 if request.method=='POST': return redirect('mailto:'+settings().email)
 return render_template('contact.html')
@app.before_request
def secure_admin():
 if request.path.startswith('/admin/') or request.path=='/admin':
  if request.endpoint not in ('admin_login','forgot_password','reset_password') and current_user.is_authenticated and not isinstance(current_user,Admin): abort(403)
@app.route('/admin/login',methods=['GET','POST'])
def admin_login():
 if request.method=='POST':
  u=Admin.query.filter_by(username=request.form.get('username','').strip()).first()
  if u and check_password_hash(u.password_hash,request.form['password']): login_user(u); return redirect(url_for('admin'))
  flash('Invalid credentials.','bad')
 return render_template('admin_login.html')
@app.route('/admin/forgot')
def admin_forgot(): return render_template('admin_forgot.html')
@app.route('/healthz')
def healthz():
 try:
  db.session.execute(text('SELECT 1'))
  return jsonify(status='ok'),200
 except Exception: return jsonify(status='unavailable'),503
@app.route('/admin/logout')
@login_required
def admin_logout(): logout_user(); return redirect(url_for('home'))
@app.route('/admin')
@login_required
def admin():
 if not isinstance(current_user,Admin): abort(403)
 return render_template('admin.html',clients=Client.query.order_by(Client.created_at.desc()).all(),client_count=Client.query.count(),posts=Post.query.order_by(Post.created_at.desc()).all(),gallery=Gallery.query.all(),services=Service.query.all())
@app.route('/admin/settings',methods=['POST'])
@login_required
def admin_settings():
 if not isinstance(current_user,Admin): abort(403)
 s=settings()
 for f in ['name','tagline','hero_title','hero_text','phone','email','address','about','facebook','linkedin','twitter','instagram','chatbot_intro','chatbot_plan','certifications']: setattr(s,f,request.form.get(f,'').strip())
 img=upload_image(request.files.get('cover_image'))
 if img:s.cover_image=img
 img=upload_image(request.files.get('profile_image'))
 if img:s.profile_image=img
 db.session.commit(); flash('Website settings updated.','ok'); return redirect(url_for('admin'))
@app.route('/admin/post',methods=['POST'])
@login_required
def admin_post():
 if not isinstance(current_user,Admin): abort(403)
 title=request.form['title'].strip(); base=slugify(title); slug=base; n=2
 while Post.query.filter_by(slug=slug).first(): slug=f'{base}-{n}'; n+=1
 p=Post(title=title,slug=slug,excerpt=request.form.get('excerpt'),body=request.form.get('body'),seo_title=request.form.get('seo_title'),meta_description=request.form.get('meta_description'),image=upload_image(request.files.get('image')),published=True)
 db.session.add(p); db.session.commit(); return redirect(url_for('admin'))
@app.route('/admin/post/<int:id>/edit',methods=['GET','POST'])
@login_required
def edit_post(id):
 if not isinstance(current_user,Admin): abort(403)
 post=db.get_or_404(Post,id)
 if request.method=='POST':
  for f in ('title','excerpt','body','seo_title','meta_description'): setattr(post,f,request.form.get(f,''))
  post.published=request.form.get('published')=='on'
  img=upload_image(request.files.get('image'))
  if img:post.image=img
  db.session.commit(); flash('Post updated.','ok'); return redirect(url_for('admin')+'#posts')
 return render_template('edit_post.html',post=post)
@app.route('/admin/password',methods=['POST'])
@login_required
def change_password():
 if not isinstance(current_user,Admin): abort(403)
 old=request.form.get('old_password',''); new=request.form.get('new_password','')
 if not check_password_hash(current_user.password_hash,old) or len(new)<12: flash('Incorrect current password or new password shorter than 12 characters.','bad')
 else:
  current_user.password_hash=generate_password_hash(new); db.session.commit(); flash('Password changed.','ok')
 return redirect(url_for('admin')+'#security')
@app.route('/admin/credentials',methods=['POST'])
@login_required
def admin_credentials():
 if not isinstance(current_user,Admin): abort(403)
 username=request.form.get('username','').strip()
 old=request.form.get('old_password','')
 if not re.fullmatch(r'[A-Za-z0-9_.-]{3,80}',username) or not check_password_hash(current_user.password_hash,old):
  flash('Invalid username or current password.','bad')
 elif Admin.query.filter(Admin.username==username,Admin.id!=current_user.id).first():
  flash('Username already in use.','bad')
 else:
  current_user.username=username
  db.session.commit()
  flash('Admin username updated.','ok')
 return redirect(url_for('admin')+'#security')
@app.route('/api/chat',methods=['POST'])
def chat():
 question=str((request.get_json(silent=True) or {}).get('message',''))[:600].lower(); site=settings()
 if any(k in question for k in ('step','plan my finance','financial plan','start')): answer=site.chatbot_plan+' Contact: '+(site.phone or 'Please use the contact section')+' | '+(site.email or 'Contact details coming soon')
 elif any(k in question for k in ('know your','planner','certif','qualification','expert','owner')):answer=site.chatbot_intro+' '+site.certifications
 else:answer='Welcome! Ask “Know your financial planner” or “How do I plan my finance step by step?” You can also reach our team through the contact section.'
 return jsonify(reply=answer,disclaimer='General information only; not personal financial advice. Verify any professional credentials independently.')
@app.route('/admin/post/<int:id>/delete',methods=['POST'])
@login_required
def delete_post(id): db.session.delete(db.get_or_404(Post,id)); db.session.commit(); return redirect(url_for('admin'))
@app.route('/admin/gallery',methods=['POST'])
@login_required
def admin_gallery():
 if not isinstance(current_user,Admin): abort(403)
 img=upload_image(request.files.get('image'))
 if img: db.session.add(Gallery(image=img,caption=request.form.get('caption'))); db.session.commit()
 return redirect(url_for('admin'))
@app.route('/admin/gallery/<int:id>/delete',methods=['POST'])
@login_required
def delete_gallery(id): db.session.delete(db.get_or_404(Gallery,id)); db.session.commit(); return redirect(url_for('admin'))
@app.route('/robots.txt')
def robots(): return Response(f'User-agent: *\nAllow: /\nDisallow: /admin\nDisallow: /login\nDisallow: /signup\nDisallow: /about\nDisallow: /services\nDisallow: /gallery\nDisallow: /blog\nDisallow: /contact\nSitemap: {os.getenv("SITE_URL",request.url_root.rstrip("/"))}/sitemap.xml\n',mimetype='text/plain')
@app.route('/sitemap.xml')
def sitemap():
 base=os.getenv('SITE_URL',request.url_root.rstrip('/')); urls=[base+'/',base+'/signup',base+'/login']
 return Response('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{u}</loc></url>' for u in urls)+'</urlset>',mimetype='application/xml')
if __name__=='__main__':
 print('Website: http://127.0.0.1:5000')
 print('Admin access: use the private /admin/login URL (not linked on the public website)')
 app.run(host='127.0.0.1',port=5000,debug=False)

# Initialize tables and small backward-compatible schema changes at process startup.
initialize_database()
