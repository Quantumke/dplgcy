from django.shortcuts import get_object_or_404, render_to_response,render
from blog.models import Entry, Link, Category,fakeusers
from django.template import RequestContext
from datetime import datetime, timedelta
from django.contrib.comments.models import Comment
from django.db.models import F
from django.contrib.auth.models import User
# Create your views here.

def entries_index(request):
	marque=Entry.objects.all().order_by('-pub_date')[:3]
	newest=Entry.objects.filter(pub_date=datetime.today())[:4]
	new_stories=Entry.objects.filter(pub_date=datetime.today())
	new_stories=new_stories.count()
	featured=Entry.objects.filter(featured=True).order_by('-pub_date')[:4]
	item_big=Entry.objects.filter(tags='Explicit').order_by('-pub_date')[:1]
	item_small=Entry.objects.all().order_by('-pub_date')[:4]
	this_week_featured=Entry.objects.filter(featured=True).order_by('-pub_date')[:4]
	featured_last_week = Entry.objects.filter(pub_date__lt=F('pub_date') - timedelta(days=7))
	last_month= datetime.today() - timedelta(days=30)
	featured_last_month = Entry.objects.filter(pub_date__lt=F('pub_date') - timedelta(days=30))
	all_stories=Entry.objects.all().order_by('-pub_date')[:5]
	sponserd=Entry.objects.filter(tags='sponsored').order_by('-pub_date')[:5]
	campus=Entry.objects.filter(tags='campus').filter(featured=True).order_by('-pub_date')[:1]
	politics=Entry.objects.filter(tags='politics').filter(featured=True).order_by('-pub_date')[:1]
	f_campus=Entry.objects.filter(tags='campus').order_by('-pub_date')[:5]
	f_politics=Entry.objects.filter(tags='politics').order_by('-pub_date')[:5]
	popular=Entry.objects.filter(tags='popular').order_by('-pub_date')[:5]
	recent=Entry.objects.all().order_by('-pub_date')[:5]
	comments=Comment.objects.all().order_by('-submit_date')[:5]
	trending=Entry.objects.all().order_by('-pub_date')[:5]
	most_recent=Entry.objects.all().order_by('-pub_date')[:1]
	#print most_recent
	other_recent=Entry.objects.all().order_by('-pub_date')[:3]
	news=Entry.objects.filter(tags='news').order_by('-pub_date')[:4]
	count_more_stories=Entry.objects.filter(tags='news')
	count_more_stories=count_more_stories.count()
	count_more_stories=	count_more_stories-4
	count_today_unread=newest.count()
	count_today_unread=count_today_unread-4
	cats=Category.objects.all()
	return render_to_response('index.html',
							  {'entries': Entry.objects.all(),
							   'marque':marque,
							   'new_stories':new_stories,
							   'featured':featured,
							   'item_big':item_big,
							   'item_small':item_small,
							   'this_week_featured':this_week_featured,
							   'featured_last_week':featured_last_week,
							   'featured_last_month':featured_last_month,
							   'all_stories':all_stories,
							   'sponserd':sponserd,
							   'campus':campus,
							   'politics':politics,
							   'f_campus':f_campus,
							   'f_politics':f_politics,
							   'popular':popular,
							   'recent':recent,
							   'comments':comments,
							   'trending':trending,
							   'most_recent':most_recent,
							   'other_recent':other_recent,
							   'news':news,
							   'count_more_stories':count_more_stories,
							   'newest':newest,
							   'count_today_unread':count_today_unread,
							   'cats':cats

							   })



def view_more(request, slug):
	#count=Entry.objects.get(slug=slug)
	#print count
	marque = Entry.objects.all().order_by('-pub_date')[:3]
	trending = Entry.objects.all().order_by('-pub_date')[:5]
	recent = Entry.objects.all().order_by('-pub_date')[:5]
	comments = Comment.objects.all().order_by('-submit_date')[:5]
	cats = Category.objects.all()
	# user = User.objects.get(username=request.user.username)
	# bio=fakeusers.objects.filter(user=user)
	o=Entry.objects.get(slug=slug)
	author_id= o.author_id
	bio=User.objects.get(id=author_id)
	id= bio.id
	bio=fakeusers.objects.filter(user_id=id)
	return render_to_response('entry_detail.html',{
	'object':get_object_or_404(Entry, slug=slug),
		'marque':marque,
		'bio':bio,
		'trending':trending,
		'recent':recent,
		'comments':comments,
		'cats':cats
	},RequestContext(request))

def search(request):
	query=request.GET.get('q', '')
	results=[]
	marque = Entry.objects.all().order_by('-pub_date')[:3]
	recent = Entry.objects.all().order_by('-pub_date')[:5]
	comments = Comment.objects.all().order_by('-submit_date')[:5]
	trending = Entry.objects.all().order_by('-pub_date')[:5]
	if query:
		results=Entry.objects.filter(title__contains=query)
		count=results.count()
	return render_to_response('search.html', {'query':query, 'results':results,
											  'marque':marque, 'count':count,
											  'recent':recent,'comments':comments,
											  'trending':trending})
def category_list(request):
	return render_to_response('category_list.html',
                                  { 'object_list': Category.objects.all() })

def category_detail(request, slug):
	return render_to_response('entry_detail.html', {
		'object': get_object_or_404(Entry, category=slug)
	}, RequestContext(request))