from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Article Model
class Article(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    ARTICLE_TYPE_CHOICES = [
        ('research', 'Research Article'),
        ('review', 'Review Article'),
        ('case_study', 'Case Study'),
        ('short_communication', 'Short Communication'),
        ('letter', 'Letter to Editor'),
    ]

    title = models.CharField(max_length=500)
    article_type = models.CharField(max_length=50, choices=ARTICLE_TYPE_CHOICES)
    discipline = models.CharField(max_length=200)
    abstract = models.TextField(max_length=2000)
    keywords = models.CharField(max_length=500)
    language = models.CharField(max_length=50, default='English')
    publication_date = models.DateField(blank=True, null=True)
    doi = models.CharField(max_length=200, blank=True)
    article_file = models.FileField(
        upload_to='articles/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Article Author Model
class ArticleAuthor(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='authors')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    affiliation = models.CharField(max_length=300, blank=True)
    orcid = models.CharField(max_length=50, blank=True)
    is_corresponding = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.article.title}"

# Journal Model
class Journal(models.Model):
    journal_name = models.CharField(max_length=300)
    journal_abbreviation = models.CharField(max_length=100, blank=True)
    publisher_name = models.CharField(max_length=300)
    publisher_address = models.TextField(blank=True)
    publisher_country = models.CharField(max_length=100)
    publisher_email = models.EmailField()
    publisher_phone = models.CharField(max_length=20, blank=True)
    publisher_website = models.URLField(blank=True)
    issn_print = models.CharField(max_length=20, blank=True)
    issn_online = models.CharField(max_length=20, blank=True)
    e_issn = models.CharField(max_length=20, blank=True)
    subject_area = models.CharField(max_length=200)
    language = models.CharField(max_length=50, default='English')
    publication_frequency = models.CharField(max_length=100, blank=True)
    first_publication_year = models.IntegerField(blank=True, null=True)
    journal_scope = models.TextField(blank=True)
    journal_logo = models.ImageField(upload_to='journals/logos/', blank=True, null=True)
    terms_accepted = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.journal_name

# Journal Editor Model
class JournalEditor(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='editors')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    affiliation = models.CharField(max_length=300, blank=True)
    role = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.journal.journal_name}"

# Project Model
class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]

    PROJECT_TYPE_CHOICES = [
        ('research', 'Research Project'),
        ('development', 'Development Project'),
        ('collaboration', 'Collaboration Project'),
        ('other', 'Other'),
    ]

    project_title = models.CharField(max_length=500)
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPE_CHOICES)
    category = models.CharField(max_length=200)
    institution = models.CharField(max_length=300)
    description = models.TextField(max_length=2000)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    project_file = models.FileField(
        upload_to='projects/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'zip'])]
    )
    additional_info = models.TextField(blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_title

# Project Contributor Model
class ProjectContributor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    affiliation = models.CharField(max_length=300, blank=True)
    role = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.project.project_title}"

# Membership Request Model
class MembershipRequest(models.Model):
    MEMBERSHIP_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('institutional', 'Institutional'),
        ('corporate', 'Corporate'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    institution = models.CharField(max_length=300, blank=True)
    position = models.CharField(max_length=200, blank=True)
    membership_type = models.CharField(max_length=50, choices=MEMBERSHIP_TYPE_CHOICES)
    research_interests = models.TextField(blank=True)
    cv_file = models.FileField(
        upload_to='membership_requests/cvs/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    motivation_letter = models.FileField(
        upload_to='membership_requests/letters/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    terms_accepted = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.membership_type}"

# Directory Application Model
class DirectoryApplication(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    institution = models.CharField(max_length=300)
    position = models.CharField(max_length=200)
    research_areas = models.TextField()
    education_background = models.TextField(blank=True)
    publications_summary = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='directory_applications/photos/', blank=True, null=True)
    cv_file = models.FileField(
        upload_to='directory_applications/cvs/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    google_scholar_link = models.URLField(blank=True)
    orcid_id = models.CharField(max_length=50, blank=True)
    terms_accepted = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Directory Application"

# Hall of Fame Application Model
class HallOfFameApplication(models.Model):
    APPLICATION_TYPE_CHOICES = [
        ('self', 'Self-Nomination'),
        ('nomination', 'Nominate Someone Else'),
    ]

    application_type = models.CharField(max_length=50, choices=APPLICATION_TYPE_CHOICES)
    nominee_first_name = models.CharField(max_length=100)
    nominee_last_name = models.CharField(max_length=100)
    nominee_email = models.EmailField()
    nominee_institution = models.CharField(max_length=300)
    nominee_position = models.CharField(max_length=200)
    research_achievements = models.TextField()
    impact_description = models.TextField()
    supporting_documents = models.FileField(
        upload_to='hall_of_fame/documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'zip'])]
    )
    nominator_first_name = models.CharField(max_length=100, blank=True)
    nominator_last_name = models.CharField(max_length=100, blank=True)
    nominator_email = models.EmailField(blank=True)
    nominator_relationship = models.CharField(max_length=200, blank=True)
    terms_accepted = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nominee_first_name} {self.nominee_last_name} - Hall of Fame"

# Plagiarism Check Model
class PlagiarismCheck(models.Model):
    CHECK_TYPE_CHOICES = [
        ('standard', 'Standard Check'),
        ('comprehensive', 'Comprehensive Check'),
        ('quick', 'Quick Check'),
    ]

    document = models.FileField(
        upload_to='plagiarism_checks/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt'])]
    )
    document_title = models.CharField(max_length=300, blank=True)
    check_type = models.CharField(max_length=50, choices=CHECK_TYPE_CHOICES)
    exclude_quotes = models.BooleanField(default=False)
    exclude_bibliography = models.BooleanField(default=False)
    exclude_small_matches = models.BooleanField(default=False)
    email = models.EmailField()
    name = models.CharField(max_length=200, blank=True)
    similarity_score = models.FloatField(null=True, blank=True)
    report_file = models.FileField(upload_to='plagiarism_reports/', blank=True, null=True)
    terms_accepted = models.BooleanField(default=False)
    privacy_accepted = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Plagiarism Check - {self.document_title or 'Untitled'}"

# Plagiarism Work Model
class PlagiarismWork(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('paraphrasing', 'Paraphrasing & Rewriting'),
        ('editing', 'Plagiarism Editing'),
        ('revision', 'Complete Revision'),
        ('consultation', 'Plagiarism Consultation'),
    ]

    URGENCY_CHOICES = [
        ('normal', 'Normal (3-5 business days)'),
        ('urgent', 'Urgent (1-2 business days)'),
        ('very-urgent', 'Very Urgent (24 hours)'),
    ]

    document = models.FileField(
        upload_to='plagiarism_work/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt'])]
    )
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    instructions = models.TextField(blank=True)
    urgency = models.CharField(max_length=50, choices=URGENCY_CHOICES, default='normal')
    email = models.EmailField()
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    terms_accepted = models.BooleanField(default=False)
    privacy_accepted = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Plagiarism Work - {self.name}"

# Thesis to Article Model
class ThesisToArticle(models.Model):
    ARTICLE_TYPE_CHOICES = [
        ('research-article', 'Research Article'),
        ('review-article', 'Review Article'),
        ('case-study', 'Case Study'),
        ('short-communication', 'Short Communication'),
        ('letter', 'Letter to Editor'),
    ]

    thesis_file = models.FileField(
        upload_to='thesis_to_article/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    target_journal = models.CharField(max_length=300, blank=True)
    article_type = models.CharField(max_length=50, choices=ARTICLE_TYPE_CHOICES)
    word_limit = models.IntegerField(null=True, blank=True)
    include_abstract = models.BooleanField(default=True)
    include_keywords = models.BooleanField(default=True)
    include_introduction = models.BooleanField(default=True)
    include_methodology = models.BooleanField(default=True)
    include_results = models.BooleanField(default=True)
    include_discussion = models.BooleanField(default=True)
    include_conclusion = models.BooleanField(default=True)
    include_references = models.BooleanField(default=True)
    special_instructions = models.TextField(blank=True)
    email = models.EmailField()
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    terms_accepted = models.BooleanField(default=False)
    privacy_accepted = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Thesis to Article - {self.name}"

# Thesis to Book Model
class ThesisToBook(models.Model):
    BOOK_TYPE_CHOICES = [
        ('monograph', 'Monograph'),
        ('textbook', 'Textbook'),
        ('edited-volume', 'Edited Volume'),
        ('reference-book', 'Reference Book'),
    ]

    thesis_file = models.FileField(
        upload_to='thesis_to_book/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    book_title = models.CharField(max_length=300, blank=True)
    book_type = models.CharField(max_length=50, choices=BOOK_TYPE_CHOICES)
    target_audience = models.CharField(max_length=300, blank=True)
    chapter_structure = models.TextField(blank=True)
    special_requirements = models.TextField(blank=True)
    email = models.EmailField()
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    terms_accepted = models.BooleanField(default=False)
    privacy_accepted = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Thesis to Book - {self.name}"

# Thesis to Book Chapter Model
class ThesisToBookChapter(models.Model):
    thesis_file = models.FileField(
        upload_to='thesis_to_book_chapter/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    chapter_title = models.CharField(max_length=300, blank=True)
    thesis_section = models.CharField(max_length=100, blank=True)
    chapter_number = models.IntegerField(null=True, blank=True)
    target_book = models.CharField(max_length=300, blank=True)
    word_limit = models.IntegerField(null=True, blank=True)
    special_instructions = models.TextField(blank=True)
    email = models.EmailField()
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    terms_accepted = models.BooleanField(default=False)
    privacy_accepted = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Thesis to Book Chapter - {self.name}"

# PowerPoint Preparation Model
class PowerPointPreparation(models.Model):
    PRESENTATION_TYPE_CHOICES = [
        ('defense', 'Thesis Defense'),
        ('conference', 'Conference Presentation'),
        ('seminar', 'Seminar/Workshop'),
        ('academic', 'Academic Presentation'),
        ('general', 'General Presentation'),
    ]

    DURATION_CHOICES = [
        ('10', '10 minutes'),
        ('15', '15 minutes'),
        ('20', '20 minutes'),
        ('30', '30 minutes'),
        ('45', '45 minutes'),
        ('60', '60 minutes'),
    ]

    DESIGN_STYLE_CHOICES = [
        ('professional', 'Professional'),
        ('modern', 'Modern'),
        ('minimalist', 'Minimalist'),
        ('academic', 'Academic'),
        ('creative', 'Creative'),
    ]

    thesis_file = models.FileField(
        upload_to='powerpoint_preparation/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    presentation_type = models.CharField(max_length=50, choices=PRESENTATION_TYPE_CHOICES)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES, blank=True)
    slide_count = models.IntegerField(null=True, blank=True)
    include_title = models.BooleanField(default=True)
    include_intro = models.BooleanField(default=True)
    include_objectives = models.BooleanField(default=True)
    include_methodology = models.BooleanField(default=True)
    include_results = models.BooleanField(default=True)
    include_discussion = models.BooleanField(default=True)
    include_conclusion = models.BooleanField(default=True)
    include_references = models.BooleanField(default=True)
    include_acknowledgments = models.BooleanField(default=False)
    design_style = models.CharField(max_length=50, choices=DESIGN_STYLE_CHOICES, blank=True)
    special_instructions = models.TextField(blank=True)
    email = models.EmailField()
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    terms_accepted = models.BooleanField(default=False)
    privacy_accepted = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PowerPoint Preparation - {self.name}"

# Site Settings Model - Stores all site-wide settings
class SiteSettings(models.Model):
    # General Settings - Theme
    default_banner_image = models.ImageField(upload_to='settings/banners/', blank=True, null=True)
    default_app_font_size = models.IntegerField(default=20, help_text="Font size in pixels")
    
    # Address & Contact
    phone = models.CharField(max_length=50, blank=True, default="+19517275906")
    office_location_address = models.TextField(blank=True, default="University of California, Experiment Station,1000 Martin Luther King Blvd. Riverside Ca 92507")
    email_address = models.EmailField(blank=True, default="xcholarindesing@gmail.com")
    whatsapp_url = models.URLField(blank=True, default="https://chat.whatsapp.com/KINOMMUWJ9YQzI0J5Zpm")
    youtube_url = models.URLField(blank=True, default="https://www.youtube.com/@scholararchive021")
    twitter_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True, default="https://facebook.com/scholarindexing")
    
    # Payment Gate
    api_secret_key = models.CharField(max_length=255, blank=True, default="sk_live_bbae3f1074bf22ceb0a1733abd08ec691d57b60d")
    api_public_key = models.CharField(max_length=255, blank=True, default="pk_live_b7da432989e4be82875d8a5c3e7b6dbbdf1c2c90")
    
    # Map Address
    map_index = models.URLField(blank=True, default="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3957.0005654309066!2d-2.390053985548167!3d7.3538")
    
    # Landing Page Settings
    banner_title = models.CharField(max_length=500, blank=True, default="Welcome! Accelerate Your Discovery")
    banner_subtitle = models.TextField(blank=True, default="Be a part of a committed society that is shaping the future of knowledge")
    footer_video = models.CharField(max_length=100, blank=True, default="JhV6DQUQsDY")
    enable_service_features = models.BooleanField(default=True)
    
    # Navigator Settings - Documents
    documentations_nav_image = models.ImageField(upload_to='settings/navigators/', blank=True, null=True)
    documentations_nav_title = models.TextField(blank=True, default="Check if you have access through your sign in credentials or via your institution.")
    documentations_nav_subtitle = models.TextField(blank=True, default="Connect different areas of knowledge and form an exploratory network. SIS mission is to make every scholarly and scientif")
    
    # Navigator Settings - Communities
    communities_nav_image = models.ImageField(upload_to='settings/navigators/', blank=True, null=True)
    communities_nav_title = models.TextField(blank=True, default="Sharing knowledge can seem like a burden to some but on the contrary, it is a reflection of teamwork and leadership")
    communities_nav_subtitle = models.TextField(blank=True, default="Researchers, teachers, students, healthcare and information professionals use SIS to improve the way they search, discove")
    
    # Navigator Settings - Requests
    requests_nav_image = models.ImageField(upload_to='settings/navigators/', blank=True, null=True)
    requests_nav_title = models.TextField(blank=True, default="Knowledge is like money: to be of value it must circulate, and in circulating it can increase in quantity and, hopefully, in valu")
    requests_nav_subtitle = models.TextField(blank=True, default="We are committed to promote the integrity of research through a range of activities and initiatives like offering free author 1")
    
    # Navigator Settings - About
    about_nav_image = models.ImageField(upload_to='settings/navigators/', blank=True, null=True)
    about_nav_title = models.TextField(blank=True)
    about_nav_subtitle = models.TextField(blank=True)
    
    # Page Enable/Disable Settings
    enable_landing_page = models.BooleanField(default=True)
    enable_indexed_articles_page = models.BooleanField(default=True)
    enable_indexed_journals_page = models.BooleanField(default=True)
    enable_project_archive_page = models.BooleanField(default=True)
    enable_directory_researchers_page = models.BooleanField(default=True)
    enable_hall_of_fame_page = models.BooleanField(default=True)
    enable_council_members_page = models.BooleanField(default=True)
    enable_team_members_page = models.BooleanField(default=True)
    enable_sponsors_page = models.BooleanField(default=True)
    enable_about_sis_page = models.BooleanField(default=True)
    enable_mission_page = models.BooleanField(default=True)
    enable_criteria_page = models.BooleanField(default=True)
    enable_tolerance_policy_page = models.BooleanField(default=True)
    enable_service_solution_page = models.BooleanField(default=True)
    enable_policy_terms_page = models.BooleanField(default=True)
    enable_check_turnitin_page = models.BooleanField(default=True)
    enable_work_plagiarism_page = models.BooleanField(default=True)
    enable_thesis_to_article_page = models.BooleanField(default=True)
    enable_thesis_to_book_page = models.BooleanField(default=True)
    enable_thesis_to_book_chapter_page = models.BooleanField(default=True)
    enable_powerpoint_preparation_page = models.BooleanField(default=True)
    
    # Pricing - Sponsorship
    premier_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sustaining_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    basic_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    power_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    double_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    single_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    compact_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    inspired_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    charity_homes_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Pricing - Registrations
    article_indexing_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    journal_indexing_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    project_archive_hosting_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    directory_researcher_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    hall_of_fame_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    check_plagiarism_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    work_plagiarism_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    thesis_to_article_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    thesis_to_book_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    thesis_to_book_chapter_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    powerpoint_preparation_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return "Site Settings"
    
    @classmethod
    def get_settings(cls):
        """Get or create the site settings singleton"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings

# Blog Model
class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('opinion', 'Opinion'),
        ('technology', 'Technology'),
        ('medicine_health', 'Medicine and Health'),
        ('education', 'Education'),
        ('science', 'Science'),
        ('business', 'Business'),
        ('general', 'General'),
    ]
    
    title = models.CharField(max_length=500)
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    tag = models.CharField(max_length=100, blank=True)
    order_priority = models.IntegerField(default=5, help_text="On a scale of 1 to 9")
    views = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    published_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-published_date', '-order_priority']
    
    def __str__(self):
        return self.title
    
    def formatted_date(self):
        """Return formatted date like '3rd September, 2024'"""
        day = self.published_date.day
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
        
        return self.published_date.strftime(f"%d{suffix} %B, %Y")