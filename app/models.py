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
    cover_image = models.ImageField(upload_to='articles/covers/', blank=True, null=True)
    volume = models.CharField(max_length=50, blank=True)
    issue = models.CharField(max_length=50, blank=True)
    pages = models.CharField(max_length=50, blank=True)
    journal_name = models.CharField(max_length=300, blank=True)
    country_of_publication = models.CharField(max_length=100, blank=True)
    year_of_publication = models.IntegerField(blank=True, null=True)
    authors_names = models.CharField(max_length=1000, blank=True, help_text="Comma-separated author names")
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
    JOURNAL_TYPE_CHOICES = [
        ('open-access', 'Open-Access Journal'),
        ('subscription', 'Subscription-Based Journal'),
        ('hybrid', 'Hybrid'),
        ('trade', 'Trade Journal'),
        ('current-affairs', 'Current affairs/Opinion Magazine'),
        ('popular', 'Popular Magazine'),
        ('preprint', 'Pre-Print Journal'),
    ]
    
    JOURNAL_FORMAT_CHOICES = [
        ('print', 'Print'),
        ('online', 'Online'),
        ('both', 'Both Print and Online'),
    ]
    
    journal_name = models.CharField(max_length=300)
    journal_abbreviation = models.CharField(max_length=100, blank=True)
    journal_cover_image = models.ImageField(upload_to='journals/covers/', blank=True, null=True)
    journal_logo = models.ImageField(upload_to='journals/logos/', blank=True, null=True)
    journal_url = models.URLField(blank=True)
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
    journal_type = models.CharField(max_length=50, choices=JOURNAL_TYPE_CHOICES, blank=True)
    journal_format = models.CharField(max_length=50, choices=JOURNAL_FORMAT_CHOICES, blank=True)
    publication_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    open_access = models.BooleanField(default=False)
    peer_review = models.BooleanField(default=False)
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
    views = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
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

# Project Payment Model - Track payments and downloads
class ProjectPayment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='payments')
    email = models.EmailField()
    payment_reference = models.CharField(max_length=255, unique=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ])
    document_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} - {self.project.project_title} - {self.payment_reference}"

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
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100)
    institution = models.CharField(max_length=300, blank=True)
    position = models.CharField(max_length=200, blank=True)
    membership_type = models.CharField(max_length=50, choices=MEMBERSHIP_TYPE_CHOICES, default='individual')
    research_interests = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='membership_requests/profiles/', blank=True, null=True)
    cv_file = models.FileField(
        upload_to='membership_requests/cvs/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        blank=True,
        null=True
    )
    motivation_letter = models.FileField(
        upload_to='membership_requests/letters/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        blank=True,
        null=True
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

    DISCIPLINE_STATUS_CHOICES = [
        ('teacher', 'Teacher'),
        ('tattoo-artist', 'Tattoo Artist'),
        ('special-effects-consultant', 'Special Effects Consultant'),
        ('set-designer', 'Set Designer'),
        ('sculptor', 'Sculptor'),
        ('product-designer', 'Product Designer'),
        ('photographer', 'Photographer'),
        ('performer', 'Performer'),
        ('painter', 'Painter'),
        ('non-profit-administrator', 'Non-profit Administrator'),
        ('museum-director', 'Museum Director'),
        ('multimedia-consultant', 'Multimedia Consultant'),
        ('medical-illustrator', 'Medical Illustrator'),
        ('landscape-designer', 'Landscape Designer'),
        ('journalist', 'Journalist'),
        ('jewelry-designer', 'Jewelry Designer'),
        ('interior-decorator', 'Interior Decorator'),
        ('illustrator', 'Illustrator'),
        ('historian', 'Historian'),
        ('graphic-designer', 'Graphic Designer'),
        ('gallery-director', 'Gallery Director'),
        ('furniture-designer', 'Furniture Designer'),
        ('fashion-designer', 'Fashion Designer'),
        ('exhibit-designer', 'Exhibit Designer'),
        ('engraver', 'Engraver'),
        ('curator', 'Curator'),
        ('critic', 'Critic'),
        ('courtroom-sketch-artist', 'Courtroom Sketch Artist'),
        ('cinematographer', 'Cinematographer'),
        ('cartoonist', 'Cartoonist'),
        ('artist', 'Artist'),
        ('art-gallery-director', 'Art Gallery Director'),
        ('art-editor', 'Art Editor'),
        ('art-consultant', 'Art Consultant'),
        ('archivist', 'Archivist'),
        ('architect', 'Architect'),
        ('political-leader', 'Political Leader'),
        ('military', 'Military'),
        ('military-and-political-leader', 'Military and Political Leader'),
        ('goddess', 'Goddess'),
        ('monk', 'Monk'),
        ('emperor', 'Emperor'),
        ('princess', 'Princess'),
        ('prince', 'Prince'),
        ('queen', 'Queen'),
        ('king', 'King'),
        ('playwright', 'Playwright'),
        ('entrepreneur', 'Entrepreneur'),
        ('ecology-and-evolutionary-biology', 'Ecology and Evolutionary Biology'),
        ('genetics-and-genomics', 'Genetics and Genomics'),
        ('laboratory-and-basic-science-research', 'Laboratory and Basic Science Research'),
        ('microbiology', 'Microbiology'),
        ('plant-sciences', 'Plant Sciences'),
        ('biotechnology', 'Biotechnology'),
        ('biology', 'Biology'),
        ('biodiversity', 'Biodiversity'),
        ('biochemistry-biophysics-and-structural-biology', 'Biochemistry, Biophysics, and Structural Biology'),
        ('animal-sciences', 'Animal Sciences'),
        ('agriculture-science', 'Agriculture Science'),
        ('data-science', 'Data Science'),
        ('mathematics', 'Mathematics'),
        ('environmental-science', 'Environmental Science'),
        ('earth-sciences', 'Earth Sciences'),
        ('chemist-and-biologist', 'Chemist and Biologist'),
        ('chemistry', 'Chemistry'),
        ('applied-mathematics', 'Applied Mathematics'),
        ('education', 'Education'),
        ('medical-doctor', 'Medical Doctor'),
        ('inventor', 'Inventor'),
        ('writer', 'Writer'),
        ('spiritual-teacher', 'Spiritual Teacher'),
        ('christian-missionary', 'Christian Missionary'),
        ('poet', 'Poet'),
        ('philosopher', 'Philosopher'),
        ('scientist', 'Scientist'),
        ('musician', 'Musician'),
        ('professional-boxer', 'Professional Boxer'),
        ('professional-wrestler', 'Professional Wrestler'),
        ('actress', 'Actress'),
        ('actor', 'Actor'),
        ('antitrust-law', 'Antitrust Law'),
        ('arbitration', 'Arbitration'),
        ('civil-law', 'Civil Law'),
        ('comparative-law', 'Comparative Law'),
        ('constitutional-administrative-law', 'Constitutional & Administrative Law'),
        ('construction-law', 'Construction Law'),
        ('contract-law', 'Contract Law'),
        ('corporate-law', 'Corporate Law'),
        ('criminal-law', 'Criminal Law'),
        ('employment-labor-law', 'Employment & Labor Law'),
        ('environment-energy-law', 'Environment & Energy Law'),
        ('european-union-law', 'European Union Law'),
        ('family-law', 'Family Law'),
        ('financial-law', 'Financial Law'),
        ('history-of-law', 'History of Law'),
        ('human-rights-immigration', 'Human Rights & Immigration'),
        ('intellectual-property-law', 'Intellectual Property Law'),
        ('international-law', 'International Law'),
        ('it-communications-law', 'IT & Communications Law'),
        ('jurisprudence-philosophy-of-law', 'Jurisprudence & Philosophy of Law'),
        ('law-politics', 'Law & Politics'),
        ('law-society', 'Law & Society'),
        ('legal-system-practice', 'Legal System & Practice'),
        ('medical-healthcare-law', 'Medical & Healthcare Law'),
        ('philosophy-of-law', 'Philosophy of Law'),
        ('policing', 'Policing'),
        ('property-law', 'Property Law'),
        ('study-revision', 'Study & Revision'),
        ('terrorism-national-security-law', 'Terrorism & National Security Law'),
        ('tort-law', 'Tort Law'),
        ('trusts-law', 'Trusts Law'),
        ('media-law', 'Media Law'),
        ('allied-health-professions', 'Allied Health Professions'),
        ('anesthesiology', 'Anesthesiology'),
        ('clinical-medicine', 'Clinical Medicine'),
        ('clinical-neuroscience', 'Clinical Neuroscience'),
        ('critical-care', 'Critical Care'),
        ('dentistry', 'Dentistry'),
        ('emergency-medicine', 'Emergency Medicine'),
        ('family-practice', 'Family Practice'),
        ('forensic-medicine', 'Forensic Medicine'),
        ('hematology', 'Hematology'),
        ('history-of-medicine', 'History of Medicine'),
        ('medical-dentistry', 'Medical Dentistry'),
        ('medical-ethics', 'Medical Ethics'),
        ('medical-skills', 'Medical Skills'),
        ('medical-statistics-methodology', 'Medical Statistics & Methodology'),
        ('midwifery', 'Midwifery'),
        ('nursing-studies', 'Nursing Studies'),
        ('nursing', 'Nursing'),
        ('obstetrics-gynecology', 'Obstetrics & Gynecology'),
        ('occupational-medicine', 'Occupational Medicine'),
        ('ophthalmology', 'Ophthalmology'),
        ('otolaryngology', 'Otolaryngology (Ear, Nose, Throat)'),
        ('pathology', 'Pathology'),
        ('pediatrics', 'Pediatrics'),
        ('pharmacology', 'Pharmacology'),
        ('popular-health', 'Popular Health'),
        ('preclinical-medicine', 'Preclinical Medicine'),
        ('psychiatry', 'Psychiatry'),
        ('psychotherapy', 'Psychotherapy'),
        ('public-health-epidemiology', 'Public Health & Epidemiology'),
        ('radiology', 'Radiology'),
        ('biological-sciences', 'Biological Sciences'),
        ('computer-science', 'Computer Science'),
        ('computing', 'Computing'),
        ('earth-sciences-geography', 'Earth Sciences & Geography'),
        ('engineering-technology', 'Engineering & Technology'),
        ('environmental-science', 'Environmental Science'),
        ('history-of-science-technology', 'History of Science & Technology'),
        ('materials-science', 'Materials Science'),
        ('neuroscience', 'Neuroscience'),
        ('physics', 'Physics'),
        ('psychology', 'Psychology'),
        ('anthropology', 'Anthropology'),
        ('business-management', 'Business & Management'),
        ('entrepreneurial-small-business-operations', 'Entrepreneurial and Small Business Operations'),
        ('entrepreneurial-large-business-operations', 'Entrepreneurial and Large Business Operations'),
        ('business-analytics', 'Business Analytics'),
        ('business-administration-management-operations', 'Business Administration, Management, and Operations'),
        ('accounting', 'Accounting'),
        ('management-information-systems', 'Management Information Systems'),
        ('technology-and-innovation', 'Technology and Innovation'),
        ('business-intelligence', 'Business Intelligence'),
        ('criminology-criminal-justice', 'Criminology & Criminal Justice'),
        ('development-studies', 'Development Studies'),
        ('economics', 'Economics'),
        ('environment', 'Environment'),
        ('human-geography', 'Human Geography'),
        ('interdisciplinary-studies', 'Interdisciplinary Studies'),
        ('museums-libraries-information-sciences', 'Museums, Libraries, & Information Sciences'),
        ('politician', 'Politician'),
        ('regional-area-studies', 'Regional & Area Studies'),
        ('research-information', 'Research & Information'),
        ('sociology', 'Sociology'),
        ('social-work', 'Social Work'),
        ('warfare-defense', 'Warfare & Defense'),
        ('legal-studies', 'Legal Studies'),
        ('leadership-studies', 'Leadership Studies'),
        ('international-and-area-studies', 'International and Area Studies'),
        ('disability-studies', 'Disability Studies'),
        ('geography', 'Geography'),
        ('communication', 'Communication'),
        ('archaeology', 'Archaeology'),
        ('architecture', 'Architecture'),
        ('art', 'Art'),
        ('biography', 'Biography'),
        ('byzantine-studies', 'Byzantine Studies'),
        ('classical-studies', 'Classical Studies'),
        ('digital-humanities', 'Digital Humanities'),
        ('egyptology', 'Egyptology'),
        ('history', 'History'),
        ('journalism', 'Journalism'),
        ('language-teaching-learning', 'Language Teaching & Learning'),
        ('linguistics', 'Linguistics'),
        ('literature', 'Literature'),
        ('media-studies', 'Media Studies'),
        ('music', 'Music'),
        ('music-sheet-music', 'Music – Sheet Music'),
        ('performing-arts', 'Performing Arts'),
        ('philosophy', 'Philosophy'),
        ('publishing', 'Publishing'),
        ('society-culture', 'Society & Culture'),
        ('africana-studies', 'Africana Studies'),
        ('religion', 'Religion'),
        ('american-studies', 'American Studies'),
        ('creative-writing', 'Creative Writing'),
        ('east-asian-languages-societies', 'East Asian Languages and Societies'),
        ('feminist-gender-sexuality-studies', 'Feminist, Gender, and Sexuality Studies'),
        ('theatre-performance', 'Theatre and Performance'),
        ('reading-language', 'Reading and Language'),
        ('race-ethnicity-post-colonial-studies', 'Race, Ethnicity and Post-Colonial Studies'),
        ('modern-literature', 'Modern Literature'),
        ('modern-languages', 'Modern Languages'),
        ('athlete', 'Athlete'),
        ('politics', 'Politics'),
        ('professional-soccer-player', 'Professional Soccer Player'),
        ('finance', 'Finance'),
    ]

    CATEGORY_CHOICES = [
        ('inspirational-people', 'Inspirational people'),
        ('humanitarians', 'Humanitarians'),
        ('royalty', 'Royalty'),
        ('sport', 'Sport'),
        ('celebrities', 'Celebrities'),
        ('theater-fine-art', 'Theater (Fine Art)'),
        ('visual-arts', 'Visual Arts'),
        ('womens-rights-activists', "Women's Rights Activists"),
        ('famous-outlaws', 'Famous Outlaws'),
        ('famous-lawyers', 'Famous Lawyers'),
        ('controversial-people', 'Controversial People'),
        ('famous-historical-figures', 'Famous Historical Figures'),
        ('courageous-people', 'Courageous People'),
        ('famous-people', 'Famous People'),
        ('influential-people', 'Influential People'),
        ('eminent-individuals', 'Eminent Individuals'),
        ('law', 'Law'),
        ('medicine-and-health', 'Medicine and Health'),
        ('science-and-mathematics', 'Science and Mathematics'),
        ('social-and-behavioral-sciences', 'Social and Behavioral Sciences'),
        ('physical-sciences-and-mathematics', 'Physical Sciences and Mathematics'),
        ('art-and-humanities', 'Art and Humanities'),
        ('life-sciences', 'Life Sciences'),
    ]

    application_type = models.CharField(max_length=50, choices=APPLICATION_TYPE_CHOICES)
    nominee_first_name = models.CharField(max_length=100)
    nominee_last_name = models.CharField(max_length=100)
    nominee_email = models.EmailField()
    nominee_institution = models.CharField(max_length=300)
    nominee_position = models.CharField(max_length=200)
    discipline_or_status = models.CharField(max_length=100, choices=DISCIPLINE_STATUS_CHOICES, blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, blank=True, null=True)
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
    document_title = models.CharField(max_length=300)
    check_type = models.CharField(max_length=50, choices=CHECK_TYPE_CHOICES, default='standard')
    exclude_quotes = models.BooleanField(default=False)
    exclude_bibliography = models.BooleanField(default=False)
    exclude_small_matches = models.BooleanField(default=False)
    email = models.EmailField()
    name = models.CharField(max_length=200)
    whatsapp_phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(blank=True)
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
    PLAGIARISM_PERCENTAGE_CHOICES = [
        ('0-10', '0-10%'),
        ('11-20', '11-20%'),
        ('21-30', '21-30%'),
        ('31-40', '31-40%'),
        ('41-50', '41-50%'),
        ('51-60', '51-60%'),
        ('61-70', '61-70%'),
        ('71-80', '71-80%'),
        ('81-90', '81-90%'),
        ('91-100', '91-100%'),
    ]

    document = models.FileField(
        upload_to='plagiarism_work/',
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx'])],
        help_text='MS Word file to work on'
    )
    plagiarism_report = models.FileField(
        upload_to='plagiarism_work/reports/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text='Plagiarism report in PDF format',
        blank=True,
        null=True
    )
    submission_title = models.CharField(max_length=300, blank=True, null=True)
    plagiarism_percentage = models.CharField(max_length=20, choices=PLAGIARISM_PERCENTAGE_CHOICES, default='0-10')
    email = models.EmailField()
    name = models.CharField(max_length=200)
    whatsapp_phone = models.CharField(max_length=20, blank=True, null=True)
    terms_accepted = models.BooleanField(default=False)
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
    submission_title = models.CharField(max_length=300, blank=True, null=True)
    number_of_article = models.CharField(max_length=50, blank=True, null=True, help_text='Number of articles to be extracted (e.g., 3, 4, or 5)')
    target_journal = models.CharField(max_length=300, blank=True)
    article_type = models.CharField(max_length=50, choices=ARTICLE_TYPE_CHOICES, default='research-article')
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
    whatsapp_phone = models.CharField(max_length=20, blank=True, null=True)
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
    submission_title = models.CharField(max_length=300, blank=True, null=True)
    number_of_books = models.CharField(max_length=50, blank=True, null=True, help_text='Number of books to be extracted (e.g., 3, 4, or 5)')
    book_title = models.CharField(max_length=300, blank=True, null=True)
    book_type = models.CharField(max_length=50, choices=BOOK_TYPE_CHOICES, blank=True, null=True)
    target_audience = models.CharField(max_length=300, blank=True, null=True)
    chapter_structure = models.TextField(blank=True, null=True)
    special_requirements = models.TextField(blank=True, null=True)
    email = models.EmailField()
    name = models.CharField(max_length=200)
    whatsapp_phone = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
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
    submission_title = models.CharField(max_length=300, blank=True, null=True)
    number_of_chapters = models.CharField(max_length=50, blank=True, null=True, help_text='Number of chapters to be extracted (e.g., 3, 4, or 5)')
    chapter_title = models.CharField(max_length=300, blank=True, null=True)
    thesis_section = models.CharField(max_length=100, blank=True, null=True)
    chapter_number = models.IntegerField(null=True, blank=True)
    target_book = models.CharField(max_length=300, blank=True, null=True)
    word_limit = models.IntegerField(null=True, blank=True)
    special_instructions = models.TextField(blank=True, null=True)
    email = models.EmailField()
    name = models.CharField(max_length=200)
    whatsapp_phone = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
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
    submission_title = models.CharField(max_length=300, blank=True, null=True)
    number_of_slides = models.CharField(max_length=50, blank=True, null=True, help_text='Number of PowerPoint slides (e.g., 10, 3, 44 or 53)')
    presentation_type = models.CharField(max_length=50, choices=PRESENTATION_TYPE_CHOICES, blank=True, null=True)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES, blank=True, null=True)
    slide_count = models.IntegerField(null=True, blank=True)
    include_title = models.BooleanField(default=True, blank=True)
    include_intro = models.BooleanField(default=True, blank=True)
    include_objectives = models.BooleanField(default=True, blank=True)
    include_methodology = models.BooleanField(default=True, blank=True)
    include_results = models.BooleanField(default=True, blank=True)
    include_discussion = models.BooleanField(default=True, blank=True)
    include_conclusion = models.BooleanField(default=True, blank=True)
    include_references = models.BooleanField(default=True, blank=True)
    include_acknowledgments = models.BooleanField(default=False, blank=True)
    design_style = models.CharField(max_length=50, choices=DESIGN_STYLE_CHOICES, blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    email = models.EmailField()
    name = models.CharField(max_length=200)
    whatsapp_phone = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
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
    
    # Carousel Images (3 images with text)
    carousel_image_1 = models.ImageField(upload_to='settings/carousel/', blank=True, null=True)
    carousel_image_1_url = models.URLField(blank=True, help_text="Alternative: Provide image URL instead of uploading")
    carousel_image_1_title = models.CharField(max_length=500, blank=True, default="Advancing Research Through Innovation")
    carousel_image_1_subtitle = models.TextField(blank=True, default="Explore groundbreaking research papers, cutting-edge methodologies, and innovative findings that shape the future of knowledge and discovery.")
    
    carousel_image_2 = models.ImageField(upload_to='settings/carousel/', blank=True, null=True)
    carousel_image_2_url = models.URLField(blank=True, help_text="Alternative: Provide image URL instead of uploading")
    carousel_image_2_title = models.CharField(max_length=500, blank=True, default="Advancing Research Through Innovation")
    carousel_image_2_subtitle = models.TextField(blank=True, default="Explore groundbreaking research papers, cutting-edge methodologies, and innovative findings that shape the future of knowledge and discovery.")
    
    carousel_image_3 = models.ImageField(upload_to='settings/carousel/', blank=True, null=True)
    carousel_image_3_url = models.URLField(blank=True, help_text="Alternative: Provide image URL instead of uploading")
    carousel_image_3_title = models.CharField(max_length=500, blank=True, default="Advancing Research Through Innovation")
    carousel_image_3_subtitle = models.TextField(blank=True, default="Explore groundbreaking research papers, cutting-edge methodologies, and innovative findings that shape the future of knowledge and discovery.")
    
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
    enable_donate_page = models.BooleanField(default=True)
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

# News Bookmark Model
class NewsBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_bookmarks')
    article = models.ForeignKey('NewsArticle', on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'article')
        ordering = ['-created_at']
        verbose_name = 'News Bookmark'
        verbose_name_plural = 'News Bookmarks'
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.article.title}"

# News Comment Model
class NewsComment(models.Model):
    article = models.ForeignKey('NewsArticle', on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_comments')
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_news_comments', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_news_comments', blank=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'News Comment'
        verbose_name_plural = 'News Comments'
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"
    
    def get_likes_count(self):
        return self.likes.count()
    
    def get_dislikes_count(self):
        return self.dislikes.count()
    
    def get_replies_count(self):
        return self.replies.filter(is_approved=True).count()

# News Tag Model
class NewsTag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    order_priority = models.IntegerField(default=0, help_text="Higher numbers appear first")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-order_priority', 'name']
        verbose_name = 'News Tag'
        verbose_name_plural = 'News Tags'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# News Writer Model
class NewsWriter(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='writers/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    order_priority = models.IntegerField(default=0, help_text="Higher numbers appear first")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-order_priority', 'name']
        verbose_name = 'News Writer'
        verbose_name_plural = 'News Writers'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# News Article Model
class NewsArticle(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True, null=True)
    featured_image = models.ImageField(upload_to='news/', blank=True, null=True)
    tags = models.ManyToManyField(NewsTag, related_name='articles', blank=True)
    writer = models.ForeignKey(NewsWriter, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    is_published = models.BooleanField(default=True)
    published_date = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-published_date']
        verbose_name = 'News Article'
        verbose_name_plural = 'News Articles'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def formatted_date(self):
        """Return formatted date like '3rd September, 2024'"""
        day = self.published_date.day
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
        
        return self.published_date.strftime(f"%d{suffix} %B, %Y")