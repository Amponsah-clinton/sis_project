from django.contrib import admin
from django.utils.html import format_html
from .models import (
    UserProfile, Article, ArticleAuthor, Journal, JournalEditor, Project, ProjectContributor,
    ProjectPayment, MembershipRequest, DirectoryApplication, HallOfFameApplication, PlagiarismCheck,
    PlagiarismWork, ThesisToArticle, ThesisToBook, ThesisToBookChapter, PowerPointPreparation,
    SiteSettings, Blog, NewsTag, NewsWriter, NewsArticle, NewsComment, NewsBookmark
)
from .forms import ProjectForm

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
    list_filter = ('status', 'article_type', 'discipline', 'language', 'created_at', 'year_of_publication', 'country_of_publication')
    search_fields = ('title', 'abstract', 'keywords', 'doi', 'journal_name', 'authors_names')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('submitted_by',)
    inlines = [ArticleAuthorInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'article_type', 'discipline', 'language', 'status')
        }),
        ('Content', {
            'fields': ('abstract', 'keywords', 'article_file', 'cover_image')
        }),
        ('Authors', {
            'fields': ('authors_names',)
        }),
        ('Publication Details', {
            'fields': ('publication_date', 'year_of_publication', 'volume', 'issue', 'pages', 'journal_name', 'country_of_publication', 'doi')
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
    list_display = ('journal_name', 'publisher_name', 'subject_area', 'journal_type', 'created_at')
    list_filter = ('publisher_country', 'language', 'journal_type', 'journal_format', 'open_access', 'peer_review', 'created_at')
    search_fields = ('journal_name', 'journal_abbreviation', 'publisher_name', 'issn_print', 'issn_online', 'e_issn', 'journal_url')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('submitted_by',)
    inlines = [JournalEditorInline]
    fieldsets = (
        ('Journal Information', {
            'fields': ('journal_name', 'journal_abbreviation', 'journal_cover_image', 'journal_logo', 'journal_url', 'subject_area', 'language', 'journal_scope')
        }),
        ('Publisher Information', {
            'fields': ('publisher_name', 'publisher_address', 'publisher_country', 'publisher_email', 'publisher_phone', 'publisher_website')
        }),
        ('ISSN Information', {
            'fields': ('issn_print', 'issn_online', 'e_issn')
        }),
        ('Publication Details', {
            'fields': ('journal_type', 'journal_format', 'publication_frequency', 'first_publication_year', 'publication_fee', 'open_access', 'peer_review')
        }),
        ('Terms', {
            'fields': ('terms_accepted',)
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
    form = ProjectForm
    list_display = ('project_title', 'project_type', 'category', 'institution', 'status', 'price_usd', 'views', 'downloads', 'created_at')
    list_filter = ('project_type', 'status', 'category', 'created_at')
    search_fields = ('project_title', 'description', 'institution', 'category')
    readonly_fields = ('created_at', 'updated_at', 'views', 'downloads')
    raw_id_fields = ('submitted_by',)
    inlines = [ProjectContributorInline]
    fieldsets = (
        ('Project Information', {
            'fields': ('project_title', 'project_type', 'category', 'institution', 'status')
        }),
        ('Details', {
            'fields': ('description', 'start_date', 'end_date', 'project_file', 'additional_info')
        }),
        ('Pricing & Stats', {
            'fields': ('price_usd', 'views', 'downloads')
        }),
        ('Metadata', {
            'fields': ('submitted_by', 'created_at', 'updated_at')
        }),
    )

# Project Payment Admin
@admin.register(ProjectPayment)
class ProjectPaymentAdmin(admin.ModelAdmin):
    list_display = ('email', 'project', 'payment_reference', 'amount_paid', 'payment_status', 'document_sent', 'created_at')
    list_filter = ('payment_status', 'document_sent', 'created_at')
    search_fields = ('email', 'payment_reference', 'project__project_title')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('project',)
    fieldsets = (
        ('Payment Information', {
            'fields': ('project', 'email', 'payment_reference', 'amount_paid', 'payment_status')
        }),
        ('Document Delivery', {
            'fields': ('document_sent',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
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
            'fields': ('profile_picture', 'cv_file', 'motivation_letter', 'terms_accepted')
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
    list_display = ('name', 'email', 'submission_title', 'plagiarism_percentage', 'created_at')
    list_filter = ('plagiarism_percentage', 'created_at')
    search_fields = ('name', 'email', 'whatsapp_phone', 'submission_title')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('submitted_by',)
    fieldsets = (
        ('Documents', {
            'fields': ('document', 'plagiarism_report')
        }),
        ('Request Details', {
            'fields': ('submission_title', 'plagiarism_percentage')
        }),
        ('Contact Information', {
            'fields': ('email', 'name', 'whatsapp_phone')
        }),
        ('Metadata', {
            'fields': ('terms_accepted', 'submitted_by', 'created_at', 'updated_at')
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

# Site Settings Admin - Singleton pattern
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the only instance
        return False
    
    list_display = ('__str__', 'email_address', 'phone', 'updated_at')
    fieldsets = (
        ('General Settings', {
            'fields': ('default_banner_image', 'default_app_font_size')
        }),
        ('Carousel Images', {
            'fields': (
                ('carousel_image_1', 'carousel_image_1_url', 'carousel_image_1_title', 'carousel_image_1_subtitle'),
                ('carousel_image_2', 'carousel_image_2_url', 'carousel_image_2_title', 'carousel_image_2_subtitle'),
                ('carousel_image_3', 'carousel_image_3_url', 'carousel_image_3_title', 'carousel_image_3_subtitle'),
            )
        }),
        ('Contact Information', {
            'fields': ('phone', 'office_location_address', 'email_address', 'whatsapp_url', 'youtube_url', 'twitter_url', 'facebook_url')
        }),
        ('Payment Gateway', {
            'fields': ('api_secret_key', 'api_public_key')
        }),
        ('Map', {
            'fields': ('map_index',)
        }),
        ('Landing Page', {
            'fields': ('banner_title', 'banner_subtitle', 'footer_video', 'enable_service_features')
        }),
        ('Navigator Settings', {
            'fields': (
                ('documentations_nav_image', 'documentations_nav_title', 'documentations_nav_subtitle'),
                ('communities_nav_image', 'communities_nav_title', 'communities_nav_subtitle'),
                ('requests_nav_image', 'requests_nav_title', 'requests_nav_subtitle'),
                ('about_nav_image', 'about_nav_title', 'about_nav_subtitle'),
            )
        }),
        ('Page Enable/Disable', {
            'fields': (
                ('enable_landing_page', 'enable_indexed_articles_page', 'enable_indexed_journals_page', 'enable_project_archive_page'),
                ('enable_directory_researchers_page', 'enable_hall_of_fame_page', 'enable_council_members_page', 'enable_team_members_page'),
                ('enable_donate_page', 'enable_about_sis_page', 'enable_mission_page', 'enable_criteria_page'),
                ('enable_tolerance_policy_page', 'enable_service_solution_page', 'enable_policy_terms_page'),
                ('enable_check_turnitin_page', 'enable_work_plagiarism_page', 'enable_thesis_to_article_page'),
                ('enable_thesis_to_book_page', 'enable_thesis_to_book_chapter_page', 'enable_powerpoint_preparation_page'),
            )
        }),
        ('Pricing - Sponsorship', {
            'fields': (
                ('premier_price', 'sustaining_price', 'basic_price', 'power_price'),
                ('double_price', 'single_price', 'compact_price', 'inspired_price', 'charity_homes_price'),
            )
        }),
        ('Pricing - Registrations', {
            'fields': (
                ('article_indexing_price', 'journal_indexing_price', 'project_archive_hosting_price', 'directory_researcher_price'),
                ('hall_of_fame_price', 'check_plagiarism_price', 'work_plagiarism_price', 'thesis_to_article_price'),
                ('thesis_to_book_price', 'thesis_to_book_chapter_price', 'powerpoint_preparation_price'),
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

# Blog Admin
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'order_priority', 'views', 'published_date', 'created_by')
    list_filter = ('category', 'is_published', 'order_priority', 'published_date', 'created_at')
    search_fields = ('title', 'content', 'tag')
    readonly_fields = ('created_at', 'updated_at', 'views')
    raw_id_fields = ('created_by',)
    fieldsets = (
        ('Blog Content', {
            'fields': ('title', 'content', 'image', 'category', 'tag')
        }),
        ('Publication Settings', {
            'fields': ('is_published', 'order_priority', 'published_date')
        }),
        ('Statistics', {
            'fields': ('views',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )

# News Tag Admin
@admin.register(NewsTag)
class NewsTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order_priority', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug')
    readonly_fields = ('slug', 'created_at', 'updated_at')
    ordering = ('-order_priority', 'name')

# News Writer Admin
@admin.register(NewsWriter)
class NewsWriterAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order_priority', 'is_active', 'email', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug', 'email', 'bio')
    readonly_fields = ('slug', 'created_at', 'updated_at')
    ordering = ('-order_priority', 'name')
    fieldsets = (
        ('Writer Information', {
            'fields': ('name', 'slug', 'bio', 'profile_image', 'email')
        }),
        ('Settings', {
            'fields': ('order_priority', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )

# News Article Admin
@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'is_published', 'published_date', 'view_count', 'created_at')
    list_filter = ('is_published', 'published_date', 'created_at', 'tags')
    search_fields = ('title', 'content', 'excerpt')
    readonly_fields = ('slug', 'view_count', 'published_date', 'created_at', 'updated_at')
    raw_id_fields = ('writer', 'created_by')
    filter_horizontal = ('tags',)
    list_per_page = 25
    date_hierarchy = 'published_date'
    ordering = ('-published_date', '-created_at')
    fieldsets = (
        ('Article Content', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'featured_image')
        }),
        ('Categorization', {
            'fields': ('tags', 'writer')
        }),
        ('Publication', {
            'fields': ('is_published', 'published_date', 'view_count')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )

@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'parent', 'is_approved', 'created_at', 'get_likes_count', 'get_dislikes_count')
    list_filter = ('is_approved', 'created_at', 'article')
    search_fields = ('content', 'user__username', 'article__title')
    readonly_fields = ('created_at', 'updated_at', 'get_likes_count', 'get_dislikes_count', 'get_replies_count')
    raw_id_fields = ('article', 'user', 'parent')
    filter_horizontal = ('likes', 'dislikes')
    fieldsets = (
        ('Comment Content', {
            'fields': ('article', 'parent', 'user', 'content')
        }),
        ('Engagement', {
            'fields': ('likes', 'dislikes', 'get_likes_count', 'get_dislikes_count', 'get_replies_count')
        }),
        ('Moderation', {
            'fields': ('is_approved',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_likes_count(self, obj):
        return obj.get_likes_count()
    get_likes_count.short_description = 'Likes'
    
    def get_dislikes_count(self, obj):
        return obj.get_dislikes_count()
    get_dislikes_count.short_description = 'Dislikes'
    
    def get_replies_count(self, obj):
        return obj.get_replies_count()
    get_replies_count.short_description = 'Replies'

@admin.register(NewsBookmark)
class NewsBookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'article__title')
    readonly_fields = ('created_at',)
    raw_id_fields = ('user', 'article')
    ordering = ('-created_at',)
