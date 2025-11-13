from django.contrib import admin
from django.utils.html import format_html
from .models import (
    UserProfile, Article, ArticleAuthor, Journal, JournalEditor, Project, ProjectContributor,
    MembershipRequest, DirectoryApplication, HallOfFameApplication, PlagiarismCheck,
    PlagiarismWork, ThesisToArticle, ThesisToBook, ThesisToBookChapter, PowerPointPreparation
)

# User Profile Admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'country', 'created_at')
    list_filter = ('country', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'country')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user',)

# Article Author Inline
class ArticleAuthorInline(admin.TabularInline):
    model = ArticleAuthor
    extra = 1
    fields = ('name', 'email', 'affiliation', 'orcid', 'is_corresponding', 'order')

# Article Admin
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'article_type', 'discipline', 'status', 'submitted_by', 'created_at')
    list_filter = ('status', 'article_type', 'discipline', 'language', 'created_at')
    search_fields = ('title', 'abstract', 'keywords', 'doi')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('submitted_by',)
    inlines = [ArticleAuthorInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'article_type', 'discipline', 'language', 'status')
        }),
        ('Content', {
            'fields': ('abstract', 'keywords', 'article_file')
        }),
        ('Publication Details', {
            'fields': ('publication_date', 'doi')
        }),
        ('Metadata', {
            'fields': ('submitted_by', 'created_at', 'updated_at')
        }),
    )

# Journal Editor Inline
class JournalEditorInline(admin.TabularInline):
    model = JournalEditor
    extra = 1
    fields = ('name', 'email', 'affiliation', 'role', 'order')

# Journal Admin
@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('journal_name', 'publisher_name', 'subject_area', 'created_at')
    list_filter = ('publisher_country', 'language', 'created_at')
    search_fields = ('journal_name', 'journal_abbreviation', 'publisher_name', 'issn_print', 'issn_online', 'e_issn')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('submitted_by',)
    inlines = [JournalEditorInline]
    fieldsets = (
        ('Journal Information', {
            'fields': ('journal_name', 'journal_abbreviation', 'subject_area', 'language', 'journal_scope', 'journal_logo')
        }),
        ('Publisher Information', {
            'fields': ('publisher_name', 'publisher_address', 'publisher_country', 'publisher_email', 'publisher_phone', 'publisher_website')
        }),
        ('ISSN Information', {
            'fields': ('issn_print', 'issn_online', 'e_issn')
        }),
        ('Publication Details', {
            'fields': ('publication_frequency', 'first_publication_year', 'terms_accepted')
        }),
        ('Metadata', {
            'fields': ('submitted_by', 'created_at', 'updated_at')
        }),
    )

# Project Contributor Inline
class ProjectContributorInline(admin.TabularInline):
    model = ProjectContributor
    extra = 1
    fields = ('name', 'email', 'affiliation', 'role', 'order')

# Project Admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'project_type', 'category', 'institution', 'status', 'created_at')
    list_filter = ('project_type', 'status', 'category', 'created_at')
    search_fields = ('project_title', 'description', 'institution', 'category')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('submitted_by',)
    inlines = [ProjectContributorInline]
    fieldsets = (
        ('Project Information', {
            'fields': ('project_title', 'project_type', 'category', 'institution', 'status')
        }),
        ('Details', {
            'fields': ('description', 'start_date', 'end_date', 'project_file', 'additional_info')
        }),
        ('Metadata', {
            'fields': ('submitted_by', 'created_at', 'updated_at')
        }),
    )

# Membership Request Admin
@admin.register(MembershipRequest)
class MembershipRequestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'membership_type', 'country', 'created_at')
    list_filter = ('membership_type', 'country', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'institution', 'position')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('submitted_by',)
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'country')
        }),
        ('Professional Information', {
            'fields': ('institution', 'position', 'membership_type', 'research_interests')
        }),
        ('Documents', {
            'fields': ('cv_file', 'motivation_letter', 'terms_accepted')
        }),
        ('Metadata', {
            'fields': ('submitted_by', 'created_at', 'updated_at')
        }),
    )

# Directory Application Admin
@admin.register(DirectoryApplication)
class DirectoryApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'institution', 'country', 'created_at')
    list_filter = ('country', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'institution', 'position', 'orcid_id')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('submitted_by',)
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'country', 'profile_photo')
        }),
        ('Professional Information', {
            'fields': ('institution', 'position', 'research_areas', 'education_background', 'publications_summary')
        }),
        ('Research Profile', {
            'fields': ('google_scholar_link', 'orcid_id', 'cv_file', 'terms_accepted')
        }),
        ('Metadata', {
            'fields': ('submitted_by', 'created_at', 'updated_at')
        }),
    )

# Hall of Fame Application Admin
@admin.register(HallOfFameApplication)
class HallOfFameApplicationAdmin(admin.ModelAdmin):
    list_display = ('nominee_first_name', 'nominee_last_name', 'nominee_institution', 'application_type', 'created_at')
    list_filter = ('application_type', 'created_at')
    search_fields = ('nominee_first_name', 'nominee_last_name', 'nominee_email', 'nominee_institution', 'nominator_first_name', 'nominator_last_name')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('submitted_by',)
    fieldsets = (
        ('Application Type', {
            'fields': ('application_type',)
        }),
        ('Nominee Information', {
            'fields': ('nominee_first_name', 'nominee_last_name', 'nominee_email', 'nominee_institution', 'nominee_position')
        }),
        ('Achievements', {
            'fields': ('research_achievements', 'impact_description', 'supporting_documents')
        }),
        ('Nominator Information', {
            'fields': ('nominator_first_name', 'nominator_last_name', 'nominator_email', 'nominator_relationship')
        }),
        ('Metadata', {
            'fields': ('terms_accepted', 'submitted_by', 'created_at', 'updated_at')
        }),
    )

# Plagiarism Check Admin
@admin.register(PlagiarismCheck)
class PlagiarismCheckAdmin(admin.ModelAdmin):
    list_display = ('document_title', 'check_type', 'email', 'similarity_score', 'created_at')
    list_filter = ('check_type', 'exclude_quotes', 'exclude_bibliography', 'exclude_small_matches', 'created_at')
    search_fields = ('document_title', 'email', 'name')
    readonly_fields = ('created_at', 'updated_at', 'similarity_score')
    raw_id_fields = ('submitted_by',)
    fieldsets = (
        ('Document Information', {
            'fields': ('document', 'document_title', 'check_type')
        }),
        ('Check Options', {
            'fields': ('exclude_quotes', 'exclude_bibliography', 'exclude_small_matches')
        }),
        ('Contact Information', {
            'fields': ('email', 'name')
        }),
        ('Results', {
            'fields': ('similarity_score', 'report_file')
        }),
        ('Metadata', {
            'fields': ('terms_accepted', 'privacy_accepted', 'submitted_by', 'created_at', 'updated_at')
        }),
    )

# Plagiarism Work Admin
@admin.register(PlagiarismWork)
class PlagiarismWorkAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service_type', 'urgency', 'created_at')
    list_filter = ('service_type', 'urgency', 'created_at')
    search_fields = ('name', 'email', 'phone', 'instructions')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('submitted_by',)
    fieldsets = (
        ('Document', {
            'fields': ('document',)
        }),
        ('Service Details', {
            'fields': ('service_type', 'instructions', 'urgency')
        }),
        ('Contact Information', {
            'fields': ('email', 'name', 'phone')
        }),
        ('Metadata', {
            'fields': ('terms_accepted', 'privacy_accepted', 'submitted_by', 'created_at', 'updated_at')
        }),
    )

# Thesis to Article Admin
@admin.register(ThesisToArticle)
class ThesisToArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'article_type', 'target_journal', 'created_at')
    list_filter = ('article_type', 'created_at')
    search_fields = ('name', 'email', 'target_journal', 'special_instructions')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('submitted_by',)
    fieldsets = (
        ('Thesis Document', {
            'fields': ('thesis_file',)
        }),
        ('Article Requirements', {
            'fields': ('target_journal', 'article_type', 'word_limit')
        }),
        ('Sections to Include', {
            'fields': ('include_abstract', 'include_keywords', 'include_introduction', 'include_methodology', 
                      'include_results', 'include_discussion', 'include_conclusion', 'include_references')
        }),
        ('Additional Information', {
            'fields': ('special_instructions', 'email', 'name', 'phone')
        }),
        ('Metadata', {
            'fields': ('terms_accepted', 'privacy_accepted', 'submitted_by', 'created_at', 'updated_at')
        }),
    )

# Thesis to Book Admin
@admin.register(ThesisToBook)
class ThesisToBookAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'book_type', 'book_title', 'created_at')
    list_filter = ('book_type', 'created_at')
    search_fields = ('name', 'email', 'book_title', 'target_audience', 'special_requirements')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('submitted_by',)
    fieldsets = (
        ('Thesis Document', {
            'fields': ('thesis_file',)
        }),
        ('Book Requirements', {
            'fields': ('book_title', 'book_type', 'target_audience', 'chapter_structure', 'special_requirements')
        }),
        ('Contact Information', {
            'fields': ('email', 'name', 'phone')
        }),
        ('Metadata', {
            'fields': ('terms_accepted', 'privacy_accepted', 'submitted_by', 'created_at', 'updated_at')
        }),
    )

# Thesis to Book Chapter Admin
@admin.register(ThesisToBookChapter)
class ThesisToBookChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'chapter_title', 'thesis_section', 'created_at')
    list_filter = ('thesis_section', 'created_at')
    search_fields = ('name', 'email', 'chapter_title', 'target_book', 'special_instructions')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('submitted_by',)
    fieldsets = (
        ('Thesis Document', {
            'fields': ('thesis_file',)
        }),
        ('Chapter Requirements', {
            'fields': ('chapter_title', 'thesis_section', 'chapter_number', 'target_book', 'word_limit', 'special_instructions')
        }),
        ('Contact Information', {
            'fields': ('email', 'name', 'phone')
        }),
        ('Metadata', {
            'fields': ('terms_accepted', 'privacy_accepted', 'submitted_by', 'created_at', 'updated_at')
        }),
    )

# PowerPoint Preparation Admin
@admin.register(PowerPointPreparation)
class PowerPointPreparationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'presentation_type', 'duration', 'created_at')
    list_filter = ('presentation_type', 'duration', 'design_style', 'created_at')
    search_fields = ('name', 'email', 'special_instructions')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('submitted_by',)
    fieldsets = (
        ('Thesis Document', {
            'fields': ('thesis_file',)
        }),
        ('Presentation Requirements', {
            'fields': ('presentation_type', 'duration', 'slide_count', 'design_style')
        }),
        ('Sections to Include', {
            'fields': ('include_title', 'include_intro', 'include_objectives', 'include_methodology',
                      'include_results', 'include_discussion', 'include_conclusion', 'include_references', 'include_acknowledgments')
        }),
        ('Additional Information', {
            'fields': ('special_instructions', 'email', 'name', 'phone')
        }),
        ('Metadata', {
            'fields': ('terms_accepted', 'privacy_accepted', 'submitted_by', 'created_at', 'updated_at')
        }),
    )
