from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    UserProfile, Article, ArticleAuthor, Journal, JournalEditor, Project, ProjectContributor,
    MembershipRequest, DirectoryApplication, HallOfFameApplication, PlagiarismCheck,
    PlagiarismWork, ThesisToArticle, ThesisToBook, ThesisToBookChapter, PowerPointPreparation
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
                  'language', 'publication_date', 'doi', 'article_file']
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
                  'position', 'membership_type', 'research_interests', 'cv_file',
                  'motivation_letter', 'terms_accepted']
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
    class Meta:
        model = HallOfFameApplication
        fields = ['application_type', 'nominee_first_name', 'nominee_last_name', 'nominee_email',
                  'nominee_institution', 'nominee_position', 'research_achievements',
                  'impact_description', 'supporting_documents', 'nominator_first_name',
                  'nominator_last_name', 'nominator_email', 'nominator_relationship', 'terms_accepted']
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
    class Meta:
        model = PlagiarismCheck
        fields = ['document', 'document_title', 'check_type', 'exclude_quotes',
                  'exclude_bibliography', 'exclude_small_matches', 'email', 'name',
                  'terms_accepted', 'privacy_accepted']
        widgets = {
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'document_title': forms.TextInput(attrs={'class': 'form-control'}),
            'check_type': forms.Select(attrs={'class': 'form-control'}),
            'exclude_quotes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'exclude_bibliography': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'exclude_small_matches': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privacy_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Plagiarism Work Form
class PlagiarismWorkForm(forms.ModelForm):
    class Meta:
        model = PlagiarismWork
        fields = ['document', 'service_type', 'instructions', 'urgency', 'email',
                  'name', 'phone', 'terms_accepted', 'privacy_accepted']
        widgets = {
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'urgency': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privacy_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Thesis Forms
class ThesisToArticleForm(forms.ModelForm):
    class Meta:
        model = ThesisToArticle
        fields = ['thesis_file', 'target_journal', 'article_type', 'word_limit',
                  'include_abstract', 'include_keywords', 'include_introduction',
                  'include_methodology', 'include_results', 'include_discussion',
                  'include_conclusion', 'include_references', 'special_instructions',
                  'email', 'name', 'phone', 'terms_accepted', 'privacy_accepted']
        widgets = {
            'thesis_file': forms.FileInput(attrs={'class': 'form-control'}),
            'target_journal': forms.TextInput(attrs={'class': 'form-control'}),
            'article_type': forms.Select(attrs={'class': 'form-control'}),
            'word_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'include_abstract': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_keywords': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_introduction': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_methodology': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_results': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_discussion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_conclusion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_references': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'special_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privacy_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ThesisToBookForm(forms.ModelForm):
    class Meta:
        model = ThesisToBook
        fields = ['thesis_file', 'book_title', 'book_type', 'target_audience',
                  'chapter_structure', 'special_requirements', 'email', 'name',
                  'phone', 'terms_accepted', 'privacy_accepted']
        widgets = {
            'thesis_file': forms.FileInput(attrs={'class': 'form-control'}),
            'book_title': forms.TextInput(attrs={'class': 'form-control'}),
            'book_type': forms.Select(attrs={'class': 'form-control'}),
            'target_audience': forms.TextInput(attrs={'class': 'form-control'}),
            'chapter_structure': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'special_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privacy_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ThesisToBookChapterForm(forms.ModelForm):
    class Meta:
        model = ThesisToBookChapter
        fields = ['thesis_file', 'chapter_title', 'thesis_section', 'chapter_number',
                  'target_book', 'word_limit', 'special_instructions', 'email',
                  'name', 'phone', 'terms_accepted', 'privacy_accepted']
        widgets = {
            'thesis_file': forms.FileInput(attrs={'class': 'form-control'}),
            'chapter_title': forms.TextInput(attrs={'class': 'form-control'}),
            'thesis_section': forms.Select(attrs={'class': 'form-control'}),
            'chapter_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'target_book': forms.TextInput(attrs={'class': 'form-control'}),
            'word_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'special_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privacy_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PowerPointPreparationForm(forms.ModelForm):
    class Meta:
        model = PowerPointPreparation
        fields = ['thesis_file', 'presentation_type', 'duration', 'slide_count',
                  'include_title', 'include_intro', 'include_objectives', 'include_methodology',
                  'include_results', 'include_discussion', 'include_conclusion',
                  'include_references', 'include_acknowledgments', 'design_style',
                  'special_instructions', 'email', 'name', 'phone', 'terms_accepted', 'privacy_accepted']
        widgets = {
            'thesis_file': forms.FileInput(attrs={'class': 'form-control'}),
            'presentation_type': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.Select(attrs={'class': 'form-control'}),
            'slide_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'include_title': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_intro': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_objectives': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_methodology': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_results': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_discussion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_conclusion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_references': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_acknowledgments': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'design_style': forms.Select(attrs={'class': 'form-control'}),
            'special_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privacy_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
