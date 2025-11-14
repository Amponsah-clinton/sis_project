from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
import time
import csv
import io
from .forms import (
    SearchForm, ContactForm, UserRegistrationForm, ArticleForm, ArticleAuthorForm,
    JournalForm, JournalEditorForm, ProjectForm, ProjectContributorForm,
    MembershipRequestForm, DirectoryApplicationForm, HallOfFameApplicationForm,
    PlagiarismCheckForm, PlagiarismWorkForm, ThesisToArticleForm, ThesisToBookForm,
    ThesisToBookChapterForm, PowerPointPreparationForm
)
from .models import (
    UserProfile, Article, ArticleAuthor, Journal, JournalEditor, Project, ProjectContributor,
    MembershipRequest, DirectoryApplication, HallOfFameApplication, PlagiarismCheck,
    PlagiarismWork, ThesisToArticle, ThesisToBook, ThesisToBookChapter, PowerPointPreparation
)

def landing(request):
    """Landing page view"""
    search_form = SearchForm()
    # Get latest articles for the landing page
    latest_articles = Article.objects.filter(status='approved').order_by('-created_at')[:6]
    return render(request, 'app/landing.html', {
        'search_form': search_form,
        'latest_articles': latest_articles,
    })

def browse(request):
    """Browse articles view"""
    search_form = SearchForm(request.GET or None)
    results = []
    
    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        # Search articles in database
        results = Article.objects.filter(title__icontains=query) | Article.objects.filter(abstract__icontains=query)
        messages.info(request, f'Found {results.count()} results for: {query}')
    
    return render(request, 'app/browse.html', {
        'search_form': search_form,
        'results': results,
    })

def submit(request):
    """Submit research view"""
    contact_form = ContactForm(request.POST or None)
    
    if request.method == 'POST':
        if contact_form.is_valid():
            # Here you could save to a Contact model if needed
            messages.success(request, 'Thank you for your submission!')
            return redirect('app:landing')
    
    return render(request, 'app/submit.html', {
        'contact_form': contact_form,
    })

def about(request):
    """About page view"""
    return render(request, 'app/about.html')

def auth(request):
    """Login/Register page view"""
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'login':
            username_or_email = request.POST.get('username_or_email')
            password = request.POST.get('password')
            
            # Try to authenticate with username or email
            user = authenticate(request, username=username_or_email, password=password)
            if user is None:
                # Try with email
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('app:dashboard')
            else:
                messages.error(request, 'Invalid username/email or password')
            
        elif form_type == 'register':
            # Create username from email if not provided
            email = request.POST.get('email')
            name = request.POST.get('name', '')
            username = request.POST.get('username', email.split('@')[0] if email else 'user')
            
            # Ensure username is unique
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            # Split name into first_name and last_name
            name_parts = name.split(' ', 1) if name else ['', '']
            first_name = name_parts[0] if len(name_parts) > 0 else ''
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            registration_data = {
                'username': username,
                'email': email,
                'password1': request.POST.get('password'),
                'password2': request.POST.get('confirm_password'),
            }
            
            form = UserRegistrationForm(registration_data)
            
            if form.is_valid():
                user = form.save()
                # Set first_name and last_name
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                
                # Create user profile with additional data
                UserProfile.objects.create(
                    user=user,
                    phone=request.POST.get('phone', ''),
                    country=request.POST.get('country', ''),
                    profile_photo=request.FILES.get('profile_photo')
                )
                # Automatically log in the user after registration
                login(request, user)
                messages.success(request, f'Registration successful! Welcome, {user.username}!')
                return redirect('app:dashboard')
            else:
                # Display form errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
                # If form is invalid, stay on auth page to show errors
                return render(request, 'app/auth.html')
    
    return render(request, 'app/auth.html')

def indexed_articles(request):
    """Indexed Articles page view"""
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'app/indexed_articles.html', {'articles': articles})

def article_detail(request, article_id):
    """Article detail page view"""
    from django.shortcuts import get_object_or_404
    from datetime import date
    
    # Try to get article from database, otherwise use dummy data
    try:
        article = Article.objects.get(id=article_id)
        authors = article.authors.all().order_by('order')
        keywords_list = []
        if article.keywords:
            keywords_list = [k.strip() for k in article.keywords.split(',') if k.strip()]
        related_articles = Article.objects.filter(
            discipline=article.discipline
        ).exclude(id=article.id).order_by('-created_at')[:4]
        # Add image attribute to real articles (default image)
        for rel_article in related_articles:
            if not hasattr(rel_article, 'image'):
                rel_article.image = 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400&h=300&fit=crop'
        is_dummy = False
    except Article.DoesNotExist:
        # Create dummy article data based on article_id
        dummy_articles = {
            1: {
                'title': 'Blood-Pressure Targets in Comatose Survivors of Cardiac Arrest',
                'article_number': 'SIS123456AI141125',
                'discipline': 'Cardiology',
                'article_type': 'research',
                'abstract': 'This double-blind, randomized trial (BOX) compared mean arterial pressure targets of 77 mm Hg versus 63 mm Hg in comatose survivors of out-of-hospital cardiac arrest. The primary outcome was a composite of death from any cause or hospital discharge with a Cerebral Performance Category (CPC) score of 3 or 4 (indicating severe neurological disability) at 90 days. Secondary outcomes included neurological function, quality of life, and serious adverse events. A total of 789 patients were randomly assigned to the higher-target group (77 mm Hg) and 789 to the lower-target group (63 mm Hg). The primary outcome occurred in 48% of patients in the higher-target group and 52% in the lower-target group (relative risk, 0.92; 95% confidence interval [CI], 0.82 to 1.03; P=0.15). There were no significant differences in secondary outcomes. Serious adverse events occurred in 31% of patients in the higher-target group and 30% in the lower-target group. In comatose survivors of out-of-hospital cardiac arrest, targeting a mean arterial pressure of 77 mm Hg, as compared with 63 mm Hg, did not result in a significant difference in the composite outcome of death or severe neurological disability at 90 days.',
                'keywords': 'Blood pressure, cardiac arrest, comatose survivors, mean arterial pressure, neurological outcomes, randomized trial, intensive care',
                'doi': '10.1056/NEJMoa1900500',
                'publication_date': date(2024, 11, 14),
                'language': 'English',
                'volume': '10',
                'issue': '4',
                'pages': '123-130',
                'issn': '1234-5678',
                'views': 150,
                'citations': 5,
                'image': 'https://images.unsplash.com/photo-1551601651-2a8555f1a136?w=400&h=300&fit=crop',
                'authors': [
                    {'name': 'Dr. Sarah Johnson', 'affiliation': 'Department of Cardiology, University Medical Center', 'is_corresponding': True},
                    {'name': 'Dr. Michael Chen', 'affiliation': 'Cardiac Research Institute', 'is_corresponding': False},
                    {'name': 'Dr. Emily Rodriguez', 'affiliation': 'Emergency Medicine Department, City Hospital', 'is_corresponding': False},
                ]
            },
            2: {
                'title': 'Perceptions of School Administrators and Teachers on Educational Technology Integration',
                'article_number': 'SIS789012ED150126',
                'discipline': 'Education',
                'article_type': 'research',
                'abstract': 'The goal of the study is to review the perceptions of school administrators and teachers regarding the integration of educational technology in K-12 classrooms. This mixed-methods research examined factors influencing technology adoption, barriers to implementation, and the impact of professional development on technology integration practices. Data were collected through surveys, interviews, and classroom observations across 25 schools. Findings indicate that while administrators generally support technology integration, teachers face significant challenges including lack of training, insufficient technical support, and concerns about student distraction. The study recommends comprehensive professional development programs and increased technical infrastructure to support effective technology integration.',
                'keywords': 'Educational technology, technology integration, school administrators, teacher perceptions, professional development, K-12 education',
                'doi': '10.1016/j.edutech.2024.12345',
                'publication_date': date(2024, 12, 15),
                'language': 'English',
                'volume': '8',
                'issue': '3',
                'pages': '45-62',
                'issn': '2345-6789',
                'views': 89,
                'citations': 3,
                'image': 'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=400&h=300&fit=crop',
                'authors': [
                    {'name': 'Dr. Robert Williams', 'affiliation': 'College of Education, State University', 'is_corresponding': True},
                    {'name': 'Dr. Lisa Anderson', 'affiliation': 'Educational Technology Research Center', 'is_corresponding': False},
                ]
            },
            3: {
                'title': 'Liberal or Restrictive Transfusion Strategy in Patients with Acute Myocardial Infarction',
                'article_number': 'SIS345678CA160127',
                'discipline': 'Cardiology',
                'article_type': 'research',
                'abstract': 'The SAHARA trial investigated the effect of a liberal versus restrictive red-cell transfusion strategy on clinical outcomes in patients with acute myocardial infarction and anemia. A total of 3,500 patients were randomly assigned to receive transfusions at a hemoglobin threshold of 10 g per deciliter (liberal strategy) or 8 g per deciliter (restrictive strategy). The primary outcome was a composite of death from any cause, recurrent myocardial infarction, or stroke at 30 days. Secondary outcomes included quality of life, functional status, and healthcare resource utilization. Results showed no significant difference in the primary composite outcome between groups (hazard ratio, 0.95; 95% CI, 0.82 to 1.10; P=0.48). However, the liberal strategy was associated with higher rates of transfusion-related complications. These findings suggest that a restrictive transfusion strategy may be appropriate for most patients with acute myocardial infarction and anemia.',
                'keywords': 'Transfusion strategy, myocardial infarction, anemia, red blood cells, clinical trial, cardiology',
                'doi': '10.1161/CIRCULATIONAHA.2024.98765',
                'publication_date': date(2024, 1, 16),
                'language': 'English',
                'volume': '12',
                'issue': '2',
                'pages': '234-251',
                'issn': '3456-7890',
                'views': 234,
                'citations': 12,
                'image': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=400&h=300&fit=crop',
                'authors': [
                    {'name': 'Dr. James Thompson', 'affiliation': 'Cardiovascular Research Institute', 'is_corresponding': True},
                    {'name': 'Dr. Patricia Martinez', 'affiliation': 'Department of Hematology, Medical Center', 'is_corresponding': False},
                    {'name': 'Dr. David Kim', 'affiliation': 'Clinical Trials Unit, University Hospital', 'is_corresponding': False},
                ]
            },
            4: {
                'title': 'Weekly Icodec versus Daily Glargine U100 in Type 2 Diabetes',
                'article_number': 'SIS456789EN170128',
                'discipline': 'Endocrinology',
                'article_type': 'research',
                'abstract': 'This phase 3a trial compared the efficacy and safety of once-weekly insulin icodec with once-daily insulin glargine U100 in adults with type 2 diabetes inadequately controlled on basal insulin. The study enrolled 1,200 participants who were randomly assigned to receive either icodec (700 units/mL) once weekly or glargine U100 (100 units/mL) once daily. The primary endpoint was the change in glycated hemoglobin (HbA1c) from baseline to week 26. Secondary endpoints included time in target glucose range, hypoglycemic events, and patient-reported outcomes. Results demonstrated non-inferiority of icodec compared to glargine U100, with mean HbA1c reductions of 1.2% and 1.1%, respectively. The incidence of hypoglycemia was similar between groups. Patient satisfaction scores were significantly higher in the icodec group, likely due to reduced injection frequency. These findings support once-weekly icodec as a convenient alternative to daily basal insulin therapy.',
                'keywords': 'Type 2 diabetes, insulin icodec, insulin glargine, weekly insulin, glycemic control, diabetes management',
                'doi': '10.2337/dc24-12345',
                'publication_date': date(2024, 1, 17),
                'language': 'English',
                'volume': '15',
                'issue': '1',
                'pages': '78-95',
                'issn': '4567-8901',
                'views': 312,
                'citations': 18,
                'image': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400&h=300&fit=crop',
                'authors': [
                    {'name': 'Dr. Jennifer Lee', 'affiliation': 'Diabetes Research Center', 'is_corresponding': True},
                    {'name': 'Dr. Christopher Brown', 'affiliation': 'Endocrinology Department, Regional Hospital', 'is_corresponding': False},
                ]
            },
        }
        
        dummy_data = dummy_articles.get(article_id, dummy_articles[1])
        
        # Create a simple object-like structure for template
        class DummyArticle:
            def __init__(self, data, art_id=None):
                self.id = art_id if art_id else article_id
                self.title = data['title']
                self.article_number = data.get('article_number', '')
                self.discipline = data['discipline']
                self.article_type = data['article_type']
                self.abstract = data['abstract']
                self.keywords = data['keywords']
                self.doi = data.get('doi', '')
                self.publication_date = data.get('publication_date')
                self.language = data.get('language', 'English')
                self.volume = data.get('volume', '')
                self.issue = data.get('issue', '')
                self.pages = data.get('pages', '')
                self.issn = data.get('issn', '')
                self.views = data.get('views', 0)
                self.citations = data.get('citations', 0)
                self.article_file = None
                self.image = data.get('image', '')
                self.created_at = data.get('publication_date', date.today())
            
            def get_article_type_display(self):
                type_map = {
                    'research': 'Research Article',
                    'review': 'Review Article',
                    'case_study': 'Case Study',
                    'short_communication': 'Short Communication',
                    'letter': 'Letter to Editor',
                }
                return type_map.get(self.article_type, 'Research Article')
        
        class DummyAuthor:
            def __init__(self, data):
                self.name = data['name']
                self.affiliation = data.get('affiliation', '')
                self.is_corresponding = data.get('is_corresponding', False)
        
        article = DummyArticle(dummy_data)
        authors = [DummyAuthor(auth) for auth in dummy_data['authors']]
        keywords_list = [k.strip() for k in dummy_data['keywords'].split(',') if k.strip()]
        
        # Dummy related articles
        related_dummy = []
        for rid in [2, 3, 4, 1]:
            if rid != article_id and rid in dummy_articles:
                rel_data = dummy_articles[rid]
                rel_article = DummyArticle(rel_data, art_id=rid)
                related_dummy.append(rel_article)
        
        related_articles = related_dummy[:4]
        is_dummy = True
    
    return render(request, 'app/article_detail.html', {
        'article': article,
        'authors': authors,
        'related_articles': related_articles,
        'keywords_list': keywords_list,
        'is_dummy': is_dummy,
    })

def indexed_journals(request):
    """Indexed Journals page view"""
    journals = Journal.objects.all().order_by('-created_at')
    return render(request, 'app/indexed_journals.html', {'journals': journals})

def project_archive(request):
    """Project | Research Archive page view"""
    projects = Project.objects.all()
    
    # Get filter parameters from GET request
    search_query = request.GET.get('search', '').strip()
    category = request.GET.get('category', '').strip()
    institution = request.GET.get('institution', '').strip()
    status = request.GET.get('status', '').strip()
    year = request.GET.get('year', '').strip()
    sort_by = request.GET.get('sort', 'recent')
    
    # Apply search filter
    if search_query:
        projects = projects.filter(
            Q(project_title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(institution__icontains=search_query) |
            Q(category__icontains=search_query)
        )
    
    # Apply category filter
    if category:
        projects = projects.filter(category__icontains=category)
    
    # Apply institution filter
    if institution:
        projects = projects.filter(institution__icontains=institution)
    
    # Apply status filter
    if status:
        projects = projects.filter(status=status)
    
    # Apply year filter
    if year:
        projects = projects.filter(created_at__year=year)
    
    # Apply sorting
    if sort_by == 'recent':
        projects = projects.order_by('-created_at')
    elif sort_by == 'oldest':
        projects = projects.order_by('created_at')
    elif sort_by == 'title':
        projects = projects.order_by('project_title')
    else:
        projects = projects.order_by('-created_at')
    
    # Get unique values for filter dropdowns
    institutions = Project.objects.values_list('institution', flat=True).distinct().order_by('institution')
    categories = Project.objects.values_list('category', flat=True).distinct().order_by('category')
    years = Project.objects.dates('created_at', 'year', order='DESC')
    
    return render(request, 'app/project_archive.html', {
        'projects': projects,
        'institutions': institutions,
        'categories': categories,
        'years': years,
        'current_search': search_query,
        'current_category': category,
        'current_institution': institution,
        'current_status': status,
        'current_year': year,
        'current_sort': sort_by,
    })

@login_required
def upload_article(request):
    """Upload Article page view"""
    if request.method == 'POST':
        try:
            # Get form data
            title = request.POST.get('title', '').strip()
            article_type_raw = request.POST.get('article_type', '').strip()
            discipline = request.POST.get('discipline', '').strip()
            abstract = request.POST.get('abstract', '').strip()
            keywords = request.POST.get('keywords', '').strip()
            language = request.POST.get('language', '').strip()
            publication_date = request.POST.get('publication_date', '').strip()
            doi = request.POST.get('doi', '').strip()
            article_file = request.FILES.get('article_file')
            
            # Validate required fields
            if not title:
                messages.error(request, 'Article title is required.')
                return render(request, 'app/upload_article.html', {'form': ArticleForm()})
            
            if not article_type_raw:
                messages.error(request, 'Article type is required.')
                return render(request, 'app/upload_article.html', {'form': ArticleForm()})
            
            if not discipline:
                messages.error(request, 'Discipline is required.')
                return render(request, 'app/upload_article.html', {'form': ArticleForm()})
            
            if not abstract:
                messages.error(request, 'Abstract is required.')
                return render(request, 'app/upload_article.html', {'form': ArticleForm()})
            
            if not language:
                messages.error(request, 'Language is required.')
                return render(request, 'app/upload_article.html', {'form': ArticleForm()})
            
            if not publication_date:
                messages.error(request, 'Publication date is required.')
                return render(request, 'app/upload_article.html', {'form': ArticleForm()})
            
            if not article_file:
                messages.error(request, 'Article file is required.')
                return render(request, 'app/upload_article.html', {'form': ArticleForm()})
            
            # Map article_type from form values to model values
            article_type_map = {
                'research-article': 'research',
                'review-article': 'review',
                'case-study': 'case_study',
                'short-communication': 'short_communication',
                'letter': 'letter',
                'editorial': 'letter',  # Default to letter if not mapped
            }
            article_type = article_type_map.get(article_type_raw, 'research')
            
            # Create article
            from datetime import datetime
            try:
                pub_date = datetime.strptime(publication_date, '%Y-%m-%d').date()
            except:
                messages.error(request, 'Invalid publication date format.')
                return render(request, 'app/upload_article.html', {'form': ArticleForm()})
            
            article = Article.objects.create(
                title=title,
                article_type=article_type,
                discipline=discipline,
                abstract=abstract,
                keywords=keywords,
                language=language,
                publication_date=pub_date,
                doi=doi if doi else '',
                article_file=article_file,
                submitted_by=request.user,
                status='pending'
            )
            
            # Handle authors - the template uses authors[0][first_name] format
            author_index = 0
            while True:
                first_name = request.POST.get(f'authors[{author_index}][first_name]', '').strip()
                last_name = request.POST.get(f'authors[{author_index}][last_name]', '').strip()
                email = request.POST.get(f'authors[{author_index}][email]', '').strip()
                affiliation = request.POST.get(f'authors[{author_index}][affiliation]', '').strip()
                
                if not first_name and not last_name and not email:
                    break  # No more authors
                
                if first_name and last_name and email:
                    author_name = f"{first_name} {last_name}".strip()
                    ArticleAuthor.objects.create(
                        article=article,
                        name=author_name,
                        email=email,
                        affiliation=affiliation,
                        is_corresponding=(author_index == 0),  # First author is corresponding
                        order=author_index
                    )
                
                author_index += 1
            
            # If no authors were found with the new format, try the old format
            if author_index == 0:
                author_count = int(request.POST.get('author_count', 0))
                for i in range(author_count):
                    author_name = request.POST.get(f'author_{i}_name', '').strip()
                    author_email = request.POST.get(f'author_{i}_email', '').strip()
                    author_affiliation = request.POST.get(f'author_{i}_affiliation', '').strip()
                    author_orcid = request.POST.get(f'author_{i}_orcid', '').strip()
                    is_corresponding = request.POST.get(f'author_{i}_corresponding') == 'on'
                    
                    if author_name and author_email:
                        ArticleAuthor.objects.create(
                            article=article,
                            name=author_name,
                            email=author_email,
                            affiliation=author_affiliation,
                            orcid=author_orcid,
                            is_corresponding=is_corresponding,
                            order=i
                        )
            
            messages.success(request, 'Article uploaded successfully! It will be reviewed before being published.')
            return redirect('app:indexed_articles')
            
        except Exception as e:
            messages.error(request, f'Error uploading article: {str(e)}')
            import traceback
            print(traceback.format_exc())
    else:
        form = ArticleForm()
    
    return render(request, 'app/upload_article.html', {'form': form})

@login_required
def register_journal(request):
    """Register Journal page view"""
    if request.method == 'POST':
        form = JournalForm(request.POST, request.FILES)
        if form.is_valid():
            journal = form.save(commit=False)
            journal.submitted_by = request.user
            journal.save()
            
            # Handle editors
            editor_count = int(request.POST.get('editor_count', 0))
            for i in range(editor_count):
                editor_name = request.POST.get(f'editor_{i}_name')
                editor_email = request.POST.get(f'editor_{i}_email')
                editor_affiliation = request.POST.get(f'editor_{i}_affiliation', '')
                editor_role = request.POST.get(f'editor_{i}_role', '')
                
                if editor_name and editor_email:
                    JournalEditor.objects.create(
                        journal=journal,
                        name=editor_name,
                        email=editor_email,
                        affiliation=editor_affiliation,
                        role=editor_role,
                        order=i
                    )
            
            messages.success(request, 'Journal registered successfully!')
            return redirect('app:indexed_journals')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = JournalForm()
    
    return render(request, 'app/register_journal.html', {'form': form})

def directory_researchers(request):
    """Directory of Researchers page view"""
    researchers = DirectoryApplication.objects.filter(terms_accepted=True)
    
    # Get filter parameters from GET request
    search_query = request.GET.get('search', '').strip()
    country = request.GET.get('country', '').strip()
    institution = request.GET.get('institution', '').strip()
    discipline = request.GET.get('discipline', '').strip()
    sort_by = request.GET.get('sort', 'recent')
    
    # Apply search filter
    if search_query:
        researchers = researchers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(institution__icontains=search_query) |
            Q(position__icontains=search_query) |
            Q(research_areas__icontains=search_query)
        )
    
    # Apply country filter
    if country:
        researchers = researchers.filter(country__icontains=country)
    
    # Apply institution filter
    if institution:
        researchers = researchers.filter(institution__icontains=institution)
    
    # Apply discipline/research area filter
    if discipline:
        researchers = researchers.filter(research_areas__icontains=discipline)
    
    # Apply sorting
    if sort_by == 'name':
        researchers = researchers.order_by('first_name', 'last_name')
    elif sort_by == 'recent':
        researchers = researchers.order_by('-created_at')
    else:
        researchers = researchers.order_by('-created_at')
    
    # Get unique values for filter dropdowns
    countries = DirectoryApplication.objects.filter(terms_accepted=True).values_list('country', flat=True).distinct().order_by('country')
    institutions = DirectoryApplication.objects.filter(terms_accepted=True).values_list('institution', flat=True).distinct().order_by('institution')
    
    return render(request, 'app/directory_researchers.html', {
        'researchers': researchers,
        'countries': countries,
        'institutions': institutions,
        'current_search': search_query,
        'current_country': country,
        'current_institution': institution,
        'current_discipline': discipline,
        'current_sort': sort_by,
    })

@login_required
def upload_project(request):
    """Upload | Archive Project page view"""
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.submitted_by = request.user
            project.save()
            
            # Handle contributors
            contributor_count = int(request.POST.get('contributor_count', 0))
            for i in range(contributor_count):
                contributor_name = request.POST.get(f'contributor_{i}_name')
                contributor_email = request.POST.get(f'contributor_{i}_email')
                contributor_affiliation = request.POST.get(f'contributor_{i}_affiliation', '')
                contributor_role = request.POST.get(f'contributor_{i}_role', '')
                
                if contributor_name and contributor_email:
                    ProjectContributor.objects.create(
                        project=project,
                        name=contributor_name,
                        email=contributor_email,
                        affiliation=contributor_affiliation,
                        role=contributor_role,
                        order=i
                    )
            
            messages.success(request, 'Project uploaded and archived successfully!')
            return redirect('app:project_archive')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProjectForm()
    
    return render(request, 'app/upload_project.html', {'form': form})

def council_members(request):
    """Council Members page view"""
    return render(request, 'app/council_members.html')

def team_members(request):
    """Team Members page view"""
    return render(request, 'app/team_members.html')

def sponsors(request):
    """Sponsors page view"""
    from django.conf import settings
    return render(request, 'app/sponsors.html', {
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
    })

def initialize_payment(request):
    """Initialize Paystack payment"""
    import requests
    from django.conf import settings
    from django.http import JsonResponse
    import json
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount_usd_cents = float(data.get('amount', 0))  # Amount in USD cents
            email = data.get('email', '')
            name = data.get('name', 'Donor')
            
            if amount_usd_cents <= 0:
                return JsonResponse({'error': 'Invalid amount'}, status=400)
            
            # Convert USD cents to GHS pesewas (1 USD = ~13.5 GHS)
            # First convert cents to dollars, then to GHS, then to pesewas
            amount_usd = amount_usd_cents / 100
            amount_ghs = amount_usd * 13.5  # Approximate conversion rate
            amount_pesewas = int(amount_ghs * 100)  # Convert to pesewas
            
            # Initialize Paystack transaction
            url = 'https://api.paystack.co/transaction/initialize'
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                'Content-Type': 'application/json'
            }
            payload = {
                'email': email,
                'amount': amount_pesewas,
                'currency': 'GHS',
                'reference': f'sponsor_{request.user.id if request.user.is_authenticated else "guest"}_{int(time.time())}',
                'metadata': {
                    'name': name,
                    'custom_fields': [
                        {
                            'display_name': 'Donation Type',
                            'variable_name': 'donation_type',
                            'value': 'Sponsor'
                        }
                    ]
                }
            }
            
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            
            if result.get('status'):
                return JsonResponse({
                    'authorization_url': result['data']['authorization_url'],
                    'access_code': result['data']['access_code'],
                    'reference': result['data']['reference']
                })
            else:
                return JsonResponse({'error': result.get('message', 'Payment initialization failed')}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def request_membership(request):
    """Request For Membership page view"""
    if request.method == 'POST':
        form = MembershipRequestForm(request.POST, request.FILES)
        if form.is_valid():
            membership = form.save(commit=False)
            if request.user.is_authenticated:
                membership.submitted_by = request.user
            membership.save()
            messages.success(request, 'Your membership request has been submitted successfully!')
            return redirect('app:landing')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = MembershipRequestForm()
    
    return render(request, 'app/request_membership.html', {'form': form})

def apply_directory(request):
    """Apply For Directory of Researcher page view"""
    if request.method == 'POST':
        form = DirectoryApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            if request.user.is_authenticated:
                application.submitted_by = request.user
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('app:directory_researchers')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = DirectoryApplicationForm()
    
    return render(request, 'app/apply_directory.html', {'form': form})

def hall_of_fame(request):
    """Hall of Fame listing page view"""
    honorees = HallOfFameApplication.objects.filter(terms_accepted=True).order_by('-created_at')
    return render(request, 'app/hall_of_fame.html', {'honorees': honorees})

def hall_of_fame_apply(request):
    """Apply For Hall of Fame page view"""
    if request.method == 'POST':
        form = HallOfFameApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            if request.user.is_authenticated:
                application.submitted_by = request.user
            application.save()
            messages.success(request, 'Your Hall of Fame application has been submitted successfully!')
            return redirect('app:hall_of_fame')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = HallOfFameApplicationForm()
    
    return render(request, 'app/hall_of_fame_apply.html', {'form': form})

def check_turnitin(request):
    """Check Turnitin Plagiarism page view"""
    if request.method == 'POST':
        form = PlagiarismCheckForm(request.POST, request.FILES)
        if form.is_valid():
            check = form.save(commit=False)
            if request.user.is_authenticated:
                check.submitted_by = request.user
            check.save()
            messages.success(request, 'Your document has been submitted for plagiarism check!')
            return redirect('app:landing')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PlagiarismCheckForm()
    
    return render(request, 'app/check_turnitin.html', {'form': form})

def work_plagiarism(request):
    """Work My Plagiarism page view"""
    if request.method == 'POST':
        form = PlagiarismWorkForm(request.POST, request.FILES)
        if form.is_valid():
            work = form.save(commit=False)
            if request.user.is_authenticated:
                work.submitted_by = request.user
            work.save()
            messages.success(request, 'Your request has been submitted successfully!')
            return redirect('app:landing')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PlagiarismWorkForm()
    
    return render(request, 'app/work_plagiarism.html', {'form': form})

def thesis_to_article(request):
    """Thesis To Article page view"""
    if request.method == 'POST':
        form = ThesisToArticleForm(request.POST, request.FILES)
        if form.is_valid():
            conversion = form.save(commit=False)
            if request.user.is_authenticated:
                conversion.submitted_by = request.user
            conversion.save()
            messages.success(request, 'Your thesis has been submitted for article conversion!')
            return redirect('app:landing')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ThesisToArticleForm()
    
    return render(request, 'app/thesis_to_article.html', {'form': form})

def thesis_to_book(request):
    """Thesis To Book page view"""
    if request.method == 'POST':
        form = ThesisToBookForm(request.POST, request.FILES)
        if form.is_valid():
            conversion = form.save(commit=False)
            if request.user.is_authenticated:
                conversion.submitted_by = request.user
            conversion.save()
            messages.success(request, 'Your thesis has been submitted for book conversion!')
            return redirect('app:landing')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ThesisToBookForm()
    
    return render(request, 'app/thesis_to_book.html', {'form': form})

def thesis_to_book_chapter(request):
    """Thesis To Book Chapter page view"""
    if request.method == 'POST':
        form = ThesisToBookChapterForm(request.POST, request.FILES)
        if form.is_valid():
            conversion = form.save(commit=False)
            if request.user.is_authenticated:
                conversion.submitted_by = request.user
            conversion.save()
            messages.success(request, 'Your thesis has been submitted for book chapter conversion!')
            return redirect('app:landing')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ThesisToBookChapterForm()
    
    return render(request, 'app/thesis_to_book_chapter.html', {'form': form})

def powerpoint_preparation(request):
    """Power Point Preparation page view"""
    if request.method == 'POST':
        form = PowerPointPreparationForm(request.POST, request.FILES)
        if form.is_valid():
            preparation = form.save(commit=False)
            if request.user.is_authenticated:
                preparation.submitted_by = request.user
            preparation.save()
            messages.success(request, 'Your thesis has been submitted for PowerPoint preparation!')
            return redirect('app:landing')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PowerPointPreparationForm()
    
    return render(request, 'app/powerpoint_preparation.html', {'form': form})

def about_sis(request):
    """About S.I.S page view"""
    return render(request, 'app/about_sis.html')

def mission(request):
    """Mission page view"""
    return render(request, 'app/mission.html')

def criteria(request):
    """Criteria page view"""
    return render(request, 'app/criteria.html')

def tolerance_policy(request):
    """Tolerance Policy page view"""
    return render(request, 'app/tolerance_policy.html')

def service_solution(request):
    """Service & Solution page view"""
    return render(request, 'app/service_solution.html')

def policy_terms(request):
    """Policy Terms and Conditions page view"""
    return render(request, 'app/policy_terms.html')

def dashboard(request):
    """Dashboard page view"""
    user = request.user
    profile = None
    if user.is_authenticated:
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
    
    # Get statistics
    articles_count = Article.objects.filter(status='approved').count()
    journals_count = Journal.objects.count()
    projects_count = Project.objects.count()
    
    # Get all pending requests from different models
    pending_plagiarism_checks = PlagiarismCheck.objects.all()
    pending_plagiarism_works = PlagiarismWork.objects.all()
    pending_thesis_articles = ThesisToArticle.objects.all()
    pending_thesis_books = ThesisToBook.objects.all()
    pending_thesis_chapters = ThesisToBookChapter.objects.all()
    pending_powerpoints = PowerPointPreparation.objects.all()
    
    # Combine all requests and get latest 10
    all_requests = []
    for req in pending_plagiarism_checks:
        all_requests.append({
            'id': req.id,
            'type': 'check_plagiarism',
            'email': req.email,
            'created_at': req.created_at,
            'document': req.document,
            'name': req.name or '',
        })
    for req in pending_plagiarism_works:
        all_requests.append({
            'id': req.id,
            'type': 'work_plagiarism',
            'email': req.email,
            'created_at': req.created_at,
            'document': req.document,
            'name': req.name or '',
        })
    for req in pending_thesis_articles:
        all_requests.append({
            'id': req.id,
            'type': 'thesis_to_article',
            'email': req.email,
            'created_at': req.created_at,
            'document': req.thesis_file,
            'name': req.name or '',
        })
    for req in pending_thesis_books:
        all_requests.append({
            'id': req.id,
            'type': 'thesis_to_book',
            'email': req.email,
            'created_at': req.created_at,
            'document': req.thesis_file,
            'name': req.name or '',
        })
    for req in pending_thesis_chapters:
        all_requests.append({
            'id': req.id,
            'type': 'thesis_to_book_chapter',
            'email': req.email,
            'created_at': req.created_at,
            'document': req.thesis_file,
            'name': req.name or '',
        })
    for req in pending_powerpoints:
        all_requests.append({
            'id': req.id,
            'type': 'powerpoint_preparation',
            'email': req.email,
            'created_at': req.created_at,
            'document': req.thesis_file,
            'name': req.name or '',
        })
    
    # Sort by created_at and get latest 10
    all_requests.sort(key=lambda x: x['created_at'] if x['created_at'] else None, reverse=True)
    latest_requests = all_requests[:10]
    pending_requests_count = len(all_requests)
    
    # Get account statistics
    total_users = User.objects.count()
    directory_researchers_count = DirectoryApplication.objects.filter(terms_accepted=True).count()
    eminent_personalities_count = HallOfFameApplication.objects.count()
    registered_members_count = MembershipRequest.objects.count()
    
    # Get recent accounts (users with profiles)
    recent_users = User.objects.select_related('profile').order_by('-date_joined')[:5]
    
    # Get recent blog posts (using articles as blog posts for now)
    recent_blogs = Article.objects.filter(status='approved').order_by('-created_at')[:5]
    
    return render(request, 'app/dashboard.html', {
        'user': user,
        'profile': profile,
        'articles_count': articles_count,
        'journals_count': journals_count,
        'projects_count': projects_count,
        'pending_requests_count': pending_requests_count,
        'latest_requests': latest_requests,
        'total_users': total_users,
        'directory_researchers_count': directory_researchers_count,
        'eminent_personalities_count': eminent_personalities_count,
        'registered_members_count': registered_members_count,
        'recent_users': recent_users,
        'recent_blogs': recent_blogs,
    })

@login_required
def account_detail(request):
    """Account Detail page view"""
    user = request.user
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    return render(request, 'app/account_detail.html', {
        'user': user,
        'profile': profile,
        'active_page': 'account_detail',
    })

@login_required
def list_accounts(request):
    """List all accounts page"""
    # Get search and filter parameters
    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort', 'recent')
    role_filter = request.GET.get('role', '')
    
    # Get all users with profiles
    users = User.objects.filter(profile__isnull=False).select_related('profile')
    
    # Apply role filter
    if role_filter == 'admin':
        users = users.filter(is_superuser=True)
    elif role_filter == 'staff':
        users = users.filter(is_staff=True, is_superuser=False)
    elif role_filter == 'user':
        users = users.filter(is_staff=False, is_superuser=False)
    
    # Apply search filter
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Apply sorting
    if sort_by == 'recent':
        users = users.order_by('-date_joined')
    elif sort_by == 'oldest':
        users = users.order_by('date_joined')
    elif sort_by == 'name':
        users = users.order_by('first_name', 'last_name', 'username')
    else:
        users = users.order_by('-date_joined')
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(users, 20)  # Show 20 users per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Calculate record range
    start_record = (page_obj.number - 1) * paginator.per_page + 1
    end_record = min(start_record + paginator.per_page - 1, paginator.count)
    
    return render(request, 'app/list_accounts.html', {
        'page_obj': page_obj,
        'users': page_obj,
        'current_search': search_query,
        'current_sort': sort_by,
        'current_role': role_filter,
        'start_record': start_record,
        'end_record': end_record,
        'total_records': paginator.count,
    })

@login_required
def view_account(request, user_id):
    """View Account page - displays account details for a specific user"""
    try:
        view_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('app:dashboard')
    
    try:
        profile = view_user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=view_user)
    
    # Calculate document counts
    doc_counts = (
        Article.objects.filter(submitted_by=view_user).count() +
        Journal.objects.filter(submitted_by=view_user).count() +
        Project.objects.filter(submitted_by=view_user).count() +
        PlagiarismCheck.objects.filter(submitted_by=view_user).count() +
        PlagiarismWork.objects.filter(submitted_by=view_user).count() +
        ThesisToArticle.objects.filter(submitted_by=view_user).count() +
        ThesisToBook.objects.filter(submitted_by=view_user).count() +
        ThesisToBookChapter.objects.filter(submitted_by=view_user).count() +
        PowerPointPreparation.objects.filter(submitted_by=view_user).count()
    )
    
    # Get position from DirectoryApplication if exists
    position = None
    organization_url = None
    try:
        directory_app = DirectoryApplication.objects.filter(submitted_by=view_user, terms_accepted=True).first()
        if directory_app:
            position = directory_app.position
            # DirectoryApplication doesn't have organization_url, so we'll use institution or None
            organization_url = getattr(directory_app, 'institution', None)
    except:
        pass
    
    # Determine role (simplified - you can enhance this based on your needs)
    role = 'user'
    if view_user.is_staff:
        role = 'staff'
    if view_user.is_superuser:
        role = 'admin'
    
    # Status
    status = 'active' if view_user.is_active else 'inactive'
    
    return render(request, 'app/view_account.html', {
        'view_user': view_user,
        'profile': profile,
        'doc_counts': doc_counts,
        'position': position or 'N/A',
        'organization_url': organization_url,
        'role': role,
        'status': status,
    })

@login_required
def export_account(request, user_id, format_type):
    """Export account details in various formats"""
    try:
        view_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('app:dashboard')
    
    try:
        profile = view_user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=view_user)
    
    # Calculate document counts
    doc_counts = (
        Article.objects.filter(submitted_by=view_user).count() +
        Journal.objects.filter(submitted_by=view_user).count() +
        Project.objects.filter(submitted_by=view_user).count() +
        PlagiarismCheck.objects.filter(submitted_by=view_user).count() +
        PlagiarismWork.objects.filter(submitted_by=view_user).count() +
        ThesisToArticle.objects.filter(submitted_by=view_user).count() +
        ThesisToBook.objects.filter(submitted_by=view_user).count() +
        ThesisToBookChapter.objects.filter(submitted_by=view_user).count() +
        PowerPointPreparation.objects.filter(submitted_by=view_user).count()
    )
    
    # Get position from DirectoryApplication if exists
    position = None
    organization_url = None
    try:
        directory_app = DirectoryApplication.objects.filter(submitted_by=view_user, terms_accepted=True).first()
        if directory_app:
            position = directory_app.position
            organization_url = getattr(directory_app, 'institution', None)
    except:
        pass
    
    # Determine role
    role = 'user'
    if view_user.is_staff:
        role = 'staff'
    if view_user.is_superuser:
        role = 'admin'
    
    status = 'active' if view_user.is_active else 'inactive'
    
    # Prepare account data
    account_data = {
        'Id': view_user.id,
        'Name': view_user.get_full_name() or view_user.username,
        'Email': view_user.email or 'N/A',
        'Phone': profile.phone or 'N/A',
        'Country': profile.country or 'N/A',
        'Status': status,
        'Role': role,
        'Doc Counts': doc_counts,
        'Itp': '0.5',
        'Ctrl': '97',
        'Profile Photo': profile.profile_photo.url if profile.profile_photo else 'null',
        'Position': position or 'N/A',
        'Organization Url': organization_url or 'null',
    }
    
    filename = f"account_{view_user.username}_{view_user.id}"
    
    if format_type == 'print':
        # Print-friendly HTML
        html_content = render_to_string('app/export_account_print.html', {
            'view_user': view_user,
            'account_data': account_data,
        })
        response = HttpResponse(html_content, content_type='text/html')
        return response
    
    elif format_type == 'pdf':
        # PDF export using reportlab or weasyprint
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.units import inch
            
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#111827'),
                spaceAfter=30,
            )
            
            elements.append(Paragraph("Account Details", title_style))
            elements.append(Spacer(1, 0.2*inch))
            
            # Create table data
            table_data = [['Field', 'Value']]
            for key, value in account_data.items():
                table_data.append([key, str(value)])
            
            table = Table(table_data, colWidths=[2*inch, 4*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f9fafb')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#374151')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#111827')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ]))
            
            elements.append(table)
            doc.build(elements)
            
            response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
            return response
        except ImportError:
            # Fallback to simple text if reportlab not available
            response = HttpResponse(content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="{filename}.txt"'
            for key, value in account_data.items():
                response.write(f"{key}: {value}\n")
            return response
    
    elif format_type == 'word':
        # Word export using python-docx
        try:
            from docx import Document
            from docx.shared import Inches, Pt
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            
            doc = Document()
            doc.add_heading('Account Details', 0)
            
            table = doc.add_table(rows=1, cols=2)
            table.style = 'Light Grid Accent 1'
            
            # Header row
            header_cells = table.rows[0].cells
            header_cells[0].text = 'Field'
            header_cells[1].text = 'Value'
            for cell in header_cells:
                cell.paragraphs[0].runs[0].font.bold = True
            
            # Data rows
            for key, value in account_data.items():
                row_cells = table.add_row().cells
                row_cells[0].text = key
                row_cells[1].text = str(value)
            
            buffer = io.BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="{filename}.docx"'
            return response
        except ImportError:
            # Fallback to simple text
            response = HttpResponse(content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="{filename}.txt"'
            for key, value in account_data.items():
                response.write(f"{key}: {value}\n")
            return response
    
    elif format_type == 'csv':
        # CSV export
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Field', 'Value'])
        for key, value in account_data.items():
            writer.writerow([key, value])
        
        return response
    
    elif format_type == 'excel':
        # Excel export using openpyxl
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill, Alignment
            
            wb = Workbook()
            ws = wb.active
            ws.title = "Account Details"
            
            # Header row
            header_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
            header_font = Font(bold=True, color="374151")
            
            ws['A1'] = 'Field'
            ws['B1'] = 'Value'
            ws['A1'].fill = header_fill
            ws['B1'].fill = header_fill
            ws['A1'].font = header_font
            ws['B1'].font = header_font
            
            # Data rows
            row = 2
            for key, value in account_data.items():
                ws[f'A{row}'] = key
                ws[f'B{row}'] = str(value)
                if row % 2 == 0:
                    ws[f'A{row}'].fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
                    ws[f'B{row}'].fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
                row += 1
            
            # Adjust column widths
            ws.column_dimensions['A'].width = 20
            ws.column_dimensions['B'].width = 40
            
            buffer = io.BytesIO()
            wb.save(buffer)
            buffer.seek(0)
            
            response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
            return response
        except ImportError:
            # Fallback to CSV if openpyxl not available
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
            writer = csv.writer(response)
            writer.writerow(['Field', 'Value'])
            for key, value in account_data.items():
                writer.writerow([key, value])
            return response
    
    else:
        messages.error(request, 'Invalid export format.')
        return redirect('app:view_account', user_id=user_id)

@login_required
def update_user_role(request, user_id):
    """Update user role (Admin, Staff, User)"""
    # Superusers can change any role, staff can change to user/staff (not admin)
    if not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse({'success': False, 'error': 'Permission denied. Only staff/superusers can change roles.'}, status=403)
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
    
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        role_type = data.get('role_type')
        
        # Set role based on selection
        # Only superusers can set admin role
        if role_type == 'admin':
            if not request.user.is_superuser:
                return JsonResponse({'success': False, 'error': 'Only superusers can assign admin role.'}, status=403)
            user.is_superuser = True
            user.is_staff = True  # Admin is also staff
            user.is_active = True
        elif role_type == 'staff':
            user.is_superuser = False
            user.is_staff = True
            user.is_active = True
        elif role_type == 'user':
            user.is_superuser = False
            user.is_staff = False
            # Keep is_active as is (don't deactivate when changing to user)
        
        user.save()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def get_user_data(request, user_id):
    """Get user data for edit modal"""
    # Allow any logged-in user to view account data (they can see it in the list anyway)
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
    
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    # Determine role
    role = 'user'
    if user.is_superuser:
        role = 'admin'
    elif user.is_staff:
        role = 'staff'
    
    return JsonResponse({
        'success': True,
        'user': {
            'username': user.username or '',
            'email': user.email or '',
            'first_name': user.first_name or '',
            'last_name': user.last_name or '',
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
            'role': role,
        },
        'profile': {
            'phone': profile.phone or '',
            'country': profile.country or '',
        }
    })

@login_required
def edit_user_account(request, user_id):
    """Edit user account page"""
    # Allow any logged-in user to edit accounts (they can see them in the list)
    # But only superusers can change roles
    
    try:
        edit_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
        messages.error(request, 'User not found.')
        return redirect('app:list_accounts')
    
    try:
        profile = edit_user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=edit_user)
    
    if request.method == 'POST':
        # Update user fields
        edit_user.username = request.POST.get('username', edit_user.username)
        edit_user.email = request.POST.get('email', edit_user.email)
        edit_user.first_name = request.POST.get('first_name', edit_user.first_name)
        edit_user.last_name = request.POST.get('last_name', edit_user.last_name)
        edit_user.is_active = request.POST.get('is_active') == 'on'
        
        # Update role (only superusers can change roles)
        role = request.POST.get('role', 'user')
        if request.user.is_superuser:
            if role == 'admin':
                edit_user.is_superuser = True
                edit_user.is_staff = True
            elif role == 'staff':
                edit_user.is_superuser = False
                edit_user.is_staff = True
            elif role == 'user':
                edit_user.is_superuser = False
                edit_user.is_staff = False
        
        edit_user.save()
        
        # Update profile fields
        profile.phone = request.POST.get('phone', profile.phone)
        profile.country = request.POST.get('country', profile.country)
        if 'profile_photo' in request.FILES:
            profile.profile_photo = request.FILES['profile_photo']
        profile.save()
        
        # Return JSON for AJAX requests, otherwise redirect
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        
        messages.success(request, 'Account updated successfully.')
        return redirect('app:view_account', user_id=user_id)
    
    return render(request, 'app/edit_user_account.html', {
        'edit_user': edit_user,
        'profile': profile,
    })

@login_required
def delete_user_account(request, user_id):
    """Delete user account"""
    if not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    if request.user.id == user_id:
        return JsonResponse({'success': False, 'error': 'Cannot delete your own account'}, status=400)
    
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def edit_account(request):
    """Edit Account page view"""
    user = request.user
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    if request.method == 'POST':
        # Update user fields
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.save()
        
        # Update profile fields
        profile.phone = request.POST.get('phone', '')
        profile.country = request.POST.get('country', '')
        if 'profile_photo' in request.FILES:
            profile.profile_photo = request.FILES['profile_photo']
        profile.save()
        
        messages.success(request, 'Account updated successfully!')
        return redirect('app:account_detail')
    
    return render(request, 'app/edit_account.html', {
        'user': user,
        'profile': profile,
        'active_page': 'edit_account',
    })

@login_required
def change_email(request):
    """Change Email page view"""
    user = request.user
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    if request.method == 'POST':
        new_email = request.POST.get('new_email', '').strip()
        password = request.POST.get('password', '')
        
        # Verify password
        if not user.check_password(password):
            messages.error(request, 'Incorrect password. Please try again.')
        elif not new_email:
            messages.error(request, 'Please provide a new email address.')
        elif User.objects.filter(email=new_email).exclude(id=user.id).exists():
            messages.error(request, 'This email is already in use by another account.')
        else:
            user.email = new_email
            user.save()
            messages.success(request, 'Email updated successfully!')
            return redirect('app:account_detail')
    
    return render(request, 'app/change_email.html', {
        'user': user,
        'profile': profile,
        'active_page': 'change_email',
    })

@login_required
def reset_password(request):
    """Reset Password page view"""
    user = request.user
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        # Verify old password
        if not user.check_password(old_password):
            messages.error(request, 'Incorrect current password.')
        elif not new_password:
            messages.error(request, 'Please provide a new password.')
        elif len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        else:
            user.set_password(new_password)
            user.save()
            # Re-authenticate user after password change
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('app:account_detail')
    
    return render(request, 'app/reset_password.html', {
        'user': user,
        'profile': profile,
        'active_page': 'reset_password',
    })
