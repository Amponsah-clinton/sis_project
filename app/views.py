from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SearchForm, ContactForm

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
        # Here you would typically search your database
        # For now, just pass the query to the template
        messages.info(request, f'Searching for: {query}')
    
    return render(request, 'app/browse.html', {
        'search_form': search_form,
        'results': results,
    })

def submit(request):
    """Submit research view"""
    contact_form = ContactForm(request.POST or None)
    
    if request.method == 'POST':
        if contact_form.is_valid():
            # Here you would typically save to database
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
            # Handle login logic here
            username_or_email = request.POST.get('username_or_email')
            password = request.POST.get('password')
            # Add your authentication logic
            messages.success(request, 'Login functionality will be implemented')
            
        elif form_type == 'register':
            # Handle registration logic here
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            country = request.POST.get('country')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            profile_photo = request.FILES.get('profile_photo')
            
            # Add validation and registration logic
            if password != confirm_password:
                messages.error(request, 'Passwords do not match')
            else:
                messages.success(request, 'Registration functionality will be implemented')
    
    return render(request, 'app/auth.html')

def indexed_articles(request):
    """Indexed Articles page view"""
    return render(request, 'app/indexed_articles.html')

def indexed_journals(request):
    """Indexed Journals page view"""
    return render(request, 'app/indexed_journals.html')

def project_archive(request):
    """Project | Research Archive page view"""
    return render(request, 'app/project_archive.html')

def upload_article(request):
    """Upload Article page view"""
    if request.method == 'POST':
        # Handle article upload logic here
        title = request.POST.get('title')
        article_type = request.POST.get('article_type')
        # Add your upload logic
        messages.success(request, 'Article uploaded successfully!')
        return redirect('app:indexed_articles')
    
    return render(request, 'app/upload_article.html')

def register_journal(request):
    """Register Journal page view"""
    if request.method == 'POST':
        # Handle journal registration logic here
        journal_name = request.POST.get('journal_name')
        publisher_name = request.POST.get('publisher_name')
        # Add your registration logic
        messages.success(request, 'Journal registered successfully!')
        return redirect('app:indexed_journals')
    
    return render(request, 'app/register_journal.html')

def directory_researchers(request):
    """Directory of Researchers page view"""
    return render(request, 'app/directory_researchers.html')

def upload_project(request):
    """Upload | Archive Project page view"""
    if request.method == 'POST':
        # Handle project upload logic here
        project_title = request.POST.get('project_title')
        project_type = request.POST.get('project_type')
        # Add your upload logic
        messages.success(request, 'Project uploaded and archived successfully!')
        return redirect('app:project_archive')
    
    return render(request, 'app/upload_project.html')

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
        # Handle membership request logic here
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        # Add your membership request logic
        messages.success(request, 'Your membership request has been submitted successfully!')
        return redirect('app:landing')
    
    return render(request, 'app/request_membership.html')

def apply_directory(request):
    """Apply For Directory of Researcher page view"""
    if request.method == 'POST':
        # Handle directory application logic here
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        # Add your directory application logic
        messages.success(request, 'Your application has been submitted successfully!')
        return redirect('app:directory_researchers')
    
    return render(request, 'app/apply_directory.html')

def hall_of_fame(request):
    """Hall of Fame listing page view"""
    return render(request, 'app/hall_of_fame.html')

def hall_of_fame_apply(request):
    """Apply For Hall of Fame page view"""
    if request.method == 'POST':
        nominee_name = request.POST.get('nominee_first_name')
        messages.success(request, 'Your Hall of Fame application has been submitted successfully!')
        return redirect('app:hall_of_fame')
    
    return render(request, 'app/hall_of_fame_apply.html')

def check_turnitin(request):
    """Check Turnitin Plagiarism page view"""
    if request.method == 'POST':
        document = request.FILES.get('document')
        messages.success(request, 'Your document has been submitted for plagiarism check!')
        return redirect('app:landing')
    
    return render(request, 'app/check_turnitin.html')

def work_plagiarism(request):
    """Work My Plagiarism page view"""
    if request.method == 'POST':
        document = request.FILES.get('document')
        messages.success(request, 'Your request has been submitted successfully!')
        return redirect('app:landing')
    
    return render(request, 'app/work_plagiarism.html')

def thesis_to_article(request):
    """Thesis To Article page view"""
    if request.method == 'POST':
        thesis_file = request.FILES.get('thesis_file')
        messages.success(request, 'Your thesis has been submitted for article conversion!')
        return redirect('app:landing')
    
    return render(request, 'app/thesis_to_article.html')

def thesis_to_book(request):
    """Thesis To Book page view"""
    if request.method == 'POST':
        thesis_file = request.FILES.get('thesis_file')
        messages.success(request, 'Your thesis has been submitted for book conversion!')
        return redirect('app:landing')
    
    return render(request, 'app/thesis_to_book.html')

def thesis_to_book_chapter(request):
    """Thesis To Book Chapter page view"""
    if request.method == 'POST':
        thesis_file = request.FILES.get('thesis_file')
        messages.success(request, 'Your thesis has been submitted for book chapter conversion!')
        return redirect('app:landing')
    
    return render(request, 'app/thesis_to_book_chapter.html')

def powerpoint_preparation(request):
    """Power Point Preparation page view"""
    if request.method == 'POST':
        thesis_file = request.FILES.get('thesis_file')
        messages.success(request, 'Your thesis has been submitted for PowerPoint preparation!')
        return redirect('app:landing')
    
    return render(request, 'app/powerpoint_preparation.html')

