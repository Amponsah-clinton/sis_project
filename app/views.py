from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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
    return render(request, 'app/landing.html', {
        'search_form': search_form,
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
                    from django.contrib.auth.models import User
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('app:landing')
            else:
                messages.error(request, 'Invalid username/email or password')
            
        elif form_type == 'register':
            # Create username from email if not provided
            email = request.POST.get('email')
            username = request.POST.get('username', email.split('@')[0] if email else 'user')
            
            registration_data = {
                'username': username,
                'email': email,
                'password1': request.POST.get('password'),
                'password2': request.POST.get('confirm_password'),
            }
            
            form = UserRegistrationForm(registration_data)
            
            if form.is_valid():
                user = form.save()
                # Create user profile with additional data
                UserProfile.objects.create(
                    user=user,
                    phone=request.POST.get('phone', ''),
                    country=request.POST.get('country', ''),
                    profile_photo=request.FILES.get('profile_photo')
                )
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('app:auth')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
    
    return render(request, 'app/auth.html')

def indexed_articles(request):
    """Indexed Articles page view"""
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'app/indexed_articles.html', {'articles': articles})

def indexed_journals(request):
    """Indexed Journals page view"""
    journals = Journal.objects.all().order_by('-created_at')
    return render(request, 'app/indexed_journals.html', {'journals': journals})

def project_archive(request):
    """Project | Research Archive page view"""
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'app/project_archive.html', {'projects': projects})

@login_required
def upload_article(request):
    """Upload Article page view"""
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.submitted_by = request.user
            article.save()
            
            # Handle authors
            author_count = int(request.POST.get('author_count', 0))
            for i in range(author_count):
                author_name = request.POST.get(f'author_{i}_name')
                author_email = request.POST.get(f'author_{i}_email')
                author_affiliation = request.POST.get(f'author_{i}_affiliation', '')
                author_orcid = request.POST.get(f'author_{i}_orcid', '')
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
            
            messages.success(request, 'Article uploaded successfully!')
            return redirect('app:indexed_articles')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
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
    researchers = DirectoryApplication.objects.filter(terms_accepted=True).order_by('-created_at')
    return render(request, 'app/directory_researchers.html', {'researchers': researchers})

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
    return render(request, 'app/sponsors.html')

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
