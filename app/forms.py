from django import forms
from django.core.validators import FileExtensionValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    UserProfile, Article, ArticleAuthor, Journal, JournalEditor, Project, ProjectContributor,
    MembershipRequest, DirectoryApplication, HallOfFameApplication, PlagiarismCheck,
    PlagiarismWork, ThesisToArticle, ThesisToBook, ThesisToBookChapter, PowerPointPreparation,
    NewsArticle
)

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'search-input',
            'placeholder': 'Search articles, authors, keywords...',
        })
    )

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Your Name',
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'your.email@example.com',
        })
    )
    subject = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Subject',
        })
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Your message...',
            'rows': 5,
        })
    )

# User Registration Form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("A user with this email already exists. Please use a different email address.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# Article Forms
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'article_type', 'discipline', 'abstract', 'keywords', 
                  'language', 'publication_date', 'doi', 'article_file', 'cover_image',
                  'volume', 'issue', 'pages', 'journal_name', 'country_of_publication',
                  'year_of_publication', 'authors_names']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'article_type': forms.Select(attrs={'class': 'form-control'}),
            'discipline': forms.TextInput(attrs={'class': 'form-control'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'keywords': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'doi': forms.TextInput(attrs={'class': 'form-control'}),
            'article_file': forms.FileInput(attrs={'class': 'form-control'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'volume': forms.TextInput(attrs={'class': 'form-control'}),
            'issue': forms.TextInput(attrs={'class': 'form-control'}),
            'pages': forms.TextInput(attrs={'class': 'form-control'}),
            'journal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'country_of_publication': forms.TextInput(attrs={'class': 'form-control'}),
            'year_of_publication': forms.NumberInput(attrs={'class': 'form-control'}),
            'authors_names': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ArticleAuthorForm(forms.ModelForm):
    class Meta:
        model = ArticleAuthor
        fields = ['name', 'email', 'affiliation', 'orcid', 'is_corresponding', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'affiliation': forms.TextInput(attrs={'class': 'form-control'}),
            'orcid': forms.TextInput(attrs={'class': 'form-control'}),
            'is_corresponding': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Journal Forms
class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['journal_name', 'journal_abbreviation', 'journal_cover_image', 'journal_logo', 'journal_url',
                  'publisher_name', 'publisher_address', 'publisher_country', 'publisher_email', 
                  'publisher_phone', 'publisher_website', 'issn_print', 'issn_online', 'e_issn', 
                  'subject_area', 'language', 'publication_frequency', 'first_publication_year', 
                  'journal_scope', 'journal_type', 'journal_format', 'publication_fee', 
                  'open_access', 'peer_review', 'terms_accepted']
        widgets = {
            'journal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'journal_abbreviation': forms.TextInput(attrs={'class': 'form-control'}),
            'journal_cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'journal_logo': forms.FileInput(attrs={'class': 'form-control'}),
            'journal_url': forms.URLInput(attrs={'class': 'form-control'}),
            'publisher_name': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'publisher_country': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'publisher_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher_website': forms.URLInput(attrs={'class': 'form-control'}),
            'issn_print': forms.TextInput(attrs={'class': 'form-control'}),
            'issn_online': forms.TextInput(attrs={'class': 'form-control'}),
            'e_issn': forms.TextInput(attrs={'class': 'form-control'}),
            'subject_area': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_frequency': forms.TextInput(attrs={'class': 'form-control'}),
            'first_publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'journal_scope': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'journal_type': forms.Select(attrs={'class': 'form-control'}),
            'journal_format': forms.Select(attrs={'class': 'form-control'}),
            'publication_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'open_access': forms.HiddenInput(),  # Handled manually via radio buttons
            'peer_review': forms.HiddenInput(),  # Handled manually via radio buttons
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class JournalEditorForm(forms.ModelForm):
    class Meta:
        model = JournalEditor
        fields = ['name', 'email', 'affiliation', 'role', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'affiliation': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Project Forms
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_title', 'project_type', 'category', 'institution', 'description',
                  'start_date', 'end_date', 'status', 'project_file', 'additional_info']
        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'form-control'}),
            'project_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'project_file': forms.FileInput(attrs={'class': 'form-control'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ProjectContributorForm(forms.ModelForm):
    class Meta:
        model = ProjectContributor
        fields = ['name', 'email', 'affiliation', 'role', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'affiliation': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Membership Request Form
class MembershipRequestForm(forms.ModelForm):
    class Meta:
        model = MembershipRequest
        fields = ['first_name', 'last_name', 'email', 'phone', 'country', 'institution',
                  'position', 'membership_type', 'research_interests', 'profile_picture',
                  'cv_file', 'motivation_letter', 'terms_accepted']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'membership_type': forms.Select(attrs={'class': 'form-control'}),
            'research_interests': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'cv_file': forms.FileInput(attrs={'class': 'form-control'}),
            'motivation_letter': forms.FileInput(attrs={'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Directory Application Form
class DirectoryApplicationForm(forms.ModelForm):
    class Meta:
        model = DirectoryApplication
        fields = ['first_name', 'last_name', 'email', 'phone', 'country', 'institution',
                  'position', 'research_areas', 'education_background', 'publications_summary',
                  'profile_photo', 'cv_file', 'google_scholar_link', 'orcid_id', 'terms_accepted']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'research_areas': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'education_background': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'publications_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'cv_file': forms.FileInput(attrs={'class': 'form-control'}),
            'google_scholar_link': forms.URLInput(attrs={'class': 'form-control'}),
            'orcid_id': forms.TextInput(attrs={'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Hall of Fame Application Form
class HallOfFameApplicationForm(forms.ModelForm):
    discipline_or_status = forms.ChoiceField(
        choices=HallOfFameApplication.DISCIPLINE_STATUS_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ChoiceField(
        choices=HallOfFameApplication.CATEGORY_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = HallOfFameApplication
        fields = ['application_type', 'nominee_first_name', 'nominee_last_name', 'nominee_email',
                  'nominee_institution', 'nominee_position', 'discipline_or_status', 'category',
                  'research_achievements', 'impact_description', 'supporting_documents', 
                  'nominator_first_name', 'nominator_last_name', 'nominator_email', 
                  'nominator_relationship', 'terms_accepted']
        widgets = {
            'application_type': forms.Select(attrs={'class': 'form-control'}),
            'nominee_first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'nominee_last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'nominee_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nominee_institution': forms.TextInput(attrs={'class': 'form-control'}),
            'nominee_position': forms.TextInput(attrs={'class': 'form-control'}),
            'research_achievements': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'impact_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'supporting_documents': forms.FileInput(attrs={'class': 'form-control'}),
            'nominator_first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'nominator_last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'nominator_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nominator_relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Plagiarism Check Form
class PlagiarismCheckForm(forms.ModelForm):
    whatsapp_phone = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = PlagiarismCheck
        fields = ['document', 'document_title', 'email', 'name', 'whatsapp_phone', 'message']
        widgets = {
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'document_title': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

# Plagiarism Work Form
class PlagiarismWorkForm(forms.ModelForm):
    whatsapp_phone = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    plagiarism_report = forms.FileField(required=True, widget=forms.FileInput(attrs={'class': 'form-control'}), 
                                        validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    submission_title = forms.CharField(max_length=300, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = PlagiarismWork
        fields = ['document', 'plagiarism_report', 'submission_title', 'plagiarism_percentage', 
                  'email', 'name', 'whatsapp_phone', 'terms_accepted']
        widgets = {
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'plagiarism_percentage': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Thesis Forms
class ThesisToArticleForm(forms.ModelForm):
    whatsapp_phone = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    submission_title = forms.CharField(max_length=300, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    number_of_article = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = ThesisToArticle
        fields = ['thesis_file', 'submission_title', 'number_of_article', 'special_instructions',
                  'email', 'name', 'whatsapp_phone', 'terms_accepted']
        widgets = {
            'thesis_file': forms.FileInput(attrs={'class': 'form-control'}),
            'special_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ThesisToBookForm(forms.ModelForm):
    whatsapp_phone = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    submission_title = forms.CharField(max_length=300, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    number_of_books = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = ThesisToBook
        fields = ['thesis_file', 'submission_title', 'number_of_books', 'special_requirements',
                  'email', 'name', 'whatsapp_phone', 'terms_accepted']
        widgets = {
            'thesis_file': forms.FileInput(attrs={'class': 'form-control'}),
            'special_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ThesisToBookChapterForm(forms.ModelForm):
    whatsapp_phone = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    submission_title = forms.CharField(max_length=300, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    number_of_chapters = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = ThesisToBookChapter
        fields = ['thesis_file', 'submission_title', 'number_of_chapters', 'special_instructions',
                  'email', 'name', 'whatsapp_phone', 'terms_accepted']
        widgets = {
            'thesis_file': forms.FileInput(attrs={'class': 'form-control'}),
            'special_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PowerPointPreparationForm(forms.ModelForm):
    whatsapp_phone = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    submission_title = forms.CharField(max_length=300, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    number_of_slides = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = PowerPointPreparation
        fields = ['thesis_file', 'submission_title', 'number_of_slides', 'special_instructions',
                  'email', 'name', 'whatsapp_phone', 'terms_accepted']
        widgets = {
            'thesis_file': forms.FileInput(attrs={'class': 'form-control'}),
            'special_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['title', 'content', 'excerpt', 'featured_image', 'tags', 'writer', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter article title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Enter article content'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter article excerpt (optional)'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control', 'style': 'display: none;'}),
            'writer': forms.Select(attrs={'class': 'form-control', 'style': 'display: none;'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'publish-checkbox'}),
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        # Remove empty HTML tags
        import re
        content = re.sub(r'<p><br></p>', '', content)
        content = re.sub(r'<p></p>', '', content)
        if not content or len(content.strip()) < 10:
            raise forms.ValidationError('Please enter article content (at least 10 characters).')
        return content
